@echo off
setlocal enabledelayedexpansion
REM Corpus Analysis Masterclass - Windows launcher.
REM
REM Double-click this file. It finds conda, offers to install it if you have none,
REM builds the course environment the first time, then starts JupyterLab.
REM
REM You do not need the Anaconda Prompt, and there is no "conda activate" step,
REM because "conda run" does the same job on its own.

cd /d "%~dp0"

set "MINIFORGE_HOME=%USERPROFILE%\miniforge3"

call :find_conda
if defined CONDA goto have_conda

echo.
echo This machine has no conda, which is what builds the course environment.
echo.
echo I can install Miniforge, the community build of conda. If you say yes:
echo.
echo   - about 75 MB is downloaded from conda-forge.org
echo   - everything goes in one folder, %MINIFORGE_HOME%
echo   - no administrator password is needed
echo   - it is not registered as your system Python, so other software is unaffected
echo   - to undo it later, delete that one folder
echo.
set /p "ANSWER=Install Miniforge now? [y/N] "
if /i not "%ANSWER%"=="y" if /i not "%ANSWER%"=="yes" (
    echo.
    echo Nothing was installed.
    goto no_conda
)

set "INSTALLER=%TEMP%\Miniforge3-Windows-x86_64.exe"
echo.
echo Downloading Miniforge ...
curl -fL --progress-bar -o "%INSTALLER%" "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
if errorlevel 1 (
    echo The download did not finish.
    goto no_conda
)

echo Installing into %MINIFORGE_HOME% ...
REM JustMe keeps it in your own account, RegisterPython=0 leaves other software alone,
REM and /S runs it without further questions.
start /wait "" "%INSTALLER%" /InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=%MINIFORGE_HOME%
if errorlevel 1 (
    echo The Miniforge install did not finish.
    goto no_conda
)
del "%INSTALLER%" >nul 2>&1
echo Miniforge installed.

call :find_conda
if defined CONDA goto have_conda

:no_conda
echo.
echo Without conda the course notebooks cannot run.
echo Ask an instructor, or open the notebooks in Google Colab instead.
echo.
pause
exit /b 1

:have_conda
echo Using conda at: %CONDA%

call "%CONDA%" env list | findstr /R /C:"^corpusanalysis " >nul
if errorlevel 1 (
    echo.
    echo First run: building the corpusanalysis environment.
    echo This downloads a few hundred megabytes and takes several minutes.
    echo Leave it alone until it finishes.
    echo.
    call "%CONDA%" env create -f environment.yml
    if errorlevel 1 (
        echo.
        echo The environment did not build. Show this window to an instructor.
        pause
        exit /b 1
    )
) else (
    echo The corpusanalysis environment is already built.
)

REM CI sets COURSE_LAUNCHER_SELFTEST to check this script end to end without leaving a
REM server running forever. Students never set it, so they never see this branch.
if defined COURSE_LAUNCHER_SELFTEST (
    echo.
    echo Self-test: confirming JupyterLab runs, rather than starting it.
    call "%CONDA%" run --no-capture-output -n corpusanalysis jupyter lab --version
    exit /b %errorlevel%
)

echo.
echo Starting JupyterLab. Your browser should open on its own.
echo Leave this window open while you work, and close it when you are done.
echo.
call "%CONDA%" run --no-capture-output -n corpusanalysis jupyter lab
pause
exit /b 0

:find_conda
set "CONDA="
for %%C in (
    "%MINIFORGE_HOME%\condabin\conda.bat"
    "%USERPROFILE%\miniconda3\condabin\conda.bat"
    "%USERPROFILE%\anaconda3\condabin\conda.bat"
    "%USERPROFILE%\AppData\Local\miniforge3\condabin\conda.bat"
    "%USERPROFILE%\AppData\Local\miniconda3\condabin\conda.bat"
    "%USERPROFILE%\AppData\Local\Continuum\anaconda3\condabin\conda.bat"
    "%PROGRAMDATA%\miniforge3\condabin\conda.bat"
    "%PROGRAMDATA%\Miniconda3\condabin\conda.bat"
    "%PROGRAMDATA%\Anaconda3\condabin\conda.bat"
) do (
    if not defined CONDA if exist %%C set "CONDA=%%~C"
)
if not defined CONDA (
    for /f "delims=" %%P in ('where conda.bat 2^>nul') do (
        if not defined CONDA set "CONDA=%%P"
    )
)
exit /b 0
