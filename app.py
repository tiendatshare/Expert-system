import pandas as pd
import streamlit as st
import os

# Đọc dữ liệu từ file CSV
df = pd.read_csv('trieuchung.csv')

# Tạo danh sách chứa các luật dưới dạng từ điển
rules = []

# Duyệt qua từng bệnh trong DataFrame
for disease in df['Disease'].unique():
    # Lọc dữ liệu cho bệnh cụ thể
    subset_df = df[df['Disease'] == disease]
    # Duyệt qua từng dòng trong subset
    for index, row in subset_df.iterrows():
        symptoms = [symptom.strip() for symptom in row[1:] if pd.notna(symptom)]
        # Nếu có sự kết hợp triệu chứng
        if symptoms:
            rule = {'symptoms': symptoms, 'disease': disease}
            rules.append(rule)

# Kiểm tra xem tệp luật đã tồn tại chưa
if not os.path.exists('luat.txt'):
    # Ghi các luật vào file txt
    with open('luat.txt', 'w') as file:
        for rule in rules:
            file.write(f"If patient has {', '.join(rule['symptoms'])}, then patient may have {rule['disease']}.\n")
else:
    # Đọc nội dung hiện có của tệp luật
    with open('luat.txt', 'r') as file:
        existing_rules = file.readlines()
    # Nếu nội dung của tệp luật khác so với các luật mới, thực hiện cập nhật
    new_rules = [f"If patient has {', '.join(rule['symptoms'])}, then patient may have {rule['disease']}.\n" for rule in rules]
    if existing_rules != new_rules:
        with open('luat.txt', 'w') as file:
            file.writelines(new_rules)

#######################################################

# Lấy danh sách các triệu chứng duy nhất
symptoms_list = set()
for symptoms in df.iloc[:, 1:].values.flatten():
    if pd.notna(symptoms):
        symptoms_list.add(symptoms.strip())
symptoms_list = list(symptoms_list)

# Hàm tìm các triệu chứng liên quan đến triệu chứng đã chọn
def get_related_symptoms(selected_symptoms):
    related_symptoms = set()
    for rule in rules:
        if any(symptom in rule['symptoms'] for symptom in selected_symptoms):
            related_symptoms.update(rule['symptoms'])
    return list(related_symptoms - set(selected_symptoms))

# Hàm chẩn đoán bệnh dựa trên triệu chứng đã chọn
def diagnose(selected_symptoms):
    possible_diseases = {}
    for rule in rules:
        if all(symptom in rule['symptoms'] for symptom in selected_symptoms):
            disease = rule['disease']
            if disease in possible_diseases:
                possible_diseases[disease] += 1
            else:
                possible_diseases[disease] = 1
    return possible_diseases

# Hiển thị logo
st.image('logo.png', width=200)
# Tạo tiêu đề cho ứng dụng
st.title("Hệ chuyên gia chẩn đoán bệnh")

# Lưu trữ các triệu chứng đã chọn trong session state
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

# Hiển thị các triệu chứng có thể chọn
if len(st.session_state.selected_symptoms) == 0:
    st.write("Chọn triệu chứng ban đầu:")
else:
    st.write(f"Các triệu chứng đã chọn: {', '.join(st.session_state.selected_symptoms)}")
    related_symptoms = get_related_symptoms(st.session_state.selected_symptoms)
    if related_symptoms:
        st.write("Chọn triệu chứng tiếp theo:")

# Chia giao diện thành hai cột
left_column, right_column = st.columns(2)

# Tạo hộp chọn cho từng triệu chứng
if len(st.session_state.selected_symptoms) == 0:
    for symptom in symptoms_list:
        if st.checkbox(symptom):
            st.session_state.selected_symptoms.append(symptom)
else:
    for symptom in related_symptoms:
        if st.checkbox(symptom):
            st.session_state.selected_symptoms.append(symptom)

mota_df = pd.read_csv('mota.csv')
phongngua_df = pd.read_csv('phongngua.csv')
df_symptoms= pd.read_csv('trieuchung.csv')
# Hàm lấy các triệu chứng của một căn bệnh
def get_symptoms_of_disease(disease_name):
    symptoms = df_symptoms[df_symptoms['Disease'] == disease_name].iloc[:, 1:].values.flatten()
    unique_symptoms = set(symptom.strip() for symptom in symptoms if pd.notna(symptom))
    return unique_symptoms

# Hàm tìm thông tin mô tả và biện pháp phòng ngừa của một căn bệnh
def get_disease_info(disease_name):
    # Tìm thông tin mô tả từ file mota.csv
    description_df = mota_df.loc[mota_df['Disease'] == disease_name, 'Description']
    description = description_df.values[0] if not description_df.empty else "Không có thông tin mô tả."
    
    # Tìm thông tin biện pháp phòng ngừa từ file phongngua.csv
    precautions_df = phongngua_df.loc[phongngua_df['Disease'] == disease_name, 'Precaution_1':'Precaution_4']
    precautions = precautions_df.values[0].tolist() if not precautions_df.empty else ["Không có biện pháp phòng ngừa."]
    
    return description, precautions

# Nút chẩn đoán
if st.button("Chẩn đoán"):
    if len(st.session_state.selected_symptoms) == 0:
        st.write("Vui lòng Chỉ chọn 1 triệu chứng, sau đó bấm nút chuẩn đoán.Điều này sẽ giúp bạn tìm bệnh dễ dàng hơn.")
    else:
        diagnosis = diagnose(st.session_state.selected_symptoms)
        if len(diagnosis) == 0:
            st.write("Không xác định được bệnh.")
        elif len(diagnosis) == 1:
            disease_name = list(diagnosis.keys())[0]
            description, precautions = get_disease_info(disease_name)
            symptoms_of_disease = get_symptoms_of_disease(disease_name)
            st.write(f"Bạn của bạn tên là : {disease_name} ")
            st.write(f"Các triệu chứng hay gặp của bệnh: ")
            for symptoms_of_disease in symptoms_of_disease:
                st.write(f"- {symptoms_of_disease}")
            st.write(f"Mô tả căn bệnh: {description}")
            st.write("Biện pháp phòng ngừa:")
            for precaution in precautions:
                st.write(f"- {precaution}")
        else:
            st.write("Các bệnh có thể:")
            for disease, count in diagnosis.items():
                st.write(f"{disease} (khớp với {count} triệu chứng)")



# Nút đặt lại để bắt đầu lại quá trình chọn triệu chứng
if st.button("Đặt lại"):
    st.session_state.selected_symptoms = []

# Nút "Không tìm thấy chứng bệnh nào"
if st.button("Không tìm thấy chứng bệnh nào"):
    st.write("Xin lỗi bạn, hệ thống không có dữ liệu triệu chứng bạn mong muốn, hệ thống sẽ cập nhật sớm nhất.")
