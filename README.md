# GitGPT VSCode 插件問卷調查

## 簡介

感謝您參與 **GitGPT VSCode 插件問卷調查**！本問卷旨在收集使用者的反饋，以改進我們的插件功能和使用體驗。
專案連結：[GitGPT VSCode 插件專案](https://github.com/Wei-Hsu-AI/vscode-version-control-chat-ai/)

![](https://private-user-images.githubusercontent.com/42505266/399153637-d62e6f2d-91dd-4852-aab7-c2973b475ff1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzU0Njk2MDUsIm5iZiI6MTczNTQ2OTMwNSwicGF0aCI6Ii80MjUwNTI2Ni8zOTkxNTM2MzctZDYyZTZmMmQtOTFkZC00ODUyLWFhYjctYzI5NzNiNDc1ZmYxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEyMjklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMjI5VDEwNDgyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTc2ZGUzODlkOWNkMWIzZjc2OWQ0NmZjMGVmZTQ0NmRhY2Q0YWI4MzNlN2NjMTFmYzNiM2Y3M2M2MzZjMGExOGQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.1_JR9oApi3ElflEH5ZLkXRQc9Py5RU-W0tbr2VFQW_o)

## 問卷參與流程

1. **Clone 專案到本地端**
   ```bash
   git clone https://github.com/jimmyhealer/git-gpt-survey.git
   ```
2. **安裝 GitGPT 插件**
   - 請從以下載 vsix 檔案，並安裝至 VSCode 中：
     - [GitGPT 插件](https://github.com/jimmyhealer/git-gpt-survey/releases/latest)
   - 安裝方式：
     - 按下 `Ctrl+Shift+P`，輸入 `Extensions: Install from VSIX...`。
     - 選擇剛剛下載的 `git-gpt-0.0.1.vsix` 檔案。
     - 或者使用指令 `code --install-extension git-gpt-0.0.1.vsix`。
3. **閱讀以下的注意事項**
4. **執行問卷程式**
   ```bash
   python main.py
   ```
5. **回答問題**
   - 根據程式指引回答問題。
6. **提交結果**
   - 將生成的 `submit.json` 上傳至 [Google 表單](https://forms.gle/L1EvJmd91rKZ4MoSA)。

## 注意事項

- **匿名性保證**：我們不會收集任何個人資訊，請放心填寫。
- 問卷包含三個情境題：
  - 您需要用「自行完成」及「使用 **GitGPT 插件** 協助完成」。
  - **自行完成時**，可使用任何工具，如文件、網路搜尋、ChatGPT/Copilot 等，但請勿使用 GitGPT 插件。
  - **使用 GitGPT 插件時**，僅限使用插件功能，不可輔以其他工具。
- **記錄要求**：
  - 若使用 GitGPT 插件協助，請記錄您輸入的第一個 Prompt。

### 使用 **GitGPT 插件** 協助完成

建議您可以參考以下步驟，以獲得最佳測試體驗：

1. 開啟新的視窗
```bash
code ./scenario_[1-3]
```
2. 按下 `Ctrl+Shift+P`，輸入 `Open Webview`。

感謝您的參與與支持！