# Playable 解包工具

把从 InsightTracker 下载的 Playable 文件还原成完整 HTML。

## 用法
双击 `启动_解包工具.command`（首次需 `chmod +x`），浏览器会打开 streamlit 界面，上传文件即可解包。

## 依赖
```
pip3 install streamlit requests
```

## 文件
- `启动_解包工具.command` — streamlit 启动器
- `unpack_web.py` — 解包逻辑（自包含）
