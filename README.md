# PlanIteam

¡Bienvenido a PlanIteam! 🏡

PlanIteam es una aplicación web familiar para organizar espacios, tareas, notas, categorías y presupuestos, pensada para la gestión colaborativa del hogar o proyectos compartidos.

## Características principales
- **Gestión de espacios** (casas, departamentos, etc.)
- **Notas, tareas y presupuestos** personales y compartidos
- **Categorías personalizables**
- **CRUD rápido** con modales y filtros
- **Paginación** para grandes volúmenes de datos
- **Exportación a CSV**
- **Autenticación de usuarios**
- **Panel de administración Django**
- **Diseño responsive** con Bootstrap

## Instalación y uso rápido
1. Clona el repositorio:
   ```sh
   git clone https://github.com/mapollaparada/PlanIteam.git
   cd PlanIteam
   ```
2. Crea un entorno virtual e instala dependencias:
   ```sh
   python -m venv ambv
   source ambv/bin/activate  # o .\ambv\Scripts\activate en Windows
   pip install -r requirements.txt
   ```
3. Copia el archivo `.env.example` a `.env` y configura tu SECRET_KEY y variables:
   ```sh
   cp .env.example .env
   # Edita .env con tus valores
   ```
4. Aplica migraciones y ejecuta el servidor:
   ```sh
   python manage.py migrate
   python manage.py runserver
   ```
5. Accede a `http://127.0.0.1:8000/` y ¡comienza a organizar!

## Variables de entorno
Configura tus secretos y parámetros en un archivo `.env`:
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

## Seguridad y buenas prácticas
- No subas tu base de datos ni archivos sensibles (ver `.gitignore`).
- Cambia `DEBUG=False` y configura `ALLOWED_HOSTS` en producción.
- Usa HTTPS en despliegues públicos.

## Docker (opcional)
¿Quieres dockerizar? Puedes agregar un `Dockerfile` y `docker-compose.yml` para facilitar el despliegue.

## Licencia
MIT

---

Hecho con ❤️ por la familia y para la familia.
