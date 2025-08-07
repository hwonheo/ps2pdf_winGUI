@echo off
chcp 65001 >nul
title PS2PDF Windows 빌드

echo ================================================
echo        PS2PDF 변환기 Windows 실행 파일 빌드
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

echo Python 버전:
python --version
echo.

:: 빌드 스크립트 실행
echo 빌드 스크립트를 실행합니다...
python build_windows.py

echo.
echo ================================================
echo 빌드가 완료되었습니다.
echo 실행 파일: dist\PS2PDF_Converter.exe
echo ================================================
echo.

:: 실행 파일 존재 확인
if exist "dist\PS2PDF_Converter.exe" (
    echo [성공] 실행 파일이 성공적으로 생성되었습니다!
    echo.
    echo 실행 파일을 테스트하시겠습니까? (y/n):
    set /p choice=
    if /i "%choice%"=="y" (
        echo 실행 파일을 테스트합니다...
        start dist\PS2PDF_Converter.exe
    )
) else (
    echo [실패] 실행 파일 생성에 실패했습니다.
    echo 위의 오류 메시지를 확인하세요.
)

echo.
pause
