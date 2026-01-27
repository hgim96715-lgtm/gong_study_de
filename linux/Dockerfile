FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# [기본 패키지 설치] 
RUN apt-get update && apt-get install -y \
    openssh-server sudo systemd systemd-sysv cron \
    vim net-tools iputils-ping curl wget man-db plocate dumb-init \
    && apt-get clean

# [유저 생성 및 권한 부여] 
RUN useradd -m -s /bin/bash ubuntu && \
    echo 'ubuntu:ubuntu' | chpasswd && \
    adduser ubuntu sudo

# [시스템 설정] 
RUN mkdir /var/run/sshd
RUN echo 'root:root' | chpasswd

# [파일 복사 및 권한 설정]  
COPY bootstrap.sh /root/bootstrap.sh
RUN chmod +x /root/bootstrap.sh

# [볼륨 및 포트 설정]
VOLUME ["/sys/fs/cgroup"]
EXPOSE 22

# [유저 전환] 
USER ubuntu
WORKDIR /home/ubuntu

# [실행]
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["sudo", "/root/bootstrap.sh"] 
