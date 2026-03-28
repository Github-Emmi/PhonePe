"""Insurance page - Insurance Insights"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._insurance import insurance_page

if __name__ == "__main__":
    insurance_page()
