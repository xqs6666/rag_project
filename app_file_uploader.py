import streamlit as st

st.title("知识库更新服务")

st.file_uploader(
    label="请上传文件",
    accept_multiple_files=True,
    type=["txt"]
)