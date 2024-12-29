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
<h1>Login</h1>
<form action="./login" method="post">
<input type="email" placeholder="Email" required><br>
<input type="text" placeholder="Nombre" required><br>
<input type="text" placeholder="Pais" required><br>
<input type="number" placeholder="Edad" required><br>
<input type="password" placeholder="Password" required><br>
<button>Registrarme</button>
</html>
'''

login='''
<html>
<h1>Login</h1>
<form action="./perfil" method="post">
<input type="email" placeholder="Email" required><br>
<input type="password" placeholder="Password" required><br>
<button>Inicar Sesion</button>
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


emailFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, el correo que usted proporcionó no figura en la base de datos</h3>
<h3>Porfavor, registrese pulsando el botón de abajo</h3>
<button><a href="./register">Registrarme</a></button>
</html>
'''

passwordFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, la contraseña que usted introdujo no es correcta</h3>
<h3>Porfavor, inicie sesión de nuevo pulsando el botón de abajo</h3>
<button><a href="./login">Iniciar Sesion</a></button>
</html>
'''

error='''
<html>
<h1>PARECE QUE HAS LLEGADO AL FINAL</h1>
<h1>ERROR 404 NOT FOUND</h1>
<button><a href="./inicio">Regresar</a></button>
</html>
'''

#Creamos el socket del server
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',65432))
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.listen()
print("Servidor abierto a la escucha de peticiones")


#Creamos las respuestas del server
ok='HTTP/1.1 200 Ok\r\n\r\n'
error='HTTP /1.1 404 Not Found\r\n\r\n'+error

#Creamos e iniciamos la base de datos
import sqlite3
conexion=sqlite3.connect('server_users.sqlite3')
cursor=conexion.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (email VARCHAR(100),nombre VARCHAR(100),\
pais VARCHAR(75),edad INTEGER, password VARCHAR(100));')
conexion.commit()



#Iniciamos el bucle para aceptar clientes
while True:
    conn,addr=server.accept()
    print("Nueva conexión desde",addr)

    peticion=conn.recv(4096).decode()
    peticion=peticion.split('\r\n')
    
    cabecera=peticion[0]
    metodo=cabecera.split()[0]
    recurso=cabecera.split()[1]

    cuerpo=peticion[-1]

    if metodo=='GET':
        if recurso=='/login':
            respuesta=ok+login
            conn.sendall(respuesta.encode('utf-8'))
        elif recurso=='/register':
            respuesta=ok+register
            conn.sendall(respuesta.encode('utf-8'))
        elif recurso=='/' or recurso=="/inicio":
            respuesta=ok+inicio
            conn.sendall(respuesta.encode('utf-8'))
    

    conn.close()














    
