import streamlit as st
import requests
import random

st.set_page_config(page_title="今日运势", page_icon="🔮")
st.title("🔮今日运势")
st.markdown("测一测今天会怎样？")

zodiacs = ["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座",
           "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"]
zodiac = st.selectbox("选择你的星座", zodiacs)
name = st.text_input("你的名字（可选）", placeholder="比如：小姜")

# 尝试从 secrets 读取 API Key（云端部署用），否则用输入框（本地测试）
try:
    api_key = st.secrets["DEEPSEEK_API_KEY"]
    key_ready = True
except:
    api_key = st.text_input("DeepSeek API Key（本地测试用）", type="password", placeholder="输入你的API Key")
    key_ready = api_key is not None and api_key.strip() != ""

def get_fortune(zodiac, name, api_key):
    user_name = name if name else "朋友"
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
            return f"API 出错：{resp.status_code}"
    except Exception as e:
        return f"网络问题：{str(e)}"

if st.button("✨ 看看今日运势", type="primary"):
    if not key_ready:
        st.error("请先输入 DeepSeek API Key（本地测试）或检查云端配置")
    else:
        with st.spinner("🔮 占卜中..."):
            fortune = get_fortune(zodiac, name, api_key)
        st.success("你的今日运势")
        st.markdown(fortune)
        lucky_phrases = ["🌟 今天会有好事发生！", "🍀 保持微笑，运气不会差", "✨ 你比你想象的更棒"]
        st.caption(random.choice(lucky_phrases))

st.markdown("---")
st.caption("💡 仅供娱乐，生活由你把握")