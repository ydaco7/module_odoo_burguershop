# Módulo Hamburguesería — Odoo

---

## Stack Tecnológico

| Tecnología | Versión | Rol |
|---|---|---|
| **Odoo** | 16 Community | Framework ERP / ORM / Vistas |
| **Python** | 3.10+ | Lógica de negocio y modelos |
| **PostgreSQL** | 14 | Base de datos |
| **Docker** | 24+ | Contenerización del entorno |
| **Docker Compose** | v2 | Orquestación de servicios |
| **XML** | — | Vistas, menús y datos de Odoo |

---

## Arquitectura del Módulo

```
hamburguesas_yadiel/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── burger_ingredient.py       # Modelo: Ingredientes
│   ├── burger_product.py          # Modelo: Productos (hamburguesas, bebidas)
│   ├── burger_order.py            # Modelo: Pedidos + estados
│   └── burger_order_line.py       # Modelo: Líneas de pedido con personalización
├── wizard/
│   ├── __init__.py
│   └── return_wizard.py           # Wizard: Gestión de devoluciones
├── views/
│   ├── ingredient_views.xml
│   ├── product_views.xml
│   ├── order_views.xml
│   ├── return_wizard_views.xml
│   └── menu_views.xml
├── security/
│   ├── security_groups.xml        # Grupos: Admin, Empleado
│   └── ir.model.access.csv        # Permisos CRUD por grupo
├── report/
│   ├── sales_report.xml           # Acción e informe QWeb
│   └── sales_report_template.xml  # Template HTML del informe
└── data/
    └── demo_data.xml              # Datos de demostración
```

---

## Plan de Implementación

### Fase 1 — Entorno Docker
**Objetivo:** Levantar Odoo 16 + PostgreSQL en contenedores listos para desarrollo.

- Crear `docker-compose.yml` con servicios `odoo` y `db`
- Crear `odoo.conf` con la configuración base
- Mapear volumen del módulo dentro del contenedor (`/mnt/extra-addons`)
- Verificar acceso a `http://localhost:8069`

**Archivos a crear:** `docker-compose.yml`, `odoo.conf`

---

### Fase 2 — Estructura Base del Módulo
**Objetivo:** Crear el esqueleto del módulo con sus modelos principales.

- Crear `__manifest__.py` con nombre, versión, dependencias (`base`, `mail`)
- Modelo `burger.ingredient` — ingredientes (nombre, tipo, precio extra)
- Modelo `burger.product` — productos con tipo (`hamburguesa`, `bebida`, `otro`)
- Relación `many2many` entre `burger.product` y `burger.ingredient`
- Modelo `burger.order` — pedido con cliente, fecha, estado
- Modelo `burger.order.line` — líneas del pedido con personalización de ingredientes

**Archivos a crear:** `models/burger_ingredient.py`, `models/burger_product.py`, `models/burger_order.py`, `models/burger_order_line.py`

---

### Fase 3 — Lógica de Negocio (Estados + Devoluciones)
**Objetivo:** Implementar el flujo de estados y el wizard de devoluciones.

- Campo `state` en `burger.order` con selección: `draft` → `waiting` → `preparing` → `ready` → `delivered` → `returned`
- Botones de transición de estado en la vista formulario
- Personalización por línea: ingredientes adicionales / eliminados por pedido
- Cálculo automático del total del pedido
- Wizard `burger.return.wizard` con campos: pedido, motivo, fecha
- Acción del wizard que cambia estado a `returned` y registra el motivo

**Archivos a crear:** `wizard/return_wizard.py`

---

### Fase 4 — Vistas e Interfaz
**Objetivo:** Crear las vistas de formulario, árbol, búsqueda y el wizard en XML.

- Vista árbol y formulario de ingredientes
- Vista árbol y formulario de productos (con pestaña de ingredientes disponibles)
- Vista formulario de pedidos con:
  - Header con botones de estado (statusbar)
  - Líneas de pedido con personalización de ingredientes
  - Total calculado
- Vista árbol de pedidos con columna de estado coloreada
- Vista formulario del wizard de devoluciones
- Menú principal "Hamburguesería" con submenús

**Archivos a crear:** `views/*.xml`, `views/menu_views.xml`

---

### Fase 5 — Seguridad y Permisos
**Objetivo:** Restringir acceso por rol de usuario.

- Grupo `hamburguesas_yadiel.group_burger_admin` (Administrador)
- Grupo `hamburguesas_yadiel.group_burger_employee` (Empleado)
- Reglas en `ir.model.access.csv`:
  - Empleado: crear/leer/editar pedidos, no puede eliminar
  - Admin: acceso total incluido eliminación y reportes

**Archivos a crear:** `security/security_groups.xml`, `security/ir.model.access.csv`

---

### Fase 6 — Reportes
**Objetivo:** Generar informes de ventas en PDF usando QWeb.

- Informe de ventas por producto (cantidad y monto)
- Informe de ventas por día
- Template QWeb con encabezado, tabla y totales
- Acción de reporte accesible desde la vista de pedidos

**Archivos a crear:** `report/sales_report.xml`, `report/sales_report_template.xml`

---


## Levantar el entorno

```bash
# Clonar repositorio
git clone <url-repo>
cd hamburguesas_yadiel_odoo

# Levantar servicios
docker compose up -d

# Acceder a Odoo
# http://localhost:8069
# Usuario: admin | Contraseña: admin

# Instalar el módulo desde Ajustes > Aplicaciones > hamburguesas_yadiel
```

---

## Modelos y Relaciones

```
burger.ingredient
  └── nombre, tipo (extra/base), precio_extra

burger.product
  ├── nombre, tipo (hamburguesa/bebida/otro), precio
  └── ingredientes_disponibles → many2many → burger.ingredient

burger.order
  ├── cliente, fecha, state (flujo completo)
  ├── lineas → one2many → burger.order.line
  └── total (campo calculado)

burger.order.line
  ├── pedido → many2one → burger.order
  ├── producto → many2one → burger.product
  ├── cantidad
  ├── ingredientes_extra → many2many → burger.ingredient
  └── ingredientes_sin → many2many → burger.ingredient

burger.return.wizard (transient)
  ├── pedido → many2one → burger.order
  ├── motivo, fecha_devolucion
  └── action_confirm() → cambia state a 'returned'
```
