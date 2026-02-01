import streamlit as st

st.title("知识库更新服务")

uploader_file = st.file_uploader(
    label="请上传文件",
    accept_multiple_files=False,
    type=["txt"]
)

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size
    
    st.subheader(f"文件名: {file_name}")
    st.write(f"格式: {file_type} | 大小: {file_size:.2f}")
    
    text = uploader_file.getvalue().decode("utf-8")
    st.write(text)