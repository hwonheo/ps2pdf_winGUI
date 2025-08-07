#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cx_Freeze를 사용한 Windows MSI 패키지 생성 스크립트
"""

import sys
import os
from cx_Freeze import setup, Executable

# Windows에서 UTF-8 인코딩 강제 설정
if sys.platform.startswith('win'):
    import locale
    import codecs
    import io
    
    # 환경 변수 설정
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    os.environ['PYTHONUTF8'] = '1'
    
    # stdout/stderr UTF-8 설정
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())
    except:
        # 이미 설정되어 있거나 실패할 경우 무시
        pass
    
    # 기본 인코딩 설정 시도
    try:
        import _locale
        _locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
    except:
        pass

# 현재 버전 정보
VERSION = "1.0.0"
DESCRIPTION = "PostScript to PDF Converter"
AUTHOR = "PS2PDF Team"

# 실행 파일에 포함할 모듈들
includes = [
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "subprocess",
    "threading",
    "pathlib",
    "os",
    "sys",
    "platform",
    "shutil",
    "time"
]

# 제외할 모듈들 (크기 최적화)
excludes = [
    "unittest",
    "email",
    "html",
    "http",
    "urllib3",
    "xml",
    "test",
    "distutils",
    "numpy",
    "scipy",
    "matplotlib",
    "pandas"
]

# 포함할 파일들
include_files = [
    ("README.md", "README.md"),
    ("LICENSE", "LICENSE")
]

# ps 파일이 존재하고 크기가 적당하면 포함
if os.path.exists("ps") and os.path.getsize("ps") < 1024 * 1024:  # 1MB 미만
    include_files.append(("ps", "ps"))
else:
    print("Warning: ps file is too large or missing, excluded from MSI.")

# 아이콘 파일 처리 (없으면 None)
icon_file = None
if os.path.exists("icon.ico"):
    icon_file = "icon.ico"

# 빌드 옵션
build_exe_options = {
    "packages": ["tkinter"],
    "includes": includes,
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
    "build_exe": "build/PS2PDF_Converter",
    "include_msvcrt": True,
    "silent": True
}

# MSI 옵션
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-5678-9012-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\PS2PDF Converter",
    "summary_data": {
        "author": AUTHOR,
        "comments": DESCRIPTION,
        "keywords": "PostScript PDF Converter"
    }
}

# 아이콘이 있으면 MSI 옵션에 추가
if icon_file:
    bdist_msi_options["install_icon"] = icon_file

# 실행 파일 설정
executable = Executable(
    script="ps2pdf_converter.py",
    base="Win32GUI",  # GUI 애플리케이션
    target_name="PS2PDF_Converter.exe",
    icon=icon_file,  # 아이콘 파일 경로 (있다면)
    shortcut_name="PS2PDF Converter",
    shortcut_dir="DesktopFolder"
)

# 설정
setup(
    name="PS2PDF Converter",
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    executables=[executable],
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    }
)
