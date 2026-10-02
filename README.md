# Order API / API de Pedidos

## Overview / Visión general

Esta aplicación es una API REST para gestionar usuarios, productos y órdenes dentro de un sistema de ventas. Está construida con FastAPI, SQLAlchemy y PostgreSQL, siguiendo una estructura modular y fácil de extender.

This application is a REST API for managing users, products, and orders in a sales system. It is built with FastAPI, SQLAlchemy, and PostgreSQL, following a modular and extensible structure.

---

## 1. Objetivo del proyecto / Project objective

El objetivo principal es proporcionar una base funcional para la gestión de pedidos con validaciones de negocio, control de inventario y registro de transacciones de compra.

The main objective is to provide a functional foundation for order management with business validations, inventory control, and purchase transaction tracking.

### Funcionalidades principales / Main features

- Registro de usuarios
- Gestión de productos
- Validación de stock antes de crear una orden
- Cálculo de subtotal y total
- Desactivación lógica de productos en lugar de eliminación física
- API REST documentada automáticamente con Swagger

- User registration
- Product management
- Stock validation before creating an order
- Subtotal and total calculation
- Logical deactivation of products instead of physical deletion
- REST API automatically documented with Swagger

---

## 2. Stack tecnológico / Tech stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- Uvicorn
- psycopg

---

## 3. Estructura del proyecto / Project structure

```text
order-api/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── databases/
│   │   ├── Base.py
│   │   └── connection.py
│   ├── models/
│   │   ├── orden.py
│   │   ├── orden_item.py
│   │   ├── product.py
│   │   └── user.py
│   ├── routes/
│   │   ├── order.py
│   │   ├── product.py
│   │   └── users.py
│   ├── schema/
│   │   ├── orden.py
│   │   ├── orden_item.py
│   │   ├── product.py
│   │   └── user.py
│   ├── security/
│   │   └── password.py
│   ├── service/
│   └── main.py
├── tests/
├── .env
├── README.md
└── venv/
```

---

## 4. Requisitos previos / Prerequisites

Antes de ejecutar el proyecto, asegúrate de tener instalado:

Before running the project, make sure you have installed:

- Python 3.11 o superior / Python 3.11 or higher
- PostgreSQL
- Un cliente o herramienta para gestionar la base de datos
- Entorno virtual recomendado / Recommended virtual environment

---

## 5. Configuración del entorno / Environment setup

### 5.1 Crear entorno virtual / Create a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5.2 Instalar dependencias / Install dependencies

```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings psycopg[binary]
```

### 5.3 Configurar variables de entorno / Set environment variables

Crea un archivo `.env` en la raíz del proyecto:

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql+psycopg://postgres:1042@localhost:5432/orden_Api
```

> Ajusta el valor según tu usuario, contraseña y nombre de base de datos.
>
> Adjust the value according to your username, password, and database name.

---

## 6. Ejecución de la aplicación / Running the application

Desde la raíz del proyecto, ejecuta:

From the project root, run:

```bash
uvicorn app.main:app --reload
```

O con Python del entorno virtual:

Or using the virtual environment Python:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

La API estará disponible en:

The API will be available at:

```text
http://127.0.0.1:8000
```

Documentación interactiva de Swagger:

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 7. Endpoints principales / Main endpoints

### 7.1 Usuarios / Users

| Método | Endpoint | Descripción | Description |
|---|---|---|---|
| POST | `/users/` | Crear usuario | Create user |

#### Ejemplo de creación de usuario / User creation example

```json
{
  "name": "Ana Gómez",
  "email": "ana@correo.com",
  "password": "MiPassword123"
}
```

Respuesta esperada / Expected response:

```json
{
  "id": 1,
  "name": "Ana Gómez",
  "email": "ana@correo.com",
  "role": "customer",
  "created_at": "2026-10-02T12:00:00Z",
  "updated_at": "2026-10-02T12:00:00Z"
}
```

### 7.2 Productos / Products

| Método | Endpoint | Descripción | Description |
|---|---|---|---|
| GET | `/product/` | Listar productos activos | List active products |
| POST | `/product/` | Crear producto | Create product |
| GET | `/product/{product_id}` | Obtener producto por ID | Get product by ID |
| PUT | `/product/{product_id}` | Actualizar producto completo | Update full product |
| PATCH | `/product/{product_id}` | Actualizar parcialmente | Partially update product |
| DELETE | `/product/{product_id}` | Desactivar producto | Deactivate product |

#### Ejemplo de creación de producto / Product creation example

```json
{
  "name": "Laptop Dell",
  "description": "Laptop para desarrollo",
  "price": 999.99,
  "stock": 10
}
```

Respuesta esperada / Expected response:

```json
{
  "id": 1,
  "name": "Laptop Dell",
  "description": "Laptop para desarrollo",
  "price": 999.99,
  "stock": 10,
  "active": true,
  "created_at": "2026-10-02T12:00:00Z",
  "updated_at": "2026-10-02T12:00:00Z"
}
```

### 7.3 Órdenes / Orders

| Método | Endpoint | Descripción | Description |
|---|---|---|---|
| POST | `/orders/` | Crear una orden | Create an order |

#### Ejemplo de creación de orden / Order creation example

```json
{
  "user_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

Respuesta esperada / Expected response:

```json
{
  "id": 1,
  "user_id": 1,
  "status": "pending",
  "total": 1999.98,
  "items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "unit_price": 999.99,
      "subtotal": 1999.98
    }
  ],
  "created_at": "2026-10-02T12:00:00Z",
  "updated_at": "2026-10-02T12:00:00Z"
}
```

### 7.4 Estado / Health

| Método | Endpoint | Descripción | Description |
|---|---|---|---|
| GET | `/` | Verifica que la API responde | Checks that the API is responding |

Respuesta esperada / Expected response:

```json
{
  "mensaje": "API funcionando",
  "message": "API working",
  "status": "ok",
  "estado": "correcto"
}
```

---

## 8. Modelo de datos / Data model

### Usuario / User

- `id`
- `name`
- `email`
- `password_hash`
- `role`
- `created_at`
- `updated_at`

### Producto / Product

- `id`
- `name`
- `description`
- `price`
- `stock`
- `active`
- `created_at`
- `updated_at`

### Orden / Order

- `id`
- `user_id`
- `status`
- `total`
- `created_at`
- `updated_at`

### Item de orden / Order item

- `id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`
- `subtotal`

---

## 9. Reglas de negocio / Business rules

Las reglas de negocio implementadas incluyen:

- Los productos no pueden tener stock negativo.
- No se puede crear una orden con un usuario que no existe.
- No se puede crear una orden si un producto no existe.
- No se puede vender más unidades de las disponibles.
- Los productos inactivos no son elegibles para compra.
- El total de la orden se calcula a partir de los subtotales.

The business rules implemented include:

- Products cannot have negative stock.
- An order cannot be created for a non-existent user.
- An order cannot be created if a product does not exist.
- More units cannot be sold than are available.
- Inactive products are not eligible for purchase.
- The order total is calculated from the subtotals.

---

## 10. Buenas prácticas / Best practices

- Usar entorno virtual para aislar dependencias.
- Mantener PostgreSQL activo antes de iniciar la API.
- No hardcodear secretos ni credenciales en el código fuente.
- Usar `.env` para configuraciones sensibles.
- Añadir pruebas unitarias e integración para usuarios, productos y órdenes.
- Mantener los modelos y schemas consistentes entre el backend y la validación.

- Use a virtual environment to isolate dependencies.
- Keep PostgreSQL running before starting the API.
- Do not hardcode secrets or credentials in source code.
- Use `.env` for sensitive configuration.
- Add unit and integration tests for users, products, and orders.
- Keep models and schemas consistent between the backend and validation layer.

---

## 11. Estado actual / Current status

El proyecto se encuentra en una base funcional para pedidos, con estructura modular y lógica de negocio básica implementada. Puede ampliarse con autenticación, paginación, manejo más robusto de errores y pruebas automatizadas.

The project is in a functional base state for order processing, with a modular structure and core business logic implemented. It can be extended with authentication, pagination, more robust error handling, and automated testing.

---

## 12. Siguientes mejoras recomendadas / Recommended next improvements

- Autenticación JWT / JWT authentication
- Paginación de resultados / Result pagination
- Manejo centralizado de errores / Centralized error handling
- Pruebas automatizadas / Automated tests
- Documentación por endpoint con ejemplos / Endpoint-by-endpoint documentation with examples
- Swagger mejorado con descripciones detalladas / Improved Swagger with detailed descriptions

---

## 13. Conclusión / Conclusion

Este repositorio funciona como una base sólida para un sistema de pedidos con arquitectura REST simple y clara. Es adecuado para continuar con mejoras de seguridad, calidad y escalabilidad.

This repository serves as a solid foundation for an order management system with a simple and clear REST architecture. It is suitable for continuing with security, quality, and scalability improvements.

---

## 14. Contacto / Contact

Proyecto desarrollado como base para gestión de pedidos.

Project developed as a foundation for order management.

---

Esta versión ya incluye ejemplos reales de JSON para cada endpoint y una estructura más clara para documentación profesional.

This version already includes real JSON examples for each endpoint and a clearer structure for professional documentation.
