import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

print("Iniciando entrenamiento local...")

# 1. Cargar el dataset que ya generaste
dataset = pd.read_csv('pae_adopciones_sintetico.csv')
dataset = dataset.drop_duplicates()

# 2. Separar variables (sin logaritmo, como acordamos)
y = dataset['Dias_Estadia'].values
X = dataset.drop(columns=['Dias_Estadia', 'ID_Ingreso', 'Nombre', 'Adoptado', 'Fecha_Ingreso'])

# 3. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Configurar preprocesador
columnas_categoricas = ['Tamano', 'Estado_Salud', 'Nivel_Sociabilidad', 'Especie', 'Esterilizado']
ct = ColumnTransformer(
    transformers=[
        ('encoder', OneHotEncoder(drop='first', sparse_output=False), columnas_categoricas)
    ],
    remainder='passthrough'
).set_output(transform="pandas")

X_train_procesado = ct.fit_transform(X_train)

# 5. Entrenar el modelo
regressor = LinearRegression()
regressor.fit(X_train_procesado, y_train)

# 6. Guardar los archivos con la versión de TU computadora
joblib.dump(ct, 'preprocesador_pae.pkl')
joblib.dump(regressor, 'modelo_pae.pkl')

print("¡Modelos generados y guardados con éxito en tu computadora!")