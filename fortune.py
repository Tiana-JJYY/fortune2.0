import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="今日运势", page_icon="🔮", layout="centered")

# ========== CSS样式（发光边框、高对比文字） ==========
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e1a2f 0%, #2a1e3c 50%, #3a2a4f 100%);
}
body, .stMarkdown, label, .stTextInput label, .stSelectbox label, .stRadio label {
    color: #f0e6ff !important;
}
.css-1kyxreq, .stSelectbox > div, .stTextInput > div, .stButton button, .stRadio > div {
    background: rgba(46, 32, 68, 0.8) !important;
    backdrop-filter: blur(8px);
    border-radius: 20px !important;
    border: 1px solid #b77dff !important;
    box-shadow: 0 0 8px #b77dff, inset 0 0 4px rgba(255,255,255,0.2) !important;
    color: #ffffff !important;
}
input, textarea, .stSelectbox span, .stRadio span {
    color: #ffffff !important;
}
.stButton button {
    background: linear-gradient(90deg, #9b4dff, #c77dff) !important;
    color: white !important;
    font-weight: bold;
    box-shadow: 0 0 15px #9b4dff, 0 0 5px #c77dff !important;
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px #9b4dff, 0 0 10px #c77dff !important;
}
h1, h2, h3 {
    text-shadow: 0 0 10px #9b4dff;
    border: none !important;
    box-shadow: none !important;
    color: #f0e6ff;
}
.stAlert {
    background: rgba(46, 32, 68, 0.9) !important;
    border: 1px solid #b77dff !important;
    border-radius: 20px !important;
    color: #f0e6ff !important;
}
</style>
""", unsafe_allow_html=True)

# ========== 会话状态：控制主界面 ==========
if "started" not in st.session_state:
    st.session_state.started = False

# ========== 主界面（未开始时显示） ==========
if not st.session_state.started:
    st.title("🔮 今日运势")
    st.markdown("*让星辰与塔罗为你揭晓今日的秘密*")
    st.markdown("""
    <div style="background: rgba(46,32,68,0.7); border-radius: 30px; padding: 20px; margin: 30px 0; text-align: center; border: 1px solid #b77dff; box-shadow: 0 0 15px #b77dff;">
        <h3>✨ 占卜师低语 ✨</h3>
        <p>“远方的旅人，欢迎你的到来。</p>
        <p>只需轻轻一点，命运的轮盘便会转动。” 🌙</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔮 开始今日占卜 🔮", type="primary", use_container_width=True):
        st.session_state.started = True
        st.rerun()
    st.stop()

# ========== 正式测试界面 ==========
st.title("🔮 今日运势")
st.markdown("*让星辰与塔罗为你揭晓今日的秘密*")

# 星座下拉框
zodiacs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
           "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
zodiac = st.selectbox("✨ 选择你的星座", zodiacs)

name = st.text_input("🌟 你的名字", placeholder="比如：小姜")
gender = st.radio("🧑 你的性别", ("不透露", "女", "男"), index=0, horizontal=True)

# API Key 获取
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    key_ready = True
except:
    api_key = st.text_input("🔑 DeepSeek API Key（本地测试用）", type="password", placeholder="输入你的API Key")
    key_ready = api_key is not None and api_key.strip() != ""

def get_fortune(zodiac, name, gender, api_key):
    user_name = name if name else "旅人"
    # 无论男女统一称呼“亲爱的朋友”
    honorific = "亲爱的朋友"
    
    prompt = f"""你是一位神秘且强大的命运塔罗牌占卜师，风格可爱幽默诙谐。请为{user_name}（{honorific}，{zodiac}）生成今日运势。

要求：
1. 分四个维度：💼事业运势、💖爱情运势、💪健康运势、💰财运
2. 每个维度几句话，积极正面或略带调侃，可以毒舌但绝不能人身攻击也不可以说别人倒霉
3. 最后给“今日幸运色”和“今日小贴士”
4. 语气像好朋友聊天，不要太严肃
5. 总字数300字左右
6. 第一句话请提示大家一天仅可以测一回否则不准

输出格式：
🌼提示：...
【💼事业】xxx
【💖爱情】xxx
【💪健康】xxx
【💰财运】xxx
🌈幸运色：xxx
📖小贴士：xxx
"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    try:
        resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=15)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
        else:
            return f"✨ 占卜师走神了，错误码：{resp.status_code}，请稍后再试~"
    except Exception as e:
        return f"🌙 网络波动，再试一次吧：{str(e)}"

if st.button("🔮 看看今日运势", type="primary"):
    if not key_ready:
        st.error("✨ 请先输入 DeepSeek API Key（本地测试）或检查云端配置 ✨")
    else:
        with st.spinner("🔮 占卜师正在连接星辰... 请稍候 🌙✨"):
            msgs = ["🌠 塔罗牌正在洗牌...", "⭐ 观测你的星盘...", "🔮 水晶球开始发亮...", "🃏 抽出一张命运之轮...", "💫 运势正在凝聚..."]
            msg_placeholder = st.empty()
            for msg in msgs:
                msg_placeholder.markdown(f"*{msg}*")
                time.sleep(0.5)
            fortune = get_fortune(zodiac, name, gender, api_key)
            msg_placeholder.empty()
        
        st.success("🌟 你的今日运势已送达 🌟")
        st.markdown(fortune)
        lucky = ["🌟 今天会有好事发生！", "🍀 保持微笑，运气不会差", "✨ 你比你想象的更棒", "🌙 记得许个愿哦", "🔮 你的直觉很准，相信它"]
        st.caption(random.choice(lucky))

st.markdown("---")
st.caption("💜 仅供娱乐，生活由你把握 | 愿你充满魔法般的惊喜 💜")
