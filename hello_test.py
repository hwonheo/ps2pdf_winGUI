#!/usr/bin/env python3
"""
간단한 테스트 스크립트
"""

print("Hello, World!")
print("Python is working correctly!")

import tkinter as tk
print("tkinter imported successfully!")

root = tk.Tk()
root.withdraw()  # 창을 숨김
print("tkinter window created successfully!")

import subprocess
print("subprocess imported successfully!")

import threading
print("threading imported successfully!")

print("All imports successful! Ready for PyInstaller!")
