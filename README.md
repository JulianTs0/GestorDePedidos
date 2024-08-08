Para ejecutar el projecto se debe crear un entorno virtual con los requerimientos que se detallan en el archivo requirements.txt antes de trasladar la carpeta src a la carpeta raiz, para crear el entorno en la carpeta raiz se accede a la consola de powershell se debe tipear:

### virtualenv -p python3 env

y para activar el entorno virual se debe tipear:

Windows con git bash:

### .\env\Scripts\activate

Linux:

### source .\env\bin\activate

Para instalar todas las dependencias del proyecto se translada el archivo requirements.txt a la carpeta raiz, luego se procede directamente en el terminal de powershell con el entorno activado ingresando el siguiente comando: 

### pip install -r .\requirements.txt

En la carpeta donde raiz se debe crear un archivo .env en donde las siguientes variables deben ser completadas con los datos detallados

### USER_GMAIL="Cuenta de gmail del proyecto"
### PASSWORD_GMAIL="Contraseña de aplicacion del gmail"
### USER_DB="Nombre de usuario de la base de datos"
### PASSWORD_DB="Contraseña de la cuenta de usuario de la base de datos"
### HOST_DB="Host de la base de datos (IP del server)"
### DATABASE="Nombre de la base de datos"
### PORT_DB="Puerto de la base de datos (PORT del server)"

Para obtener estos datos contactese con el desarollador del proyecto.

Una vez finalizado los anteriores pasos translade la carpeta src a la carpeta raiz y ejecute el archivo front.py