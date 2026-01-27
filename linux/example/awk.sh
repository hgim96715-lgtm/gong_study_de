# file1.txt
```
Harry	10	30
Key	15	1
Sally	30	20
Admin	39	40
```

# file.csv
```
a,1,2
b,2,3
c,3,4
d,4,5
```
# timestamps.txt
```
1714624931
```


# $1: 첫 번째 칸, $2: 두 번째 칸 ... $0: 전체 줄
awk '{print $1, $3}' file1.txt


awk '{sum += $2} END {print sum}' file1.txt


awk '$2 > 20' file1.txt


awk '{printf "Name: %s, Age: %d\n", $1, $2}' file1.txt

# Admin이라는 단어가 포함된 줄 출력 
awk '/Admin/ {print $0}' file1.txt

# 2번째 컬럼의 합계 과 평균 출력
awk '{total += $2; count++} END {print "Average:", total/count}' file1.txt

# 콤마로 구분된 csv 파일에서 첫 번째 컬럼 출력
awk -F, '{print $1}' file.csv

# OFS 출력 구분자 
echo "a b c" | awk '{ OFS = ","; print $1, $2, $3 }'
# a,b,c

# NR 줄 번호 같이 찍기 
echo -e "line 1\nline 2\nline 3" | awk '{ print NR, $0 }'
1 line 1
2 line 2
3 line 3


awk '{total += $2; count++} END {print "Total:", total; print "Average:", total/count}' file1.txt


threshold=20 && awk -v thresh="$threshold" '$2 > thresh {print $0}' file1.txt


awk '$2 > 20 {print $0}' file1.txt > temp.txt && mv temp.txt file1.txt


awk '{names[$1]++} END {for (name in names) print name, names[name]}' file1.txt


awk '{print strftime("%Y-%m-%d %H:%M:%S", $1)}' timestamps.txt
