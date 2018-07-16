from golang:1.9-stretch

RUN apt-get update && apt-get install -y \
    postgresql

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

RUN pip3 install \
    nose-exclude \
    sqlalchemy \
    testing.postgresql
RUN pip3 install click psycopg2-binary
RUN pip3 install numpy scipy 
RUN pip install -U git+git://github.com/heschao/craniutil.git
RUN go get github.com/bemasher/rtlamr

RUN adduser --disabled-password --gecos '' amr
USER amr
