# streamlit-link-button-extended

Streamlit Component that allows the developer to track when it's been clicked

## Installation instructions 

```sh
pip install streamlit-link-button-extended
```

## Usage instructions

```python
import streamlit as st

from streamlit_link_button_extended import streamlit_link_button_extended

label = "Google"
url = "https://www.google.com"

streamlit_link_button_extended(label, url, key="google_link_button")

