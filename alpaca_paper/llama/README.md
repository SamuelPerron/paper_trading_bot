# Llama, a broker mock

## Installation
1. **Build docker environnment**

    `docker-compose up --build`
2. **Create databases** 

    `docker exec -it llama_db_1 psql -Upostgres -c "CREATE DATABASE llama;"`
    
    `docker exec -it llama_db_1 psql -Upostgres -c "CREATE DATABASE test_llama;"`
3. **Run migrations**

    `docker exec -it llama_api_1 flask db upgrade`

## Tests
https://pythonhosted.org/Flask-Testing/

**Running tests**

`docker exec -it llama_api_1 pytest`

## Migrations
https://flask-migrate.readthedocs.io/en/latest/index.html

**Creating migrations**

`docker exec -it llama_api_1 flask db migrate`

**Running migrations**

`docker exec -it llama_api_1 flask db upgrade`