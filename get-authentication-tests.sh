docker build -t heyimjustalex/authentication-ms ./backend/authentication-ms/
docker build -t heyimjustalex/orders-ms ./backend/orders-ms/
docker build -t heyimjustalex/products-ms ./backend/products-ms/

docker push heyimjustalex/authentication-ms
docker push heyimjustalex/orders-ms
docker push heyimjustalex/products-ms