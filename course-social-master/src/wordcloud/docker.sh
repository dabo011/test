docker network create wordcloud-app

docker run -d \
    --network wordcloud-app --network-alias mysql \
    -v wordcloud-mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=secret \
    -e MYSQL_DATABASE=wordcloud \
    mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci


docker run -d \
  -w /app -v "$(pwd):/app" \
  --network wordcloud-app \
  -e MYSQL_HOST=mysql \
  -e MYSQL_USER=root \
  -e MYSQL_PASSWORD=secret \
  -e MYSQL_DB=wordcloud \
  python:3.7-buster \
  sh -c "python crawler.py"
