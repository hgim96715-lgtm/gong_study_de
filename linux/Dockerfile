FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

# 기본 패키지
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    systemd \
    systemd-sysv \
    cron \
    vim \
    net-tools \
    iputils-ping \
    curl \
    wget \
    man-db \
    plocate \
    dumb-init \
    && apt-get clean

# SSH 설정
RUN mkdir /var/run/sshd

# root 비밀번호 설정 (실습용)
RUN echo 'root:root' | chpasswd

# systemd 최소 동작용
VOLUME ["/sys/fs/cgroup"]

# bootstrap 스크립트 복사
COPY bootstrap.sh /root/bootstrap.sh
RUN chmod +x /root/bootstrap.sh

EXPOSE 22

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/root/bootstrap.sh"]
