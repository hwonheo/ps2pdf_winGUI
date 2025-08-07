@echo off
chcp 65001 >nul
title PS2PDF 변환기

echo ================================================
echo           PS2PDF 변환기 실행
echo ================================================
echo.

:: Python 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되지 않았습니다.
    echo Python 3.7 이상을 설치하세요: https://python.org
    echo.
    pause
    exit /b 1
)

:: 가상환경 활성화 (있는 경우)
if exist "venv\Scripts\activate.bat" (
    echo 가상환경 활성화 중...
    call venv\Scripts\activate.bat
)

:: 패키지 설치 확인
echo 필요한 패키지 확인 중...
pip install -r requirements.txt >nul 2>&1

:: 프로그램 실행
echo PS2PDF 변환기를 시작합니다...
echo.
python ps2pdf_converter.py

:: 종료 메시지
echo.
echo ================================================
echo 프로그램이 종료되었습니다.
echo ================================================
pause
