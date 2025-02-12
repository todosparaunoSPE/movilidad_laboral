# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 12:56:13 2025

@author: jperezr
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis de Movilidad Laboral", page_icon="📊", layout="wide")

# Título de la aplicación
st.title("Análisis de Movilidad Laboral y su Impacto en Pensiones")

# --- Sección de Ayuda en la barra lateral ---
st.sidebar.header("Ayuda / Acerca de")
st.sidebar.write("""
**Descripción de la aplicación:**

Esta aplicación permite analizar datos de movilidad laboral y su impacto en las pensiones. Con ella puedes:
- Cargar un archivo CSV con datos de movilidad laboral.
- Filtrar los datos por año y región.
- Visualizar gráficos de migración por género.
- Analizar el salario promedio y la tasa de desempleo por región y género.
- Explorar la relación entre el salario promedio y la tasa de desempleo.
- Proyectar el impacto de la movilidad laboral en la demanda de pensiones.
- Exportar los datos filtrados para su uso posterior.
""")
st.sidebar.write("""
**Instrucciones de uso:**
1. Sube un archivo CSV con los datos de movilidad laboral.
2. Usa los filtros en la barra lateral para seleccionar el rango de años y las regiones de interés.
3. Explora los gráficos y análisis generados automáticamente.
4. Exporta los datos filtrados si lo necesitas.
""")
st.sidebar.write("---")
st.sidebar.write("© 2023 Javier Horacio Pérez Ricárdez. Todos los derechos reservados.")
#st.sidebar.write("Desarrollado con ❤️ usando Streamlit y Python.")

# Carga automática del archivo CSV
archivo_csv = "datos_movilidad_laboral-copia.csv"  # Nombre del archivo CSV
data = pd.read_csv(archivo_csv)

# Mostrar los datos cargados
st.subheader("Datos de Movilidad Laboral")
st.write(data)

# Selección múltiple de años
st.sidebar.subheader("Filtros Avanzados")
años_disponibles = sorted(data["Año"].unique())
año_min = int(data["Año"].min())
año_max = int(data["Año"].max())

# Slider de selección múltiple de años
años_seleccionados = st.sidebar.slider(
    "Selecciona un rango de años",
    min_value=año_min,
    max_value=año_max,
    value=(año_min, año_max)  # Valor inicial del rango
)

# Filtrar datos por el rango de años seleccionado
filtered_data = data[(data["Año"] >= años_seleccionados[0]) & (data["Año"] <= años_seleccionados[1])]

# Mostrar datos filtrados
st.subheader(f"Datos Filtrados para los años {años_seleccionados[0]} - {años_seleccionados[1]}")
st.write(filtered_data)

# Selección múltiple de regiones
st.subheader("Filtros por Región")
regiones_disponibles = filtered_data["Región"].unique()
regiones_seleccionadas = st.multiselect(
    "Selecciona una o más regiones para analizar",
    options=regiones_disponibles,
    default=regiones_disponibles  # Selecciona todas las regiones por defecto
)

# Filtrar datos por regiones seleccionadas
region_data = filtered_data[filtered_data["Región"].isin(regiones_seleccionadas)]

# --- Gráficos de Migración por Género ---
st.subheader("Migración Laboral por Género")
if not regiones_seleccionadas:
    st.warning("Por favor, selecciona al menos una región.")
else:
    # Filtrar datos por género
    data_masculino = region_data[region_data["Género"] == "Masculino"]
    data_femenino = region_data[region_data["Género"] == "Femenino"]
    
    # Sumar la migración por región para masculino
    suma_masculino = data_masculino.groupby("Región", as_index=False)["Migración"].sum()
    
    # Sumar la migración por región para femenino
    suma_femenino = data_femenino.groupby("Región", as_index=False)["Migración"].sum()
    
    # Crear gráfico de barras para masculino
    fig_masculino = px.bar(
        suma_masculino,
        x="Región",
        y="Migración",
        labels={"Migración": "Número de Migrantes", "Región": "Región"},
        title=f"Migración Laboral Masculina en {', '.join(regiones_seleccionadas)}",
        text="Migración"  # Muestra el valor de la migración en las barras
    )
    
    fig_masculino.update_traces(
        hovertemplate="<b>Región:</b> %{x}<br><b>Migración:</b> %{y}"
    )
    
    # Crear gráfico de barras para femenino
    fig_femenino = px.bar(
        suma_femenino,
        x="Región",
        y="Migración",
        labels={"Migración": "Número de Migrantes", "Región": "Región"},
        title=f"Migración Laboral Femenina en {', '.join(regiones_seleccionadas)}",
        text="Migración"  # Muestra el valor de la migración en las barras
    )
    
    fig_femenino.update_traces(
        hovertemplate="<b>Región:</b> %{x}<br><b>Migración:</b> %{y}"
    )
    
    # Mostrar los gráficos en Streamlit
    st.plotly_chart(fig_masculino, use_container_width=True)
    st.plotly_chart(fig_femenino, use_container_width=True)

# --- Gráficos de Salario Promedio y Tasa de Desempleo ---
st.subheader("Análisis de Salario Promedio y Tasa de Desempleo")
if not regiones_seleccionadas:
    st.warning("Por favor, selecciona al menos una región.")
else:
    # Gráfico de Salario Promedio por Región y Género
    st.write("#### Salario Promedio por Región y Género")
    salario_promedio = region_data.groupby(["Región", "Género"], as_index=False)["Salario Promedio"].mean()
    
    fig_salario = px.bar(
        salario_promedio,
        x="Región",
        y="Salario Promedio",
        color="Género",
        barmode="group",
        labels={"Salario Promedio": "Salario Promedio ($)", "Región": "Región"},
        title="Salario Promedio por Región y Género"
    )
    st.plotly_chart(fig_salario, use_container_width=True)

    # Gráfico de Tasa de Desempleo por Región y Género
    st.write("#### Tasa de Desempleo por Región y Género")
    tasa_desempleo = region_data.groupby(["Región", "Género"], as_index=False)["Tasa de Desempleo"].mean()
    
    fig_desempleo = px.bar(
        tasa_desempleo,
        x="Región",
        y="Tasa de Desempleo",
        color="Género",
        barmode="group",
        labels={"Tasa de Desempleo": "Tasa de Desempleo (%)", "Región": "Región"},
        title="Tasa de Desempleo por Región y Género"
    )
    st.plotly_chart(fig_desempleo, use_container_width=True)

    # Gráfico de Dispersión: Salario Promedio vs Tasa de Desempleo
    st.write("#### Relación entre Salario Promedio y Tasa de Desempleo")
    fig_dispersion = px.scatter(
        region_data,
        x="Salario Promedio",
        y="Tasa de Desempleo",
        color="Región",
        hover_name="Género",
        labels={"Salario Promedio": "Salario Promedio ($)", "Tasa de Desempleo": "Tasa de Desempleo (%)"},
        title="Relación entre Salario Promedio y Tasa de Desempleo"
    )
    st.plotly_chart(fig_dispersion, use_container_width=True)

    # Calcular la correlación entre Salario Promedio y Tasa de Desempleo
    correlacion = region_data["Salario Promedio"].corr(region_data["Tasa de Desempleo"])
    
    # Mostrar el coeficiente de correlación
    st.write(f"**Coeficiente de Correlación de Pearson:** {correlacion:.2f}")
    
    # Interpretación del coeficiente de correlación
    if correlacion > 0:
        st.write("Existe una **correlación positiva** entre el Salario Promedio y la Tasa de Desempleo.")
    elif correlacion < 0:
        st.write("Existe una **correlación negativa** entre el Salario Promedio y la Tasa de Desempleo.")
    else:
        st.write("No existe una **correlación lineal** significativa entre el Salario Promedio y la Tasa de Desempleo.")

# --- Proyección de Impacto en Pensiones ---
st.subheader("Proyección de Impacto en Pensiones")
if not regiones_seleccionadas:
    st.warning("Por favor, selecciona al menos una región.")
else:
    # Calcular el impacto en pensiones para masculino
    impacto_pensiones_masculino = suma_masculino.copy()
    impacto_pensiones_masculino["Impacto"] = impacto_pensiones_masculino["Migración"] * 0.1  # Factor de impacto hipotético
    
    # Calcular el impacto en pensiones para femenino
    impacto_pensiones_femenino = suma_femenino.copy()
    impacto_pensiones_femenino["Impacto"] = impacto_pensiones_femenino["Migración"] * 0.1  # Factor de impacto hipotético
    
    st.write("### Impacto en Pensiones para Hombres")
    for _, row in impacto_pensiones_masculino.iterrows():
        migracion_formateada = "{:,.0f}".format(row['Migración'])  # Formatear con separadores de miles
        impacto_formateado = "{:,.0f}".format(row['Impacto'])  # Formatear con separadores de miles
        st.write(f"**Migración total en {row['Región']}:** {migracion_formateada} personas")
        st.write(f"**Impacto estimado en la demanda de pensiones:** {impacto_formateado} solicitudes adicionales")
    
    st.write("### Impacto en Pensiones para Mujeres")
    for _, row in impacto_pensiones_femenino.iterrows():
        migracion_formateada = "{:,.0f}".format(row['Migración'])  # Formatear con separadores de miles
        impacto_formateado = "{:,.0f}".format(row['Impacto'])  # Formatear con separadores de miles
        st.write(f"**Migración total en {row['Región']}:** {migracion_formateada} personas")
        st.write(f"**Impacto estimado en la demanda de pensiones:** {impacto_formateado} solicitudes adicionales")

# Exportar resultados
st.subheader("Exportar Resultados")
if st.button("Exportar Datos Filtrados a CSV"):
    filtered_data.to_csv("datos_filtrados.csv", index=False)
    st.success("Datos exportados correctamente como 'datos_filtrados.csv'")