import socket

#Aquí serán creados los html basicos

inicio='''
<html>
<h1>Bienvenido al Server</h1>
<button href="./login">Inicar Sesión</button>
<button href="./register">Registrarme</button>
</html>
'''

register='''
<html>
<h1>Login</h1>
<form action="./login" method="post">
<input type="email" placeholder="Email" required>
<input type="text" placeholder="Nombre" required>
<input type="text" placeholder="País" required>
<input type="number" placeholder="Edad" required>
<input type="password" placeholder="Password" required>
<button>Registrarme</button>
</html>
'''

login='''
<html>
<h1>Login</h1>
<form action="./perfil" method="post">
<input type="email" placeholder="Email" required>
<input type="password" placeholder="Password" required>
<button>Inicar Sesión</button>
</html>
'''

perfil='''
<html>
<h1>Perfil</h1>
<h3>Email:{}</h3>
<h3>Nombre:{}</h3>
<h3>País:{}<h3>
<h3>Edad:{}</h3>
<button href="./inicio">Cerrar sesión</button>
</html>
'''


emailFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, el correo que usted proporcionó no figura en la base de datos</h3>
<h3>Porfavor, registrese pulsando el botón de abajo</h3>
<button href="./register">Registrarme</button>
</html>
'''

passwordFalse='''
<html>
<h1>Lo sentimos</h1>
<h3>Al parecer, la contraseña que usted introdujo no es correcta</h3>
<h3>Porfavor, inicie sesión de nuevo pulsando el botón de abajo</h3>
<button href="./login">Iniciar Sesión</button>
</html>
'''

error='''
<html>
<h1>PARECE QUE HAS LLEGADO AL FINAL</h1>
<h1>ERROR 404 NOT FOUND</h1>
<button href="./inicio">Regresar</button>
</html>
'''

#Creamos el socket del server
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('localhost',65432))
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.listen()
print("Servidor abierto a la escucha de peticiones")



#Iniciamos el bucle para aceptar clientes
while True:
    conn,addr=server.accept()
    print("Nueva conexión desde",addr)
