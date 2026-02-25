import streamlit as st
import requests
import base64
import re
import yaml

st.set_page_config(
    page_title="Project | Data Engineer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)


GITHUB_USER="hgim96715-lgtm"
GITHUB_REPO="gong_home"
GITHUB_REPO_PROJECT="gong_study_de"
BRANCH ="main"
PROJECT_PATH="10_Projects/15_Project"
GITHUB_PATH="project"


STEPS = [
    {"file": "00_Project_HomePage", "label": " Overview",       "color": "#00C2FF"},
    {"file": "01_Faker_data",        "label": " Faker",          "color": "#A78BFA"},
    {"file": "02_Streamlit_Dashboard","label": " Dashboard",     "color": "#34D399"},
    {"file": "03_kafka_to_Postgres", "label": " Kafka → DB",     "color": "#F59E0B"},
    {"file": "04_Spark_Batch",       "label": " Spark Batch",    "color": "#F87171"},
    {"file": "05_Airflow_DAG",       "label": " Airflow",        "color": "#60A5FA"},
    {"file": "06_Flink_job",         "label": " Flink",          "color": "#FB923C"},
    {"file": "07_minIO",             "label": " MinIO",          "color": "#4ADE80"},
]

# 전체 기술 스택
TECH_STACK = [
    ("Apache Kafka",   "#F59E0B"),
    ("Apache Spark",   "#F87171"),
    ("Apache Flink",   "#FB923C"),
    ("Apache Airflow", "#60A5FA"),
    ("PostgreSQL",     "#34D399"),
    ("MinIO",          "#4ADE80"),
    ("Python",         "#A78BFA"),
    ("Docker",         "#00C2FF"),
    ("Streamlit",      "#FF4B4B"),
]


st.html("""
<style>
section[data-testid="stSidebar"] { padding-top: 2rem; }
a{text-decoration:none;}
section[data-testid="stSidebar"] .sub-title{color:#8b949e;font-family:monospace;}
.divider{border:none;border-top:1px solid #30363d;margin:1.2rem 0;}
.page-title { font-size: 2rem; font-weight: 700; font-family: monospace; color: #e6edf3; }
.page-sub   { font-family: monospace; color: #8b949e; font-size: 0.9rem; margin-bottom: 1rem; }
.page-label{font-family:monospace; color:#00C2FF;}
.project-header{background:#161b22;border:1px solid #30363d;border-top:3px solid #00C2FF;border-radius:10px;padding:1.5rem 2rem; margin-bottom:1rem;font-family:monospace;}
.project-title{fontsize:1.3rem;font-weight:700;font-family:monospace;color:#e6edf3;margin-bottom:0.4rem;}
.stack-badge{display:inline-block;border-radius:6px;padding:4px 12px; margin:3px;font-size:0.8rem;font-weight:600;border:1px solid;opacity:0.85;cursor:default;}
.gh-btn{display:inline-block;background:#21262d;color:#e6edf3 !important;border:1px solid #30363d;border-radius:8px;padding:8px 18px;font-size:0.88rem;}
.gh-btn:hover{border-color:#00C2FF;color:#00C2FF !important;}
.stMarkdown table{width:100%;font-family: monospace;}
.stMarkdown thead tr th {color: #00C2FF;background: #161b22;text-align:center;}
.stMarkdown code{font-family:monospace;}
</style>
""")

@st.cache_data(ttl=600)
def get_md(file_name:str)->str:
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{PROJECT_PATH}/{file_name}.md?ref={BRANCH}"
    headers={}
    if "GITHUB_TOKEN" in st.secrets:
        headers["Authorization"]=f"token {st.secrets['GITHUB_TOKEN']}"
    r=requests.get(url,headers=headers,timeout=10)
    if r.status_code !=200:
        return ""
    return base64.b64decode(r.json()["content"]).decode("utf-8")

def extract_mermaid(text: str):
    diagrams = re.findall(r'```mermaid\n([\s\S]*?)```', text)
    cleaned  = re.sub(r'```mermaid\n[\s\S]*?```', '<!-- mermaid -->', text)
    return diagrams, cleaned



def clean_md(text: str) -> str:
    # frontmatter 제거
    text = re.sub(r'^---[\s\S]*?---\n', '', text)
    # dataview 제거
    text = re.sub(r'```dataview[\s\S]*?```', '> 📊 *Dataview 블록은 Obsidian에서 확인하세요*', text)
    # callout
    text = re.sub(r'>\s*\[!(\w+)\]\s*', r'> **[\1]** ', text)
    def replace_image(m):
        filename = m.group(1).strip()
        filename = re.sub(r'\|.*$', '', filename)
        encoded = requests.utils.quote(filename)
        url = f"https://raw.githubusercontent.com/{GITHUB_USER}/{GITHUB_REPO}/{BRANCH}/99_Assets(이미지&첨부파일저장소)/{encoded}"
        # st.write(f"이미지 URL: {url}")
        return f"![{filename}]({url})"
    text = re.sub(r'!\[\[([^\]]+)\]\]', replace_image, text)
    return text.strip()

def render_md_with_mermaid(raw:str):
    diagrams,text=extract_mermaid(raw)
    cleaned=clean_md(text)
    
    parts = cleaned.split('<!-- mermaid -->')
    
    for i,part in enumerate(parts):
        if part.strip():
            st.markdown(part)
        if i<len(diagrams):
            try:
                from streamlit_mermaid import st_mermaid
                st_mermaid(diagrams[i],height=400)
            except ImportError:
                st.code(diagrams[i],language="text")
                st.caption("`pip3 install streamlit-mermaid` 설치시 다이어그램으로 표시됩니다.!")


# 사이드
with st.sidebar:  
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p class='sub-title'>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    st.markdown("**🏗️ 프로젝트 단계**")
    
    selected_step=st.radio(
        label="프로젝트 Step",
        options=[s["file"] for s in STEPS],
        format_func=lambda f:next(s["label"] for s in STEPS if s["file"]==f),
        label_visibility="collapsed"
    )
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")
    

# main

st.html("""
    <h1 class='page-title'><i class="fa-brands fa-usb" style="color: #00C2FF;"></i> Pipeline Project</h1>
    <div class='page-sub'>Kafka · Spark · Flink · Airflow · MinIO 기반 대용량 데이터 파이프라인</div>
""")

stack_badges=" ".join([
    f"<span class='stack-badge' style='color:{c};border-color:{c}44;background:{c}11;'>{n}</span>"
    for n,c in TECH_STACK
])
# st.write(stack_badges)

st.html(f"""
    <div class='project-header'>
        <div class='project-title'>Real-time&Batch Data Pipeline</div>
        <div class='project-desc'>
            Kafka로 실시간 로그를 수집하고 PostgreSQL에 적재,
            Spark로 배치 분석, Flink로 스트리밍 집계, Airflow로 워크플로우 자동화,
            MinIO에 Parquet 파일로 저장하는 End-to-End 파이프라인입니다.
            모든 인프라는 Docker Compose로 로컬에서 재현 가능하게 구성했습니다.
        </div>
        <br/>
        {stack_badges}
        <br/><br/>
        <a class='gh-btn' href='https://github.com/{GITHUB_USER}/{GITHUB_REPO_PROJECT}/tree/{BRANCH}/{GITHUB_PATH}' target='_blank'>
            <i class='fa-brands fa-github'></i> GitHub 코드 보기
        </a>
    </div>
    """)

st.html("<hr class='divider'/>")

current=next(s for s in STEPS if s["file"]==selected_step)
st.html(f"<strong class='page-label'>{current['label']}</strong>")

with st.spinner("노트 데려오는중..🚗"):
    raw=get_md(selected_step)
    cleaned_raw = clean_md(raw)

if cleaned_raw:
    render_md_with_mermaid(cleaned_raw)

else:
    st.warnig("🥹GitHub에서 파일을 불러올 수 없습니다.경로를 다시 확인해주세요")
    st.code(f"{PROJECT_PATH}/{selected_step}.md",language="text")


