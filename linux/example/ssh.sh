# Docker 로 가짜 SSH 서버를 실행하는 예제 스크립트

$ docker run -d -p 2223:22 --name ssh-lab rastasheep/ubuntu-sshd



# SSH 키 생성
ssh-keygen -t rsa -f ~/.ssh/lab_key


# key 등록
ssh-copy-id -p 2223 -i ~/.ssh/lab_key.pub root@localhost

# SSH 접속
ssh -i ~/.ssh/lab_key -p 2223 root@localhost

# scp 파일 전송
scp -P 2223 -i ~/.ssh/lab_key test.txt root@localhost:/root/


