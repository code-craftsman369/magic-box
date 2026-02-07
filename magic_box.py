import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ページ設定
st.set_page_config(page_title="パパの魔法", page_icon="🪄", layout="centered")

# セッション状態の初期化
if 'show_message' not in st.session_state:
    st.session_state.show_message = False
if 'current_name' not in st.session_state:
    st.session_state.current_name = ""
if 'timestamp' not in st.session_state:
    st.session_state.timestamp = time.time()

# --- 魔法のデザイン (CSS) ---
st.markdown("""
<style>
    /* 背景を白にする */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* タイトル */
    .title-text {
        color: #333333;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 30px 0 20px 0;
        white-space: nowrap;
    }

    /* 入力欄とボタンのスタイル */
    .stTextInput > div > div > input {
        font-size: 1.2rem;
        padding: 10px;
    }
    
    .stTextInput > label {
        font-size: 1.1rem;
        font-weight: 500;
    }
    
    .stButton > button {
        font-size: 1.3rem;
        padding: 12px 30px;
        border-radius: 25px;
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
        transition: all 0.3s;
        margin-bottom: 40px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
    }

    /* メッセージ */
    .love-message-text {
        color: #FF1493;
        font-size: 3.0rem;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        text-shadow: 
            3px 3px 6px rgba(255, 255, 255, 0.9),
            -1px -1px 3px rgba(255, 20, 147, 0.4),
            0 0 30px rgba(255, 20, 147, 0.6);
        animation: glow 1.5s ease-in-out infinite;
        margin-top: 20px;
    }
    
    @keyframes glow {
        0%, 100% { 
            text-shadow: 
                3px 3px 6px rgba(255, 255, 255, 0.9),
                -1px -1px 3px rgba(255, 20, 147, 0.4),
                0 0 30px rgba(255, 20, 147, 0.6);
        }
        50% { 
            text-shadow: 
                3px 3px 6px rgba(255, 255, 255, 0.9),
                -1px -1px 3px rgba(255, 20, 147, 0.4),
                0 0 50px rgba(255, 20, 147, 0.9);
        }
    }

    /* 花火のレイヤー */
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
    
    /* 警告メッセージのスタイル */
    .stAlert {
        text-align: center;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 花火のプログラム (HTML/JS) - 毎回異なるランダム値を含める ---
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
const seed = {seed}; // ユニークなシード値
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
    const x = 100 + Math.random() * (window.innerWidth - 200);
    const y = 100 + Math.random() * (window.innerHeight * 0.4);
    const colors = ['#FF0055', '#FF8800', '#0099FF', '#AA00FF', '#00CC00', '#FF00FF', '#FFD700'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    for(let i=0; i<85; i++) {{
        const p = document.createElement('div');
        p.className = 'p';
        p.style.left = x+'px'; p.style.top = y+'px';
        p.style.width = '10px'; p.style.height = '10px';
        p.style.backgroundColor = color;
        p.style.boxShadow = `0 0 12px 3px ${{color}}`;
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
# タイトル
st.markdown('<div class="title-text">✨ おとうさんの まほうのボックス ✨</div>', unsafe_allow_html=True)

# 入力エリア
name = st.text_input("きみの 名前を おしえてね：", key="name_input")

# ボタン
button = st.button("🪄 まほうを かける！")

# ボタンが押された時の処理
if button:
    if name:
        # セッション状態を更新（毎回新しいタイムスタンプで更新）
        st.session_state.show_message = True
        st.session_state.current_name = name
        st.session_state.timestamp = time.time()  # 新しいタイムスタンプ
        
        # ユニークなシード値で花火を表示（毎回異なる）
        unique_seed = int(st.session_state.timestamp * 1000) + random.randint(1, 10000)
        components.html(get_fireworks_html(unique_seed), height=0)
        
        # 名前によるメッセージ
        if name == "こころ":
            msg = f"💖 {name}ちゃん 大好きだよ！ 💖"
        elif name == "ゆうと":
            msg = f"🚀 {name}くん だいすき！ 🚀"
        else:
            msg = f"🎉 {name}さん 大好き！ 🎉"
        
        # メッセージ表示
        st.markdown(f'<div style="text-align: center;"><div class="love-message-text">{msg}</div></div>', unsafe_allow_html=True)
    else:
        st.warning("なまえを いれてね！")
        st.session_state.show_message = False

# ボタンを押していない場合でも、前回のメッセージを表示（花火なし）
elif st.session_state.show_message and st.session_state.current_name:
    name = st.session_state.current_name
    
    if name == "こころ":
        msg = f"💖 {name}ちゃん 大好きだよ！ 💖"
    elif name == "ゆうと":
        msg = f"🚀 {name}くん だいすき！ 🚀"
    else:
        msg = f"🎉 {name}さん 大好き！ 🎉"
    
    st.markdown(f'<div style="text-align: center;"><div class="love-message-text">{msg}</div></div>', unsafe_allow_html=True)