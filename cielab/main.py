import streamlit as st
#import clamd
import io
import pandas as pd
from typing import List
from PIL import Image
from .mkcsv import mkcsv_gui
from .mkpptx import mkpptx_gui

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

def safe_open_image(uploaded_file) -> Image.Image:
    """画像を安全に開く（巨大画像・破損チェック・EXIF除去）"""
    uploaded_file.seek(0)
    img = Image.open(uploaded_file)
    img.verify()  # 破損や不正データの簡易チェック
    uploaded_file.seek(0)
    img = Image.open(uploaded_file).convert("RGB")  # 再オープンしてRGB化
    # 再エンコードしてEXIF除去
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    buf.seek(0)
    return Image.open(buf)

#def scan_file_with_clamav(uploaded_file) -> bool:
#    """ClamAV でアップロードファイルをスキャン"""
#    cd = clamd.ClamdUnixSocket()  # Linux / Dockerで使用
#    with tempfile.NamedTemporaryFile(delete=False) as tmp:
#        tmp.write(uploaded_file.getbuffer())
#        tmp_path = tmp.name
#    result = cd.scan(tmp_path)
#    if result is None or "OK" in str(result):
#        return True
#    return False

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

def mkslide_gui():

    # EXPLANATIONS
    st.markdown("#### CIE Lab変換")
    st.markdown("""CSVファイルに記載された情報をもとに、画像ファイルを条件ごとに抽出・表示するツールです。
    画像情報が記載されたエクセルファイルをアップロードし「MKSLIDEが作成したCSVファイルですか？」を
    NoにしてMKSLIDE用のCSVファイルを作成してください。問題なく作成されると表が出力されますので、表の右上のメニューアイコンから
    ダウンロードしてください。一度作成したCSVファイルは再利用可能です。
    次に、ダウンロードしたCSVファイルをアップロードして「MKSLIDEが作成したCSVファイルですか？」を
    Yesにして画像をアップロードしてください。条件を選択すれば、条件と一致したファイルが
    抽出され表示されます。出力結果はパワーポイントのスライドとしてダウンロード可能です（デフォルトでは白色無地です）。
    テンプレートをアップロードして、好みのスライドデザインに表示画像を出力することも可能です。このアプリにアップロード
    した画像は全てメモリ上に保存されます。セッションの終了と同時にサーバー上の画像情報は完全に消去されます。また、
    出力されるCSVにはコードインジェクションの無効化処理が施されています。安心してダウンロードしてください。""") 
    st.markdown("---")
    
    # INITIALIZE SESSIONS
    if 'data_df' not in st.session_state:
        st.session_state.data_df = None
    if 'condition_count' not in st.session_state:
        st.session_state.condition_count = 1
    if 'all_images' not in st.session_state:
        st.session_state.all_images = {}

    # CSV FILE READER
    uploaded_file = st.file_uploader("Excel/CSVファイルをアップロード", 
                    type=["xlsx", "xls", "xlsm", "csv"])
    option_form = st.radio("MKSLIDEが作成したCSVファイルですか？", ["Yes", "No"], 
                           index=1 if st.session_state.data_df is None else 0,
                           horizontal=True)

    if uploaded_file:
       if option_form == "No":
          df = mkcsv_gui(uploaded_file)
          df = None 
          st.session_state.data_df = df
       elif option_form == "Yes":
          try:
             file_name = uploaded_file.name.lower()
             if file_name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
             elif file_name.endswith((".xlsx", ".xls", ".xlsm")):
                df = pd.read_excel(uploaded_file, engine="openpyxl")
             else:
                raise ValueError("対応していないファイル形式です。")
             st.session_state.data_df = df
             df_safe = sanitize_for_csv_injection(df.copy())
             #st.dataframe(df_safe, use_container_width=True)
             # 2025/12/03 START
             df_safe.columns = df_safe.columns.map(str)
             # 2025/12/03 END 
             st.dataframe(df_safe, width="content")
             #df = pd.read_csv(uploaded_file)
             #st.session_state.data_df = df
             #df_safe = sanitize_for_csv_injection(df.copy()) 
             #st.dataframe(df_safe, use_container_width=True) 
          except Exception as e:
             st.error(f"CSVファイルの読み込み中にエラーが発生しました: {e}")
             st.session_state.data_df = None
             st.stop()
    
    df = st.session_state.data_df
    if df is None:
       st.info("データファイル（CSV）をアップロードして「Yes」を選択してください。")
       return

    st.markdown("---")

    # UPLOADED FILES
    uploaded_pict = st.file_uploader("画像ファイルを選択してください（複数可）",
                                     type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    #safe_images = {}
    #if uploaded_pict:
    #   for pic in uploaded_pict:
    #       if not scan_file_with_clamav(pic):
    #          st.error(f"ウイルス検出: {pic.name} を拒否しました")
    #          continue
    #       safe_images[sanitize_filename(pic.name)] = safe_open_image(pic)
    #   st.session_state.all_images = safe_images
    #   st.success(f"{len(safe_images)} 件の画像をアップロードしました") 

    st.session_state.all_images = {pic.name: Image.open(pic) for pic in uploaded_pict}
    st.success(f"{len(uploaded_pict)} 件の画像をアップロードしました")

    images = st.session_state.all_images
    if not images:
       st.info("画像ファイルをアップロードしてください。")
       return

    # SELECT
    condition_id = 1
    current_df_ui = df.copy()
    condition_container = st.expander(f"条件を設定/確認", expanded=True)

    for col_name in FILTER_COLS:
        options = ["全て選択"] + current_df_ui[col_name].astype(str).unique().tolist()
        key_multiselect = f'condition_{condition_id}_{col_name}'
        selected_values = st.session_state.get(key_multiselect, ["全て選択"])

        condition_container.multiselect(
            f"▼ {col_name} を選んでください（複数選択可）",
            options=options,
            default=selected_values,
            key=key_multiselect
        )

        if selected_values and "全て選択" not in selected_values:
           current_df_ui = current_df_ui[current_df_ui[col_name].astype(str).isin(selected_values)]

    # FILLTERING RESULTS
    final_results = get_filtered_names_by_multiselect_full_order(df, condition_id=condition_id, filter_cols=FILTER_COLS)

    display_names = [name for name in final_results if name in images]
               
    condition_container.subheader(f"✅ 条件に合致する画像 ({len(display_names)} 件)")
    if len(final_results) == 0:
       condition_container.warning("条件に合致する画像はありません。")
    else:
       cols = condition_container.columns(COLUMNS_PER_ROW)
       for j, name in enumerate(display_names):
           col = cols[j % COLUMNS_PER_ROW]
           #col.image(images[name], use_container_width=True) 
           #col.image(images[name], 
           #          caption=name if len(name) <= 40 else name[:40] + "...", 
           #          use_container_width=True)
           col.image(images[name], 
                     caption=name if len(name) <= 40 else name[:40] + "...", 
                     width="content")
    # PPTX GENERATOR
    if final_results:
       st.subheader("PPTXファイル生成")
       st.info(f"PPTXファイルには、全ての条件で選択された画像 ({len(display_names)} 件) が含まれます。")
       #mkpptx_gui(df, images, final_results)
       mkpptx_gui(df, images, display_names)

# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
