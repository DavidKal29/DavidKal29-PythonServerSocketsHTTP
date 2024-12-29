import socket

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
