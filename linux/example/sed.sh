# file.txt context
```
hello world hello world
hello world
delete me
apple is so sweet

insert_here

Apple
```

#  첫번째 "hello"를 "world"로 바꾸기
sed 's/hello/world/' file.txt

# 모든 "hello"를 "world"로 바꾸기
sed 's/hello/world/g' file.txt

# "delete me"가 포함된 줄 삭제
sed '/delete me/d' file.txt

# 파일을 직접 수정 (in-place) 하여 모든 "apple"을 "orange"로 바꾸기
sed -i 's/apple/orange/g' file.txt

#  "apple"을 "orange"로 바꾸고, 바뀐 줄만  조용히 출력하기
sed -n 's/apple/orange/p' file.txt

# 3번째 줄부터 마지막 줄까지 삭제 -> 1~2번째 줄만 남김
sed '3,$ d' file.txt

# -a : 뒤에 추가 
# insert_here라는 단어가 포함된 줄 다음 줄에 "New Line" 추가
sed '/insert_here/a New Line' file.txt

# -i : 앞에 삽입
# insert_here라는 단어가 포함된 줄 이전 줄에 "New Line before" 추가
sed '/insert_here/i New Line before' file.txt

# -e : 여러 명령 한 번에 실행
# 여러 sed 명령어를 한 번에 실행. 이 예제는 "apple"을 "orange"로 바꾸고 "delete me"가 포함된 줄을 삭제합니다.
sed -e 's/apple/orange/g' -e '/delete me/d' file.txt

# 특정 줄 범위 내에서 작업 수행. 이 예제는 첫 번째 줄부터 세 번째 줄까지 삭제합니다.
sed '1,3d' file.txt

# gI : 대소문자 구분 없이 모든 "apple"을 "orange"로 바꾸기
sed 's/apple/orange/gI' file.txt
