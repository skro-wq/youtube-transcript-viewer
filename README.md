# YouTube Transcript Viewer

유튜브 영상의 한국어/영어 자막을 자동으로 가져오는 간단한 웹 앱입니다.

A simple web app to automatically fetch Korean/English transcripts from YouTube videos.

![YouTube Transcript Viewer](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

## ✨ Features | 기능

- 🌐 **Auto Language Detection** - 한국어/영어 자막 자동 감지
- 📋 **Easy Copy** - 클릭 한 번으로 전체 텍스트 복사
- 📊 **CSV Export** - 타임스탬프와 텍스트를 열로 구분한 CSV 파일
- 📄 **TXT Export** - 타임스탬프가 포함된 텍스트 파일
- 🎨 **Clean UI** - 깔끔하고 사용하기 쉬운 인터페이스
- ⚡ **Fast** - 캐싱으로 빠른 성능

## 🚀 Quick Start | 빠른 시작

### Installation | 설치

```bash
# Clone the repository | 저장소 복제
git clone https://github.com/skro-wq/youtube-transcript-viewer.git
cd youtube-transcript-viewer

# Run the app | 앱 실행
./yt
```

That's it! The app will open in your default browser.

끝! 앱이 기본 브라우저에서 자동으로 열립니다.

## 📋 Requirements | 필요 사항

- **Python 3.8 or higher** | Python 3.8 이상
- **macOS, Linux, or Windows** with bash
- **Internet connection** | 인터넷 연결

## 💻 Usage | 사용법

### Method 1: Quick Launch | 방법 1: 빠른 실행

```bash
./yt
```

The app will:
1. Create a virtual environment (first time only)
2. Install dependencies (first time only)
3. Launch the app
4. Open in your browser automatically

앱이 자동으로:
1. 가상 환경 생성 (처음만)
2. 필요한 패키지 설치 (처음만)
3. 앱 실행
4. 브라우저에서 열기

### Method 2: Manual Setup | 방법 2: 수동 설정

```bash
# Create virtual environment | 가상 환경 생성
python3 -m venv venv

# Activate virtual environment | 가상 환경 활성화
source venv/bin/activate  # macOS/Linux
# or on Windows: venv\Scripts\activate

# Install dependencies | 의존성 설치
pip install -r requirements.txt

# Run the app | 앱 실행
streamlit run app.py
```

### Using the App | 앱 사용하기

1. **Paste YouTube URL** | 유튜브 URL 붙여넣기
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Click "Get Transcript"** | "Get Transcript" 버튼 클릭
   - The app will auto-detect Korean or English subtitles
   - 앱이 자동으로 한국어 또는 영어 자막을 감지합니다

3. **Export or Copy** | 내보내기 또는 복사
   - 📋 Copy text from the code box
   - 📄 Download as TXT file
   - 📊 Download as CSV file (Timestamp, Text columns)

## 🛠️ Advanced Setup | 고급 설정

### Add to PATH for Global Access | 전역 명령어로 설정

You can run `yt` from anywhere on your system:

시스템 어디서든 `yt` 명령어를 실행할 수 있습니다:

**For macOS/Linux:**

Add to your `~/.zshrc` or `~/.bash_profile`:

```bash
# Add alias for YouTube Transcript Viewer
alias yt='cd /path/to/youtube-transcript && ./yt'
```

Then reload:
```bash
source ~/.zshrc  # or source ~/.bash_profile
```

**Or add to PATH:**

```bash
export PATH="$PATH:/path/to/youtube-transcript"
```

Now you can type `yt` from anywhere!

이제 어디서든 `yt`를 입력하면 앱이 실행됩니다!

## 📁 Project Structure | 프로젝트 구조

```
youtube-transcript/
├── app.py              # Main Streamlit application | 메인 앱
├── requirements.txt    # Python dependencies | 파이썬 패키지
├── yt                  # Quick launch script | 빠른 실행 스크립트
├── run.sh             # Alternative launch script | 대체 실행 스크립트
├── README.md          # This file | 이 파일
└── .gitignore         # Git ignore rules
```

## 🎯 Supported Features | 지원 기능

### Transcript Languages | 자막 언어
- ✅ Korean (한국어)
- ✅ English (영어)
- 🔄 Auto-detection | 자동 감지

### URL Formats | URL 형식
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`
- URLs with parameters (playlists, timestamps, etc.)

### Export Formats | 내보내기 형식
- **TXT**: Plain text with timestamps `[00:15] Text here`
- **CSV**: Structured format with columns
  ```csv
  Timestamp,Text
  "00:15","Text here"
  "00:30","More text"
  ```

## ❓ Troubleshooting | 문제 해결

### "No transcript found" | "자막을 찾을 수 없습니다"
- The video might not have Korean or English subtitles
- 영상에 한국어나 영어 자막이 없을 수 있습니다
- Try a different video with known captions
- 자막이 있는 다른 영상을 시도해보세요

### "Transcripts are disabled" | "자막이 비활성화되어 있습니다"
- The video owner has disabled captions
- 영상 소유자가 자막을 비활성화했습니다
- This cannot be bypassed
- 우회할 수 없습니다

### Port already in use | 포트가 이미 사용 중
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Or use a different port
streamlit run app.py --server.port=8502
```

### Python not found | Python을 찾을 수 없음
```bash
# Install Python 3
# macOS:
brew install python3

# Ubuntu/Debian:
sudo apt-get install python3

# Windows:
# Download from python.org
```

## 🤝 Contributing | 기여하기

Contributions are welcome! Please feel free to submit a Pull Request.

기여를 환영합니다! Pull Request를 자유롭게 제출해주세요.

## 📝 License | 라이선스

This project is open source and available for personal and educational use.

이 프로젝트는 오픈 소스이며 개인 및 교육 목적으로 사용할 수 있습니다.

## 🙏 Acknowledgments | 감사

- [Streamlit](https://streamlit.io/) - Web framework
- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) - YouTube transcript fetching

## 📧 Support | 지원

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check existing issues for solutions

문제가 발생하거나 질문이 있으시면:
- GitHub에 이슈를 열어주세요
- 기존 이슈에서 해결책을 확인하세요

---

**Built with ❤️ using Streamlit and Python**

**Streamlit과 Python으로 제작**
