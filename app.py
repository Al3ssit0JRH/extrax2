from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__, static_folder="static")
app.secret_key = 'alex123'


# Conectar a la base de datos
def conectar_db():
    uri = "mongodb+srv://23301224:20301224@junior.52vo42c.mongodb.net/ProyectoCaso"
    try:
        client = MongoClient(uri)
        client.list_database_names()
        return client['ProyectoCaso']
    except PyMongoError as e:
        return {'message': f"Error de conexión a la base de datos: {str(e)}"}


# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/eje')
def eje():
    return render_template('ejemplo.html')

# Ruta para la página de modificables
@app.route('/modificables')
def modificables():
    return render_template('modificables.html')


# Ruta para la página de inicio de sesión
@app.route('/iniSes')
def iniciar_sesion():
    return render_template('iniciar_sesion.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contra = request.form['contra']

        # Conectar a la base de datos
        db = conectar_db()
        user = db.IniciarSesion.find_one({'correo': usuario})

        # Verificar si el usuario existe y si la contraseña es correcta
        if user and user['contra'] == contra:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('modificables'))
        else:
            return "Login fallido. Por favor, verifica tu nombre de usuario y contraseña."

    return render_template('iniciar_sesion.html')


@app.route('/insertar_servidor', methods=['POST'])
def insertar_servidor():
    db = conectar_db()
    try:
        nombre_servidor = request.form.get('nombre_servidor_insertar')
        numero_rack = request.form.get('numero_rack_insertar')
        capacidad_almacenamiento = request.form.get('capacidad_almacenamiento_insertar')
        sistema_operativo = request.form.get('sistema_operativo_insertar')
        seguridad = request.form.get('seguridad_insertar')
        estado = request.form.get('estado_insertar')
        temperatura = request.form.get('temperatura_insertar')
        hora_respaldo = request.form.get('hora_respaldo_insertar')

        # Crear el documento a insertar
        servidor = {
            'nombre_servidor': nombre_servidor,
            'numero_rack': numero_rack,
            'capacidad_almacenamiento': capacidad_almacenamiento,
            'sistema_operativo': sistema_operativo,
            'seguridad': seguridad,
            'estado': estado,
            'temperatura': temperatura,
            'hora_respaldo': hora_respaldo
        }

        # Insertar el documento en la colección
        db.Servidores.insert_one(servidor)

        return jsonify({'message': 'Servidor insertado correctamente'}), 200

    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500




@app.route('/buscar_servidor', methods=['POST'])
def buscar_servidor():
    numero_rack = request.form.get('numero_rack')
    db = conectar_db()
    resultado = db.Servidores.find_one({'numero_rack': numero_rack})

    if resultado:
        # Convertir el resultado a un formato JSON adecuado
        resultado_json = {
            'nombre_servidor': resultado.get('nombre_servidor', ''),
            'capacidad_almacenamiento': resultado.get('capacidad_almacenamiento', ''),
            'sistema_operativo': resultado.get('sistema_operativo', ''),
            'seguridad': resultado.get('seguridad', ''),
            'estado': resultado.get('estado', ''),
            'temperatura': resultado.get('temperatura', ''),
            'hora_respaldo': resultado.get('hora_respaldo', '')
        }
        return jsonify(resultado_json)
    else:
        return 404




@app.route('/modificar_servidor', methods=['POST'])
def modificar_servidor():
    nombre_servidor = request.form.get('nombre_servidor_modificar')

    # Define los campos que se actualizarán
    actualizaciones = {
        'capacidad_almacenamiento': request.form.get('capacidad_almacenamiento_modificar'),
        'sistema_operativo': request.form.get('sistema_operativo_modificar'),
        'seguridad': request.form.get('seguridad_modificar'),
        'estado': request.form.get('estado_modificar'),
        'temperatura': request.form.get('temperatura_modificar'),
        'hora_respaldo': request.form.get('hora_respaldo_modificar')
    }

    db = conectar_db()
    resultado = db.Servidores.update_one(
        {'nombre_servidor': nombre_servidor},
        {'$set': actualizaciones}
    )

    if resultado.modified_count > 0:
        return jsonify({'message': 'Servidor modificado con éxito'})
    else:
        return jsonify({'message': 'No se encontró el servidor o no se realizaron cambios'})





@app.route('/eliminar_servidor', methods=['POST'])
def eliminar_servidor():
    nombre_servidor = request.form.get('nombre_servidor_eliminar')
    db = conectar_db()
    resultado = db.Servidores.delete_one({'nombre_servidor': nombre_servidor})

    if resultado.deleted_count > 0:
        return jsonify({'message': 'Servidor eliminado con éxito'})
    else:
        return jsonify({'message': 'No se encontró el servidor'})

if __name__ == "__main__":
    app.run(debug=True)
