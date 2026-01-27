diff file1.txt file2.txt

# f1.txt
hello world
hello world1
hello world1

# f2.txt
hello world
hello world2
hello world1


diff f1.txt f2.txt
# 2c2 # 2번째 줄이 다름
# < hello world1 <: 왼쪽 내용 파일
# ---
# > hello world2  >: 오른쪽 내용 파일


diff -u f1.txt f2.txt
# --- f1.txt	2024-05-09 04:41:52.850359012 +0000
# +++ f2.txt	2024-05-09 04:33:01.133867002 +0000
# @@ -1,3 +1,3 @@
#  hello world
# -hello world1
# +hello world2
#  hello world1