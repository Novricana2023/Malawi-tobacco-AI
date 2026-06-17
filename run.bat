@echo off
cd /d "%~dp0"
echo Starting Tobacco Farmer Assist Malawi...
echo Open http://localhost:8501 in your browser
python -m streamlit run app.py --server.port 8501
pause
