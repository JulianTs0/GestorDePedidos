Para ejecutar el projecto se debe crear un entorno virtual con los requerimientos que se detallan en el archivo requirements.txt 
para instalarlos a todos directamente en el terminal de powershell con el entorno activado se debe ingresar el siguiente comando: 
### pip install -r .\requirements.txt
En la carpeta donde este situado el projecto, es decir donde esta la carpeta src y la carpeta del entorno, 
al mismo nivel se debe crear un archivo .env en donde las siguientes variables deben ser completadas con los datos detallados

### USER_GMAIL="Cuenta de gmail utilizada"
### PASSWORD_GMAIL="Contraseña de aplicacion del gmail"
### USER_DB="Nombre de usuario de la base de datos"
### PASSWORD_DB="Contraseña de la base de datos"
### HOST_DB="Host de la base de datos (IP)"
### DATABASE="Nombre de la base de datos"
### PORT_DB="Puerto de la base de datos"