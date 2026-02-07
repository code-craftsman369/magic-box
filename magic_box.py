import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ページ設定
st.set_page_config(page_title="パパの魔法", page_icon="🪄", layout="centered")

# --- セッション状態の初期化（エラー防止） ---
if 'show_message' not in st.session_state:
    st.session_state.show_message = False
if 'current_name' not in st.session_state:
    st.session_state.current_name = ""
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = time.time()

# --- 魔法のデザイン (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    
    .title-text {
        color: #333333;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
        white-space: nowrap;
    }

    .stButton > button {
        width: 100%;
        font-size: 1.2rem;
        padding: 12px;
        border-radius: 25px;
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 100%);
        color: white;
        border: none;
    }

    .love-message-text {
        color: #FF1493;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.9);
        margin-top: 30px;
    }

    /* iPhoneで一行に収まるように自動調整 */
    @media (max-width: 600px) {
        .title-text { font-size: 1.4rem; }
        .love-message-text { font-size: 7vw; }
    }

    iframe {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        border: none;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 花火のプログラム ---
def get_fireworks_html(seed):
    return f"""
<!DOCTYPE html>
<html>
<head>
<style>
    body {{ margin: 0; background: transparent; overflow: hidden; height: 100vh; width: 100vw; }}
    .p {{ position: absolute; border-radius: 50%; pointer-events: none; }}
    @keyframes f {{
        0% {{ transform: translate(0,0) scale(1); opacity: 1; }}
        100% {{ transform: translate(var(--x), var(--y)) scale(0); opacity: 0; }}
    }}
</style>
</head>
<body>
<script>
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function boom() {{
    const o = audioCtx.createOscillator();
    const g = audioCtx.createGain();
    o.type = 'triangle';
    o.connect(g); g.connect(audioCtx.destination);
    const n = audioCtx.currentTime;
    o.frequency.setValueAtTime(150, n);
    o.frequency.exponentialRampToValueAtTime(40, n + 0.4);
    g.gain.setValueAtTime(0.5, n);
    g.gain.exponentialRampToValueAtTime(0.01, n + 0.4);
    o.start(); o.stop(n + 0.4);
}}
function launch() {{
    boom();
    const x = Math.random() * window.innerWidth;
    const y = window.innerHeight * 0.4;
    const colors = ['#FF0055', '#FF8800', '#0099FF', '#AA00FF', '#00CC00', '#FF00FF'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    for(let i=0; i<85; i++) {{
        const p = document.createElement('div');
        p.className = 'p';
        p.style.left = x+'px'; p.style.top = y+'px';
        p.style.width = '8px'; p.style.height = '8px';
        p.style.backgroundColor = color;
        p.style.boxShadow = `0 0 10px 2px ${{color}}`;
        const a = Math.random() * Math.PI * 2;
        const v = 120 + Math.random() * 200;
        p.style.setProperty('--x', Math.cos(a)*v+'px');
        p.style.setProperty('--y', Math.sin(a)*v+'px');
        p.style.animation = 'f 1.3s ease-out forwards';
        document.body.appendChild(p);
        setTimeout(()=>p.remove(), 1300);
    }}
}}
setTimeout(launch, 100);
setTimeout(launch, 700);
setTimeout(launch, 1300);
</script>
</body>
</html>
"""

# --- 画面表示 ---
st.markdown('<div class="title-text">✨ おとうさんの まほうのボックス ✨</div>', unsafe_allow_html=True)

name = st.text_input("きみの 名前を おしえてね：", key="name_input")
button = st.button("🪄 まほうを かける！")

if button:
    if name:
        st.session_state.show_message = True
        st.session_state.current_name = name
        st.session_state.timestamp = time.time()
        
        unique_seed = int(st.session_state.timestamp * 1000)
        components.html(get_fireworks_html(unique_seed), height=0)
        
        if name == "こころ":
            msg = f"💖 {name}ちゃん 大好きだよ！ 💖"
        elif name == "ゆうと":
            msg = f"🚀 {name}くん だいすき！ 🚀"
        else:
            msg = f"🎉 {name}さん 大好き！ 🎉"
        
        st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)
    else:
        st.warning("なまえを いれてね！")
        st.session_state.show_message = False

# エラーを回避しつつ、前回のメッセージを保持する処理
elif st.session_state.get('show_message') and st.session_state.get('current_name'):
    name = st.session_state.current_name
    if name == "こころ":
        msg = f"💖 {name}ちゃん 大好きだよ！ 💖"
    elif name == "ゆうと":
        msg = f"🚀 {name}くん だいすき！ 🚀"
    else:
        msg = f"🎉 {name}さん 大好き！ 🎉"
    st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)