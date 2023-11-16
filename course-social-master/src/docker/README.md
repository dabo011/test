$ docker run -d \
    --name social-mysql \
    -p 3306:3306 \
    -v mysql-data:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=socialpassword \
    -e MYSQL_DATABASE=socialdb \
    -e MYSQL_USER=social \
    -e MYSQL_PASSWORD=socialpassword \
    mysql:5.7

$ docker exec -it <container_id> bash
# mysql -u social -p
Enter password:
>

$ mysql -u social -p
Enter password:
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)

$ mysql --protocol=tcp -u social -p
> use socialdb;
> create table news_articles (pub_date date, publisher tinytext, title tinytext, contents text); 


$ docker rm <container_id>
$ docker contaniner prune
$ docker volume rm <volume_name>