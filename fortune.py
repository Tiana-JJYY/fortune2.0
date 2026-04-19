import streamlit as st
import requests
import random
import time

# ========== 页面配置 ==========
st.set_page_config(page_title="AI今日运势", page_icon="🔮", layout="centered")

# ========== 自定义 CSS 和 HTML 动画 ==========
st.markdown("""
<style>
/* 紫色主题背景 */
.stApp {
    background: linear-gradient(135deg, #1e1a2f 0%, #2a1e3c 50%, #3a2a4f 100%);
    color: #f0e6ff;
}

/* 主卡片样式 */
.css-1kyxreq, .stSelectbox, .stTextInput, .stButton button {
    background: rgba(46, 32, 68, 0.7) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px !important;
    border: 1px solid #b77dff !important;
    color: #f0e6ff !important;
}

/* 按钮特殊效果 */
.stButton button {
    background: linear-gradient(90deg, #9b4dff, #c77dff) !important;
    color: white !important;
    font-weight: bold;
    box-shadow: 0 0 15px rgba(155, 77, 255, 0.5);
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(155, 77, 255, 0.8);
}

/* 标题发光 */
h1, h2, h3 {
    text-shadow: 0 0 10px #9b4dff;
    font-family: 'Segoe UI', 'Emoji', sans-serif;
}

/* 飘落动画容器 */
#magic-falling {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;  /* 让飘落元素不干扰点击 */
    z-index: 999;
    overflow: hidden;
}
.falling-emoji {
    position: absolute;
    top: -50px;
    font-size: 28px;
    animation: fall linear forwards;
    pointer-events: none;
}
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}
</style>

<div id="magic-falling"></div>

<script>
// 动态生成飘落 emoji
const emojis = ['🌙', '✨', '🔮', '⭐', '🌠', '🃏', '💜', '🌟', '🌌', '🔮', '🪄', '💫'];
function createFallingEmoji() {
    const div = document.createElement('div');
    div.classList.add('falling-emoji');
    div.innerText = emojis[Math.floor(Math.random() * emojis.length)];
    const size = Math.random() * 20 + 20; // 20px - 40px
    div.style.fontSize = size + 'px';
    div.style.left = Math.random() * 100 + '%';
    div.style.animationDuration = Math.random() * 4 + 4 + 's'; // 4-8秒
    div.style.animationDelay = Math.random() * 5 + 's';
    document.getElementById('magic-falling').appendChild(div);
    setTimeout(() => div.remove(), 10000);
}
// 每0.5秒生成一个飘落元素
setInterval(createFallingEmoji, 500);
</script>
""", unsafe_allow_html=True)

# ========== 界面主体 ==========
st.title("🔮今日运势")
st.markdown("*让我来为你揭晓今日的秘密*")

zodiacs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
           "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
zodiac = st.selectbox("✨ 选择你的星座", zodiacs)
name = st.text_input("🌟 你的名字", placeholder="比如：小姜")

# 尝试从 secrets 读取 API Key（云端部署用），否则用输入框（本地测试）
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    key_ready = True
except:
    api_key = st.text_input("🔑 DeepSeek API Key（本地测试用）", type="password", placeholder="输入你的API Key")
    key_ready = api_key is not None and api_key.strip() != ""

def get_fortune(zodiac, name, api_key):
    user_name = name if name else "旅人"
    prompt = f"""你是塔罗牌占卜师兼星座博主，风格幽默温暖。请为{user_name}（{zodiac}）生成今日运势。

要求：
1. 分四个维度：💼事业运势、💖爱情运势、💪健康运势、💰财运
2. 每个维度一句话，积极正面或略带调侃
3. 最后给“今日幸运色”和“今日小贴士”
4. 语气像好朋友聊天，不要太严肃
5. 总字数150字以内

输出格式：
【事业】xxx
【爱情】xxx
【健康】xxx
【财运】xxx
幸运色：xxx
小贴士：xxx
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

# ========== 自定义加载动画（点击按钮后显示） ==========
if st.button("🔮 看看今日运势", type="primary"):
    if not key_ready:
        st.error("✨ 请先输入 DeepSeek API Key（本地测试）或检查云端配置 ✨")
    else:
        # 自定义加载占位符
        with st.spinner("🔮 占卜师正在连接星辰... 请稍候 🌙✨"):
            # 额外增加趣味文字变化（每隔0.5秒变一下）
            import itertools
            messages = ["🌠 塔罗牌正在洗牌...", "⭐ 观测你的星盘...", "🔮 水晶球开始发亮...", "🃏 抽出一张命运之轮...", "💫 运势正在凝聚..."]
            msg_cycle = itertools.cycle(messages)
            placeholder = st.empty()
            for i in range(3):  # 快速显示三条不同消息，模拟加载过程
                placeholder.markdown(f"*{next(msg_cycle)}*")
                time.sleep(0.8)
            placeholder.empty()
            
            fortune = get_fortune(zodiac, name, api_key)
        
        st.success("🌟 你的今日运势已送达 🌟")
        st.markdown(fortune)
        
        # 额外的小彩蛋
        lucky_phrases = ["🌟 今天会有好事发生！", "🍀 保持微笑，运气不会差", "✨ 你比你想象的更棒", "🌙 记得许个愿哦", "🔮 你的直觉很准，相信它", "😈恭喜你随机得到了厄运彩蛋 请在心里默念蔡林娜是猪三遍解除厄运彩蛋"]
        st.caption(random.choice(lucky_phrases))

st.markdown("---")
st.caption("💜 仅供娱乐，生活由你把握 | 愿你充满魔法般的惊喜 💜")
