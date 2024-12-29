# Servidor HTTP con Sockets en Python
Este proyecto tiene como finalidad, crear un servidor ligero y sencillo utilizando python y a través de sockets y el protocolo HTTP. El funcionamiento es sencillo, el usuario podrá registrarse con sus datos los cuales seran almacenados en una base de datos sencilla en SQLITE, y a partir de esa información podrá loguearse y entrar a su perfil el cual será una pagina simple que mostrará algunos de sus datos.

## Características
- Soporta solicitudes HTTP GET y POST
- Manejo de una base de datos sencilla den SQLITE
- Responde con código de estado HTTP adecuado (200, 404, etc.).
- Basado en sockets, con un manejo simple de conexiones concurrentes.
