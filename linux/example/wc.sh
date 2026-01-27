# file.txt
hello world hello world
hello world
delete me
apple is so sweet

insert_here

Apple

# file1.txt
hello world


# wc file.txt 결과는 [줄 수][단어 수][용량][파일명] 순서

$ wc file.txt
# 8 14 82 file.txt
# 8 Lines : 엔터키를 8번 쳤으므로 8줄
# 14 Words : 띄어쓰기로 구분된 단어 덩어리가 14개
# 82 Bytes : 파일의 전체 용량이 82바이트

# 파일을 여러개 나열하면, 각각의 통계를 보여주고 , 마지막에 합계를 구해준다.
$ wc file.txt file1.txt
# 8 14 82 file.txt
# 1  2 12 file1.txt
# 9 16 94 total

# 파이프라인으로 전달된 데이터의 통계도 구할 수 있다.
$ echo "hello world" | wc
      1       2      12

# 옵션으로 하나만 , 몇줄인지
$ wc -l file.txt
# 8 file.txt