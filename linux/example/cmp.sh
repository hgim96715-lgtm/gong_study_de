cmp [options] file1 file2

# f1.txt
hello world
hello world1
hello world1

# f2.txt
hello world
hello world2
hello world1

cmp f1.txt f2.txt
# f1.txt f2.txt differ: char 24, line 2

# 결과(Exit Code) 확인
echo $?
# 1 (다름), 0 (같음), 2 (오류)


cmp -l f1.txt f2.txt
# 24  61  62

cmp -b f1.txt f2.txt
# f1.txt f2.txt differ: byte 24, line 2 is  61 1  62 2
