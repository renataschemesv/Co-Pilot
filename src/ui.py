from pathlib import Path

import streamlit as st


def render_page_feature(image_name: str, heading: str, description: str, caption: str) -> None:
    image_path = Path(__file__).resolve().parent.parent / "imagens" / image_name

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3 {
            color: #00377f;
        }
        [data-testid="stImage"] img {
            border-radius: 8px;
            box-shadow: 0 12px 28px rgba(20, 72, 117, 0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    image_column, copy_column = st.columns([1.15, 1], gap="large")
    with image_column:
        st.image(str(image_path), use_container_width=True)
        st.caption(caption)
    with copy_column:
        st.subheader(heading)
        st.write(description)