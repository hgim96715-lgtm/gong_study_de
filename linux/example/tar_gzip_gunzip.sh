echo hello > file1.txt
echo world > file2.txt

# tar
tar -cvf archive.tar file1.txt file2.txt
tar -czvf archive.tar.gz file1.txt file2.txt
tar -xzvf archive.tar.gz

# archive.tar.gz 안에 뭐 들었는지 리스트만 보기
tar -tf archive.tar.gz

# gzip
gzip file.txt
gzip file1.txt file2.txt

# gunzip
gunzip file.txt.gz
gunzip file1.txt.gz file2.txt.gz

