FROM ubuntu:latest
RUN apt update
RUN apt install wget -y
RUN wget https://github.com/natohutch/floodaware/raw/server-backup/floodawaredb.sql

FROM postgis/postgis
COPY --from=0 /floodawaredb.sql /floodawaredb.sql
#RUN psql -U postgres -c "create database floodaware"
#RUN pg_restore -U postgres -d floodaware -cC floodawaredb.sql
#CMD psql -U postgres -c "create database floodaware"