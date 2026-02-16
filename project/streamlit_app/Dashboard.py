import streamlit as st
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
import json
import pandas as pd
import time
from pathlib import Path

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

st.subheader("카테고리별 실시간 통계")
category_table_slot=st.empty()

st.markdown("### Streaming Data & Logs")


col_chart,col_log=st.columns([2,1])
with col_chart:
    st.caption("Chart")
    chart_placeholder=st.empty()
with col_log:
    st.caption("Data Log(실시간)")
    log_placeholder=st.empty()




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
    
    time.sleep(0.05)
        