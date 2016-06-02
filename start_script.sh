docker stop psql-server
docker stop middleware
docker rm -f psql-server
docker rm -f middleware

docker create -v /dbdata --name dbdata1 psql-server /bin/true
docker run  --volumes-from dbdata1  --name psql-server -e POSTGRES_PASSWORD=pass -d smani6/psql-server

#docker  run -v /host/ver1/pgdata/:/var/pgdata  -v /host/:/host/ --name psql-server -e POSTGRES_PASSWORD=pass -d smani6/psql-server
docker run -it -p 5000:5000 --link psql-server:postgres  --name middleware -v /host/:/code/ smani6/middleware
 

#docker run -d psql-server 
#docker run -it -p 82:5000 -v /host/:/code/ middleware