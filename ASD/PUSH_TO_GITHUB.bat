@echo off
title ASD App - GitHub Push
color 0A
echo.
echo =====================================================
echo    ASD Prediction System - GitHub Deploy
echo =====================================================
echo.
echo [1/5] Initializing git...
git init
echo.
echo [2/5] Adding all files...
git add .
echo.
echo [3/5] Creating commit...
git commit -m "ASD Prediction System - full deploy"
echo.
echo [4/5] Setting branch to main...
git branch -M main
echo.
echo [5/5] Pushing to GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/kapse91-repo/asd-prediction-system.git
git push -f https://kapse91-repo:ghp_Ql0zBNomc09wGT62XaaXxa0XNdBTZf3fCjC5@github.com/kapse91-repo/asd-prediction-system.git main

echo.
echo =====================================================
if %errorlevel% == 0 (
    echo    SUCCESS! Code pushed to GitHub!
    echo    Streamlit will redeploy in 2-3 minutes.
    echo    URL: https://asdprediction.streamlit.app
) else (
    echo    ERROR: Push failed. Check above for details.
)
echo =====================================================
echo.
pause
