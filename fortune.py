import streamlit as st
import requests
import random
import time
from datetime import date

st.set_page_config(page_title="今日运势", page_icon="🔮", layout="centered")

# ========== 紫色主题（去掉标题边框） ==========
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #1e1a2f 0%, #2a1e3c 50%, #3a2a4f 100%);
    color: #f0e6ff;
}
h1, h2, h3, .stMarkdown {
    border: none !important;
    box-shadow: none !important;
}
.css-1kyxreq, .stSelectbox, .stTextInput, .stButton button {
    background: rgba(46, 32, 68, 0.7) !important;
    backdrop-filter: blur(10px);
    border-radius: 20px !important;
    border: none !important;
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
</style>
""", unsafe_allow_html=True)

st.title("🔮今日运势")
st.markdown("*请让我来为你揭晓今日的秘密*")

# ========== 生日 → 星座 ==========
def get_zodiac(birth_date):
    month_day = (birth_date.month, birth_date.day)
    if (month_day >= (3, 21) and month_day <= (4, 19)):
        return "白羊座"
    elif (month_day >= (4, 20) and month_day <= (5, 20)):
        return "金牛座"
    elif (month_day >= (5, 21) and month_day <= (6, 21)):
        return "双子座"
    elif (month_day >= (6, 22) and month_day <= (7, 22)):
        return "巨蟹座"
    elif (month_day >= (7, 23) and month_day <= (8, 22)):
        return "狮子座"
    elif (month_day >= (8, 23) and month_day <= (9, 22)):
        return "处女座"
    elif (month_day >= (9, 23) and month_day <= (10, 23)):
        return "天秤座"
    elif (month_day >= (10, 24) and month_day <= (11, 22)):
        return "天蝎座"
    elif (month_day >= (11, 23) and month_day <= (12, 21)):
        return "射手座"
    elif (month_day >= (12, 22) or month_day <= (1, 19)):
        return "摩羯座"
    elif (month_day >= (1, 20) and month_day <= (2, 18)):
        return "水瓶座"
    else:
        return "双鱼座"

default_birth = date(2000, 1, 1)
birthday = st.date_input("🎂 选择你的生日", value=default_birth, min_value=date(1900,1,1), max_value=date.today())
zodiac = get_zodiac(birthday)
st.info(f"✨ 你的星座是：**{zodiac}**")

name = st.text_input("🌟 你的名字", placeholder="比如：小姜")

# ========== 新增性别选择 ==========
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
    # 根据性别设置称呼
    if gender == "女":
        honorific = "亲爱的朋友"
    elif gender == "男":
        honorific = "亲爱的朋友"
    else:
        honorific = "亲爱的朋友"
    
    prompt = f"""你是一位神秘且强大的命运塔罗牌占卜师，风格可爱幽默。请为{user_name}（{honorific}，{zodiac}）生成今日运势。

要求：
1. 分四个维度：💼事业运势、💖爱情运势、💪健康运势、💰财运
2. 每个维度一句话，积极正面或略带调侃，可以毒舌但绝不能人身攻击也不可以说别人倒霉
3. 最后给“今日幸运色”和“今日小贴士”
4. 语气像好朋友聊天，不要太严肃
5. 总字数150字以内
6. 第一句话请提示大家一天仅可以测一回否则不准

输出格式：
🐱提示：...
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
            fortune = get_fortune(zodiac, name, gender, api_key)  # 传入gender
            msg_placeholder.empty()
        
        st.success("🌟 你的今日运势已送达 🌟")
        st.markdown(fortune)
        lucky = ["🌟 今天会有好事发生！", "🍀 保持微笑，运气不会差", "✨ 你比你想象的更棒", "🌙 记得许个愿哦", "🔮 你的直觉很准，相信它"]
        st.caption(random.choice(lucky))

st.markdown("---")
st.caption("💜 仅供娱乐，生活由你把握 | 愿你充满魔法般的惊喜 💜")
