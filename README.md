# PAE · Sistema de Adopciones con IA

Aplicación multipágina en Streamlit, diseñada con un enfoque **Tier S+ (Premium Dashboard)**, para la predicción y gestión operacional de animales en el refugio PAE.

## 📁 Estructura del proyecto

Todos los archivos se encuentran unificados en el directorio raíz.

```text
/
├── Inicio.py                     # Entry point de la aplicación (Portada)
├── pages/
│   ├── 1_Dashboard.py            # Panel operacional con KPIs, alertas y gráficos Plotly
│   └── 2_Predictor.py            # Predictor de estadía con IA interactivo
├── services/
│   ├── data_service.py           # Acceso y filtrado de datos (repository pattern)
│   └── prediction_service.py     # Encapsula la inferencia del modelo ML
├── ui/
│   └── styles.py                 # Sistema de diseño CSS Tier S+ (Paleta oscura, Material Icons)
├── pae_adopciones_sintetico.csv  # Base de datos local (con datos históricos y nombres)
├── entrenar.py                   # Pipeline ML para regenerar el modelo
├── preprocesador_pae.pkl         # Transformer/Encoder pre-entrenado
└── modelo_pae.pkl                # Modelo Random Forest entrenado
```

## 🚀 Ejecución

El proyecto está diseñado para ejecutarse en entornos de Windows utilizando el launcher de Python `py`.

```powershell
# Ejecutar la aplicación en tu navegador local
py -m streamlit run Inicio.py
```

## 📊 Arquitectura y Datos

### Base de Datos (`pae_adopciones_sintetico.csv`)
La aplicación lee directamente de este archivo a través de `data_service.py` aplicando un esquema estricto (excluyendo datos malformados de forma automática).
El CSV incluye metadatos visuales como `Nombre`, `Adoptado`, y `Fecha_Ingreso` utilizados exclusivamente para los KPIs y la tabla de alertas del `Dashboard`.

### Pipeline de Machine Learning (`entrenar.py`)
Para evitar el *Data Leakage* (fuga de datos) al momento de entrenar la Inteligencia Artificial, las columnas exclusivamente informativas (`Nombre`, `Adoptado`, `Fecha_Ingreso`) son **ignoradas explícitamente** durante el entrenamiento.
Si deseas reentrenar el modelo con nuevos datos en el futuro, simplemente debes ejecutar:
```powershell
py entrenar.py
```
Esto sobrescribirá de forma segura `modelo_pae.pkl` y `preprocesador_pae.pkl`.

## 🎨 Sistema de Diseño (Tier S+)

El proyecto cuenta con un sistema de interfaz avanzado controlado desde `ui/styles.py`:
- **Cero Emojis Textuales:** La navegación utiliza **Material Symbols** de Google integrados de forma nativa en el código para mantener un look 100% corporativo y profesional.
- **Paleta de Colores:** Basado en la paleta premium `Teal 700` (`#0F766E`) y `Slate 900` (`#0F172A`).
- **Tipografía:** Inyecta automáticamente las fuentes web `Inter` (para lectura) y `Fira Code` (para visualización precisa de KPIs).
- **Adaptabilidad Visual:** Los gráficos de `Plotly` tienen fondos transparentes (`rgba(0,0,0,0)`) que se adaptan orgánicamente al Dashboard sin cajas blancas disruptivas. Todos los selectores están encapsulados con CSS inyectado para fundirse con la barra lateral oscura.
