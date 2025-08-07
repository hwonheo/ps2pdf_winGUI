#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 실행 파일 빌드 스크립트
PyInstaller를 사용하여 ps2pdf_converter.py를 exe 파일로 변환
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_exe():
    """Windows 실행 파일 빌드"""
    print("PS2PDF 변환기 Windows 실행 파일 빌드 시작...")
    
    # 현재 디렉토리 확인
    script_dir = Path(__file__).parent
    main_script = script_dir / "ps2pdf_converter.py"
    
    if not main_script.exists():
        print(f"오류: {main_script}을 찾을 수 없습니다.")
        return False
    
    # 빌드 디렉토리 정리
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        dir_path = script_dir / dir_name
        if dir_path.exists():
            print(f"{dir_name} 디렉토리 정리 중...")
            shutil.rmtree(dir_path)
    
    # spec 파일 삭제 (새로 생성하기 위해)
    spec_file = script_dir / "ps2pdf_converter.spec"
    if spec_file.exists():
        spec_file.unlink()
    
    try:
        # PyInstaller 명령 구성
        cmd = [
            "pyinstaller",
            "--onefile",                    # 단일 실행 파일
            "--windowed",                   # 콘솔 창 숨기기
            "--name=PS2PDF_Converter",      # 실행 파일 이름
            "--icon=NONE",                  # 아이콘 (없으면 기본값)
            "--add-data=ps;.",              # PS 샘플 파일 포함
            str(main_script)
        ]
        
        print("PyInstaller 실행 중...")
        print(f"명령: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ 빌드 성공!")
            
            # 생성된 파일 위치 확인
            exe_file = script_dir / "dist" / "PS2PDF_Converter.exe"
            if exe_file.exists():
                file_size = exe_file.stat().st_size / (1024 * 1024)  # MB
                print(f"✓ 실행 파일 생성: {exe_file}")
                print(f"✓ 파일 크기: {file_size:.1f} MB")
                
                # 사용 안내
                print("\n=== 사용 안내 ===")
                print("1. Ghostscript가 설치되어 있어야 합니다:")
                print("   https://www.ghostscript.com/download/gsdnld.html")
                print("2. PS2PDF_Converter.exe를 실행하세요.")
                print("3. PS 파일을 선택하고 변환 버튼을 클릭하세요.")
                
                return True
            else:
                print("✗ 실행 파일을 찾을 수 없습니다.")
                return False
        else:
            print("✗ 빌드 실패!")
            print(f"표준 출력: {result.stdout}")
            print(f"표준 오류: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("✗ PyInstaller를 찾을 수 없습니다.")
        print("다음 명령으로 설치하세요: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"✗ 빌드 중 오류 발생: {e}")
        return False

def install_requirements():
    """필요한 패키지 설치"""
    print("필요한 패키지 설치 중...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✓ 패키지 설치 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 패키지 설치 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("=" * 50)
    print("PS2PDF 변환기 Windows 빌드 도구")
    print("=" * 50)
    
    # 패키지 설치
    if not install_requirements():
        print("패키지 설치에 실패했습니다. 수동으로 설치하세요:")
        print("pip install -r requirements.txt")
        return
    
    # 실행 파일 빌드
    if build_exe():
        print("\n빌드가 완료되었습니다!")
    else:
        print("\n빌드에 실패했습니다.")

if __name__ == "__main__":
    main()
