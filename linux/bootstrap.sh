#!/bin/bash

echo "Starting Linux Docker Container..."

# SSH 시작
service ssh start

# cron 시작
service cron start

# locate DB 생성
updatedb

# 컨테이너 종료 방지
tail -f /dev/null
