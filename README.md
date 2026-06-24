# PAE · Sistema de Adopciones con IA

Aplicación Streamlit multipage para predicción y gestión operacional
de animales en el refugio PAE.

## Estructura del proyecto

```
pae_app/
├── 🏠_Inicio.py                  # Entry point
├── pages/
│   ├── 1_📊_Dashboard.py         # Panel operacional con KPIs y alertas
│   └── 2_🔮_Predictor.py         # Predictor de estadía con IA
├── services/
│   ├── data_service.py           # Acceso a datos históricos (repository pattern)
│   └── prediction_service.py     # Encapsula el modelo ML
├── ui/
│   └── styles.py                 # Sistema de diseño CSS (single source of truth)
├── data/
│   └── historico_adopciones.csv  # Coloca aquí tu CSV con datos reales
├── preprocesador_pae.pkl         # ← REQUERIDO: tu preprocesador entrenado
├── modelo_pae.pkl                # ← REQUERIDO: tu modelo entrenado
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
# Desde la carpeta pae_app/
streamlit run 🏠_Inicio.py
```

## Esquema del CSV histórico

El archivo `data/historico_adopciones.csv` debe tener estas columnas:

| Columna              | Tipo     | Valores posibles                              |
|----------------------|----------|-----------------------------------------------|
| Nombre               | str      | Nombre del animal                             |
| Especie              | str      | "Perro" / "Gato"                              |
| Edad_Meses           | int      | 1 – 240                                       |
| Peso_Kg              | float    | 0.5 – 80.0                                    |
| Tamano               | str      | "Pequeño" / "Mediano" / "Grande"              |
| Estado_Salud         | str      | "Excelente" / "Bueno" / "Regular" / "En Tratamiento" |
| Nivel_Sociabilidad   | str      | "Alto" / "Medio" / "Bajo"                    |
| Esterilizado         | str      | "Si" / "No"                                   |
| Publicaciones        | int      | 0 – 50                                        |
| Interacciones_RRSS   | int      | 0 – 5000                                      |
| Fecha_Ingreso        | date     | YYYY-MM-DD                                    |
| Dias_Estadia         | int      | Días que estuvo/está en el refugio            |
| Adoptado             | bool     | True / False                                  |

Si el CSV no existe, la app corre en **modo demo** con datos sintéticos realistas
y muestra un aviso en pantalla.

## Notas técnicas

- El CSS se inyecta desde `ui/styles.py` como single source of truth.
  Para cambiar colores, solo modifica el dict `COLORS`.
- El caché de datos (`@st.cache_data(ttl=300)`) refresca cada 5 minutos.
  Ajusta el TTL según la frecuencia de actualización de tu CSV.
- Para cambiar la fuente de datos (SQLite, PostgreSQL, API),
  solo modifica `services/data_service.py` → función `load_historical_data()`.
  Las páginas no se tocan.
