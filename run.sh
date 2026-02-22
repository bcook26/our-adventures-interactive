#!/bin/bash

# Quick start script for Adventures streamlit app

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run the Streamlit app
streamlit run app.py --server.port=8501 --server.address=localhost