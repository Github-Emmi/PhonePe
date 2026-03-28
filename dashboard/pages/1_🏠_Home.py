"""Home page - PhonePe Dashboard Overview"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._home import home_page

if __name__ == "__main__":
    home_page()
