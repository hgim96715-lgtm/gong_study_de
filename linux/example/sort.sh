sort [options] [file...]

# s1.txt
1,c
30,a
20,z
11,b
12,s
15,k
24,l

sort -n s1.txt
# 1,c
# 11,b
# 12,s
# 15,k
# 20,z
# 24,l
# 30,a

sort -r -n s1.txt
# 30,a
# 24,l
# 20,z
# 15,k
# 12,s
# 11,b
# 1,c

# -t : 이 파일은 쉼표로 구분되어있다고 알려주는 것 
sort -t, -k2 s1.txt
# 30,a
# 11,b
# 1,c
# 15,k
# 24,l
# 12,s
# 20,z


# s2.txt (|)
1 | c
30 | a
20 | z
11 | b
12 | s
15 | k
24 | l

sort -t'|' -k2 s2.txt
# 30 | a
# 11 | b
# 1 | c
# 15 | k
# 24 | l
# 12 | s
# 20 | z    

sort -t'|' -k2 -r s2.txt
# 20 | z
# 12 | s 
# 24 | l
# 15 | k
# 1 | c
# 11 | b
# 30 | a


sort -n s2.txt
# 1 | c
# 11 | b
# 12 | s
# 15 | k
# 20 | z
# 24 | l
# 30 | a

sort -nr s2.txt
# 30 | a
# 24 | l
# 20 | z
# 15 | k
# 12 | s
# 11 | b
# 1 | c