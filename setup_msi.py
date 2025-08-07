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
    "sys"
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
    ("ps", "ps"),  # 샘플 PS 파일
    ("README.md", "README.md"),
    ("LICENSE", "LICENSE")
]

# 빌드 옵션
build_exe_options = {
    "packages": [],
    "includes": includes,
    "excludes": excludes,
    "include_files": include_files,
    "optimize": 2,
    "build_exe": "build/PS2PDF_Converter"
}

# MSI 옵션
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-5678-9012-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\PS2PDF Converter",
    "install_icon": "icon.ico"  # 아이콘 파일이 있다면
}

# 실행 파일 설정
executable = Executable(
    script="ps2pdf_converter.py",
    base="Win32GUI",  # GUI 애플리케이션
    target_name="PS2PDF_Converter.exe",
    icon=None,  # 아이콘 파일 경로 (있다면)
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
