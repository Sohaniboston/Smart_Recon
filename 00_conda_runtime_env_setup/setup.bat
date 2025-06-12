@echo off
echo Setting up smart_recon_apps environment...

:: Create conda environment
call conda create -n smart_recon_apps python=3.9 -y
if %ERRORLEVEL% neq 0 (
    echo Failed to create conda environment.
    exit /b %ERRORLEVEL%
)

:: Activate environment
call conda activate smart_recon_apps
if %ERRORLEVEL% neq 0 (
    echo Failed to activate environment.
    exit /b %ERRORLEVEL%
)

:: Install packages
call conda install -c conda-forge pandas -y
call conda install -c conda-forge faker -y

echo Environment setup complete!
echo To activate the environment, run: conda activate smart_recon_apps
