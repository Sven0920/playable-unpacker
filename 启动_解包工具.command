#!/bin/bash
cd "$(dirname "$0")"
echo "正在启动解包工具..."
/Library/Developer/CommandLineTools/usr/bin/python3 -m streamlit run unpack_web.py