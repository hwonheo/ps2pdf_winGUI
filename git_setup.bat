@echo off
chcp 65001 >nul
title PS2PDF GitHub 저장소 설정

echo ======================================
echo PS2PDF GitHub 저장소 설정
echo ======================================
echo.

:: Git 설치 확인
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Git이 설치되지 않았습니다.
    echo Git을 설치하세요: https://git-scm.com
    echo.
    pause
    exit /b 1
)

:: Git 저장소 초기화
echo Git 저장소 초기화 중...
git init

:: 원격 저장소 추가
echo 원격 저장소 추가 중...
git remote add origin https://github.com/hwonheo/ps2pdf_winGUI.git

:: 모든 파일 추가
echo 파일들을 Git에 추가 중...
git add .

:: 첫 번째 커밋
echo 첫 번째 커밋 생성 중...
git commit -m "Initial commit: PS2PDF 변환기 프로젝트" -m "Features:" -m "- PostScript to PDF 변환 GUI 프로그램" -m "- Tkinter 기반 사용자 인터페이스" -m "- Ghostscript 기반 고품질 변환" -m "- Windows MSI/Portable 자동 빌드 설정" -m "- 다양한 PDF 품질 옵션 지원"

:: 기본 브랜치를 main으로 설정
echo 기본 브랜치를 main으로 설정 중...
git branch -M main

:: 원격 저장소로 푸시
echo GitHub으로 푸시 중...
echo 참고: GitHub 인증이 필요할 수 있습니다.
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ======================================
    echo 설정 완료!
    echo ======================================
    echo.
    echo 다음 단계:
    echo 1. GitHub에서 저장소 확인: https://github.com/hwonheo/ps2pdf_winGUI
    echo 2. GitHub Actions 빌드 상태 확인
    echo 3. 태그를 생성하여 릴리스 빌드 시작:
    echo    git tag v1.0.0
    echo    git push origin v1.0.0
    echo.
    echo MSI 파일은 다음에서 다운로드 가능:
    echo - Actions 탭의 아티팩트 (매 커밋마다)
    echo - Releases 탭 (태그 생성 시)
) else (
    echo.
    echo [오류] 푸시에 실패했습니다.
    echo GitHub 인증을 확인하고 다시 시도하세요.
)

echo.
pause
