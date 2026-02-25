import streamlit as st


st.set_page_config(
    page_title="Home | Data Engineer",
    page_icon='🙇‍♀️',
    layout='wide',
    initial_sidebar_state='expanded'
)
st.markdown("""
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)


st.html("""
    <style>
        section[data-testid="stSidebar"] { padding-top: 2rem; }

        a { text-decoration: none; font-family: monospace; }

        .divider { border: none; border-top: 1px solid #30363d; margin: 1.5rem 0; }

        nav { width: 100%; display: inline-flex; align-items: center; justify-content: space-around; font-size: 0.9rem; }

        .btn-github { background-color: transparent; color: #e6edf3; }
        .btn-email { background-color: transparent; color: #58a6ff; }
        .btn-github:hover { color: #00C2FF; }
        .btn-email:hover { color: #7dd3fc; }

        .main-title { font-size: 3rem; font-weight: 700; font-family: monospace; color: #e6edf3; line-height: 1.5; }
        .highlight { color: #00C2FF; }

        .intro-card { background-color: transparent; border: 1px solid #30363d; border-left: 3px solid #00C2FF; border-radius: 8px; padding: 1.2rem 1.5rem; font-size: 1rem; line-height: 1.8; color: #c9d1d9; }

        .badge { display: inline-block; background: #1c2d3f; color: #00C2FF; border: 1px solid #00C2FF44; border-radius: 6px; padding: 4px 12px; margin: 4px; font-size: 0.82rem; font-family: monospace; user-select: none; cursor: default; }

        .github-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1rem; }
        .github-card img { width: 100%; border-radius: 4px; }
    </style>
""")




# side

with st.sidebar:
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    st.html("""
        <nav>
        <a href="https://github.com/hgim96715-lgtm" class="link-btn btn-github" target='_blank'> <i class="fa-brands fa-github"></i> GitHub</a>
        <a class="link-btn btn-email" href="mailto:hgim96715@email.com?subject=[포트폴리오%20문의]%20데이터%20엔지니어%20포지션&body=안녕하세요%20김한경%20님,%0A%0A(여기에%20내용을%20입력하세요)"><i class="fa-solid fa-envelope"></i> Email</a>
        </nav>
    """)
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")
    
    
# main
col_text,col_gap=st.columns([4,1])

with col_text:
    st.html("""
        <h2 class='main-title'>안녕하세요👋<br/><span class='highlight'>김한경</span>입니다.</h2>
        <h3 class='subtitle'> Data Engineer</h3>
    """)
    st.html("<hr class='divider'/>")


    st.html("""
        <section class='intro-card'>
        <b>응급구조사</b>로 시작해, 컴퓨터에 관심을 갖게 되어 <b>디지털 교과서 퍼블리셔</b>로 전직했습니다.<br/>
         JavaScript로 미니게임을 개발하며 개발자의 길에 첫 발을 내딛었습니다.<br/>
        이후 데이터에 매력을 느껴 <b>Kafka · Spark · Airflow · Flink</b> 기반의 대용량 파이프라인을 직접 설계·구축하며 Data Engineer로 전환 중입니다.<br/>
        모든 인프라를 <b>Docker Compose</b>로 컨테이너화하여 재현 가능한 환경을 구성합니다.<br/>
        <b>Obsidian</b>으로 학습 내용을 꾸준히 기록하며, 이를 블로그 형태로 공유합니다.
        </section>
        """)
    
    st.html("""
        <nav>
        <a href="https://github.com/hgim96715-lgtm" class="link-btn btn-github" target='_blank'> <i class="fa-brands fa-github"></i> GitHub</a>
        <a class="link-btn btn-email" href="mailto:hgim96715@email.com?subject=[포트폴리오%20문의]%20데이터%20엔지니어%20포지션&body=안녕하세요%20김한경%20님,%0A%0A(여기에%20내용을%20입력하세요)"><i class="fa-solid fa-envelope"></i> Email</a>
        </nav>
    """)
    
    st.html("<hr class='divider'/>")
    
    
    st.subheader("Tech Stack")
    st.caption( "데이터 엔지니어링 파이프라인 구축·운영에 활용 중인 핵심 기술과, 과거 실무 경험을 통해 축적한 기술 스택입니다.")
    
    badges = [
        "Apache Kafka", "Apache Spark", "Apache Flink", "Apache Airflow",
        "Python", "SQL", "PostgreSQL", "MinIO",
        "Docker", "Docker Compose", "Streamlit",
        "HTML", "CSS", "JavaScript",
    ]
    
    st.html(
        " ".join([f"<span class='badge'>{b}</span>" for b in badges]),
    )
    st.html("<hr class='divider'/>")
    
    
    GITHUB_ID='hgim96715-lgtm'
    st.html(f"""
    <h3>🌱Github Commit History</h3>
    <div class='github-card'>
        <img src="https://ghchart.rshah.org/216E39/{GITHUB_ID}"
             alt="GitHub contribution chart"/>
    </div>
    """)