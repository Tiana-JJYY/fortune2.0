import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="今日运势", page_icon="🔮", layout="centered")

# ========== 纯 CSS 飘落 emoji（无JS，兼容手机） ==========
st.markdown("""
<style>
/* 紫色主题背景 */
.stApp {
    background: linear-gradient(135deg, #1e1a2f 0%, #2a1e3c 50%, #3a2a4f 100%);
    color: #f0e6ff;
}
/* 卡片样式 */
.css-1kyxreq, .stSelectbox, .stTextInput, .stButton button {
    background: rgba(46, 32, 68, 0.7) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px !important;
    border: 1px solid #b77dff !important;
    color: #f0e6ff !important;
}
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
h1, h2, h3 {
    text-shadow: 0 0 10px #9b4dff;
}
/* 飘落容器 */
.falling-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 9999;
    overflow: hidden;
}
.emoji {
    position: absolute;
    top: -50px;
    font-size: 28px;
    animation: fall linear infinite;
    pointer-events: none;
}
/* 不同延迟和速度 */
@keyframes fall {
    0% { transform: translateY(0) rotate(0deg); opacity: 1; }
    100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
}
/* 每个 emoji 单独控制位置和时长（随机生成在下面） */
</style>
<div class="falling-container" id="falling-container"></div>
<script>
// 用 JS 动态生成 30 个 emoji 并设置随机位置、时长、延迟（这是 JS，但手机通常支持）
(function() {
    const container = document.getElementById('falling-container');
    const emojis = ['🌙', '✨', '🔮', '⭐', '🌠', '🃏', '💜', '🌟', '🌌', '🪄', '💫'];
    for (let i = 0; i < 35; i++) {
        const emoji = document.createElement('div');
        emoji.className = 'emoji';
        emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
        const left = Math.random() * 100;
        const duration = Math.random() * 6 + 4; // 4-10秒
        const delay = Math.random() * 10;
        emoji.style.left = left + '%';
        emoji.style.animationDuration = duration + 's';
        emoji.style.animationDelay = delay + 's';
        emoji.style.fontSize = (Math.random() * 20 + 20) + 'px';
        container.appendChild(emoji);
    }
})();
</script>
""", unsafe_allow_html=True)

st.title("🔮今日运势")
st.markdown("*请让我为你揭晓今日的命运吧*")

zodiacs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
           "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
zodiac = st.selectbox("✨ 选择你的星座", zodiacs)
name = st.text_input("🌟 你的名字", placeholder="比如：小姜")

try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    key_ready = True
except:
    api_key = st.text_input("🔑 DeepSeek API Key（本地测试用）", type="password", placeholder="输入你的API Key")
    key_ready = api_key is not None and api_key.strip() != ""

def get_fortune(zodiac, name, api_key):
    user_name = name if name else "旅人"
    prompt = f"""你是塔罗牌占卜师兼星座博主，风格幽默可爱。请为{user_name}（{zodiac}）生成今日运势。

要求：
1. 分四个维度：💼事业运势、💖爱情运势、💪健康运势、💰财运
2. 每个维度一句话，积极正面或略带调侃
3. 最后给“今日幸运色”和“今日小贴士”
4. 语气像好朋友聊天，不要太严肃，可以稍稍毒舌一点，但绝对不能说别人倒霉也不可以人身攻击哦
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

if st.button("🔮 看看今日运势", type="primary"):
    if not key_ready:
        st.error("✨ 请先输入 DeepSeek API Key（本地测试）或检查云端配置 ✨")
    else:
        with st.spinner("🔮 占卜师正在连接星辰... 请稍等我~🌙✨"):
            # 趣味加载动画
            msgs = ["🌠 塔罗牌正在洗牌...", "⭐ 观测你的星盘...", "🔮 水晶球开始发亮...", "🃏 抽出一张命运之轮...", "💫 运势正在凝聚..."]
            msg_placeholder = st.empty()
            for msg in msgs:
                msg_placeholder.markdown(f"*{msg}*")
                time.sleep(0.6)
            msg_placeholder.empty()
            fortune = get_fortune(zodiac, name, api_key)
        st.success("🌟 你的今日运势已送达 🌟")
        st.markdown(fortune)
        lucky = ["🌟 今天会有好事发生！", "😈 你遇到了厄运小恶魔！请默念蔡林娜是猪打败他！"]
        st.caption(random.choice(lucky))

st.markdown("---")
st.caption("💜 仅供娱乐，生活由你把握 | 愿你充满魔法般的惊喜 💜")
