#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cx_Freeze를 사용한 Windows MSI 패키지 생성 스크립트
"""

import sys
import os
from cx_Freeze import setup, Executable

# 현재 버전 정보
VERSION = "1.0.0"
DESCRIPTION = "PostScript to PDF 변환기"
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
    print("경고: ps 파일이 너무 크거나 없어서 MSI에서 제외됩니다.")

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
        "keywords": "PostScript PDF 변환기"
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
    shortcut_name="PS2PDF 변환기",
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
