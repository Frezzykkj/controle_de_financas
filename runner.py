import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "streamlit_app.py"]
sys.exit(stcli.main())