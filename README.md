# Dokuemntasi

Projek microservice menggunakan pyhton dan database postgresql, dibuat untuk memenuhi tugas UAS Mata Kuliah PLSQL

Kelompok 12:

- Muhammad Iqbal Ilham Rahayu ( 220401010108 )

Postman Export: [api.postman_collection.json](https://github.com/x-bal/uas_microservice_api_crud_plsql_unsia/UAS_PLSQL.postman_collection.json)

## Instalasi Projek

### Clone Projek

1. Clone the project with this command:

```
git clone https://github.com/x-bal/uas_microservice_api_crud_plsql_unsia.git
```

### Buka project di Visual Studio Code

### Install semua requirement.

Gunakan perintah berikut:

```
pip install -r requirements.txt
```

### Setup Database:

Buka file app.py

```
conn = psycopg2.connect(
    database="uas_plsql",
    user="postgres",
    password="root",
    host="127.0.0.1",
    port="5432"
)
```

Ubah isi `database`, `user`, dan `password` dengan data yang ada pada server Anda.

## REST API Endpoints

Endpoints yang tidak perlu login:

```
1. POST /login
```

Endpoints yang perlu login:

```
3. GET /users
4. GET /users/<int:id>
6. POST /users
7. PATCH/PUT /users/<int:id>
8. DELETE /users/<int:id>
5. GET /logout
```

### Rest Api Resource

POST http://127.0.0.1:5000/login
Request Body :

```
{
    "username" : "developer",
    "password" : "secret"
}
```

Response :

```
{
    "status": "Login successful",
    "user": [
        "developer",
        "admin"
    ]
}
```

GET http://127.0.0.1:5000/users
Request Body :

```

```

Response :

```
{
    "data": [
        {
            "id": 4,
            "name": "Test User",
            "password": "\\x4c664a7a4465724654554b784243715a7666482d59773d3d",
            "role": null,
            "username": "test"
        },
        {
            "id": 1,
            "name": "Developer Update Lagi",
            "password": "secret",
            "role": "admin",
            "username": "developer"
        }
    ]
}
```

POST http://127.0.0.1:5000/users
Request Body :

```
{
    "username" : "test.user.1",
    "name" : "Test User 1",
    "password" : "secret",
    "role" : "admin"
}
```

Response :

```
{
    "status": "Data berhasil ditambahkan"
}
```

PUT/PATCH http://127.0.0.1:5000/users/1
Request Body :

```
{
    "name" : "Test User 1",
}
```

Response :

```
{
    "status": "Data berhasil diupdate"
}
```

DELETE http://127.0.0.1:5000/users/1
Request Body :

```
-
```

Response :

```
{
    "status": "Data berhasil didelete"
}
```

### TRIGGER LOG

Trigger akan menyimpan semua log perubahan pada data users

1. Buat table user_logs

```
CREATE TABLE user_log (
    id SERIAL PRIMARY KEY AUTO INCREMENT,
    event_type VARCHAR(10),
    event_time TIMESTAMP,
    username VARCHAR(50),
    event_desc VARCHAR(255)
);
```

2. Buat Function log_user_trigger

```
CREATE OR REPLACE FUNCTION public.log_user_trigger()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_logs (event_type, event_time, username, event_desc)
        VALUES ('INSERT', NOW(), NEW.username, 'User added');
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_logs (event_type, event_time, username, event_desc)
        VALUES ('UPDATE', NOW(), NEW.username, 'User updated');
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO user_logs (event_type, event_time, username, event_desc)
        VALUES ('DELETE', NOW(), OLD.username, 'User deleted');
    END IF;
    RETURN NEW;
END;
$function$;
```

3. Buat Trigger yang menghubungkan function dengan table users

```
create trigger trigger after
insert
    or
delete
    or
update
    on
    public.users for each row execute function log_user_trigger()
```

## Testing

1. REST API
   Untuk pengetesan gunakan [Postman](https://www.postman.com/).

2. Screenshoot table users dan user_logs
   Table users
   [image](https://github.com/x-bal/uas_microservice_api_crud_plsql_unsia/table_users.png)

   Table user_logs
   [image](https://github.com/x-bal/uas_microservice_api_crud_plsql_unsia/table_user_logs.png)
