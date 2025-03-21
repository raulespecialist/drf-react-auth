# **Backend - Autenticación con Django y DRF**

Este proyecto es un backend desarrollado en Django y Django REST Framework (DRF) que implementa un sistema de autenticación de usuarios con autenticación de dos factores (2FA) utilizando Google Authenticator.

----------

## **Propósito**

El propósito de este backend es proporcionar una API para:

1.  **Registro de usuarios**.
    
2.  **Inicio de sesión**  con autenticación básica (usuario y contraseña).
    
3.  **Configuración de Google Authenticator**  para la autenticación de dos factores (2FA).
    
4.  **Verificación de códigos OTP**  generados por Google Authenticator.
    
5.  **Cierre de sesión**.
    

----------

## **Librerías Utilizadas**

-   **Django**: Framework principal para el desarrollo del backend.
    
-   **Django REST Framework (DRF)**: Para crear la API RESTful.
    
-   **django-rest-knox**: Para manejar la autenticación basada en tokens.
    
-   **pyotp**: Para generar y verificar códigos OTP (One-Time Password).
    
-   **qrcode**: Para generar códigos QR que los usuarios pueden escanear con Google Authenticator.
    

----------

## **Endpoints**

### **1. Registro de Usuarios**

-   **Método**:  `POST`
    
-   **URL**:  `/api/register/`
    
-   **Descripción**: Permite a los usuarios registrarse en la aplicación.
    
-   **Restricciones**:
    
    -   El nombre de usuario y el correo electrónico deben ser únicos.
        
    -   La contraseña debe tener al menos 8 caracteres.
        
-   **Modelo de Negocio**:
    
    -   Crea un nuevo usuario en la base de datos.
        
    -   Crea un perfil asociado al usuario para almacenar el secreto de Google Authenticator.
        

----------

### **2. Inicio de Sesión**

-   **Método**:  `POST`
    
-   **URL**:  `/api/login/`
    
-   **Descripción**: Permite a los usuarios iniciar sesión con su nombre de usuario y contraseña.
    
-   **Restricciones**:
    
    -   El usuario debe estar registrado.
        
    -   Las credenciales deben ser válidas.
        
-   **Modelo de Negocio**:
    
    -   Verifica las credenciales del usuario.
        
    -   Devuelve un token de autenticación si las credenciales son válidas.
        
    -   Redirige al usuario a  `/qr`  si no tiene un secreto de Google Authenticator configurado.
        
    -   Redirige al usuario a  `/verify-otp`  si ya tiene un secreto configurado.
        

----------

### **3. Generación de Código QR para Google Authenticator**

-   **Método**:  `GET`
    
-   **URL**:  `/api/generate-qr/`
    
-   **Descripción**: Genera un código QR que el usuario puede escanear con Google Authenticator.
    
-   **Restricciones**:
    
    -   El usuario debe estar autenticado.
        
    -   El usuario no debe tener un secreto de Google Authenticator configurado previamente.
        
-   **Modelo de Negocio**:
    
    -   Genera un secreto aleatorio y lo almacena en el perfil del usuario.
        
    -   Genera un código QR que contiene el secreto y lo devuelve en formato base64.
        

----------

### **4. Verificación de Código OTP**

-   **Método**:  `POST`
    
-   **URL**:  `/api/verify-otp/`
    
-   **Descripción**: Verifica el código OTP ingresado por el usuario.
    
-   **Restricciones**:
    
    -   El usuario debe estar autenticado.
        
    -   El usuario debe tener un secreto de Google Authenticator configurado.
        
-   **Modelo de Negocio**:
    
    -   Verifica si el código OTP coincide con el secreto almacenado en el perfil del usuario.
        
    -   Marca al usuario como verificado si el código es válido.
        

----------

### **5. Cierre de Sesión**

-   **Método**:  `POST`
    
-   **URL**:  `/api/logout/`
    
-   **Descripción**: Permite a los usuarios cerrar sesión.
    
-   **Restricciones**:
    
    -   El usuario debe estar autenticado.
        
-   **Modelo de Negocio**:
    
    -   Elimina el token de autenticación del usuario.
        
    -   Marca al usuario como no autenticado.
        

----------

## **Modelos de Negocio**

### **1. Usuario (`User`)**

-   **Descripción**: Modelo de usuario predeterminado de Django.
    
-   **Campos**:
    
    -   `username`: Nombre de usuario único.
        
    -   `email`: Correo electrónico único.
        
    -   `password`: Contraseña encriptada.
        

### **2. Perfil (`Profile`)**

-   **Descripción**: Modelo que extiende el modelo de usuario para almacenar el secreto de Google Authenticator.
    
-   **Campos**:
    
    -   `user`: Relación uno a uno con el modelo  `User`.
        
    -   `totp_secret`: Secreto de Google Authenticator (cadena de 32 caracteres).
        

----------

## **Instalación y Ejecución**

1.  **Clonar el repositorio**:
    
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    
2.  **Instalar dependencias**:
    
    pip install -r requirements.txt
    
3.  **Aplicar migraciones**:
    
    python manage.py migrate
    
4.  **Ejecutar el servidor**:

    python manage.py runserver
    
----------

## **Contribuciones**

Si deseas contribuir a este proyecto, sigue estos pasos:

1.  Haz un fork del repositorio.
    
2.  Crea una rama para tu contribución (`git checkout -b feature/nueva-funcionalidad`).
    
3.  Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
    
4.  Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
    
5.  Abre un pull request.
    

----------

## **Licencia**

Este proyecto está bajo la licencia MIT. Para más detalles, consulta el archivo  [LICENSE](https://license/).

----------

¡Gracias por usar este backend! Si tienes alguna pregunta o sugerencia, no dudes en contactarme. 😊

----------