docker build -t news_server -f Dockerfile . --build-arg MODE=prod

docker tag news_server:latest qimo/news_server:latest