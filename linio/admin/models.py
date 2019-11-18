from linio import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    telefono = db.Column(db.String(9), unique=False, nullable=False)
    distrito = db.Column(db.String(2), unique=False, nullable=False)
    direccion = db.Column(db.String(40), unique=False, nullable=False)
    nro_tarjeta = db.Column(db.String(16), unique=False, nullable=False)
    def __repr__(self):
        return '<Usuario %r>' % self.username

'''
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), unique=False, nullable=False)
    telefono = db.Column(db.String(9), unique=False, nullable=False)
    distrito = db.Column(db.String(20), unique=False, nullable=False)
    direccion = db.Column(db.String(40), unique=False, nullable=False)
    nro_tarjeta = db.Column(db.String(16), unique=False, nullable=False)

    def __repr__(self):
        return '<usuario %r>' % self.username

class Comercio(db.Model):
    id_comercio = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=False, nullable=False)
    telefono = db.Column(db.String(9), unique=False, nullable=False)
    distrito = db.Column(db.String(20), unique=False, nullable=False)
    direccion = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return '<comercio %r>' % self.nombre


class Categoria(db.Model):
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    descripcion = db.Column(db.String(40), unique=False, nullable=False)

    def __repr__(self):
        return '<categoria %r>' % self.nombre


class Producto(db.Model):
    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30), unique=False, nullable=False)
    precio = db.Column(db.Numeric(10, 2), unique=False, nullable=False)
    descripcion = db.Column(db.String(200), unique=False, nullable=False)
    id_comercio = db.Column(db.Integer, db.ForeignKey('comercio.id_comercio'), nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    imagen = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return '<producto %r>' % self.nombre


class Carrito(db.Model):
    id_carrito = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    monto = db.Column(db.Numeric(10, 2), unique=False, nullable=False)

    def __repr__(self):
        return '<carrito %r>' % self.id_carrito


class Pedido(db.Model):
    id_pedido = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.Integer)
    id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id_carrito'), nullable=False)
    estado = db.Column(db.String(3), unique=False, nullable=False)
    monto = db.Column(db.Numeric(10, 2), unique=False, nullable=False)

    def __repr__(self):
        return '<pedido %r>' % self.id_pedido


class Pago(db.Model):
    id_pago = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedido.id_pedido'), nullable=False)
    tipo = db.Column(db.String(3), unique=False, nullable=False)
    cvv = db.Column(db.String(3), unique=False, nullable=False)
    nombre_titular = db.Column(db.String(20), unique=False, nullable=False)
    codigo_cip = db.Column(db.String(10), unique=False, nullable=False)

    def __repr__(self):
        return '<pago %r>' % self.id_pago


class Carrito_producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_carrito = db.Column(db.Integer, db.ForeignKey('carrito.id_carrito'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'), nullable=False)

'''
db.create_all()

