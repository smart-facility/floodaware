docker exec -ti floodaware_db_1 bash -c "\
psql -U postgres -c 'DROP DATABASE floodaware' &&\
psql -U postgres -c 'CREATE DATABASE floodaware' &&\
pg_restore -U postgres -d floodaware -cC floodawaredb.sql &&\
exit
"
echo initialised and restored database