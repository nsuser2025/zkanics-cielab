import streamlit as st
import io
import pandas as pd
from typing import List
from PIL import Image
from .mkcsv import mkcsv_gui

def cielab_gui():

    # EXPLANATIONS
    st.markdown("#### CIE Lab変換")
    st.markdown("""透過率スペクトルをCIE Lab変換するアプリです.
    光源はD65, 等色関数はCIEが公開している CIE_xyz_1931_2deg.csv, 
    光源D65の分光強度分布は同じくCIEが公開している CIE_std_illum_D65.csv を用いています。
    このアプリにアップロードした情報は全てメモリ上に保存されます。
    セッションの終了と同時にサーバー上のスペクトル情報は完全に消去されます。
    また、出力されるCSVにはコードインジェクションの無効化処理が施されています。
    安心してダウンロードしてください。""") 
    st.markdown("---")
    
    # INITIALIZE SESSIONS
    if 'data_df' not in st.session_state:
        st.session_state.data_df = None
    if 'condition_count' not in st.session_state:
        st.session_state.condition_count = 1
        
    # CSV FILE READER
    uploaded_file = st.file_uploader("透過率スペクトルのExcel/CSVファイルをアップロード", 
                    type=["xlsx", "xls", "xlsm", "csv"])

    if uploaded_file:
       df = mkcsv_gui(uploaded_file)
       df = None 
       st.session_state.data_df = df
    
    df = st.session_state.data_df
    if df is None:
       st.info("データファイル（CSV）をアップロードしてください。")
       return

    st.markdown("---")


# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
