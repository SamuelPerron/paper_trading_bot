# Llama, a broker mock

## Installation
1. **Build docker environnment**

    `docker-compose up --build`
2. **Create database** 

    `docker exec -it llama_db_1 psql -Upostgres -c "CREATE DATABASE llama;"`
3. **Run migrations**

    `docker exec -it llama_api_1 flask db upgrade`