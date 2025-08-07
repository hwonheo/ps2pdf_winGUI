#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PS to PDF Converter
Windows용 PostScript 파일을 PDF로 변환하는 GUI 프로그램
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess
import threading
from pathlib import Path
import sys

class PS2PDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PS to PDF 변환기")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        self.check_ghostscript()
        
    def setup_ui(self):
        """UI 구성 요소 설정"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="PostScript to PDF 변환기", 
                               font=("맑은 고딕", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 입력 파일 선택
        ttk.Label(main_frame, text="PS 파일 선택:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.input_path = tk.StringVar()
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(input_frame, text="찾아보기", 
                  command=self.browse_input_file).grid(row=0, column=1)
        
        input_frame.columnconfigure(0, weight=1)
        
        # 출력 폴더 선택
        ttk.Label(main_frame, text="출력 폴더:").grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        
        self.output_path = tk.StringVar()
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="찾아보기", 
                  command=self.browse_output_folder).grid(row=0, column=1)
        
        output_frame.columnconfigure(0, weight=1)
        
        # 옵션 설정
        options_frame = ttk.LabelFrame(main_frame, text="변환 옵션", padding="10")
        options_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # PDF 품질 설정
        ttk.Label(options_frame, text="PDF 품질:").grid(row=0, column=0, sticky=tk.W)
        self.quality = tk.StringVar(value="ebook")
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality, 
                                   values=["screen", "ebook", "printer", "prepress"],
                                   state="readonly", width=15)
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 해상도 설정
        ttk.Label(options_frame, text="해상도 (DPI):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.resolution = tk.StringVar(value="300")
        resolution_spin = ttk.Spinbox(options_frame, from_=72, to=1200, increment=50,
                                    textvariable=self.resolution, width=15)
        resolution_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # 변환 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        self.convert_button = ttk.Button(button_frame, text="변환 시작", 
                                       command=self.start_conversion,
                                       style="Accent.TButton")
        self.convert_button.grid(row=0, column=0, padx=10)
        
        self.clear_button = ttk.Button(button_frame, text="초기화", 
                                     command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=10)
        
        # 진행 상황 표시
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # 상태 메시지
        self.status_var = tk.StringVar(value="변환할 PS 파일을 선택하세요.")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               foreground="blue")
        status_label.grid(row=8, column=0, columnspan=3, pady=5)
        
        # 로그 영역
        log_frame = ttk.LabelFrame(main_frame, text="변환 로그", padding="5")
        log_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(9, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def check_ghostscript(self):
        """Ghostscript 설치 확인"""
        try:
            # Windows에서 Ghostscript 경로 확인
            gs_commands = ['gswin64c', 'gswin32c', 'gs']
            gs_found = False
            
            for cmd in gs_commands:
                try:
                    subprocess.run([cmd, '--version'], 
                                 capture_output=True, check=True, timeout=5)
                    self.gs_command = cmd
                    gs_found = True
                    break
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    continue
            
            if not gs_found:
                self.log_message("경고: Ghostscript가 설치되지 않았거나 PATH에 없습니다.")
                self.log_message("Ghostscript 다운로드: https://www.ghostscript.com/download/gsdnld.html")
                self.convert_button.configure(state='disabled')
            else:
                self.log_message(f"Ghostscript 발견: {self.gs_command}")
                
        except Exception as e:
            self.log_message(f"Ghostscript 확인 중 오류: {str(e)}")
    
    def browse_input_file(self):
        """입력 파일 선택"""
        filename = filedialog.askopenfilename(
            title="PS 파일 선택",
            filetypes=[("PostScript files", "*.ps"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            # 출력 폴더가 비어있으면 입력 파일과 같은 폴더로 설정
            if not self.output_path.get():
                self.output_path.set(os.path.dirname(filename))
            self.status_var.set("PS 파일이 선택되었습니다.")
    
    def browse_output_folder(self):
        """출력 폴더 선택"""
        folder = filedialog.askdirectory(title="출력 폴더 선택")
        if folder:
            self.output_path.set(folder)
    
    def clear_fields(self):
        """입력 필드 초기화"""
        self.input_path.set("")
        self.output_path.set("")
        self.status_var.set("변환할 PS 파일을 선택하세요.")
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message):
        """로그 메시지 추가"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_conversion(self):
        """변환 시작 (별도 스레드에서 실행)"""
        if not self.input_path.get():
            messagebox.showerror("오류", "PS 파일을 선택하세요.")
            return
        
        if not self.output_path.get():
            messagebox.showerror("오류", "출력 폴더를 선택하세요.")
            return
        
        if not os.path.exists(self.input_path.get()):
            messagebox.showerror("오류", "입력 파일이 존재하지 않습니다.")
            return
        
        if not os.path.exists(self.output_path.get()):
            messagebox.showerror("오류", "출력 폴더가 존재하지 않습니다.")
            return
        
        # UI 상태 변경
        self.convert_button.configure(state='disabled')
        self.progress.start()
        self.status_var.set("변환 중...")
        
        # 별도 스레드에서 변환 실행
        threading.Thread(target=self.convert_file, daemon=True).start()
    
    def convert_file(self):
        """실제 파일 변환 수행"""
        try:
            input_file = self.input_path.get()
            output_dir = self.output_path.get()
            
            # 출력 파일명 생성
            input_name = Path(input_file).stem
            output_file = os.path.join(output_dir, f"{input_name}.pdf")
            
            self.log_message(f"변환 시작: {os.path.basename(input_file)} -> {os.path.basename(output_file)}")
            
            # Ghostscript 명령 구성
            quality_settings = {
                "screen": ["-dPDFSETTINGS=/screen"],
                "ebook": ["-dPDFSETTINGS=/ebook"],
                "printer": ["-dPDFSETTINGS=/printer"],
                "prepress": ["-dPDFSETTINGS=/prepress"]
            }
            
            cmd = [
                self.gs_command,
                "-dNOPAUSE",
                "-dBATCH",
                "-dSAFER",
                "-sDEVICE=pdfwrite",
                f"-r{self.resolution.get()}",
                *quality_settings.get(self.quality.get(), ["-dPDFSETTINGS=/ebook"]),
                f"-sOutputFile={output_file}",
                input_file
            ]
            
            self.log_message(f"실행 명령: {' '.join(cmd)}")
            
            # 변환 실행
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_message("✓ 변환 완료!")
                self.log_message(f"출력 파일: {output_file}")
                
                # UI 스레드에서 메시지박스 표시
                self.root.after(0, lambda: messagebox.showinfo(
                    "완료", f"변환이 완료되었습니다!\n\n출력 파일: {output_file}"))
                    
                self.root.after(0, lambda: self.status_var.set("변환 완료"))
            else:
                error_msg = result.stderr or result.stdout or "알 수 없는 오류"
                self.log_message(f"✗ 변환 실패: {error_msg}")
                self.root.after(0, lambda: messagebox.showerror(
                    "변환 실패", f"변환 중 오류가 발생했습니다:\n{error_msg}"))
                self.root.after(0, lambda: self.status_var.set("변환 실패"))
                
        except subprocess.TimeoutExpired:
            self.log_message("✗ 변환 시간 초과 (60초)")
            self.root.after(0, lambda: messagebox.showerror(
                "시간 초과", "변환 시간이 60초를 초과했습니다."))
            self.root.after(0, lambda: self.status_var.set("변환 시간 초과"))
            
        except Exception as e:
            self.log_message(f"✗ 예외 발생: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror(
                "오류", f"예기치 않은 오류가 발생했습니다:\n{str(e)}"))
            self.root.after(0, lambda: self.status_var.set("변환 오류"))
            
        finally:
            # UI 상태 복원
            self.root.after(0, self.reset_ui)
    
    def reset_ui(self):
        """UI 상태 복원"""
        self.progress.stop()
        self.convert_button.configure(state='normal')

def main():
    """메인 함수"""
    root = tk.Tk()
    app = PS2PDFConverter(root)
    
    # 아이콘 설정 시도 (실패해도 계속 진행)
    try:
        # 프로그램 아이콘이 있다면 설정
        pass
    except:
        pass
    
    root.mainloop()

if __name__ == "__main__":
    main()
