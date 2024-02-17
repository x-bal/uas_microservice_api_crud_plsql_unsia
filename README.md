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
2. Buka project di Visual Studio Code

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

## REST API Resources

{
"info": {
"\_postman_id": "e57cd0ec-4f79-40c6-ae17-0fadfdb6cdd3",
"name": "UAS PLSQL",
"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
"\_exporter_id": "11627091"
},
"item": [
{
"name": "Login",
"request": {
"method": "POST",
"header": [],
"body": {
"mode": "raw",
"raw": "{\r\n \"username\" : \"developer\",\r\n \"password\" : \"secret\"\r\n}",
"options": {
"raw": {
"language": "json"
}
}
},
"url": {
"raw": "http://127.0.0.1:5000/login",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"login"
]
}
},
"response": []
},
{
"name": "Get Users",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "http://127.0.0.1:5000/users",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"users"
]
}
},
"response": []
},
{
"name": "Create User",
"request": {
"method": "POST",
"header": [],
"body": {
"mode": "raw",
"raw": "{\r\n \"username\" : \"test.user.1\",\r\n \"name\" : \"Test User 1\",\r\n \"password\" : \"secret\"\r\n}",
"options": {
"raw": {
"language": "json"
}
}
},
"url": {
"raw": "http://127.0.0.1:5000/users",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"users"
]
}
},
"response": []
},
{
"name": "Get User",
"request": {
"method": "GET",
"header": [],
"url": {
"raw": "http://127.0.0.1:5000/users/1",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"users",
"1"
]
}
},
"response": []
},
{
"name": "Update User",
"request": {
"method": "PUT",
"header": [],
"body": {
"mode": "raw",
"raw": "{\r\n \"name\" : \"Developer Update Lagi\",\r\n \"password\" : \"secret\"\r\n}",
"options": {
"raw": {
"language": "json"
}
}
},
"url": {
"raw": "http://127.0.0.1:5000/users/2",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"users",
"2"
]
}
},
"response": []
},
{
"name": "Delete User",
"request": {
"method": "DELETE",
"header": [],
"url": {
"raw": "http://127.0.0.1:5000/users/4",
"protocol": "http",
"host": [
"127",
"0",
"0",
"1"
],
"port": "5000",
"path": [
"users",
"4"
]
}
},
"response": []
}
]
}

### Trigger Log

Trigger Log is configured in the database, not in the application, with this query

1. Create audit_log table

```
CREATE TABLE audit_log(
   log_id serial PRIMARY KEY,
   users_id VARCHAR(255),
   changed_field VARCHAR(255),
   old_value VARCHAR(255),
   new_value VARCHAR(255),
   log_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
```

2. Create log_user_changes function

```
CREATE OR REPLACE FUNCTION log_users_changes()
RETURNS TRIGGER AS $$
BEGIN
   IF NEW.email IS DISTINCT FROM OLD.email THEN
   INSERT INTO audit_log(users_id, changed_field, old_value, new_value)
   VALUES (current_user::text, 'email', OLD.email, NEW.email);
END IF;

   IF NEW.password IS DISTINCT FROM OLD.password THEN
   INSERT INTO audit_log(users_id, changed_field, old_value, new_value)
   VALUES(current_user::text, 'password', OLD.password, NEW.password);
END IF;

RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

3. Create trigger users_changes_trigger and execute log_users_changes function

```
CREATE TRIGGER users_changes_trigger
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION log_users_changes();
```

## Testing

1. REST API
   You can test our REST API with [Postman](https://www.postman.com/). You can download Postman and install it on your local computer before testing the REST API

2. TRIGGER LOG
   there is email and password that saved on database

![image](https://github.com/josikie/UAS-Microservice-CRUD-API-PL-SQL-UNSIA/assets/63739078/565b4c31-8ab8-4009-b91d-8cc8cbf4e5fc)

when the user changes data, the changes will be saved in the audit_log table with encypted aes256 format
![image](https://github.com/josikie/UAS-Microservice-CRUD-API-PL-SQL-UNSIA/assets/63739078/2912bc33-57bc-4f21-9623-e56ccdd0f432)
