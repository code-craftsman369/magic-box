import streamlit as st
import streamlit.components.v1 as components
import random
import time

# ページ設定
st.set_page_config(page_title="パパの魔法", page_icon="🪄", layout="centered")

# --- セッション状態の初期化 ---
if 'show_message' not in st.session_state:
    st.session_state.show_message = False
if 'current_name' not in st.session_state:
    st.session_state.current_name = ""

# --- 魔法のデザイン (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF; }
    
    /* タイトル：特大サイズ */
    .title-text {
        color: #333333;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
    }

    /* 「まほうをかける」ボタン：ピンクのグラデーション */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 100%) !important;
        color: white !important;
        width: 100%;
        font-size: 1.5rem !important;
        padding: 15px !important;
        border-radius: 30px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.4) !important;
    }

    /* 楽器ボタン：限界突破の巨大化 */
    .instrument-container div.stButton > button {
        font-size: 15rem !important; /* 文字サイズをさらにアップ */
        line-height: 1 !important;
        height: 350px !important;    /* 縦幅もさらに確保 */
        background: white !important;
        border: 5px solid #FFB6C1 !important;
        border-radius: 50px !important;
        margin-bottom: 30px !important;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1) !important;
        transition: transform 0.1s !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .instrument-container div.stButton > button:active {
        transform: scale(0.8) !important; /* 押した時に大きく凹むように */
    }

    .love-message-text {
        color: #FF1493;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        white-space: nowrap;
        text-shadow: 2px 2px 5px rgba(255, 255, 255, 0.9);
        margin-top: 10px;
    }

    /* iPhone/スマホ向けのレスポンシブ設定：画面幅いっぱいに */
    @media (max-width: 600px) {
        .title-text { font-size: 8vw; }
        .love-message-text { font-size: 8vw; }
        .instrument-container div.stButton > button { 
            font-size: 8rem !important; /* スマホの横幅3分割の限界サイズ */
            height: 200px !important; 
            border-radius: 30px !important;
        }
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

# --- サウンドプログラム（変更なし） ---
def play_sound(js_code):
    components.html(f"<script>(function(){{{js_code}}})();</script>", height=0)

def get_fireworks_html():
    rid = random.randint(0, 999999)
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
<div id="id-{rid}"></div>
<script>
(function() {{
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
    setTimeout(launch, 600);
    setTimeout(launch, 1100);
}})();
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
        
        if name == "こころ":
            msg = f"💖 {name}さん 大好きだよ！ 💖"
        elif name == "ゆうと":
            msg = f"🚀 {name}くん だいすき！ 🚀"
        else:
            msg = f"🎉 {name}さん 大好き！ 🎉"
        
        st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)
        components.html(get_fireworks_html(), height=0)
    else:
        st.warning("なまえを いれてね！")
        st.session_state.show_message = False

elif st.session_state.get('show_message') and st.session_state.get('current_name'):
    name = st.session_state.current_name
    if name == "こころ":
        msg = f"💖 {name}さん 大好きだよ！ 💖"
    elif name == "ゆうと":
        msg = f"🚀 {name}くん だいすき！ 🚀"
    else:
        msg = f"🎉 {name}さん 大好き！ 🎉"
    st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)

# --- 🎹 おとあそび コーナー ---
st.markdown('<hr style="margin: 5px 0;">', unsafe_allow_html=True)
st.markdown('<div style="text-align:center; color:#555; font-weight:bold; font-size:1.5rem; margin-bottom:5px;">🎹 おとあそび</div>', unsafe_allow_html=True)

st.markdown('<div class="instrument-container">', unsafe_allow_html=True)

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    if st.button("🎹", key="w1"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const o=a.createOscillator();const g=a.createGain();o.type='sine';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(440,a.currentTime);g.gain.setValueAtTime(0.5,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.5);o.start();o.stop(a.currentTime+0.5);")
with row1_col2:
    if st.button("🥁", key="w2"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const s=a.sampleRate*0.5;const b=a.createBuffer(1,s,a.sampleRate);const d=b.getChannelData(0);for(let i=0;i<s;i++){d[i]=Math.random()*2-1;}const n=a.createBufferSource();n.buffer=b;const f=a.createBiquadFilter();f.type='highpass';f.frequency.value=5000;const g=a.createGain();n.connect(f);f.connect(g);g.connect(a.destination);g.gain.setValueAtTime(0.5,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.5);n.start();")
with row1_col3:
    if st.button("🔔", key="w3"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const o=a.createOscillator();const g=a.createGain();o.type='triangle';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(880,a.currentTime);g.gain.setValueAtTime(0.3,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+1.0);o.start();o.stop(a.currentTime+1.0);")

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    if st.button("🪘", key="w4"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const o=a.createOscillator();const g=a.createGain();o.type='sine';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(100,a.currentTime);o.frequency.exponentialRampToValueAtTime(10,a.currentTime+0.2);g.gain.setValueAtTime(0.8,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.2);o.start();o.stop(a.currentTime+0.2);")
with row2_col2:
    if st.button("🎷", key="w5"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const o=a.createOscillator();const g=a.createGain();o.type='square';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(349.23,a.currentTime);g.gain.setValueAtTime(0.2,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.8);o.start();o.stop(a.currentTime+0.8);")
with row2_col3:
    if st.button("👏", key="w6"):
        play_sound("const a=new (window.AudioContext||window.webkitAudioContext)();const s=a.sampleRate*0.1;const b=a.createBuffer(1,s,a.sampleRate);const d=b.getChannelData(0);for(let i=0;i<s;i++){d[i]=Math.random()*2-1;}const n=a.createBufferSource();n.buffer=b;const f=a.createBiquadFilter();f.type='bandpass';f.frequency.value=2000;const g=a.createGain();n.connect(f);f.connect(g);g.connect(a.destination);g.gain.setValueAtTime(0.8,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.1);n.start();")

st.markdown('</div>', unsafe_allow_html=True)