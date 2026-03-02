docker network create proxy

cd ..

mkdir postgres_data

docker-compose up -d

cd build-scripts

docker network inspect proxy