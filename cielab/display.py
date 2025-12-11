import streamlit as st

def display_images(result, images, label):
    if not result:
       st.warning(f"{label} に該当する画像はありません。")
       return
    cols = st.columns(3)
    for i, name in enumerate(result):
        img = images[name]
        cols[i % 3].image(img, caption=f"{label}: {name}", use_container_width=True)
