import streamlit as st
import requests
import re
from datetime import datetime, date,timedelta
import calendar
import base64
import yaml
import concurrent.futures


st.set_page_config(
    page_title="Challenge | Python_SQL_Linux",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded"
)

GITHUB_USER="hgim96715-lgtm"
GITHUB_REPO="gong_home"
BRANCH ="main"

CHALLENGES = {
    "11_Daily_SQL_Challenge":    {"label": " SQL",    "color": "#F29D38", "source": "solvesql",    "source_url": "https://solvesql.com"},
    "12_Daily_Python_Challenge": {"label": "Python", "color": "#3C8DBC", "source": "programmers", "source_url": "https://school.programmers.co.kr"},
    "13_Daily_Linux_Challenge":  {"label": " Linux",  "color": "#4CAF50", "source": "hackerrank",  "source_url": "https://www.hackerrank.com"},
}

st.markdown("""
<link rel="stylesheet"
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)


st.html("""
    <style>
        section[data-testid="stSidebar"] { padding-top: 2rem; }
        section[data-testid="stSidebar"] .sub-title{color:#8b949e;font-family:monospace;}
        .divider{border:none;border-top:1px solid #30363d;margin:1.2rem 0;}

        .page-title { font-size: 2rem; font-weight: 700; font-family: monospace; color: #e6edf3; }
        .page-sub   { font-family: monospace; color: #8b949e; font-size: 0.9rem; margin-bottom: 1rem; }

        .cal-table { width: 100%; border-collapse: separate; border-spacing: 4px; font-family: monospace; }
        .cal-header { text-align: center; color: #8b949e; font-size: 0.8rem; padding: 6px 0; }
        .cal-day {text-align: center;vertical-align: top;width: 14.28%;border-radius: 8px;padding: 8px 4px;font-size: 0.82rem;min-height: 48px;color: #8b949e;background: #0d1117;border: 1px solid #21262d;}
        .cal-day.has-entry {color: #e6edf3;border: 1px solid #30363d;cursor: pointer;}
        .cal-day.today {border: 1px solid #00C2FF !important;color: #00C2FF !important;}
        .cal-dot {display: inline-block;width: 7px; height: 7px;border-radius: 50%;margin: 2px 1px 0;}
        .cal-month-title {font-family: monospace;font-size: 1.1rem;color: #e6edf3;margin-bottom: 0.5rem;}
        .stat-row { display: flex; gap: 1rem; margin-bottom: 1rem; }
        .stat-box {flex: 1;background: #161b22;border: 1px solid #30363d;border-radius: 10px;padding: 1rem 1.2rem;text-align: center;font-family: monospace;}
        .stat-num { font-size: 2rem; font-weight: 700; color: #00C2FF; }
        .stat-text { font-size: 0.78rem; color: #8b949e; margin-top: 2px; }
        .file-item {background: #161b22;border: 1px solid #30363d;border-left: 3px solid;border-radius: 8px;padding: 0.75rem 1rem;margin-bottom: 0.4rem;font-family: monospace;font-size: 0.88rem;color: #c9d1d9;}
        .file-item-top {display: flex;justify-content: space-between;align-items: center;margin-bottom: 0.3rem;}
        .file-title-text { font-weight: 600; }
        .file-date { color: #8b949e; font-size: 0.78rem; }
        .file-badges { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px;}
        .badge-source {font-size: 0.72rem;padding: 2px 8px;border-radius: 4px;background: #1c2d3f;color: #58a6ff;border: 1px solid #58a6ff44;text-decoration: none;}
        .badge-source:hover { border-color: #58a6ff; }
        .badge-status-solved,.badge-status-unsolved  { font-size: 0.72rem; padding: 2px 8px; }
        .badge-difficulty { font-size: 0.72rem; padding: 2px 8px;  background: #21262d; color: #8b949e; border: 1px solid #30363d; border-radius:10px;}
    </style>
""")



@st.cache_data(ttl=300)
def get_files(folder: str) -> list:
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/10_Projects/{folder}?ref={BRANCH}"
    headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
    r = requests.get(url, headers=headers, timeout=10)
    
    if r.status_code != 200:
        return []
        
    items = r.json()
    valid_items = []
    
    #  API 호출 없이 이름만으로 파싱 가능한 '대상 파일 목록'만 먼저 추려내기
    for item in items:
        if item["type"] == "file" and item["name"].endswith(".md"):
            name = item["name"].replace(".md", "")
            m = re.search(r"^(\d{4}-\d{2}-\d{2})_(.+)$", name)
            
            if m:
                try:
                    valid_items.append({
                        "date": datetime.strptime(m.group(1), "%Y-%m-%d").date(),
                        "title": m.group(2),
                        "path": item["path"],
                        "name": name
                    })
                except ValueError:
                    pass

    #  병렬 처리를 위해 각 파일의 Frontmatter를 덧붙여주는 헬퍼 함수 정의
    def fetch_meta(file_info):
        fm = get_frontmatter(file_info["path"]) 
        
        raw_diff = fm.get("difficulty", "")
        difficulty = str(raw_diff[0]).strip() if isinstance(raw_diff, list) and raw_diff else str(raw_diff).strip()
        status = str(fm.get("status", "")).strip()
        
        # 딕셔너리에 추가
        file_info["difficulty"] = difficulty
        file_info["status"] = status
        return file_info

    files = []
    if valid_items:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            files = list(executor.map(fetch_meta, valid_items))
            
    return sorted(files, key=lambda x: x['date'])

@st.cache_data(ttl=300)
def get_frontmatter(path:str)->dict:
     url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{path}?ref={BRANCH}"
     headers = {"Authorization": f"token {st.secrets['GITHUB_TOKEN']}"}
     r = requests.get(url, timeout=10,headers=headers)
     if r.status_code !=200:
         return {}
     content = base64.b64decode(r.json()["content"]).decode("utf-8")
     m = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
     if not m:
         return {}
     try:
         return yaml.safe_load(m.group(1)) or {}
     except Exception:
         return {}

    
def render_file_card(f: dict, color: str, source: str, source_url: str) -> str:
    
    difficulty=f.get("difficulty","")
    status=f.get("status","")
    
    status_badge = ""
    if status:
        if "해결" in status:
            status_badge = f"<span class='badge-status-solved'>{status}</span>"
        else:
            status_badge = f"<span class='badge-status-unsolved'>{status}</span>"
    
    diff_badge = f"<span class='badge-difficulty'>{difficulty}</span>" if difficulty else ""
    source_badge = f"<a class='badge-source' href='{source_url}' target='_blank'>🔗 {source}</a>"
    
    return f"""
    <div class='file-item' style='border-left-color:{color}; margin-top: 5px;'>
        <div class='file-item-top'>
            <span class='file-title-text'>📄 {f.get('title', '제목 없음')}</span>
            <span class='file-date'>{f['date'].strftime('%Y-%m-%d')}</span>
        </div>
        <div class='file-badges'>
            {source_badge}
            {diff_badge}
            {status_badge}
        </div>
    </div>
    """




def build_calendar_html(year:int,month:int,dated_files:dict,color:str)->str:
    cal=calendar.monthcalendar(year,month)
    today=date.today()
    days_kr = ["월", "화", "수", "목", "금", "토", "일"]
    
    html_parts=[
        f"<div class='cal-month-title'>{year}년 {month}월</div>",
        "<table class='cal-table'>",
        "<tr>"
    ]
    
    html_parts.append("".join([f"<th class='cal-header'>{d}</th>" for d in days_kr])+"</tr>")
    
    for week in cal:
        html_parts.append("<tr>")
        for day in week:
            if day==0:
                html_parts.append("<td class='cal-day'></td>")
                continue
            
            d=date(year,month,day)
            has_entry=d in dated_files
            # st.write(d,has_entry)
            
            classes=['cal-day']
            if has_entry: classes.append("has-entry")
            if d==today: classes.append("today")
            class_str=" ".join(classes)
            
            dot=f"<br/><span class='cal-dot' style='background:{color}'></span>" if has_entry else ""
            title_tip=dated_files[d]["title"] if has_entry else ""
            
            html_parts.append(f"<td class='{class_str}',title='{title_tip}'>{day}{dot}</td>")
        html_parts.append("</tr>")
    
    html_parts.append("</table>")
    
    return "".join(html_parts)

    

# 사이드
with st.sidebar:  
    st.markdown("### 👩‍💻 Kim Han Gyeong")
    st.html("<p class='sub-title'>Data Engineer</p>")
    st.html("<hr class='divider'/>")
    st.markdown("**💪 챌린지 선택!**")
    
    selected_folder=st.radio(
        label="챌린지 목록",
        options=list(CHALLENGES.keys()),
        format_func=lambda k:CHALLENGES[k]["label"],
        label_visibility="collapsed"
    )
    st.html("<hr class='divider'/>")
    st.caption("© 2026 Kim Han Gyeong")
    

# main
ch=CHALLENGES[selected_folder]
# st.write(ch)
color=ch["color"]

st.html(f"""
    <h1 class='page-title'> <i class="fa-solid fa-calendar-days" style="color: #00C2FF;"></i> Daily Challenge</h1>
    <div class='page-sub'>{ch['label']} 챌린지 학습 현황</div>
""")

st.html("<hr class='divider'/>")

with st.spinner("파일 데려오는중..🚙"):
    files=get_files(selected_folder)
    # st.write(files)
if not files:
    st.info("😅 아직 파일이 없어요..! 공부를 해보세요!")
    st.stop()

dated={f['date']: f for f in files}
total=len(files)
first_day=files[0]['date']
today=date.today()
streak=0
check = today
while check in dated:
    streak += 1
    check = check - timedelta(days=1)
# 오늘 완료 안 했으면 어제부터 체크
if streak == 0:
    check = today - timedelta(days=1)
    while check in dated:
        streak += 1
        check = check - timedelta(days=1)

    
st.html(f"""
    <div class='stat-row' role='group' aria-labe='챌린지 통계'>
        <div class='stat-box'>
            <div class='stat-num' style='color:{color};'>{total}</div>
            <div class='sata-text'>총 완료</div>
        </div>
        <div class='stat-box'>
            <div class='stat-num' style='color:{color};'>{streak}</div>
            <div class='sata-text'>연속 일수</div>
        </div>
        <div class='stat-box'>
            <div class='stat-num' style='color:{color};'>{first_day.strftime('%m/%d')}</div>
            <div class='sata-text'>시작일</div>
        </div>
        <div class='stat-box'>
            <div class='stat-num' style='color:{color};'>{files[-1]['date'].strftime('%m/%d')}</div>
            <div class='sata-text'>최근 완료</div>
        </div>

    </div>""")

st.html("<hr class='divider'/>")

# 캘린더 + 파일목록
tab_cal,tab_list=st.tabs(["캘린더","목록"])
with tab_cal:
    months_available=sorted(set((f['date'].year,f['date'].month) for f in files),reverse=True)
    # st.write(months_available)
    month_labels=[f"{y}년 {m}월" for y,m in months_available]
    selected_month_idx=st.selectbox("월 선택",options=range(len(month_labels)),format_func=lambda i:month_labels[i],index=None,placeholder='월 선택 해주세요~')
    
    if selected_month_idx is None:
        st.info("월을 선택해줘야 합니다")
        st.stop()
    sel_year,sel_month=months_available[selected_month_idx]
    # st.write(sel_year,sel_month)
    
    month_dated={d:f for d, f in dated.items() if d.year==sel_year and d.month==sel_month}
    
    cal_html=build_calendar_html(sel_year,sel_month,month_dated,color)
    st.html(cal_html)
    
    month_files=[f for f in files if f["date"].year ==sel_year and f["date"].month==sel_month]
    if month_files:
        st.html("<br/>")
        st.markdown(f"**{sel_month}월 완료 목록** ({len(month_files)}개)")
        # st.write(month_files)
        for f in reversed(month_files):
            st.html(render_file_card(f,color,ch["source"],ch["source_url"]))
            
with tab_list:
    st.markdown(f"**전체 {total}개**")
    
    available_diffs=sorted(list(set(f["difficulty"] for f in files if f["difficulty"])))
    
    col1,col2=st.columns([6,4])
    with col1:
        search=st.text_input("🔎 제목 검색", placeholder='찾고싶은 제목을 입력하세요~!',key='challenge_search')
    with col2:
        selected_diffs=st.multiselect("난이도 검색 필터",options=available_diffs,placeholder='난이도 검색')
    
    filtered=list(reversed(files))
    
    if search:
        filtered=[f for f in filtered if search.lower() in f["title"].lower()]
    if selected_diffs:
        filtered=[f for f in filtered if f["difficulty"] in selected_diffs]
        
    if not filtered:
        st.info("검색 조건에 맞는 챌린지가 없습니다. 😅")
    else:
        for f in filtered:
            st.html(render_file_card(f,color,ch["source"],ch["source_url"]))     