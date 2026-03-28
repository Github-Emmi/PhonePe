"""Geographic page - Geographic Analysis"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._geographic import geographic_page

if __name__ == "__main__":
    geographic_page()
