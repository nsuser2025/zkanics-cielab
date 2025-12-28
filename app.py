# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import json
import os

#st.set_page_config(layout="wide")　最大化

markdown_contents = {}
note_paths = {
    "topics0001": "notes/topics0001.md",
    "topics0002": "notes/topics0002.md",
    "topics0003": "notes/topics0003.md",
    "topics0004": "notes/topics0004.md",
    "dem_geldart": "DEM/geldart.md",
    "dem_install": "DEM/install.md",
    "dem_parallel": "DEM/parallel.md",
}

for key, path in note_paths.items():
    try:
        with open(path, "r", encoding="utf-8") as f:
            markdown_contents[key] = f.read()
    except FileNotFoundError:
        st.error(f"ZKANICS ERROR: note file not found: {path}")
        st.stop()

markdown_json = json.dumps(markdown_contents)

with open("index.html", encoding="utf-8") as f:
    html_template = f.read()

html_content = html_template.replace(
    "// MARKDOWN_DATA_PLACEHOLDER",
    f"const allMarkdownData = {markdown_json};"
)

components.html(html_content, height=2000, scrolling=True)
#components.html(html_content, height=800, width=None, scrolling=True)　最大化
