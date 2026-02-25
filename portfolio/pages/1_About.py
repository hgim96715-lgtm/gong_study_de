import streamlit as st

st.set_page_config(
    page_title="About ME | Portfolio ",
    page_icon="👩‍💻",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">""", unsafe_allow_html=True)

st.html("""
    <style>
    section[data-testid="stSidebar"] { padding-top: 2rem; }
    a{text-decoration:none;}
    section[data-testid="stSidebar"] .sub-title{background-color: #1c2d3f; border: 1px solid #00C2FF44; border-radius: 8px; padding: 15px; text-align: center; margin-top: 20px; transition: 0.3s;cursor:pointer}
    .sub-title>a{color: #00C2FF; text-decoration: none; font-weight: 700; display: block;}
    .sub-title:hover{background-color: #263b52 !important;border-color: #00C2FF !important;}
    .divider{border:none;border-top:1px solid #30363d;margin:2rem 0;}
    
    .main .block-container{padding: 0; padding-bottom: 2rem; max-width: 100%;}
    
    .section-title{font-family: 'monospace';font-size: 1.4rem;font-weight: 800;color: #e6edf3;margin-bottom: 1.5rem;display: flex;align-items: center;}
    
    .hero-name{font-size:2.8rem;font-weight:800;color:#e6edf3;letter-spacing:-1px;display:flex;gap:3px;}
    .hero-name-en{color:#8b949e; margin-top: -2px;}
    .hero-role{font-size:1.2rem;color:#00C2FF;font-weight:600;margin:0.5rem 0 1.5rem;display:inline-block;background:#00C2FF22;padding:9px 17px;border-radius:20px;}
    .link-btn{display:inline-flex;align-items:center;background:#21262d;color:#e6edf3 !important;border:1px solid #30363d;border-radius:12px;padding:10px 20px;font-weight:600;margin-right:10px;transition:all 0.3s ease;}
    .link-btn:hover{border-color: #00C2FF;background: #00C2FF22; transform: translateY(-3px);}
    
    p,.intro-box{word-break:break-word;overflow-wrap:break-word;}
    .intro-box{background: #21262d;border: 1px solid #30363d; border-left: 4px solid #00C2FF;padding:25px 30px;border-radius: 10px;margin: 40px 0px;line-height: 1.8;color: #c9d1d9;}
    .intro-box h3{color: #00C2FF; font-size: 1.25rem;margin-top: 0;margin-bottom: 20px;font-weight: 700;line-height: 1.5;}
    .intro-box p{margin-bottom: 15px;font-size: 1rem;}
    .intro-box b{color: #e6edf3; font-weight: 700;}
    
    .dot-container{position: relative;padding-left: 45px;margin-bottom: 35px;}
    .dot-container::before{content:'';position:absolute;left: 13px;top: 12px;bottom:-35px;width: 2px;background:#30363d;}
    .dot-container:last-child::before{display: none;}
    .dot-icon{position: absolute;left: 0;top: 5px;width: 28px;height: 28px;background-color: #161b22;border: 2px solid #00C2FF;border-radius: 50%;color: #00C2FF;text-align: center;line-height: 24px;font-size: 13px;font-weight: bold;box-shadow: 0 0 10px #00C2FF44;}
    .dot-title{font-size: 1.15em;font-weight: 700;color: #e6edf3;margin-bottom: 8px;}
    .dot-desc{color: #8b949e; font-size: 0.95em;line-height: 1.7;}
    .highlight{background: #00C2FF15;padding: 2px 6px; border-radius: 4px; font-weight: 600;color: #58a6ff;}
    
    
    .skill-section{margin-bottom: 1.5rem;}
    .skill-label{font-size: 0.9rem; color: #8b949e; margin-bottom: 0.6rem;font-weight: 600;}
    .skill-badge{display: inline-block;border-radius: 20px; padding:6px 14px;margin: 0 6px 8px 0;font-size: 0.85rem;font-weight: 700;cursor:default;}
    
    .cert-card{background: #21262d; border: 1px solid #30363d;border-radius: 12px;padding: 1rem 1.5rem;margin-bottom:0.8rem;display:flex;justify-content:space-between;align-items:center;}
    .cert-name{font-size: 0.95rem;font-weight: 700;color: #e6edf3;}
    .cert-date{font-size: 0.8rem;color: #8b949e; margin-top: 4px;}
    .cert-badge{font-size: 0.75rem;padding: 4px 10px; border-radius: 20px;font-weight: 600;border: 1px solid;}
    .cert-badge-done{background: #1a2f1a;color: #4CAF50;border-color:  #4CAF5044;}
    .cert-badge-pending{background: #2d2a1a; color: #F59E0B; border-color:  #F59E0B44;}
    .github-container{background: #21262d;border: 1px solid #30363d;border-radius: 12px;padding: 1.5rem;text-align: center;}
    .github-container>img{width:100%; max-width:100%; border-radius:4px; opacity:0.9;}
    .github-container>div{margin-top:10px; font-size:0.8rem; color:#8b949e;}
    
    
    </style>
""")

GITHUB_ID = "hgim96715-lgtm"
EMAIL     = "hgim96715@email.com"
NAME_KO   = "김한경"
NAME_EN   = "Kim Han Gyeong"
MAILTO    = f"mailto:{EMAIL}?subject=[포트폴리오 문의] 데이터 엔지니어 포지션&body=안녕하세요 {NAME_KO} 님,%0A%0A"


with st.sidebar:
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")
    st.html("""
    <div class='sub-title'>
        <a href='/Obsidian',target='_self'>저의 portfolio를 구경<br/>하러 가실까요? 🚀</a>
    </div>""")
    
    
    
    


st.html(f"""
    <div class="hero-name">{NAME_KO} <span class="hero-name-en">({NAME_EN})</span></div>
    <div class="hero-role">👩‍💻&nbsp;Data Engineer</div>
    <div class="hero-contact">
        <a href="{MAILTO}" class="link-btn"><i class="fa-solid fa-envelope"></i>&nbsp;Contact Me</a>
        <a href="https://github.com/{GITHUB_ID}" target="_blank" class="link-btn"><i class="fa-brands fa-github"></i>
            &nbsp;GitHub</a>
    </div>
""")

col_left,col_right=st.columns([7,5],gap="large")

with col_left:
    st.html("""
    <div class="intro-box">
        <h3>안녕하세요! 응급구조사에서 출발해 디지털 교과서 퍼블리셔를 거쳐,<br/>이제는 데이터의 흐름을 설계하는 데이터 엔지니어로 나아가고 있습니다.</h3>
        <p>
            지하철이나 기차를 탈 때 찍는 카드 기록들, 일상생활에서 무심코 지나치는 이 모든 것들이 '데이터'라는 사실을 깨달았을 때의 놀라움과 흥미가 저를 이 길로 이끌었습니다.<i>'우리에게 이렇게 가까운 데이터들이 과연 어떤 인트라를 거쳐, 어떻게 가공되어 우리 눈앞에 보여지는 걸까?'</i>라는 단순한 호기심은 곧 열정으로 바뀌었습니다.
        </p>
        <p>
            디지털 교과서에서 미니게임을 개발할 당시, 처음 기획자로부터 SB(스토리보드)를 받았을 땐 어디서부터 손대야 할지 막막하기도 했습니다.
            하지만 하나하나 조건을 찾아가며 논리적인 흐름을 완성하고, 마침내 게임이 제 의도대로 실행되었을때의 그 짜릿한 성취감은 지금도 잊을 수 없습니다.
        </p>
        <p>
            응급구조사로서 응급상황에서 기른 <b>빠른 상황 판단과 문제 해결 능력</b>, 퍼블리셔로서 치열하게 고민했던 <b>사용자 중심의 UI/UX 감각과 프로그래밍 흐름도에 대한 이해</b> 등
            이 모든 경험들은 이제 Python·SQL·Kafka·Spark·Flink·Airflow 기반의 End-to-End 데이터 파이프라인을 직접 설계하고 구축하는 저만의 든든한 밑거름이 되었습니다.
        </p>
        <p>
            어제보다 더 나은 데이터 엔지니어가 되기 위해, <b>매일 매일 옵시디언(Obsidian)에 학습 내용을 체계적으로 기록하고, Linux,Python 코딩테스트, SQL 쿼리 작성 연습</b>을 꾸준히 연습하며 차근차근 성장해 나가고 있습니다.
        </p>
    </div>
""")

st.html("""<div class="section-title"><i class="fa-solid fa-link" style="color: #00C2FF;"></i>&nbsp;작은 점들이 이어진 성장의 과정</div>""")

st.html("""
    <div class="dot-container">
        <div class="dot-icon">🚑</div>
        <div class="dot-tile">응급구조사: 예측 불가능한 현장에서의 문제 해결</div>
        <div class="dot-desc">
            생명이 오가는 현장에서 가장 중요한 것은 <span class="highlight">빠른 판단력과 정확한 대처</span>였습니다.
            이때 몸에 밴 '문제 상황을 직면했을 때 당황하지 않고 원인을 찾아 해결하는 태도'는
            현재 복잡한 데이터 인프라에서 발생하는 에러를 디버깅하고 해결하는데 강력한 무기가 되고 있습니다.
        </div>
    </div>
    <div class="dot-container">
        <div class="dot-icon">📖</div>
        <div class="dot-tile">디지털 교과서 퍼블리셔 : SB를 현실의 로직으로 구현하다</div>
        <div class="dot-desc">
            복잡한 요구사항이 담긴 스토리보드를 분석해 HTML/CSS/JavaScript로 미니게임을 개발했습니다.
            막연했던 아이디어를 하나하나 조건문과 로직으로 분해하여 <span class="highlight">실행 가능한 프로그램으로 만들어내는 성취감</span>을 느낄 수 있었습니다.
            또한, 사용자가 데이터를 어떻게 시각적으로 인지하는지 고민하며 UI/UX를 개선하는 과정에서 <span class="highlight">사용자 중심의 사고방식</span>을 키울 수 있었습니다.
        </div>
    </div>
    <div class="dot-container">
        <div class="dot-icon">♾️</div>
        <div class="dot-tile">데이터 엔지니어 : 무수한 데이터의 흐름을 설계하는 건축가</div>
        <div class="dot-desc">
           저만의 커리어로 쌓아온 '문제 해결력'과 '로직 구현력','사용자 중심의 사고방식'을 하나로 모아, 현재는 <span class="highlight">Kafka,Spark,Airflow등을 활용한 End-to-End 파이프라인</span>을 구축하고 있습니다.
           매일 옵시디언에 학습 로그를 남기고, Linux와 Python,SQL을 손에 익히며 저만의 데이터 엔지니어링 역량을 키워가고 있습니다.
        </div>
    </div>
""")

with col_right:
    st.html("<div style='margin-top: 20px;'></div>")
    st.html("""<div class='section-title'><i class='fa-solid fa-layer-group' style="color: #00C2FF;"'></i>&nbsp;Tech Stack</div>""")
    
    skills = {
        "Core Engineering": [("Kafka", "#F59E0B"), ("Spark", "#F87171"), ("Flink", "#FB923C"), ("Airflow", "#60A5FA")],
        "Infrastructure & DB": [("Docker", "#00C2FF"), ("MinIO", "#4ADE80"), ("PostgreSQL", "#34D399")],
        "Languages & Tools": [("Python", "#A78BFA"), ("SQL", "#34D399"), ("JavaScript", "#F7DF1E"), ("Streamlit", "#FF4B4B"), ("Obsidian", "#9c27b0")]
    }
    for category,stack in skills.items():
        badges = " ".join([f"<span class='skill-badge' style='color:{c};border-color:{c};background:{c}15;'>{n}</span>" for n, c in stack])
        st.html(f"""<div class='skill-section'><div class='skill-label'>{category}</div>{badges}</div>""")
        
    st.html("<hr class='divider'/>")
    
    st.html("""<div class='section-title'><i class='fa-solid fa-seedling' style='color:#4CAF50;'></i>&nbsp;Growth & Certs</div>""")
    
    st.html(f"""
        <div class="github-container">
            <img src="https://ghchart.rshah.org/216E39/{GITHUB_ID}" alt="Github chart">
            <div>하루하루 쌓아가는 GitHub 기록 <i class='fa-solid fa-seedling' style='color:#4CAF50;'></i></div>
        </div>
    """)
    st.html("""<div style='margin-top: 1.5rem;'></div>""")
    
    st.html("""
    <div class="cert-card">
        <div>
            <div class="cert-name">정보처리기능사</div>
            <div class="cert-date">한국산업인력공단</div>
        </div>
        <span class="cert-badge cert-badge-done"><i class="fa-solid fa-check"></i> 취득 완료</span>
    </div>
    <div class="cert-card">
        <div>
            <div class="cert-name">SQLD(예정)</div>
            <div class="cert-date">데이터자격시험</div>
        </div>
        <span class="cert-badge cert-badge-pending"><i class="fa-solid fa-check"></i> 준비 중</span>
    </div>
    """)

