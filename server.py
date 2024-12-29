import socket

#Aquí serán creados los html basicos
inicio='''
<html>
<h1>Bienvenido al Server</h1>
<a href="./login">
<button><a href="./login">Iniciar Sesion</a></button>
<button><a href="./register">Registrarme</a></button>
</html>
'''

register='''
<html>
<h1>Register</h1>
<form action="/login" method="post">
<input type="email" placeholder="Email" name="email" required><br>
<input type="text" placeholder="Nombre" name="nombre" required><br>
<input type="text" placeholder="Pais" name="pais" required><br>
<input type="number" placeholder="Edad" name="edad" required><br>
<input type="password" placeholder="Password" name="password" required><br>
<button type="submit">Registrarme</button>
</html>
'''

login='''
<html>
<h1>Login</h1>
<form action="/perfil" method="post">
<input type="email" placeholder="Email" name="email" required><br>
<input type="password" placeholder="Password" name="password" required><br>
<button type="submit">Inicar Sesion</button>
</html>
'''

perfil='''
<html>
<h1>Perfil</h1>
<h3>Email:{}</h3>
<h3>Nombre:{}</h3>
<h3>País:{}<h3>
<h3>Edad:{}</h3>
<button><a href="./inicio">Cerrar Sesion</a></button>
</html>
'''

#Si el usuario ya existe a la hora de registrarse
usuarioExiste='''
<html>
<h1>Lo sentimos</h1>
<h3>El correo que usted introdujo ya pertenece a una cuenta registrada</h3>
<h3>Porfavor, registrese otra vez pulsando el boton de abajo</h3>
<button><a href="./register">Registrarme otra vez</a></button>
</html>
'''

#Si el email al loguearse no esta en la base de datos
emailFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, el correo que usted proporciono no figura en la base de datos</h3>
<h3>Porfavor, registrese pulsando el boton de abajo</h3>
<button><a href="./register">Registrarme</a></button>
</html>
'''

#Si la contraseña al loguearse es incorrecta
passwordFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, el password que usted introdujo no es correcto</h3>
<h3>Porfavor, inicie sesion de nuevo pulsando el boton de abajo</h3>
<button><a href="./login">Iniciar Sesion</a></button>
</html>
'''

#Error si el usuario hace alguna petición no controlada por el sistema
errorHtml='''
<html>
<h1>PARECE QUE HAS LLEGADO AL FINAL</h1>
<h1>ERROR 404 NOT FOUND</h1>
<button><a href="./inicio">Regresar</a></button>
</html>
'''


#Creamos el socket del server
try:
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(('localhost',65432))
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.listen()
    print("Servidor abierto a la escucha de peticiones")
except:
    print("Sucedió un error mientras se montaba el servidor")


#Creamos las respuestas del server
ok='HTTP/1.1 200 Ok\r\n\r\n'
error='HTTP /1.1 404 Not Found\r\n\r\n'
signos={'+':' ','%40':'@'}
#La linea de arriba es para sustituir los signos de los datos
#que habremos introducido en los inputs y que apareceran en el cuerpo
#del mensaje al hacer el post

#Creamos e iniciamos la base de datos
import sqlite3
conexion=sqlite3.connect('server_users.sqlite3')
cursor=conexion.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (email VARCHAR(100),nombre VARCHAR(100),\
pais VARCHAR(75),edad INTEGER, password VARCHAR(100));')
conexion.commit()



#Iniciamos el bucle para aceptar clientes
try:
    while True:
        conn,addr=server.accept()
        print("Nueva conexión desde",addr)

        peticion=conn.recv(4096).decode()
        peticion=peticion.split('\r\n')
        
        cabecera=peticion[0]#Es la primera linea de la peticion
        metodo=cabecera.split()[0]#El metodo(GET o POST)
        recurso=cabecera.split()[1]#El recurso que nos pide (/login,/perfil,etc)

        cuerpo=peticion[-1]#El cuerpo de la peticion(Cuando el metodo sea post, aqui estaran los datos metidos en los inputs)


        if metodo=='GET':#Si el metodo es get, dependiendo de lo que nos pida el usuario, le enviaremos a un sitio u a otro
            if recurso=='/login':
                respuesta=ok+login
                conn.sendall(respuesta.encode('utf-8'))
            elif recurso=='/register':
                respuesta=ok+register
                conn.sendall(respuesta.encode('utf-8'))
            elif recurso=='/' or recurso=="/inicio":
                respuesta=ok+inicio
                conn.sendall(respuesta.encode('utf-8'))
            else:
                respuesta=error+errorHtml
                conn.sendall(respuesta.encode('utf-8'))
        
        elif metodo=='POST':
            #Si el metodo es post, manipularemos el cuerpo(donde estaran los datos(si se ha registrado)
            #o solo el email y el password(si se ha logueado))
            cuerpo=cuerpo.replace('+',signos['+'])
            cuerpo=cuerpo.replace('%40',signos['%40'])
            cuerpo=cuerpo.split('&')

            cuerpo='='.join(cuerpo)
            cuerpo=cuerpo.split('=')
            #Los pasos anteriores son para procesar los datos del cuerpo
            #los cuales tenian y estaban separados por simbolos raros

            if recurso=='/login':
                #El usuario quiere registrarse(porque solicita ir al login), por lo que tendremos 5 valores, que meteremos en la bd

                email=cuerpo[1].strip()
                nombre=cuerpo[3].strip()
                pais=cuerpo[5].strip()
                edad=cuerpo[7].strip()
                password=cuerpo[9].strip()


                #Debemos comprobar si el usuario ya existe por lo que hacemos la consulta
                cursor.execute('SELECT * FROM usuarios')
                usuarios=cursor.fetchall()
                comprobarUsuario=False

                for user in usuarios:
                    if user[0]==email:
                        comprobarUsuario=True


                if comprobarUsuario:
                    respuesta=error+usuarioExiste
                    conn.sendall(respuesta.encode('utf-8'))
                else:
                    cursor.execute('INSERT INTO usuarios (email,nombre,pais,edad,password) VALUES (?,?,?,?,?)',
                                (email,nombre,pais,edad,password))
                    conexion.commit()
                    
                    #Hemos metido en la bd al nuevo usuario

                    respuesta=ok+login
                    conn.sendall(respuesta.encode('utf-8'))

            elif recurso=='/perfil':
                #El usuario quiere iniciar sesion(porque solicita ir al perfil), por lo que solo tenemos su email y password
                #los cuales debemos verificar si existen en la base de datos

                email=cuerpo[1].strip()
                password=cuerpo[3].strip()

                cursor.execute('SELECT * FROM usuarios')
                usuarios=cursor.fetchall()

                #Estos parámetros nos ayudaran a saber si los datos están en la bd
                comprobarEmail=False
                comprobarPassword=False

                #Recorremos la tabla y vemos si el email y el password coinciden
                for user in usuarios:
                    if user[0]==email:
                        comprobarEmail=True

                        if user[-1]==password:
                            comprobarPassword=True

                            nombre=user[1]
                            pais=user[2]
                            edad=user[3]
                                

                #Dependiendo de la comprobacion de arriba, seremos enviados a un sitio u a otro
                if comprobarEmail:
                    if comprobarPassword:
                        respuesta=ok+perfil.format(email,nombre,pais,edad)
                        conn.sendall(respuesta.encode('utf-8'))
                    else:
                        respuesta=error+passwordFalse
                        conn.sendall(respuesta.encode('utf-8'))
                else:
                    respuesta=ok+emailFalse
                    conn.sendall(respuesta.encode('utf-8'))

            else:
                respuesta=error+errorHtml
                conn.sendall(respuesta.encode('utf-8'))
                                
        conn.close()
except:
    print("Sucedió un error mientras se manejaban las peticiones")