import streamlit as st
import string
import pandas as pd
from openpyxl import load_workbook

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


def mkcsv_gui(uploaded_file):

    file_name = uploaded_file.name.lower()

    # --- ファイル形式を判定 ---
    is_csv = file_name.endswith(".csv")
    is_excel = file_name.endswith((".xlsx", ".xls", ".xlsm"))

    if not (is_csv or is_excel):
        st.error("対応形式は CSV / Excel のみです。")
        st.stop()

    # --- Excel の場合 ---
    if is_excel:
        try:
            wb = load_workbook(uploaded_file, data_only=True)
            ws = wb.active
        except Exception as e:
            st.error(f"Excel ファイル読み込みエラー: {e}")
            st.stop()

        # Excel を pandas 読み込み
        df_orig = pd.read_excel(uploaded_file, header=None)

    # --- CSV の場合 ---
    else:
        # CSV は load_workbook 不要
        wb = None
        ws = None

        try:
            df_orig = pd.read_csv(uploaded_file, header=None, encoding="utf-8")
        except Exception:
            # Excel 形式として開いて再チャレンジ（Shift-JISなど）
            try:
                df_orig = pd.read_csv(uploaded_file, header=None, encoding="shift_jis")
            except Exception as e:
                st.error(f"CSV ファイル読み込みエラー: {e}")
                st.stop()

    # --- 表示処理 ---
    df_orig.columns = list(string.ascii_uppercase[:len(df_orig.columns)])
    df_orig.index = range(1, len(df_orig) + 1)

    df_orig_safe = sanitize_for_csv_injection(df_orig.copy())
    df_orig_safe.columns = df_orig_safe.columns.map(str)

    st.dataframe(df_orig_safe)
    st.markdown("---")

    # Excel のときだけ範囲指定の GUI を表示
    if is_excel:
        st.markdown("**各データのExcel範囲を A1:A10 のように入力してください。（1列のみ対応）**")

        file_input = st.text_input("ファイル名範囲", value="A1:A10", key="k_file")
        exam_input = st.text_input("試験範囲", value="B1:B10", key="k_exam")
        face_input = st.text_input("測定面範囲", value="C1:C10", key="k_face")
        cath_input = st.text_input("正極範囲", value="D1:D10", key="k_cath")
        mesu_input = st.text_input("測定範囲", value="E1:E10", key="k_mesu")
        elec_input = st.text_input("電解液範囲", value="F1:F10", key="k_elec")
        magn_input = st.text_input("倍率範囲", value="G1:G10", key="k_magn")

        range_inputs = {
            "ファイル名": file_input,
            "試験": exam_input,
            "測定面": face_input,
            "正極": cath_input,
            "測定": mesu_input,
            "電解液": elec_input,
            "倍率": magn_input,
        }

        # 範囲抽出処理（Excelのみ）
        def extract_range_data(range_str):
            try:
                cells = ws[range_str]
                return [c[0].value for c in cells], None
            except:
                return None, f"無効な範囲: {range_str}"

        if st.button("CSVファイルを生成"):
            extracted_data = {}
            errors = []

            for col_name, range_str in range_inputs.items():
                lst, err = extract_range_data(range_str)
                if err:
                    errors.append(f"{col_name}: {err}")
                extracted_data[col_name] = lst

            if errors:
                st.error("範囲エラーがあります")
                for e in errors:
                    st.write("- " + e)
                st.stop()

            df_out = pd.DataFrame(extracted_data)
            df_safe = sanitize_for_csv_injection(df_out.copy())
            df_safe.columns = df_safe.columns.map(str)

            st.dataframe(df_safe)
            return df_out

    # CSV の場合はそのまま返す
    return df_orig_safe


# MODULE ERROR MESSAGE
if __name__ == "__main__":
   raise RuntimeError("Do not run this file directly; use it as a module.")
