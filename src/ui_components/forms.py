import streamlit as st
from typing import List, Optional


def dynamic_list_input(
        label: str,
        key: str,
        default_value: Optional[List[str]] = None
) -> List[str]:
    """
    Creates a dynamic list input form using Streamlit's session state.
    """
    if key not in st.session_state:
        if default_value:
            st.session_state[key] = default_value
        else:
            st.session_state[key] = [""]

    st.markdown(f"**{label}**")

    current_list = st.session_state[key]
    new_list = []

    # We use a container to manage the dynamic buttons and inputs
    with st.container():
        for i, item in enumerate(current_list):
            col1, col2 = st.columns([10, 1])
            with col1:
                new_item = st.text_input(
                    label=f"Item {i + 1}",
                    value=item,
                    label_visibility="collapsed",
                    key=f"{key}_item_{i}"
                )
                new_list.append(new_item)
            with col2:
                if st.button("x", key=f"{key}_remove_{i}"):
                    st.session_state[key].pop(i)
                    st.rerun()

    st.session_state[key] = new_list

    if st.button("Add another", key=f"{key}_add_button"):
        st.session_state[key].append("")
        st.rerun()

    return [item for item in st.session_state[key] if item]
