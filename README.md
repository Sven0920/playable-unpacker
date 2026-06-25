# Playable 解包工具

把从 InsightTracker 下载的 AppLovin 加载器（几 KB 的 HTML）还原成完整的 Playable 文件。

## 在线版（推荐）
👉 https://sven0920.github.io/playable-unpacker/

纯前端，打开网页上传加载器 HTML 即可解包，文件不上传服务器。

## 本地 streamlit 版
双击 `启动_解包工具.command`，浏览器会打开界面。依赖：
```
pip3 install streamlit requests
```

## 文件
- `index.html` — 浏览器版（GitHub Pages 托管）
- `启动_解包工具.command` — 本地 streamlit 启动器
- `unpack_web.py` — 本地版解包逻辑
