import streamlit as st
import streamlit.components.v1 as components
import random

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
    .title-text { color: #333333; font-size: 2.5rem; font-weight: bold; text-align: center; padding: 20px 0; }
    
    /* まほうをかけるボタン（ピンク） */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #FF6B9D 0%, #C06C84 100%) !important;
        color: white !important; 
        width: 100%; 
        font-size: 1.5rem !important;
        padding: 15px !important; 
        border-radius: 30px !important; 
        border: none !important;
    }
    
    /* スマホでも3列を維持 */
    [data-testid="column"] { 
        width: 32% !important; 
        flex: 1 1 30% !important; 
        min-width: 30% !important; 
    }
    
    /* 楽器ボタン */
    .instrument-container div.stButton > button {
        font-size: 3.5rem !important; 
        height: 100px !important; 
        background: white !important;
        border: 3px solid #FFB6C1 !important; 
        border-radius: 20px !important; 
        margin-bottom: 10px !important;
    }
    
    .love-message-text { color: #FF1493; font-size: 2.5rem; font-weight: bold; text-align: center; margin-top: 10px; }
    
    @media (max-width: 600px) {
        .title-text { font-size: 8vw; } 
        .love-message-text { font-size: 8vw; }
        .instrument-container div.stButton > button { font-size: 3rem !important; height: 90px !important; }
    }
    
    iframe { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; border: none; pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# --- 音出し用関数（iPhoneの制限を解除する resume を含む） ---
def play_sound(js_inner_code):
    components.html(f"""
    <script>
    (function(){{
        const a = new (window.AudioContext || window.webkitAudioContext)();
        if (a.state === 'suspended') {{ a.resume(); }}
        {js_inner_code}
    }})();
    </script>
    """, height=0)

# --- 花火のプログラム ---
def get_fireworks_html():
    rid = random.randint(0, 999999)
    return f"""
<!DOCTYPE html>
<html>
<head><style>body {{ margin: 0; background: transparent; overflow: hidden; }} .p {{ position: absolute; border-radius: 50%; pointer-events: none; }} @keyframes f {{ 0% {{ transform: translate(0,0) scale(1); opacity: 1; }} 100% {{ transform: translate(var(--x), var(--y)) scale(0); opacity: 0; }} }}</style></head>
<body><div id="id-{rid}"></div><script>(function() {{
    const a = new (window.AudioContext || window.webkitAudioContext)();
    if (a.state === 'suspended') {{ a.resume(); }}
    function boom() {{ 
        const o=a.createOscillator(); const g=a.createGain(); o.type='triangle'; o.connect(g); g.connect(a.destination); 
        const n=a.currentTime; o.frequency.setValueAtTime(150,n); o.frequency.exponentialRampToValueAtTime(40,n+0.4); 
        g.gain.setValueAtTime(0.5,n); g.gain.exponentialRampToValueAtTime(0.01,n+0.4); o.start(); o.stop(n+0.4); 
    }}
    function launch() {{ 
        boom(); const x=Math.random()*window.innerWidth; const y=window.innerHeight*0.4; 
        const colors=['#FF0055','#FF8800','#0099FF','#AA00FF','#00CC00','#FF00FF']; 
        const c=colors[Math.floor(Math.random()*colors.length)]; 
        for(let i=0;i<85;i++){{ 
            const p=document.createElement('div'); p.className='p'; p.style.left=x+'px'; p.style.top=y+'px'; 
            p.style.width='8px'; p.style.height='8px'; p.style.backgroundColor=c; p.style.boxShadow=`0 0 10px 2px ${{c}}`; 
            const ang=Math.random()*Math.PI*2; const v=120+Math.random()*200; 
            p.style.setProperty('--x',Math.cos(ang)*v+'px'); p.style.setProperty('--y',Math.sin(ang)*v+'px'); 
            p.style.animation='f 1.3s ease-out forwards'; document.body.appendChild(p); setTimeout(()=>p.remove(),1300); 
        }} 
    }}
    setTimeout(launch,100); setTimeout(launch,600); setTimeout(launch,1100);
}})();</script></body></html>
"""

# --- メイン画面 ---
st.markdown('<div class="title-text">✨ おとうさんの まほうのボックス ✨</div>', unsafe_allow_html=True)
name = st.text_input("きみの 名前を おしえてね：", key="name_input")

if st.button("🪄 まほうを かける！"):
    if name:
        st.session_state.show_message = True
        st.session_state.current_name = name
        msg = f"💖 {name}ちゃん 大好きだよ！ 💖" if name=="こころ" else f"🚀 {name}くん だいすき！ 🚀" if name=="ゆうと" else f"🎉 {name}さん 大好き！ 🎉"
        st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)
        components.html(get_fireworks_html(), height=0)
    else: 
        st.warning("なまえを いれてね！")

elif st.session_state.show_message:
    n = st.session_state.current_name
    msg = f"💖 {n}ちゃん 大好きだよ！ 💖" if n=="こころ" else f"🚀 {n}くん だいすき！ 🚀" if n=="ゆうと" else f"🎉 {n}さん 大好き！ 🎉"
    st.markdown(f'<div class="love-message-text">{msg}</div>', unsafe_allow_html=True)

# --- 🎹 おとあそび コーナー ---
st.markdown('<hr style="margin: 5px 0;"><div style="text-align:center; color:#555; font-weight:bold; font-size:1.5rem; margin-bottom:5px;">🎹 おとあそび</div>', unsafe_allow_html=True)
st.markdown('<div class="instrument-container">', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🎹", key="btn1"): 
        play_sound("const o=a.createOscillator();const g=a.createGain();o.type='sine';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(440,a.currentTime);g.gain.setValueAtTime(0.5,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.5);o.start();o.stop(a.currentTime+0.5);")
    if st.button("🪘", key="btn4"): 
        play_sound("const o=a.createOscillator();const g=a.createGain();o.type='sine';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(100,a.currentTime);o.frequency.exponentialRampToValueAtTime(10,a.currentTime+0.2);g.gain.setValueAtTime(0.8,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.2);o.start();o.stop(a.currentTime+0.2);")
with c2:
    if st.button("🥁", key="btn2"): 
        play_sound("const s=a.sampleRate*0.5;const b=a.createBuffer(1,s,a.sampleRate);const d=b.getChannelData(0);for(let i=0;i<s;i++){d[i]=Math.random()*2-1;}const n=a.createBufferSource();n.buffer=b;const f=a.createBiquadFilter();f.type='highpass';f.frequency.value=5000;const g=a.createGain();n.connect(f);f.connect(g);g.connect(a.destination);g.gain.setValueAtTime(0.5,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.5);n.start();")
    if st.button("🎷", key="btn5"): 
        play_sound("const o=a.createOscillator();const g=a.createGain();o.type='square';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(349.23,a.currentTime);g.gain.setValueAtTime(0.2,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.8);o.start();o.stop(a.currentTime+0.8);")
with c3:
    if st.button("🔔", key="btn3"): 
        play_sound("const o=a.createOscillator();const g=a.createGain();o.type='triangle';o.connect(g);g.connect(a.destination);o.frequency.setValueAtTime(880,a.currentTime);g.gain.setValueAtTime(0.3,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+1.0);o.start();o.stop(a.currentTime+1.0);")
    if st.button("👏", key="btn6"): 
        play_sound("const s=a.sampleRate*0.1;const b=a.createBuffer(1,s,a.sampleRate);const d=b.getChannelData(0);for(let i=0;i<s;i++){d[i]=Math.random()*2-1;}const n=a.createBufferSource();n.buffer=b;const f=a.createBiquadFilter();f.type='bandpass';f.frequency.value=2000;const g=a.createGain();n.connect(f);f.connect(g);g.connect(a.destination);g.gain.setValueAtTime(0.8,a.currentTime);g.gain.exponentialRampToValueAtTime(0.01,a.currentTime+0.1);n.start();")

st.markdown('</div>', unsafe_allow_html=True)