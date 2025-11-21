# Copilot Instructions - TP Canchas DAO

## Architecture Overview
This is a Flask-based sports court management system using a **3-layer DAO pattern** with SQLite. The project follows a strict separation: Models (domain objects) → DAO (data access) → Services (Flask blueprints) → Frontend (modular JS/HTML). Mantener siempre bajo acopplamiennto y alta cohesión entre objetos y tambien entre capas.

## Key Patterns & Conventions

### DAO Pattern Implementation
- **All database operations** go through DAO classes in `apps/dao/*/` 
- **Singleton DB connection** via `ConexionDB` class (`apps/dao/conexion.py`)
- **Auto table creation** on app startup via `crear_tablas()` in `bd_canchas.py`
- Each entity has its own DAO folder: `CanchaDAO/`, `ClienteDAO/`, `ReservaDAO/`, etc.

### Model Structure
- Domain models in `apps/models/*/` mirror database tables
- Models contain **business logic** and object relationships (e.g., `Cancha.calcular_costo_total()`)
- **Gestor classes** act as singletons for business orchestration (`models/Gestor.py`)

### Service Layer (Flask Blueprints)
- Each blueprint in `apps/servicios/` exposes RESTful endpoints (pattern: `/api/{entity}/`)
- Services import DAOs directly and return JSON responses
- All blueprints registered in `apps/app.py` with consistent naming: `bp_clientes`, `bp_canchas`, etc.

## Critical Workflows

### Running the Application
```bash
cd apps/
python app.py  # Starts Flask on port 5000, auto-creates tables
```

### Project Structure Navigation
- **Entry point**: `apps/app.py` (Flask app + blueprint registration)
- **Database init**: `apps/bd_canchas.py` (table creation sequence matters - foreign keys!)
- **Frontend**: Modular JS in `apps/static/js/` (see `README_JS_MODULES.md`)
- **Templates**: Componentized HTML in `apps/templates/` using base template pattern

### Adding New Entities
1. Create model class in `apps/models/{Entity}/`
2. Create DAO class in `apps/dao/{Entity}DAO/` with `crear_tabla()` method
3. Add table creation call to `bd_canchas.py` (respect FK dependencies)
4. Create service blueprint in `apps/servicios/`
5. Register blueprint in `apps/app.py`

## Project-Specific Conventions

### Database Naming
- Table names match model class names (e.g., `Cancha` table for `Cancha` model)  
- Foreign keys follow pattern: `id_{referenced_table}` (e.g., `id_tipo` references `TipoCancha`)
- Primary keys are auto-increment integers with descriptive names (e.g., `nro_cancha`, not just `id`)

### Frontend Architecture  
- **7 modular JS files** replace original monolithic `main.js`
- API calls use consistent endpoint pattern: `/api/{plural_entity}/`
- Form handling centralized in `forms.js` with validation in `validaciones.js`
- Template inheritance from `base.html` with modular sections

### Error Handling Pattern
- DAO methods use try/catch at service level, return JSON with `{'error': str(e)}` 
- Database constraints handled at DAO level, business rules at model level
- Frontend validation before API calls using `Validaciones` class methods

## Integration Points
- **SQLite DB**: `bd_canchas.db` created in project root
- **CORS enabled** for potential frontend separation
- **Flask-CORS** dependency for API access
- **Auto-initialization**: Tables created on every app start (idempotent)

When modifying this codebase, always follow the DAO→Service→Frontend flow and maintain the existing naming conventions for consistency.