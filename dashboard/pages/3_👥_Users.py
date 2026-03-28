"""Users page - User Analytics"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._users import users_page

if __name__ == "__main__":
    users_page()
