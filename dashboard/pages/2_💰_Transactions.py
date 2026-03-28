"""Transactions page - Transaction Analytics"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from pages._transactions import transactions_page

if __name__ == "__main__":
    transactions_page()
