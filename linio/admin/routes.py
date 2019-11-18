from flask import *
from linio import app, db, bcrypt
from .models import *
from .forms import *
import sqlite3, hashlib, os
import os
import random
import string

@app.route('/home')
def home():
    return render_template('admin/index.html', title = 'Inicio')



@app.route("/registerationForm", methods = ['GET', 'POST'])
def registro():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        usuario = Usuario(nombre=form.nombre.data, username=form.username.data, email =form.email.data,
                            password =hash_password, telefono=form.telefono.data, distrito=form.distrito.data,
                            direccion=form.direccion.data, nro_tarjeta=form.tarjeta.data)
        #db.session.add(usuario)
        #db.session.commit()
        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute("INSERT INTO usuario (nombre,username,password,email,telefono,"
                            "distrito,direccion,nro_tarjeta) "
                            "VALUES (?,?,?,?,?,?,?,?)",
                            (usuario.nombre, usuario.username, usuario.password, usuario.email,
                             usuario.telefono, usuario.distrito, usuario.direccion,
                             usuario.nro_tarjeta))
                con.commit()

                cur = con.cursor()
                cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + usuario.email + "'")
                con.commit()
                userId = cur.fetchone()

                cur.execute("INSERT INTO carrito (id_usuario) "
                           "VALUES (?)",
                           (userId))
                con.commit()


                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("admin/inicio.html")
    return render_template("admin/registro.html", error='', form=form)

'''
@app.route('/registro', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        usuario = Usuario(nombre=form.nombre.data, username=form.username.data, email =form.email.data,
                            password =hash_password, telefono=form.telefono.data, distrito=form.distrito.data, 
                            direccion=form.direccion.data, tarjeta=form.tarjeta.data)
        db.session.add(usuario)
        db.session.commit()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO usuario (nombre,username,password,email,telefono,"
                        "distrito,direccion,nro_tarjeta) "
                        "VALUES (?,?,?,?,?,?,?,?)", (usuario.nombre, usuario.username, usuario.password, usuario.email,
                                                     usuario.telefono, usuario.distrito, usuario.direccion,
                                                     usuario.tarjeta))

        flash(f' Bienvenido {form.nombre.data} Gracias por registrarte', 'aprobado')
        return redirect(url_for('login'))
    return render_template('admin/registro.html', form=form, title = 'Pagina registro')
'''

def valido(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM usuario')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/loginForm")
def inicio_sesion():
    if 'email' in session:
        return redirect(url_for('onlineStore'))
    else:
        return render_template('admin/inicio.html', error='')
    return render_template('admin/inicio.html', error='')


@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        #usuario = Usuario.query.filter_by(email=form.email.data).first()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT username FROM usuario WHERE email = '" + form.email.data + "'")
            conn.commit()
            usuario = cur.fetchone()[0]

            cur.execute("SELECT password FROM usuario WHERE email = '" + form.email.data + "'")
            conn.commit()
            password = cur.fetchone()[0]


        if usuario and bcrypt.check_password_hash(password, form.password.data):
            session['email'] = form.email.data
            # flash(f'Bienvenido {form.email.data} Iniciaste sesion', 'exito')
            return redirect(url_for('onlineStore'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('admin/inicio.html', error=error)

    return render_template('admin/inicio.html', error='')



@app.route("/addToCart")
def añadirCarrito():
    if 'email' not in session:
        return redirect(url_for('login'))
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + session['email'] + "'")
        conn.commit()
        idUser = cur.fetchone()[0]

        cur.execute("SELECT id_carrito FROM carrito WHERE id_usuario = '" + str(idUser) + "'")
        conn.commit()
        carId = cur.fetchone()[0]
        try:
            cur.execute("INSERT INTO carrito_producto (id_carrito, id_producto) VALUES (?, ?)", (carId, productId))
             #Agregar product id a la tabla carrito
            conn.commit()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"
    conn.close()

    return redirect(url_for('cart'))

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT id_usuario, nombre FROM usuario WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            #cur.execute("SELECT count(productId) FROM carrito_producto WHERE userId = " + str(userId))
            noOfItems = 3 #cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

def  getIdCategoria(categoria):
    if(categoria == "Arte y Artesanias"):
        return 1
    elif(categoria == "Computadoras"):
        return 2
    elif(categoria=="Moda"):
        return 3
    elif(categoria=="Belleza y cuidado personal"):
        return 4
    elif(categoria=="Salud y bienestar"):
        return 5
    elif(categoria=="Deportes"):
        return 6
    elif(categoria=="Jueguetes y Electrodomésticos"):
        return 7



@app.route("/", methods=["GET","POST"])
def onlineStore():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    form = SearchForm(request.form)
    id_categoria = 1
    if request.method == 'POST':
        id_categoria = form.categoria.data
        #id_categoria = getIdCategoria(categoria)
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute(
                'SELECT id_producto, nombre, precio, descripcion, id_comercio, id_categoria, imagen FROM producto WHERE id_categoria = ' + str(
                    id_categoria))
            itemData = cur.fetchall()
            cur.execute('SELECT id_categoria, nombre FROM categoria')
            categoryData = cur.fetchall()
        itemData = parse(itemData)
        return render_template('admin/home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                               noOfItems=noOfItems, categoryData=categoryData, form=form)

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id_producto, nombre, precio, descripcion, id_comercio, id_categoria, imagen FROM producto WHERE id_categoria = ' + str(id_categoria))
        itemData = cur.fetchall()
        cur.execute('SELECT id_categoria, nombre FROM categoria')
        categoryData = cur.fetchall()
    itemData = parse(itemData)
    return render_template('admin/home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName,
                       noOfItems=noOfItems, categoryData=categoryData, form=form)



@app.route("/checkout2", methods=['GET', 'POST'])
def pago2():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']

    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute(
            "SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = " + str(
                userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
        print(row)
        cur.execute("INSERT INTO Orders (id_usuario, productId) VALUES (?, ?)", (userId, row[0]))
    cur.execute("DELETE FROM kart WHERE id_usuario = " + str(userId))
    conn.commit()

    return render_template("checkout.html", products=products, totalPrice=totalPrice, loggedIn=loggedIn,
                           firstName=firstName, noOfItems=noOfItems)


@app.route("/checkout", methods=["GET","POST"])
def pago():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    """
    form = PagoForm(request.form)
#    form2 = TarjetaForm(request.form)
    if request.method == 'POST' and form.validate():
        def cipgenerar(stringLength=9):
            caracteres = string.ascii_letters + string.digits
            return ''.join(random.choice(caracteres) for i in range(stringLength))

            #pago = payment(tipo=form1.tipo.data)
        #db.session.add(pago)
        #db.session.commit()

        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            #cur.execute("INSERT INTO Pago(tipo, cvv, nombre_titular, codigo_cip) VALUES(?,?,?,?) ('" "EFE"  "', '', '', '')")

            #cur.execute('SELECT id_pago, tipo FROM pago')
            #tipo = 'EFE'
            #if tipo == 'EFE':
            cip = cipgenerar()
            cur.execute("INSERT INTO pago(tipo, cvv, nombre_titular, codigo_cip) VALUES(?,?,?,?)" , ('EFE', '', '', cip))
            flash(f' Tu codigo de pago es  {cip} ')
            #conn.commit()

        conn.close()
        return redirect(url_for('onlineStore'))
 #           else:
  #              cur = conn.cursor()
   #             cur.execute('SELECT tarjeta  WHERE email = '" + session['email'] + "'"')
    #            tarjeta = cur.fetchone()
     #           pago = pago(cvv=form2.cvv.data, nombre_titular=form2.titular.data)
      #          cur.execute("INSERT INTO pago(cvv, nombre_titular), VALUES(?,?),"(pago.cvv, pago.nombre_titular))
       #         return redirect(url_for('onlineStore'))
    """
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute(
            "SELECT producto.id_producto, producto.nombre, producto.precio, producto.imagen FROM producto, carrito, carrito_producto "
            "WHERE producto.id_producto = carrito_producto.id_producto AND carrito_producto.id_carrito=carrito.id_carrito"
            " AND carrito.id_usuario = " + str(
                userId))
        products = cur.fetchall()
        totalPrice = 0
        for row in products:
            totalPrice += row[2]
        envio = 10
        totalPrice = float(totalPrice) +envio

        db.session.commit()

        return render_template("admin/checkout.html", products=products, envio=envio, totalPrice=totalPrice, loggedIn=loggedIn,
                       firstName=firstName, noOfItems=noOfItems#, form=form#
                       )


@app.route("/removeFromCart")
def borarrDeCarrito():
    if 'email' not in session:
        return redirect(url_for('login'))
    email = session['email']
    productId = int(request.args.get('productId'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + str(email) + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT id_carrito FROM carrito WHERE id_usuario = '" + str(userId) + "'")
        carId = cur.fetchone()[0]
        conn.commit()
        try:
            cur.execute("DELETE FROM carrito_producto WHERE id_carrito = " + str(carId) + " AND id_producto = " + str(productId))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('cart'))

@app.route("/logout")
def cerrar_sesion():
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route("/cart")
def carrito():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE email = '" + email + "'")
        userId = cur.fetchone()[0]
        cur.execute("SELECT producto.id_producto, producto.nombre, producto.precio, producto.imagen FROM "
                    "producto, carrito_producto, carrito WHERE producto.id_producto = carrito_producto.id_producto AND "
                    "carrito_producto.id_carrito =carrito.id_carrito AND carrito.id_usuario= " + str(userId))
        products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("admin/cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


@app.route("/productDescription")
def Descripcionproducto():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id_producto, nombre, precio, descripcion, imagen, 0 FROM producto WHERE id_producto = ' + productId)
        productData = cur.fetchone()
    conn.close()
    return render_template("admin/productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)


@app.route("/efectivo")
def pago_efectivo():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    def cipgenerar(stringLength=9):
            caracteres = string.ascii_letters + string.digits
            return ''.join(random.choice(caracteres) for i in range(stringLength))

    cip = cipgenerar()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        
        cur.execute("INSERT INTO pago(tipo, cvv, nombre_titular, codigo_cip) VALUES(?,?,?,?)" , ('EFE', '', '', cip))
    
    return render_template("admin/efectivo.html", cip = cip)

@app.route("/tarjeta", methods = ['POST', 'GET'])
def pago_tarjeta():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']

    form = TarjetaForm(request.form)

    if request.method == 'POST' and form.validate():
        #tarjeta = form.tarjeta.data
        cvv = form.cvv.data
        titular = form.titular.data        
        
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO pago(tipo,cvv, nombre_titular), VALUES(?,?,?)", ('TAR',cvv,titular))
        con.commit()

    