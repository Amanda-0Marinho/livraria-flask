import os

basedir = os.path.abspath(os.path.dirname(__file__))


local_db_path = os.path.join(basedir, "..", "data")
os.makedirs(local_db_path, exist_ok=True)

local_db_uri = "sqlite:///" + os.path.join(local_db_path, "library.db")

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "minha_chave_secreta_library")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", local_db_uri)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
