docker stop psql-server
docker stop middleware
docker rm -f psql-server
docker rm -f middleware
docker create -v /dbdata --name dbdata psql-server /bin/true
docker run --volumes-from dbdata  --name psql-server -e POSTGRES_PASSWORD=pass -d psql-server
docker run -it -p 5000:5001 --link psql-server:postgres  -v /host/:/code/ middleware

#docker run -d psql-server 
#docker run -it -p 82:5000 -v /host/:/code/ middleware