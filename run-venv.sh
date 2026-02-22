#!/bin/bash
# set -e

if ! command -v gcloud &> /dev/null; then
    echo "Error: gcloud command not found. Please install the Google Cloud SDK."
    exit 1
fi

# rm -rf myenv
python3 -m venv myenv
source myenv/bin/activate
python3 -m pip install --upgrade pip
export SYSTEM_VERSION_COMPAT=1
pip3 install -r requirements.txt
streamlit run app.py
# deactivate
# rm -rf myenv