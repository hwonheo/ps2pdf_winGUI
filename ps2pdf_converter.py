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
import webbrowser

# 서드파티 라이브러리
import cairosvg
from PIL import Image
from PyPDF2 import PdfMerger

class PS2PDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PS to PDF 변환기")
        self.root.geometry("750x650")
        self.root.resizable(True, True)
        
        # Ghostscript 사용 가능 여부 플래그
        self.gs_available = False
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        self.style = style
        
        self.setup_ui()
        self.check_ghostscript()
        
    def setup_ui(self):
        """UI 구성 요소 설정"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="PostScript to PDF 변환기", 
                               font=("맑은 고딕", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

        # 링크 & 테마 설정 행
        link_label = ttk.Label(main_frame, text="Ghostscript 다운로드", foreground="blue", cursor="hand2")
        link_label.grid(row=1, column=0, sticky=tk.W)
        link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.ghostscript.com/download/gsdnld.html"))

        ttk.Label(main_frame, text="테마:").grid(row=1, column=2, sticky=tk.E)
        self.theme_var = tk.StringVar(value="light")
        theme_combo = ttk.Combobox(main_frame, textvariable=self.theme_var, values=["light", "dark"], state="readonly", width=8)
        theme_combo.grid(row=1, column=3, sticky=tk.E)
        theme_combo.bind("<<ComboboxSelected>>", lambda e: self.apply_theme())

        # 입력 파일 선택
        ttk.Label(main_frame, text="PS 파일 선택:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.input_path = tk.StringVar()
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_path, width=50)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(input_frame, text="찾아보기", 
                  command=self.browse_input_file).grid(row=0, column=1)
        
        input_frame.columnconfigure(0, weight=1)
        
        # 출력 폴더 선택
        ttk.Label(main_frame, text="출력 폴더:").grid(row=4, column=0, sticky=tk.W, pady=(20, 5))
        
        self.output_path = tk.StringVar()
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=5, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(output_frame, text="찾아보기", 
                  command=self.browse_output_folder).grid(row=0, column=1)
        
        output_frame.columnconfigure(0, weight=1)
        
        # 옵션 설정
        options_frame = ttk.LabelFrame(main_frame, text="변환 옵션", padding="10")
        options_frame.grid(row=6, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=20)
        
        # PDF 품질 설정
        ttk.Label(options_frame, text="PDF 품질:").grid(row=0, column=0, sticky=tk.W)
        self.quality = tk.StringVar(value="전자책(보통)")
        quality_labels = [
            "화면(저화질)",
            "전자책(보통)",
            "프린터(고화질)",
            "인쇄소(최고)"
        ]
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality,
                                    values=quality_labels,
                                    state="readonly", width=20)
        quality_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # 해상도 설정
        ttk.Label(options_frame, text="해상도 (DPI):").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.resolution = tk.StringVar(value="300")
        resolution_spin = ttk.Spinbox(options_frame, from_=72, to=1200, increment=50,
                                    textvariable=self.resolution, width=15)
        resolution_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # 변환/종료 버튼
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=4, pady=20)
        
        self.convert_button = ttk.Button(button_frame, text="변환 시작", 
                                       command=self.start_conversion,
                                       style="Accent.TButton")
        self.convert_button.grid(row=0, column=0, padx=10)
        
        self.clear_button = ttk.Button(button_frame, text="초기화", 
                                     command=self.clear_fields)
        self.clear_button.grid(row=0, column=1, padx=10)

        exit_btn = ttk.Button(button_frame, text="종료", command=self.root.destroy)
        exit_btn.grid(row=0, column=2, padx=10)

        # 진행 표시줄
        progress_row = 8
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=progress_row, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=10)
        
        # 상태 메시지
        self.status_var = tk.StringVar(value="변환할 PS 파일을 선택하세요.")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=progress_row+1, column=0, columnspan=4, pady=5)
        
        # 로그 영역
        log_frame = ttk.LabelFrame(main_frame, text="변환 로그", padding="5")
        log_frame.grid(row=progress_row + 2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=10, width=70)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # 그리드 가중치 설정
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(progress_row + 2, weight=1) # Adjusted row for log_frame
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
                self.gs_available = False
                self.log_message("경고: Ghostscript가 설치되지 않았거나 PATH에 없습니다. PS 파일 변환은 제한됩니다.")
                self.log_message("Ghostscript 다운로드: https://www.ghostscript.com/download/gsdnld.html")
            else:
                self.gs_available = True
                self.log_message(f"Ghostscript 발견: {self.gs_command}")
                
        except Exception as e:
            self.log_message(f"Ghostscript 확인 중 오류: {str(e)}")
    
    def browse_input_file(self):
        """입력 파일 선택"""
        filename = filedialog.askopenfilename(
            title="벡터/PS 파일 선택",
            filetypes=[("PS 파일(확장자 .ps 및 없는 파일)", ("*.ps", "ps")),
                       ("SVG 파일", "*.svg"),
                       ("EPS 파일", "*.eps"),
                       ("모든 파일", "*.*")],
            multiple=True,
            initialfile="ps"
        )
        if filename:
            # 여러 파일 선택 시 세미콜론으로 구분하여 저장
            if isinstance(filename, (list, tuple)):
                chosen_files = list(filename)
                self.input_path.set(";".join(chosen_files))
                first_file = chosen_files[0]
            else:
                self.input_path.set(filename)
                first_file = filename
            # 출력 폴더가 비어있으면 입력 파일과 같은 폴더로 설정
            if not self.output_path.get():
                self.output_path.set(os.path.dirname(first_file))
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
 
        input_paths = [p for p in self.input_path.get().split(";") if p]
        missing = [p for p in input_paths if not os.path.exists(p)]
        if missing:
            messagebox.showerror("오류", f"다음 입력 파일이 존재하지 않습니다:\n{chr(10).join(missing)}")
            return

        if not os.path.exists(self.output_path.get()):
            messagebox.showerror("오류", "출력 폴더가 존재하지 않습니다.")
            return
        
        # UI 상태 변경
        self.log_message("=== 변환 작업 시작 ===")
        self.convert_button.configure(state='disabled')
        self.progress.start()
        self.status_var.set("변환 중...")
        
        # 별도 스레드에서 변환 실행
        threading.Thread(target=self.convert_file, daemon=True).start()
    
    def convert_file(self):
        """실제 파일 변환 수행 (여러 파일 및 다양한 포맷 지원)"""
        self.log_message("변환 스레드 실행 중 ...")
        try:
            input_paths = [p for p in self.input_path.get().split(";") if p]
            output_dir = self.output_path.get()

            if not input_paths:
                raise ValueError("입력 파일 목록이 비어 있습니다.")

            pdf_files = []  # 생성된 PDF 목록

            # PDF 품질 매핑 (Ghostscript 전용)
            quality_settings = {
                "화면(저화질)": ["-dPDFSETTINGS=/screen"],
                "전자책(보통)": ["-dPDFSETTINGS=/ebook"],
                "프린터(고화질)": ["-dPDFSETTINGS=/printer"],
                "인쇄소(최고)": ["-dPDFSETTINGS=/prepress"]
            }

            for in_file in input_paths:
                ext = Path(in_file).suffix.lower()
                base_name = Path(in_file).stem
                out_pdf = os.path.join(output_dir, f"{base_name}.pdf")

                self.log_message(f"▶ {os.path.basename(in_file)} 변환 시작 → {os.path.basename(out_pdf)}")

                # 확장자가 없으면 파일 내용 앞부분을 검사해 PS 여부를 추정하거나 기본적으로 PS로 간주
                if ext == "":
                    # 간단히 파일 서두 확인 ("%!PS" 여부). 실패해도 PS로 처리.
                    try:
                        with open(in_file, "rb") as fh:
                            header = fh.read(4)
                        if header.startswith(b"%!PS"):
                            ext = ".ps"  # PS로 간주
                    except Exception:
                        ext = ".ps"

                if ext == ".ps":
                    if not self.gs_available:
                        self.log_message("  ✗ Ghostscript가 없어 PS 변환 불가: 스킵")
                        continue
                    # Ghostscript 사용
                    cmd = [
                        self.gs_command,
                        "-dNOPAUSE",
                        "-dBATCH",
                        "-dSAFER",
                        "-sDEVICE=pdfwrite",
                        f"-r{self.resolution.get()}",
                        *quality_settings.get(self.quality.get(), ["-dPDFSETTINGS=/ebook"]),
                        f"-sOutputFile={out_pdf}",
                        in_file
                    ]
                    self.log_message(f"  실행: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    if result.returncode != 0:
                        raise RuntimeError(result.stderr or result.stdout or "Ghostscript 오류")
                elif ext == ".svg":
                    # CairoSVG 사용
                    cairosvg.svg2pdf(url=in_file, write_to=out_pdf)
                elif ext == ".eps":
                    # Pillow 사용 (Ghostscript 필요할 수 있음)
                    img = Image.open(in_file)
                    img.save(out_pdf, "PDF", resolution=int(self.resolution.get()))
                else:
                    self.log_message(f"  ✗ 지원되지 않는 확장자: {ext}")
                    continue

                self.log_message("  ✓ 변환 성공")
                pdf_files.append(out_pdf)

            # 여러 PDF를 하나로 병합
            if len(pdf_files) > 1:
                merged_path = os.path.join(output_dir, "merged_output.pdf")
                self.log_message("PDF 병합 시작 ...")
                merger = PdfMerger()
                for pdf in pdf_files:
                    merger.append(pdf)
                merger.write(merged_path)
                merger.close()
                self.log_message(f"✓ 병합 완료 → {merged_path}")

                self.root.after(0, lambda: messagebox.showinfo(
                    "완료", f"모든 파일 변환 및 병합이 완료되었습니다!\n\n출력 파일: {merged_path}"))
            elif len(pdf_files) == 1:
                self.root.after(0, lambda: messagebox.showinfo(
                    "완료", f"변환이 완료되었습니다!\n\n출력 파일: {pdf_files[0]}"))

            self.root.after(0, lambda: self.status_var.set("변환 완료"))
        except subprocess.TimeoutExpired:
            self.log_message("✗ 변환 시간 초과 (120초)")
            self.root.after(0, lambda: messagebox.showerror(
                "시간 초과", "변환 시간이 120초를 초과했습니다."))
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

    def apply_theme(self):
        """테마 변경 적용 (간단한 색상 변경)"""
        theme = self.theme_var.get()

        if theme == "dark":
            bg = "#2b2b2b"
            fg = "#e6e6e6"
            entry_bg = "#3c3f41"
            btn_bg = "#444444"
            btn_active = "#5c5c5c"
            disabled_bg = "#666666"
        else:
            bg = "#f2f2f2"
            fg = "#000000"
            entry_bg = "#ffffff"
            btn_bg = "#d9d9d9"
            btn_active = "#c0c0c0"
            disabled_bg = "#e0e0e0"

        # 창 배경
        self.root.configure(bg=bg)

        # 모든 프레임과 라벨 등 색상 적용
        for widget in self.root.winfo_children():
            try:
                widget.configure(background=bg, foreground=fg)
            except tk.TclError:
                pass

        # ttk style 기반 색상 (라벨, 버튼 등)
        self.style.configure("TFrame", background=bg)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("TLabelframe", background=bg, foreground=fg)
        self.style.configure("TLabelframe.Label", background=bg, foreground=fg)
        self.style.configure("TButton", background=btn_bg, foreground=fg)
        self.style.configure("Accent.TButton", background=btn_bg, foreground=fg)
        self.style.map("TButton", background=[("active", btn_active), ("disabled", disabled_bg)])
        self.style.map("Accent.TButton", background=[("active", btn_active), ("disabled", disabled_bg)])

        # Entry 스타일
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)

        # Text 위젯 색상
        self.log_text.configure(background=entry_bg, foreground=fg)
        self.input_entry.configure(background=entry_bg, foreground=fg)
        self.output_entry.configure(background=entry_bg, foreground=fg)
        self.log_text.configure(background=entry_bg, foreground=fg, insertbackground=fg)

        # Combobox & Spinbox 스타일
        self.style.configure("TCombobox", fieldbackground=entry_bg, foreground=fg, background=entry_bg)
        self.style.map("TCombobox", fieldbackground=[("readonly", entry_bg)])
        self.style.configure("TSpinbox", fieldbackground=entry_bg, foreground=fg, arrowsize=12)

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
