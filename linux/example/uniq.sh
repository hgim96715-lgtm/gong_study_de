uniq [options] [input_file] [output_file]

# u1.txt
1
1
2
3
3
4
5
6
6

# 빈도수 세기
uniq -c u1.txt
#   2 1
#   1 2
#   2 3
#   1 4
#   1 5
#   2 6

# 중복된 라인만 출력
uniq -d u1.txt
# 1
# 3
# 6

# 중복되지 않은 라인만 출력
uniq -u u1.txt
# 2
# 4
# 5

# sort 명령어와 함께 사용

sort u1.txt | uniq

sort u1.txt | uniq -c