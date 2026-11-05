# 🎙️ ZaloRec - AI-Powered Call Recorder for Zalo PC

<p align="center">
  <img src="assets/companion.ico" width="80" height="80" alt="ZaloRec Logo">
</p>

<p align="center">
  <b>Smart, automated call audio recorder and AI meeting transcriber for Zalo on Windows.</b><br>
  Dual-channel crystal-clear recording (Mic & Speaker) with integrated Gemini AI call transcription & summaries.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-blue?style=flat-square&logo=windows" alt="Platform">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/AI-Gemini%203.1%20Flash--Lite-orange?style=flat-square&logo=google" alt="AI Engine">
  <img src="https://img.shields.io/badge/Audio-Dual--Channel%20WASAPI-emerald?style=flat-square" alt="Audio">
  <img src="https://img.shields.io/badge/Privacy-100%25%20Local-purple?style=flat-square" alt="Privacy">
</p>

---

## 🇻🇳 Giới thiệu tiếng Việt

**ZaloRec** (trước đây là Ghi Âm Zalo PC) là giải pháp ghi âm cuộc gọi và trợ lý ghi nhớ thông minh hàng đầu dành cho người dùng **Zalo PC trên Windows 10/11**:
- 🎧 **Thu âm 2 kênh riêng biệt:** Giọng của bạn (Microphone) và giọng đối phương (Loa/Tai nghe) được ghi độc lập, lọc ồn và cân bằng âm lượng tự động.
- 🤖 **Bóc băng & Tóm tắt AI (Gemini 3.1 Flash-Lite):** Chuyển đổi toàn bộ cuộc gọi thành văn bản tiếng Việt cực chuẩn, tự động trích xuất việc cần làm (Action Items) và biên bản cuộc họp.
- ⚡ **Tự động nhận diện cuộc gọi:** Tự động phát hiện khi có cuộc gọi đến/đi từ Zalo PC mà không can thiệp vào mạng hay dữ liệu cá nhân.
- 🗂️ **Xuất biên bản 1-click:** Xuất file `.doc` / `.txt` gửi khách hàng hoặc lưu trữ nội bộ chỉ với 1 click.
- 🪄 **Widget nổi & Phím tắt:** Widget thu nhỏ đính kèm màn hình và phím tắt toàn cầu `Ctrl+Shift+R`.

---

## ✨ Key Features

### 🎙️ Dual-Channel Studio Recording
- **Independent Channels:** Microphone (caller) recorded on Channel 1, Speaker (callee) on Channel 2.
- **Hardware Loopback via WASAPI:** Captures exact speaker audio without room echo or acoustic feedback.
- **Dynamic Noise Reduction & Leveling:** Balances soft and loud speakers automatically for maximum intelligibility.

### 🤖 Gemini AI Speech-to-Text & Summaries
- **Infinite Length Audio Support:** Intelligent audio chunking handles 1-minute calls to multi-hour conferences seamlessly.
- **Automated Minutes of Meeting:** Extracts key takeaways, decisions, and deadlines directly from spoken dialogue.
- **Full-Text Keyword Search:** Search through months of conversations by typing any phrase mentioned during calls.

### 🛡️ Non-Intrusive & Privacy-First
- **Zero Network Tampering:** Does not modify Zalo binaries, proxy connections, or inspect private chats.
- **100% Local Storage:** All audio WAV/MP3 files stay strictly on your local disk (`C:\...`).
- **Encrypted API Keys:** Gemini API keys are kept secure and local.

### ⌨️ Global Controls & Workflow
- **Global Hotkey:** `Ctrl + Shift + R` to toggle recording anywhere.
- **Stealth Tray Companion:** Runs silently in the system tray, popping up only when a call starts.
- **Built-in Waveform Editor:** Trim, preview, and speed up playback (0.75x to 2.0x).

---

## 🚀 Quick Start

### Requirements
- Windows 10 or Windows 11 (64-bit)
- Python 3.10+ (Tested on Python 3.14)
- Zalo PC (Official desktop app)

### Running from Source
```bash
# 1. Clone repository
git clone https://github.com/tiudaiza95/ghi-am-cuoc-goi-zalo-pc.git
cd ghi-am-cuoc-goi-zalo-pc/Source

# 2. Install dependencies
py -3 -m pip install -r requirements.txt

# 3. Launch ZaloRec
py -3 main.py
```

Or run `CHAY_BANG_PYTHON.bat` or the **ZaloRec** shortcut on your Desktop!

---

## 🧪 Testing

Run the full automated test suite (105+ unit tests):
```bash
py -3 -m unittest discover -s tests
```

---

## 📄 Disclaimer

ZaloRec is an independent tool designed to enhance user productivity and record personal/business calls on Windows. It is not affiliated with or endorsed by VNG Corporation or Zalo. Please inform all call participants and comply with applicable local consent and privacy laws before recording.

## 📄 License
MIT License.
