import streamlit as st
import requests
import random
import time

# ========== 页面配置 ==========
st.set_page_config(page_title="今日运势", page_icon="🔮", layout="centered")

# ========== 自定义CSS（星空、闪烁、神秘感） ==========
st.markdown("""
<style>
/* 全局背景：深邃星空 */
.stApp {
    background: radial-gradient(ellipse at center, #0a0f2a 0%, #030518 100%);
    color: #e0d4ff;
}
/* 标题发光 */
h1, h2, h3 {
    text-align: center;
    font-family: 'Segoe UI', 'Emoji', sans-serif;
    text-shadow: 0 0 15px #b77dff, 0 0 5px #9b4dff;
}
/* 闪烁星星动画 */
@keyframes twinkle {
    0% { opacity: 0.2; }
    50% { opacity: 1; }
    100% { opacity: 0.2; }
}
.star {
    position: fixed;
    background-color: white;
    border-radius: 50%;
    opacity: 0.6;
    animation: twinkle 3s infinite alternate;
    z-index: 0;
}
/* 主卡片样式 */
.mystic-card {
    background: rgba(20, 15, 45, 0.75);
    backdrop-filter: blur(12px);
    border-radius: 48px;
    border: 1px solid rgba(183, 125, 255, 0.5);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(155,77,255,0.3);
    padding: 2rem;
    margin: 1rem auto;
    max-width: 600px;
    text-align: center;
}
/* 按钮样式 */
.stButton > button {
    background: linear-gradient(135deg, #9b4dff, #c77dff);
    color: white;
    border: none;
    border-radius: 60px;
    padding: 0.6rem 1.8rem;
    font-size: 1.2rem;
    font-weight: bold;
    box-shadow: 0 0 15px #9b4dff;
    transition: 0.3s;
    width: 100%;
}
.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px #c77dff;
}
/* 表单输入框 */
.stSelectbox, .stTextInput, .stRadio > div {
    background: rgba(30, 20, 55, 0.8);
    border-radius: 30px;
    border: 1px solid #b77dff;
    color: #f0e6ff;
}
/* 运势结果卡片 */
.result-card {
    background: rgba(0,0,0,0.6);
    border-left: 6px solid #c77dff;
    border-radius: 28px;
    padding: 1.5rem;
    margin-top: 1.5rem;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ========== 生成随机星星背景 ==========
def add_stars():
    stars_html = ""
    for i in range(80):
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        size = random.randint(1, 3)
        duration = random.uniform(2, 5)
        stars_html += f'<div class="star" style="left:{left}%; top:{top}%; width:{size}px; height:{size}px; animation-duration:{duration}s;"></div>'
    st.markdown(f'<div style="position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none;">{stars_html}</div>', unsafe_allow_html=True)

add_stars()

# ========== 会话状态管理：是否显示表单 ==========
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# ========== 封面页 ==========
if not st.session_state.show_form:
    st.markdown('<div class="mystic-card">', unsafe_allow_html=True)
    st.markdown("# 🔮 今日运势测试")
    st.markdown("#### *星辰轮转，塔罗低语*")
    st.markdown("#### 你的命运，此刻揭晓")
    st.markdown("")
    if st.button("✨ 开始占卜 ✨", key="start"):
        st.session_state.show_form = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    # 底部装饰
    st.caption("✨ 点击水晶球，开启神秘之旅 ✨")
    st.stop()  # 停止执行，不显示表单

# ========== 表单页（用户输入） ==========
st.markdown('<div class="mystic-card">', unsafe_allow_html=True)
st.markdown("## 🔮 请输入你的信息")
st.markdown("*占卜师将为你量身定制运势*")

# 表单输入
zodiacs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
           "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
zodiac = st.selectbox("🌟 你的星座", zodiacs)
name = st.text_input("✨ 你的名字（或昵称）", placeholder="如：小姜")
gender = st.radio("💫 性别", ["女", "男", "不愿透露"], horizontal=True)
mbti_options = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
                "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP"]
mbti = st.selectbox("🌙 MBTI 人格类型", mbti_options)

# API Key 处理
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    key_ready = True
except:
    api_key = st.text_input("🔑 DeepSeek API Key（本地测试用）", type="password")
    key_ready = api_key is not None and api_key.strip() != ""

# 生成运势按钮
if st.button("🔮 查看今日运势", type="primary"):
    if not key_ready:
        st.error("✨ 请提供 DeepSeek API Key ✨")
    else:
        # 趣味加载
        with st.spinner("🔮 占卜师正在冥想..."):
            messages = ["🌠 星盘转动...", "🃏 塔罗牌阵展开...", "🔮 水晶球显像...", "✨ 命运之线交织..."]
            msg_placeholder = st.empty()
            for msg in messages:
                msg_placeholder.markdown(f"*{msg}*")
                time.sleep(0.6)
            msg_placeholder.empty()
            
            # 构造个性化 Prompt
            user_name = name if name else "旅人"
            gender_text = gender if gender != "不愿透露" else "神秘人"
            prompt = f"""你是一位神秘而可爱的占卜师，精通星座、MBTI和塔罗。请为以下用户生成一份专属的今日运势分析。

用户信息：
- 名字：{user_name}
- 性别：{gender_text}
- 星座：{zodiac}
- MBTI：{mbti}

要求：
1. 以第二人称“你”来称呼用户。
2. 结合性别、星座和MBTI特点给出个性化的建议，每个人都尽量不一样哦。
3. 分四个维度：💼事业学业、💖感情人际、💪身心健康、💰财运机遇。
4. 每个维度2-3句话，积极正面且具体。
5. 最后给出“✨今日幸运物”和“🌙今日小贴士”。
6. 整体语气温柔、神秘、鼓励，总字数250字以内。
7. 请第一句就提示大家，一天仅可测试一次，多测就不准了，语气俏皮。

输出格式：
🐱提示：...
【事业学业】...
【感情人际】...
【身心健康】...
【财运机遇】...
✨今日幸运物：...
🌙今日小贴士：...
"""
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.85}
            try:
                resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=20)
                if resp.status_code == 200:
                    fortune = resp.json()["choices"][0]["message"]["content"]
                else:
                    fortune = f"✨ 占卜师暂时无法连接，错误码：{resp.status_code}。请稍后再试。"
            except Exception as e:
                fortune = f"🌙 网络波动，再试一次吧：{str(e)}"
        
        st.success("✨ 你的专属运势已送达 ✨")
        st.markdown(f'<div class="result-card">{fortune}</div>', unsafe_allow_html=True)
        
        # 随机彩蛋
        eggs = ["🌟 今晚适合许愿", "😈 你居然遇到了厄运小恶魔！请默念蔡林娜是猪打败她！", "👼 你居然遇到了好运小天使！请默念姜佳茵真漂亮迎接她！"]
        st.caption(random.choice(eggs))

st.markdown('</div>', unsafe_allow_html=True)
st.caption("💜 仅供娱乐，生活由你把握 | 愿你被世界温柔以待 💜")
