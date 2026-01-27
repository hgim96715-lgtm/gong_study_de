head [options] [file...]

# f1.txt
hello world
hello world1
hello world1

# f2.txt
hello world
hello world2
hello world1

head -n 2 f1.txt
# hello world
# hello world1

head f1.txt f2.txt
# ==> f1.txt <==
# hello world
# hello world1
# hello world1

# ==> f2.txt <==
# hello world
# hello world2
# hello world1

head -q f1.txt f2.txt
# hello world
# hello world1
# hello world1
# hello world
# hello world2
# hello world1
