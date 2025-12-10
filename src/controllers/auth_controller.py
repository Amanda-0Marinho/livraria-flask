from src.models.user import User
from flask import jsonify, request
from src.extensions import db
import jwt
import datetime
from src.config import Config
from functools import wraps


def decode_token():
    token = request.headers.get("Authorization")
    if not token:
        return None, jsonify({"error": "Token obrigatório"}), 401
    try:
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return data, None, None
    except:
        return None, jsonify({"error": "Token inválido"}), 401


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data, error, code = decode_token()
        if error:
            return error, code
        return f(data, *args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        data, error, code = decode_token()
        if error:
            return error, code
        if data["role"] != "admin":
            return jsonify({"error": "Apenas admin pode acessar"}), 403
        return f(data, *args, **kwargs)
    return wrapper


def register(data):
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"error": "Campos obrigatórios"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Usuário já existe"}), 400

    user = User(username=username, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    
    return jsonify({"message": "Usuário registrado"}), 201


def login(data):
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = jwt.encode(
        {
            "user_id": user.id,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        },
        Config.SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})


@login_required
def delete_user(data, user_id):
    target = User.query.get(user_id)

    if not target:
        return jsonify({"error": "Usuário não encontrado"}), 404

    requester = User.query.get(data["user_id"])

    if requester.role != "admin" and target.role == "admin":
        return jsonify({"error": "Usuário não pode deletar admin"}), 403

    db.session.delete(target)
    db.session.commit()

    return jsonify({"message": "Usuário deletado"})
