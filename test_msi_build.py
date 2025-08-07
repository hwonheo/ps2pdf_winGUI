#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSI 빌드 테스트 스크립트
로컬에서 MSI 빌드를 테스트하고 문제점을 진단합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """필요한 요구사항들 확인"""
    print("=== 빌드 요구사항 확인 ===")
    
    # Python 버전 확인
    print(f"Python 버전: {sys.version}")
    
    # 필요한 모듈들 확인
    required_modules = ["cx_Freeze", "tkinter", "pathlib"]
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module} 사용 가능")
        except ImportError:
            print(f"✗ {module} 없음 - 설치가 필요합니다")
            return False
    
    # 메인 스크립트 확인
    if not os.path.exists("ps2pdf_converter.py"):
        print("✗ ps2pdf_converter.py를 찾을 수 없습니다")
        return False
    else:
        print("✓ ps2pdf_converter.py 존재")
    
    # 파일 크기 확인
    if os.path.exists("ps"):
        size = os.path.getsize("ps") / 1024  # KB
        print(f"ps 파일 크기: {size:.1f} KB")
        if size > 1024:  # 1MB 이상
            print("경고: ps 파일이 큽니다. MSI에서 제외됩니다.")
    
    return True

def clean_build():
    """빌드 디렉토리 정리"""
    print("\n=== 빌드 디렉토리 정리 ===")
    
    directories_to_clean = ["build", "dist"]
    for dir_name in directories_to_clean:
        if os.path.exists(dir_name):
            print(f"{dir_name} 디렉토리 삭제 중...")
            shutil.rmtree(dir_name)
        else:
            print(f"{dir_name} 디렉토리 없음")

def test_build():
    """실제 빌드 테스트"""
    print("\n=== MSI 빌드 테스트 ===")
    
    try:
        # 먼저 build 단계만 실행
        print("1단계: build 실행 중...")
        result = subprocess.run([sys.executable, "setup_msi.py", "build"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print("✗ build 단계 실패!")
            print(f"표준 출력: {result.stdout}")
            print(f"표준 오류: {result.stderr}")
            return False
        else:
            print("✓ build 단계 성공")
        
        # bdist_msi 단계 실행
        print("2단계: MSI 생성 중...")
        result = subprocess.run([sys.executable, "setup_msi.py", "bdist_msi"], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print("✗ MSI 생성 실패!")
            print(f"표준 출력: {result.stdout}")
            print(f"표준 오류: {result.stderr}")
            return False
        else:
            print("✓ MSI 생성 성공")
            
        # 결과 확인
        dist_dir = Path("dist")
        if dist_dir.exists():
            msi_files = list(dist_dir.glob("*.msi"))
            if msi_files:
                for msi_file in msi_files:
                    size = msi_file.stat().st_size / (1024 * 1024)  # MB
                    print(f"✓ MSI 파일 생성: {msi_file.name} ({size:.1f} MB)")
                return True
            else:
                print("✗ MSI 파일을 찾을 수 없습니다")
                return False
        else:
            print("✗ dist 디렉토리를 찾을 수 없습니다")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ 빌드 시간 초과 (5분)")
        return False
    except Exception as e:
        print(f"✗ 빌드 중 예외 발생: {e}")
        return False

def main():
    """메인 함수"""
    print("PS2PDF MSI 빌드 테스트 도구")
    print("=" * 50)
    
    # 요구사항 확인
    if not check_requirements():
        print("\n빌드 요구사항이 충족되지 않습니다.")
        print("필요한 패키지를 설치하세요: pip install -r requirements.txt")
        return 1
    
    # 빌드 디렉토리 정리
    clean_build()
    
    # 빌드 테스트
    if test_build():
        print("\n🎉 MSI 빌드가 성공했습니다!")
        print("dist/ 디렉토리에서 MSI 파일을 확인하세요.")
        return 0
    else:
        print("\n❌ MSI 빌드가 실패했습니다.")
        print("위의 오류 메시지를 확인하고 문제를 해결하세요.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
