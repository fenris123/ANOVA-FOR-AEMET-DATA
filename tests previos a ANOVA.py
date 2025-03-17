# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 17:12:24 2025

@author: fenris123
"""

"""
Script para evaluar normalidad y homogeneidad de varianza en datos de temperatura máxima.
"""

import json
import pandas as pd
from scipy.stats import shapiro, levene

# Ruta del archivo JSON
ruta_json = r"C:\espaciopython\CODIGOS UTILES\AEMET\Datos_Sevilla_2024.json"

# Cargar datos JSON
with open(ruta_json, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Convertir datos a DataFrame
df = pd.DataFrame(datos)

# Filtrar columnas necesarias
df = df[["fecha", "nombre", "tmax"]]

# Reemplazar comas por puntos en los valores de "tmax"
df["tmax"] = df["tmax"].str.replace(",", ".", regex=False)

# Convertir "tmax" a número (manejar posibles errores)
df["tmax"] = pd.to_numeric(df["tmax"], errors="coerce")

# Eliminar filas con valores nulos en "tmax" (temperatura máxima)
df = df.dropna(subset=["tmax"])

# Separar datos por estación
estaciones = df["nombre"].unique()
tmax_estaciones = {estacion: df[df["nombre"] == estacion]["tmax"].tolist() for estacion in estaciones}

# Test de normalidad (Shapiro-Wilk)
print("Test de Normalidad (Shapiro-Wilk):")
for estacion, datos in tmax_estaciones.items():
    stat, p = shapiro(datos)
    print(f"{estacion}: p-valor = {p:.4f} {'✅ Normal' if p > 0.05 else '❌ No normal'}")

# Test de homogeneidad de varianzas (Levene)
stat, p = levene(*tmax_estaciones.values())
print("\nTest de Homogeneidad de Varianzas (Levene):")
print(f"p-valor = {p:.4f} {'✅ Varianzas iguales' if p > 0.05 else '❌ Varianzas diferentes'}")
