import streamlit as st
import io
import pandas as pd
from typing import List
from PIL import Image
from .mkcsv import mkcsv_gui
#from .mkpptx import mkpptx_gui

FILTER_COLS = ["試験", "測定面", "正極", "測定", "電解液", "倍率"]
COLUMNS_PER_ROW = 3

# SAFETY TOOLS
def sanitize_for_csv_injection(df):
    for col in df.columns:
        if df[col].dtype == 'object':
           df[col] = (
                df[col]
                .fillna("")
                .astype(str)
                .str.replace(r'^([=+\-@])', r"'\1", regex=True)
            )
    return df

def sanitize_filename(name: str) -> str:
    name = name.replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9._-]", "", name)[:200]

# CSV FILLTERING TOOL
def get_filtered_names_by_multiselect_full_order(df: pd.DataFrame, condition_id: int, filter_cols: List[str]) -> List[str]:
    
    current_df = df.copy()
    category_definitions = {}

    for col_name in filter_cols:
        key_multiselect = f'condition_{condition_id}_{col_name}'
        selected_values = st.session_state.get(key_multiselect, ["全て選択"])

        if selected_values and "全て選択" not in selected_values:
           current_df = current_df[current_df[col_name].astype(str).isin(selected_values)]
           category_definitions[col_name] = selected_values

    if category_definitions:
       sort_by_cols = []
       for col_name, categories in category_definitions.items():
           cat_type = pd.CategoricalDtype(categories=categories, ordered=True)
           current_df[col_name] = current_df[col_name].astype(str).astype(cat_type)
           sort_by_cols.append(col_name)
       current_df = current_df.sort_values(by=sort_by_cols)

    return current_df["ファイル名"].astype(str).tolist()

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

    #if uploaded_file:
    #   df = mkcsv_gui(uploaded_file)
    #   df = None 
    #   st.session_state.data_df = df
    
    df = st.session_state.data_df
    if df is None:
       st.info("データファイル（CSV）をアップロードして「Yes」を選択してください。")
       return

    st.markdown("---")

    # FILLTERING RESULTS
    #final_results = get_filtered_names_by_multiselect_full_order(df, condition_id=condition_id, filter_cols=FILTER_COLS)

    #display_names = [name for name in final_results if name in images]
               
    #condition_container.subheader(f"✅ 条件に合致する画像 ({len(display_names)} 件)")
    #if len(final_results) == 0:
    #   condition_container.warning("条件に合致する画像はありません。")
    #else:
    #   cols = condition_container.columns(COLUMNS_PER_ROW)
    #   for j, name in enumerate(display_names):
    #       col = cols[j % COLUMNS_PER_ROW]
    #       #col.image(images[name], use_container_width=True) 
    #       #col.image(images[name], 
    #       #          caption=name if len(name) <= 40 else name[:40] + "...", 
    #       #          use_container_width=True)
    #       col.image(images[name], 
    #                 caption=name if len(name) <= 40 else name[:40] + "...", 
    #                 width="content")

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
