import streamlit as st
import re
import json
import requests
import time

# 设置页面标题
st.set_page_config(page_title="Playable 解包神器", page_icon="📦")

st.title("📦 Playable 广告解包工具")
st.markdown("### 第一步：从加载器提取完整游戏")
st.info("💡 请上传那个只有几 KB 的 AppLovin 加载器 HTML 文件 (例如 Block Out!.html)")

# --- 核心解包逻辑 (复用之前的V4稳定版) ---
def extract_game_content(html_content):
    # 1. 找链接
    url_match = re.search(r'src="(https://res1\.applovin\.com/.*?_js_load\.js)"', html_content)
    if not url_match:
        return None, "❌ 未能在文件中找到 AppLovin JS 下载链接。"

    js_url = url_match.group(1)
    st.write(f"🔗 **发现目标链接:** `{js_url}`")
    
    # 2. 下载
    try:
        with st.spinner(f"⏳ 正在下载游戏数据 (从 AppLovin 服务器)..."):
            response = requests.get(js_url, timeout=30)
            response.encoding = 'utf-8'
            js_content = response.text
    except Exception as e:
        return None, f"❌ 下载失败: {str(e)}"

    # 3. 智能解析 (V4逻辑)
    html_extracted = None
    
    # 策略A: 寻找最外层 {}
    start = js_content.find('{')
    end = js_content.rfind('}')
    
    if start != -1 and end != -1:
        try:
            json_str = js_content[start : end+1]
            data = json.loads(json_str)
            if 'html' in data:
                html_extracted = data['html']
        except:
            pass
            
    # 策略B: 暴力截取 (如果策略A失败)
    if not html_extracted:
        prefix = '"html":"'
        p_idx = js_content.find(prefix)
        if p_idx != -1:
            content_start = p_idx + len(prefix)
            content_end = js_content.rfind('"')
            if content_end > content_start:
                raw = js_content[content_start:content_end]
                # 处理转义
                try:
                    html_extracted = json.loads(f'"{raw}"')
                except:
                    html_extracted = raw.encode('utf-8').decode('unicode_escape')

    if html_extracted:
        return html_extracted, "Success"
    else:
        return None, "❌ 解析失败：无法从 JS 中提取 HTML 内容。"

# --- 网页界面 ---

uploaded_file = st.file_uploader("📂 把文件拖拽到这里", type=["html"])

if uploaded_file:
    # 读取文件
    file_content = uploaded_file.getvalue().decode("utf-8", errors='ignore')
    
    # 执行解包
    if st.button("🚀 开始解包"):
        extracted_html, msg = extract_game_content(file_content)
        
        if extracted_html:
            st.success("🎉 解包成功！文件已生成。")
            st.balloons()
            
            # 计算大小
            size_mb = len(extracted_html.encode('utf-8')) / (1024 * 1024)
            st.write(f"📦 **完整包大小:** {size_mb:.2f} MB")
            
            # 提供下载按钮
            new_filename = f"Extracted_{uploaded_file.name}"
            st.download_button(
                label="📥 点击下载完整 HTML",
                data=extracted_html,
                file_name=new_filename,
                mime="text/html"
            )
        else:
            st.error(msg)