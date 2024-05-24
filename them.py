import streamlit as st
import pandas as pd

# Đọc dữ liệu từ các file CSV
df_trieuchung = pd.read_csv('trieuchung.csv')
df_mota = pd.read_csv('mota.csv')
df_phongngua = pd.read_csv('phongngua.csv')

# Hàm bổ sung dữ liệu vào các DataFrame và lưu vào CSV
def add_data(disease, symptoms, description, precautions):
    # Bổ sung dữ liệu vào trieuchung.csv
    new_symptoms = [disease] + symptoms + [''] * (17 - len(symptoms))
    new_row_trieuchung = pd.DataFrame([new_symptoms], columns=df_trieuchung.columns)
    df_trieuchung_updated = pd.concat([df_trieuchung, new_row_trieuchung], ignore_index=True)
    df_trieuchung_updated.to_csv('trieuchung.csv', index=False)
    
    # Bổ sung dữ liệu vào mota.csv
    new_row_mota = pd.DataFrame([[disease, description]], columns=df_mota.columns)
    df_mota_updated = pd.concat([df_mota, new_row_mota], ignore_index=True)
    df_mota_updated.to_csv('mota.csv', index=False)
    
    # Bổ sung dữ liệu vào phongngua.csv
    new_row_phongngua = pd.DataFrame([[disease] + precautions], columns=df_phongngua.columns)
    df_phongngua_updated = pd.concat([df_phongngua, new_row_phongngua], ignore_index=True)
    df_phongngua_updated.to_csv('phongngua.csv', index=False)

# Giao diện người dùng
st.title('Thêm dữ liệu vào hệ thống')

# Nhập thông tin bệnh
disease = st.text_input('Tên bệnh')

# Nhập triệu chứng
symptoms = []
for i in range(1, 18):
    symptom = st.text_input(f'Triệu chứng {i}')
    if symptom:
        symptoms.append(symptom)

# Nhập mô tả bệnh
description = st.text_area('Mô tả bệnh')

# Nhập biện pháp phòng ngừa
precautions = []
for i in range(1, 5):
    precaution = st.text_input(f'Biện pháp phòng ngừa {i}')
    precautions.append(precaution)

# Nút thêm dữ liệu
if st.button('Thêm dữ liệu'):
    if not disease:
        st.error('Vui lòng nhập tên bệnh.')
    elif not symptoms:
        st.error('Vui lòng nhập ít nhất một triệu chứng.')
    elif not description:
        st.error('Vui lòng nhập mô tả bệnh.')
    elif not any(precautions):
        st.error('Vui lòng nhập ít nhất một biện pháp phòng ngừa.')
    else:
        add_data(disease, symptoms, description, precautions)
        st.success('Dữ liệu đã được thêm thành công!')
