from linio import db

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(30), unique=True, nullable=False)
    descripcion = db.Column(db.String(100), unique=False, nullable=False)


db.create_all()