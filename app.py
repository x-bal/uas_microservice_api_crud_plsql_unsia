from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64
from functools import wraps
from flask import Flask, request, jsonify, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'secret'

conn = psycopg2.connect(
    database="uas_plsql",
    user="postgres",
    password="root",
    host="127.0.0.1",
    port="5432"
)

# Api


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({"message": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=["POST"])
def login():
    data = request.json
    username = data["username"]

    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, role FROM users WHERE username = %s", (username,))
    user_data = cursor.fetchone()
    if user_data:
        session['username'] = user_data[0]
        session['role'] = user_data[1]

        return jsonify({"status": "Login successful", "user": user_data}), 200
    return jsonify({"status": "Login failed"}), 401


@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return jsonify({"status": "Logout successful"}), 200


@app.route('/users', methods=["GET"])
@admin_required
def get():
    cur = conn.cursor()
    cur.execute("select * from users")
    rows = [dict((cur.description[i][0], value)
                 for i, value in enumerate(row)) for row in cur.fetchall()]
    return jsonify({'data': rows})


def encrypt_password(password, salt):
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())
    cipher = Cipher(algorithms.AES(key[:32]), modes.CBC(
        b'\x00' * 16), backend=backend)
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(password.encode()) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(ct)


@app.route('/users/<int:id>', methods=['GET'])
@admin_required
def first(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    return jsonify({'data': user})


@app.route('/users', methods=["POST"])
@admin_required
def store():
    data = request.json
    salt = os.urandom(16)
    encrypted_password = encrypt_password(data["password"], salt)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, name, password, role) VALUES (%s, %s, %s, %s)", (data["username"], data["name"], encrypted_password, data["role"]))
    conn.commit()
    return jsonify({"status": "Data berhasil ditambahkan"}), 201


@app.route("/users/<int:id>", methods=["PUT"])
@admin_required
def update(id):
    data = request.json
    # salt = os.urandom(16)
    # encrypted_password = encrypt_password(data["password"], salt)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s WHERE id = %s",
                   (data["name"], id))
    conn.commit()
    return jsonify({"status": "Data berhasil diupate"}), 200


@app.route("/users/<int:id>", methods=["DELETE"])
@admin_required
def delete_user(id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    conn.commit()
    return jsonify({"status": "Data berhasil dihapus"}), 200


if __name__ == '__main__':
    app.run(debug=True)
