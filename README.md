# SocialMedia Statistics API

## How to run
### Docker
1. Create config file `.env` in root of project. You can copy this from file `.env.example` with default values or set your values.
2. Run it with docker-compose: `sudo docker-compose up -d`
4. Now server is running on port 8000
5. For run tests use command: ` sudo docker exec -t -i social_statistics_api_django_1 python manage.py test`

### Without docker
1. You need use postgreSQL on your machine and configure it. On your psql create db and user:    
    - `CREATE DATABASE database_name_db;`.
    - `CREATE USER username WITH password 'password';`.
    - `GRANT ALL ON DATABASE database_name_db TO username;`.
    - `ALTER USER username CREATEDB;`.
2. Create config file `.env` in root of project. You can copy this from file `.env.example` with default values or set your values.
4. Install requirements in your environment: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Start application: `python manage.py runserver`
7. Now server is running on port 8000
5. For run tests use command: ` python manage.py test`

## Endpoints
- `http://localhost:8000/posts_statistics/` - Create post statistic object. 
Send POST request with data for example: 
        `{
                'user_id': '1',
                'post_id': '2',
                'likes_count': -100
        }`
- `http://localhost:8000/posts_statistics/posts/{POST_ID}/latest/` - Get latest statistics for a specific post id
- `http://localhost:8000/posts_statistics/users/{USER_ID}/latest/` - Get latest statistics for all posts of a specific user id
- `http://localhost:8000/posts_statistics/users/{USER_ID}/average/` - Get average number of likes per day for a specific user id for the last 30 days.
