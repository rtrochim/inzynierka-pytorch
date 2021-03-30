FROM ubuntu:18.04

RUN apt update && apt -y install python gnubg

WORKDIR /usr/src/app

COPY app/gnubg/server.py .

EXPOSE 8001

CMD ["/usr/games/gnubg","-t","-p", "server.py"]