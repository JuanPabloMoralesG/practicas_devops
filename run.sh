docker-compose down python-api
docker-compose down mongodb

docker-compose up --build -d mongodb
docker-compose up --build -d python-api