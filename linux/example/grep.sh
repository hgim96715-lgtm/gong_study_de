# grep [options] pattern [file...]
grep "apple" fruits.txt

# fruits.txt
apple
orange
melon
apples
Apple


# -i: 대소문자 구분 없이 검색합니다.
grep -i "apple" fruits.txt

# -v: 해당 패턴과 일치하지 않는 라인을 출력합니다.
grep -v "apple" fruits.txt

# -r or -R: 하위 디렉토리를 재귀적으로 검색합니다.
grep -r "apple" /path/to/directory

# -l: 해당 패턴을 포함하는 파일 이름만 출력합니다.
grep -l "apple" /path/to/directory/*

# -n: 해당 패턴이 포함된 라인 번호를 함께 출력합니다.
grep -n "apple" fruits.txt

# -c: 해당 패턴이 포함된 라인의 개수를 출력합니다.
grep -c "apple" fruits.txt

# using pipe
cat fruits.txt | grep "apple"


# 정규 표현식 사용 예제

#server.log
```text
2026-01-26 09:00:01 INFO  Server started successfully
2026-01-26 09:01:12 INFO  User admin logged in
2026-01-26 09:02:45 WARN  Disk usage at 85%
2026-01-26 09:03:10 ERROR Failed to connect to database
2026-01-26 09:03:11 INFO  Retrying database connection
2026-01-26 09:03:15 ERROR Connection timeout
2026-01-26 09:04:00 INFO  Database connection established
2026-01-26 09:05:22 INFO  File upload completed
2026-01-26 09:06:30 FAIL Authentication failed for user guest
2026-01-26 09:07:45 INFO  User admin logged out
2026-01-26 09:08:10 ERROR Failed to write to log file
2026-01-26 09:09:00 INFO  Server shutdown initiated
```


# "Error" 또는 "Fail" 이 포함된 라인을 server.log 파일에서 찾기
# 대소문자 구분없이 검색
grep -iE "error|fail" server.log