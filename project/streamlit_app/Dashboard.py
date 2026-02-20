import streamlit as st
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import pandas as pd
import time
from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import plotly.express as px

load_dotenv()

st.set_page_config(
    page_title="Data PipeLine",
    page_icon="✅",
    layout="wide"
)

st.title("Kafka Dashboard")
st.divider()


# layout
m1,m2,m3,m4=st.columns(4)
with m1:
    st.info("총 주문건수")
    data_total_count=st.empty()
with m2:
    st.info("최근 주문금액")
    data_last_value=st.empty()
with m3:
    st.info("최근 카테고리")
    data_category_status=st.empty()
with m4:
    data_connect_status=st.empty()

st.divider()


category_table_slot=st.empty()

st.markdown("### Streaming Data & Logs")


col_chart,col_log=st.columns([2,1])
with col_chart:
    st.caption("Chart")
    chart_placeholder=st.empty()
with col_log:
    st.caption("Data Log(실시간)")
    log_placeholder=st.empty()
    

st.divider()

db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)


st.subheader("Spark Batch Analysis")
db_report_col1,db_report_col2=st.columns(2)

with db_report_col1:
    st.caption("카테고리별 누적 집계")
    db_table_slot=st.empty()
    data_db_sales = st.empty()
    
with db_report_col2:
    db_chart_slot=st.empty()
    
try:
    df_db = pd.read_sql("SELECT * FROM report_category_sales", engine)
    total_db_sales = df_db['total_sales'].sum()
    data_db_sales.metric("총 매출액", f"{int(total_db_sales):,}원")
    db_table_slot.dataframe(df_db, use_container_width=True, hide_index=True)
    fig=px.bar(
        df_db,
        x="category",
        y="total_sales",
        title="카테고리별 매출",
        color="category",
        text="total_sales"
    )
    fig.update_traces(texttemplate='%{text:,}')
    fig.update_layout(showlegend=True, xaxis_title="카테고리", yaxis_title="매출액")
    db_chart_slot.plotly_chart(fig, use_container_width=True)
except Exception as e:
    db_table_slot.warning(f"DB 에러: {e}")
    

st.divider()
st.subheader("PyFlink 1분마다 집계 하는 현황판")
flink_col1,flink_col2=st.columns(2)

with flink_col1:
    st.caption("최근 1분 카테고리별 매출 (sales_aggregation 테이블)")
    flink_table_slot=st.empty()
    
with flink_col2:
    flink_chart_slot=st.empty()
    
    






# kafka Consumer
try:
    consumer=KafkaConsumer(
        'user-log',
        bootstrap_servers=['localhost:29092'],
        auto_offset_reset='latest',
        value_deserializer=lambda x:json.loads(x.decode('utf-8')),
        consumer_timeout_ms=1000
    )
    data_connect_status.success("Kafka랑 연결되었다")
except NoBrokersAvailable:
    st.error(" Broker Unavailable. Kafka가 꺼져 있나요?")
    st.stop()
    
except Exception as e:
    st.error(f"Error! {e}")
    st.stop()
    
# 데이터 수집

if "user_logs" not in st.session_state:
    st.session_state.user_logs=[]
    
total_count=0

loop_count=0

if st.sidebar.button("모니터링 그만하고 싶다면 클릭"):
    Path(".stop_signal").write_text("stop",encoding="utf-8")
    st.toast("종료버튼 클릭했습니다.")
    # st.success("producer에게 종료신호를 보냅니다.")
    st.stop()

for message in consumer:
    row=message.value
    # data_connect_status.success(f"데이터 수신 중! 마지막 ID: {row['order_id'][:8]}...")
    st.session_state.user_logs.append(row)
    total_count+=1
    loop_count+=1
    
    if len(st.session_state.user_logs)>100:
        st.session_state.user_logs.pop(0)
        
    df=pd.DataFrame(st.session_state.user_logs)
    
    data_total_count.metric(label="Total Message",value=total_count)
    

    data_last_value.metric(label="마지막 금액",value=f"{int(row['total_amount']):,}원")
    data_category_status.metric(label="최근 카테고리",value=row['category'])
    data_connect_status.success(f"연결됨: {row['order_id'][:8]}...")
    
    
    # df_summary=df.groupby('category')['order_id'].count().reset_index()
    # df_summary.columns=['카테고리','현재 주문 건수']
    # category_table_slot.dataframe(df_summary,use_container_width=True)
    
    df_summary=(
        df
        .groupby('category')
        .agg(건수=('order_id','count'),매출액=('total_amount','sum'))
    ).reset_index()
    
    df_summary['매출액']=df_summary['매출액'].apply(lambda x:f"{int(x):,}원")
    category_table_slot.dataframe(df_summary,use_container_width=True,hide_index=True)
    
    
    numeric_cols=df.select_dtypes(include=['number']).columns
    
    
    if not df.empty and len(numeric_cols)>0:
        chart_placeholder.line_chart(df[[numeric_cols[0]]])
        
    log_placeholder.dataframe(df.tail(10).iloc[::-1],use_container_width=True)
    
    #==========새로 추가된 부분 PyFlink==================# 
    if loop_count% 20==0:
        try:
            flink_query="""
                SELECT category,total_sales,total_orders,window_end
                FROM sales_aggregation
                WHERE window_end=(SELECT MAX(window_end) FROM sales_aggregation)
                ORDER BY total_sales DESC
            """
            df_flink=pd.read_sql(flink_query,engine)
        
            if not df_flink.empty:
                flink_table_slot.dataframe(df_flink,use_container_width=True,hide_index=True)
                
                latest_time=df_flink['window_end'].iloc[0].strftime('%H:%M:%S')
                fig_flink=px.pie(
                    df_flink,
                    names='category',
                    values='total_sales',
                    title=f"최근 1분 매출 비율 ({latest_time}기준)",
                    hole=0.4,
                    color='category'
                )
                flink_chart_slot.plotly_chart(fig_flink,use_container_width=True,key=f"flink_pie_{loop_count}")
        
        except Exception as e:
            flink_table_slot.warning(f"Flink대기중...{e}")
    
    time.sleep(0.05)
        