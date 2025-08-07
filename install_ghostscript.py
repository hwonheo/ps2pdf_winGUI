#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ghostscript 설치 도우미
Windows에서 Ghostscript 다운로드 및 설치 안내
"""

import os
import sys
import webbrowser
import subprocess
import urllib.request
import tempfile
from pathlib import Path

def check_ghostscript():
    """Ghostscript 설치 확인"""
    print("Ghostscript 설치 상태 확인 중...")
    
    gs_commands = ['gswin64c', 'gswin32c', 'gs']
    
    for cmd in gs_commands:
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().split('\n')[0]
                print(f"✓ Ghostscript 발견: {cmd}")
                print(f"✓ 버전: {version}")
                return True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print("✗ Ghostscript가 설치되지 않았거나 PATH에 없습니다.")
    return False

def get_download_info():
    """다운로드 정보 제공"""
    print("\n=== Ghostscript 설치 안내 ===")
    print("Ghostscript는 PostScript 파일을 PDF로 변환하는 데 필요합니다.")
    print()
    
    # Windows 아키텍처 확인
    import platform
    is_64bit = platform.machine().endswith('64')
    
    if is_64bit:
        print("시스템: Windows 64-bit")
        download_url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10021/gs10021w64.exe"
        print(f"권장 다운로드: {download_url}")
    else:
        print("시스템: Windows 32-bit")
        download_url = "https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10021/gs10021w32.exe"
        print(f"권장 다운로드: {download_url}")
    
    print()
    print("설치 방법:")
    print("1. 위 링크에서 Ghostscript를 다운로드하세요.")
    print("2. 다운로드한 exe 파일을 실행하세요.")
    print("3. 설치 시 'Add Ghostscript to PATH' 옵션을 체크하세요.")
    print("4. 설치 완료 후 컴퓨터를 재시작하세요.")
    print()
    
    return download_url

def open_download_page():
    """Ghostscript 다운로드 페이지 열기"""
    try:
        # 공식 다운로드 페이지
        url = "https://www.ghostscript.com/download/gsdnld.html"
        webbrowser.open(url)
        print(f"✓ 브라우저에서 다운로드 페이지를 열었습니다: {url}")
        return True
    except Exception as e:
        print(f"✗ 브라우저 열기 실패: {e}")
        return False

def download_ghostscript():
    """Ghostscript 직접 다운로드 시도"""
    download_url = get_download_info()
    
    try:
        print("\n직접 다운로드를 시도하시겠습니까? (y/n): ", end="")
        choice = input().lower().strip()
        
        if choice != 'y':
            return False
        
        print("다운로드 중... (시간이 오래 걸릴 수 있습니다)")
        
        # 임시 파일로 다운로드
        with tempfile.NamedTemporaryFile(suffix='.exe', delete=False) as tmp_file:
            urllib.request.urlretrieve(download_url, tmp_file.name)
            
            print(f"✓ 다운로드 완료: {tmp_file.name}")
            print("다운로드한 파일을 실행하여 설치하세요.")
            
            # 파일 실행 시도
            try:
                os.startfile(tmp_file.name)
                print("✓ 설치 프로그램을 실행했습니다.")
            except:
                print(f"수동으로 다음 파일을 실행하세요: {tmp_file.name}")
            
            return True
            
    except Exception as e:
        print(f"✗ 다운로드 실패: {e}")
        return False

def main():
    """메인 함수"""
    print("=" * 50)
    print("Ghostscript 설치 도우미")
    print("=" * 50)
    
    # 현재 설치 상태 확인
    if check_ghostscript():
        print("\n✓ Ghostscript가 이미 설치되어 있습니다!")
        print("PS2PDF 변환기를 사용할 수 있습니다.")
        return
    
    print("\nGhostscript 설치가 필요합니다.")
    print()
    print("선택하세요:")
    print("1. 브라우저에서 다운로드 페이지 열기 (권장)")
    print("2. 직접 다운로드 시도")
    print("3. 설치 정보만 표시")
    print("4. 종료")
    
    while True:
        try:
            choice = input("\n선택 (1-4): ").strip()
            
            if choice == '1':
                if open_download_page():
                    get_download_info()
                break
            elif choice == '2':
                download_ghostscript()
                break
            elif choice == '3':
                get_download_info()
                break
            elif choice == '4':
                print("종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 1-4 중에서 선택하세요.")
                
        except KeyboardInterrupt:
            print("\n\n종료합니다.")
            break
        except EOFError:
            break

if __name__ == "__main__":
    main()
