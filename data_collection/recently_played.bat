set CONDAPATH=$YOUR_ANACONDA_FOLDER_PATH
set ENVPATH=%CONDAPATH%
call %CONDAPATH%\Scripts\activate.bat %ENVPATH%
cd "$YOUR_PYTHON_SCRIPT_PATH"
python recently_played_spotify.py
