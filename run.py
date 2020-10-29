from app import app
from db import db

db.init_app(app)

# Criação de tabelas no DB antes de qualquer request
@app.before_first_request
def create_tables():
    db.create_all()