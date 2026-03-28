"""Reports page - Reports & Data Export"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._reports import reports_page

if __name__ == "__main__":
    reports_page()
