tail [options] [file...]

# f1.txt
hello world
hello world1
hello world1

# f2.txt
hello world
hello world2
hello world1

tail -n 2 f1.txt
# hello world1
# hello world1

# follow the logs only while a specific process (PID 1234) is active
tail -f --pid=1234 logfile.log
