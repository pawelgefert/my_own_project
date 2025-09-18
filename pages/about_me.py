import streamlit as st
import config



# --- PAGE SETUP ---
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
with col1:
    st.image(config.IMAGES_DIR +f"/logo.png")   
with col2:
    st.title("O Mnie")
    st.write("Programista amator i pasjonat technologii. W wolnym czasie tworzę aplikacje webowe i eksploruję nowe technologie.")

   