# 특정 필드 값만 추출
echo '{"name": "John", "age": 30}' | jq '.name'
# "John"

# 배열 데이터 필터링
echo '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]' | jq '.[].name'
# "John"
# "Jane"

# JSON 데이터 수정
echo '{"name": "John", "age": 30}' | jq '.age = 31'
# {
#   "name": "John",
#   "age": 31
# }

# JSON 데이터 재구성
echo '[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]' | jq '[{name: .[].name}]'

# JSON 데이터 예쁘게 출력
echo '{"name": "John", "age": 30}' | jq .
# {
#   "name": "John",
#   "age": 30
# }

# -r 옵션을 사용하여 Raw 출력
echo '{"name": "Alice", "age": 25}' | jq -r '.name'
# Alice

# -s 옵션을 사용하여 Slurp 모드
echo '{"name": "Alice"}' > file1.json
echo '{"name": "Bob"}' > file2.json
jq -s '.' file1.json file2.json
# [
#   {
#     "name": "Alice"
#   },
#   {
#     "name": "Bob"
#   }
# ]

# -c 옵션을 사용해서 한줄로 압축해서 출력 
echo '{"name": "Alice", "age": 25}' | jq -c '.'
# {"name":"Alice","age":25}

# -M 옵션을 사용해서 색상 출력을 비활성화 , 로그 파일로 저장하거나 파이프로 전달할 때 유용
echo '{"name": "Alice", "age": 25}' | jq -M '.'
# {
#   "name": "Alice",
#   "age": 25
# }