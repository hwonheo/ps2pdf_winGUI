#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows에서 UTF-8 인코딩 문제를 해결하기 위한 스크립트
"""

import sys
import os
import codecs

def setup_utf8_environment():
    """UTF-8 환경 설정"""
    print("Setting up UTF-8 environment for Windows...")
    
    # 환경 변수 설정
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # Windows에서 UTF-8 강제 설정
    if sys.platform.startswith('win'):
        try:
            import locale
            import io
            
            # 기본 인코딩 확인 및 설정
            print(f"Current default encoding: {sys.getdefaultencoding()}")
            print(f"Current file system encoding: {sys.getfilesystemencoding()}")
            print(f"Current locale encoding: {locale.getpreferredencoding()}")
            
            # stdout/stderr 재설정 시도
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            if hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
                
        except Exception as e:
            print(f"UTF-8 setup warning: {e}")
    
    print("UTF-8 environment setup completed.")

def test_file_reading():
    """파일 읽기 테스트"""
    test_files = ['ps2pdf_converter.py', 'setup_msi.py']
    
    for filename in test_files:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✓ Successfully read {filename} ({len(content)} characters)")
            except Exception as e:
                print(f"✗ Failed to read {filename}: {e}")
        else:
            print(f"? File {filename} not found")

if __name__ == "__main__":
    setup_utf8_environment()
    test_file_reading()
    print("Encoding fix script completed.")
