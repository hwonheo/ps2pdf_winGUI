# PS2PDF 변환기

PostScript (PS) 파일을 PDF로 변환하는 Windows용 GUI 프로그램입니다.

## 📋 기능

- **쉬운 GUI 인터페이스**: 간단한 파일 선택과 클릭으로 변환
- **벡터 포맷 지원**: PS 이외에도 **SVG / EPS** 파일을 PDF로 변환
- **다양한 옵션**: PDF 품질(저화질~인쇄소급) 및 해상도 설정 가능
- **라이트·다크 테마**: 실시간 전환 가능한 UI 테마
- **편의 기능**: Ghostscript 설치 링크, 다중 파일 선택 & 자동 병합, 종료 버튼 등
- **실시간 로그**: 변환 과정을 실시간으로 확인
- **Windows 최적화**: Windows 환경에 맞춘 사용자 친화적 인터페이스

## 🔧 시스템 요구사항

- **운영체제**: Windows 7/8/10/11 (32bit/64bit)
- **Ghostscript**: 필수 설치 (자동 설치 도우미 제공)
- **메모리**: 최소 2GB RAM
- **저장공간**: 50MB 이상

## 📦 설치 방법

### 방법 1: MSI 설치 파일 사용 (권장) 🔥

[![Build Status](https://github.com/hwonheo/ps2pdf_winGUI/actions/workflows/build-windows-msi.yml/badge.svg)](https://github.com/hwonheo/ps2pdf_winGUI/actions)

1. [GitHub Releases](https://github.com/hwonheo/ps2pdf_winGUI/releases)에서 최신 MSI 파일 다운로드
2. MSI 파일 실행하여 자동 설치
3. 시작 메뉴에서 "PS2PDF 변환기" 실행

### 방법 2: 포터블 버전 사용

1. [GitHub Releases](https://github.com/hwonheo/ps2pdf_winGUI/releases)에서 Portable ZIP 다운로드
2. 압축 해제 후 `PS2PDF_Converter.exe` 실행
3. Ghostscript 별도 설치 필요 (아래 참조)

### 방법 3: 소스코드에서 실행

```bash
# 저장소 클론
git clone https://github.com/hwonheo/ps2pdf_winGUI.git
cd ps2pdf_winGUI

# 필요한 패키지 설치
pip install -r requirements.txt

# 프로그램 실행
python ps2pdf_converter.py
```

## 🖥️ Ghostscript 설치

PS 파일 변환을 위해 Ghostscript가 필요합니다.

### 자동 설치 도우미 사용

```bash
python install_ghostscript.py
```

### 수동 설치

1. [Ghostscript 공식 사이트](https://www.ghostscript.com/download/gsdnld.html) 방문
2. Windows용 최신 버전 다운로드:
   - 64bit: `gs10021w64.exe`
   - 32bit: `gs10021w32.exe`
3. 설치 시 **"Add Ghostscript to PATH"** 옵션 체크
4. 컴퓨터 재시작

## 🚀 사용 방법

### 1. 프로그램 실행
`PS2PDF_Converter.exe`를 더블클릭하여 실행

### 2. 파일 선택
- **PS 파일 선택**: 변환할 PostScript 파일 선택
- **출력 폴더**: PDF가 저장될 폴더 선택 (기본값: 입력 파일과 같은 폴더)

### 3. 변환 옵션 설정
- **PDF 품질**:
  - `screen`: 화면 보기용 (72 DPI)
  - `ebook`: 전자책용 (150 DPI) - 기본값
  - `printer`: 프린터용 (300 DPI)
  - `prepress`: 인쇄소용 (300 DPI, 최고 품질)
- **해상도**: 72-1200 DPI 설정 가능

### 4. 변환 실행
"변환 시작" 버튼 클릭하여 변환 시작

### 5. 결과 확인
- 진행 상황이 하단 로그 영역에 표시됩니다
- 변환 완료 시 알림 창이 표시됩니다

## 📁 파일 구조

```
ps2pdf/
├── .github/workflows/       # GitHub Actions 워크플로우
│   └── build-windows-msi.yml
├── ps2pdf_converter.py      # 메인 GUI 프로그램
├── setup_msi.py            # MSI 패키지 빌드 설정
├── build_windows.py         # PyInstaller 빌드 스크립트
├── install_ghostscript.py   # Ghostscript 설치 도우미
├── git_setup.sh/.bat       # Git 저장소 초기화 스크립트
├── run.bat                 # Windows 실행 스크립트
├── build.bat               # Windows 빌드 스크립트
├── requirements.txt         # Python 패키지 목록
├── ps                      # 샘플 PostScript 파일
├── LICENSE                 # MIT 라이선스
├── .gitignore              # Git 무시 파일 목록
└── README.md               # 이 파일
```

## 🔨 개발자 정보

### 자동 빌드 (GitHub Actions)

이 프로젝트는 GitHub Actions를 사용하여 자동으로 Windows 바이너리를 빌드합니다:

- **MSI 설치 파일**: cx_Freeze를 사용한 정식 설치 패키지
- **포터블 버전**: PyInstaller를 사용한 단일 실행 파일
- **자동 릴리스**: 태그 생성 시 자동으로 GitHub Releases에 업로드

### 로컬 빌드

#### MSI 패키지 빌드
```bash
# MSI 패키지 생성
pip install cx-freeze
python setup_msi.py bdist_msi
```

#### 포터블 실행 파일 빌드
```bash
# PyInstaller로 exe 파일 생성
python build_windows.py
```

### 사용된 기술

- **Python 3.7+**: 메인 프로그래밍 언어
- **tkinter**: GUI 프레임워크
- **Ghostscript**: PS/PDF 변환 엔진
- **cx_Freeze**: MSI 패키지 생성
- **PyInstaller**: 포터블 실행 파일 생성
- **GitHub Actions**: CI/CD 자동화

## 🐛 문제 해결

### 1. "Ghostscript를 찾을 수 없습니다" 오류

**해결방법**:
- Ghostscript가 설치되어 있는지 확인
- 환경변수 PATH에 Ghostscript가 추가되어 있는지 확인
- `install_ghostscript.py` 실행하여 설치 상태 확인

### 2. 변환이 실패하는 경우

**확인사항**:
- 입력 파일이 올바른 PostScript 파일인지 확인
- 출력 폴더에 쓰기 권한이 있는지 확인
- 디스크 공간이 충분한지 확인

### 3. 프로그램이 실행되지 않는 경우

**해결방법**:
- Visual C++ Redistributable 설치
- Windows Defender 예외 목록에 추가
- 관리자 권한으로 실행

## 📄 지원 파일 형식

### 입력 파일
- `.ps` (PostScript)
- `.eps` (Encapsulated PostScript)

### 출력 파일
- `.pdf` (Portable Document Format)

## 🚀 릴리스 생성 방법

새 버전을 릴리스하려면:

```bash
# 태그 생성 및 푸시
git tag v1.0.1
git push origin v1.0.1
```

GitHub Actions가 자동으로:
1. MSI 패키지 빌드
2. 포터블 ZIP 파일 생성
3. GitHub Releases에 자동 업로드

## 🔄 버전 히스토리

- **v1.0.0**: 초기 릴리스
  - PS to PDF 기본 변환 기능
  - GUI 인터페이스
  - Windows MSI/포터블 빌드 자동화
  - GitHub Actions CI/CD 설정

## 📞 지원 및 문의

문제가 발생하거나 개선 사항이 있으시면:

1. GitHub Issues에 버그 리포트 작성
2. 로그 정보와 함께 상세한 설명 제공
3. 시스템 환경 정보 포함

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

---

**PS2PDF 변환기** - PostScript를 PDF로 쉽고 빠르게! 🚀
