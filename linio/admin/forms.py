from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField

class RegistrationForm(Form):
    nombre = StringField('Nombre', [validators.Length(min=4, max=30)])
    username = StringField('Username', [validators.Length(min=4, max=35)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    telefono = StringField('Telefono', [validators.Length(min=9, max=9)])
    distrito = SelectField('Distrito', choices=[('SM','San Miguel'), ('PL', 'Pueblo Libre'), ('JM', 'Jesús Maria'), ('MA', 'Magdalena'),
              ('LI', 'Lince'), ('SI', 'San Isidro'), ('MI', 'Miraflores'), ('SU', 'Surquillo'),
              ('SB', 'San Borja'), ('BA', 'Barranco'), ('SU', 'Santiago de Surco'), ('MO' ,'La Molina')])
    direccion = StringField('Direccion', [validators.Length(min=4, max=40)])
    tarjeta = StringField('Tarjeta de Credito',[validators.Length(min=16, max=16)] )
    
    accept_tos = BooleanField('Confirmo ser mayor de edad', [validators.DataRequired()])


class LoginForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=35), validators.Email(),validators.DataRequired()])
    password = PasswordField('Contraseña', [validators.DataRequired()])


class SearchForm(Form):
    categoria = SelectField(u'Categoria', choices=[('1', 'Arte y Artesanias'), ('2', 'Computadoras'), ('3', 'Moda'),
                            ('4','Belleza y cuidado personal'),('5','Salud'),('6','Deportes'),('7','Juguetes y Electrodomésticos')])


class PagoForm(Form):
    tipo = SelectField('Tipo', choices = [('EFE','Efectivo'), ('TAR', 'Tarjeta')])



class TarjetaForm(Form):
    tarjeta = StringField('Tarjeta de Credito',[validators.Length(min=16, max=16)] )
    cvv = StringField('CVV',[validators.Length(min=3, max=3)] )
    titular = StringField('Nombre', [validators.Length(min=4, max=20)])
