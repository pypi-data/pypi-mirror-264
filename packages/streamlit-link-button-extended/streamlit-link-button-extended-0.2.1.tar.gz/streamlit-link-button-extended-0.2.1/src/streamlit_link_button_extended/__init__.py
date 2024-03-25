from pathlib import Path
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components

# Path to the directory where the frontend code lives
frontend_dir = (Path(__file__).parent / "frontend").absolute()

# Declare the component
_component_func = components.declare_component(
    "streamlit_link_button_extended", 
    path=str(frontend_dir)
)

def streamlit_link_button_extended(
    label: str,
    url: str,
    disabled: Optional[bool] = False,
    type: Optional[str] = "secondary",
    key: Optional[str] = None,
) -> bool:
    """
    A custom Streamlit component that creates a link button with tracking capability.
    
    Parameters:
    - label (str): The text displayed on the button.
    - url (str): The URL to open when the button is clicked.
    - disabled (bool, optional): If True, the button is disabled. Default is False.
    - type (str, optional): The button style type, e.g., "primary" or "secondary". Default is "secondary".
    - key (str, optional): An optional key that uniquely identifies this component instance.

    Returns:
    - bool: True if the button was clicked, False otherwise.
    """
    component_value = _component_func(
        label=label,
        url=url,
        disabled=disabled,
        type=type,
        key=key,
        default=False,  # Default value returned if the component hasn't been interacted with
    )

    return component_value


def main():
    """
    Example usage of the custom Streamlit component.
    """
    st.session_state.setdefault("clicked", False)
    if st.button("Mock user query"):
        with st.expander("Author, document, section, date"):
            st.markdown("Mock response summary")
            clicked = streamlit_link_button_extended(
                label="Visit Google",
                url="https://www.google.com",
                key="google_link"
            )

        
    if st.session_state.clicked:
        st.write("The button was clicked!")

if __name__ == "__main__":
    main()