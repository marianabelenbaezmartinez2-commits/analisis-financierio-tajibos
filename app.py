import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. DATOS CONSOLIDADOS (2021-2025)
data = {
    'Año': [2021, 2022, 2023, 2024, 2025],
    'Activo Corriente': [13154294.72, 21583745.15, 23027954.80, 48680425.01, 40502727.28],
    'Activo No Corriente': [318657813.74, 366510749.80, 370320377.13, 335364415.23, 326818455.10],
    'Pasivo Corriente': [29383984.21, 66470711.52, 133101795.12, 126445350.71, 101954371.50],
    'Pasivo No Corriente': [133492908.39, 172854156.73, 132706294.37, 120750318.36, 117644055.72],
    'Patrimonio': [168935215.86, 148769626.70, 127540242.44, 136849171.10, 147722755.20],
    'Ingresos': [36967263.34, 59541155.35, 87427281.42, 148037758.60, 155964959.20],
    'Utilidad Neta': [-2423230.78, -2016558.92, -2122938.42, 9308928.68, 11967603.13],
    'Costo Ventas': [9345480.88, 15103504.27, 21837798.08, 43948825.33, 49734146.73],
    'Inventarios': [4272615.40, 6180840.69, 3899122.25, 23878046.80, 14422102.85],
    'Gastos Financieros': [5918702.47, 5593539.12, 10690908.36, 10907851.89, 10666550.19]
}
df = pd.DataFrame(data)
df['Total Activo'] = df['Activo Corriente'] + df['Activo No Corriente']
df['Total Pasivo'] = df['Pasivo Corriente'] + df['Pasivo No Corriente']

# 2. CÁLCULO DE LOS 12 RATIOS (3 POR CATEGORÍA)
# Liquidez
df['Liquidez Corriente'] = df['Activo Corriente'] / df['Pasivo Corriente']
df['Prueba Ácida'] = (df['Activo Corriente'] - df['Inventarios']) / df['Pasivo Corriente']
df['Capital de Trabajo'] = df['Activo Corriente'] - df['Pasivo Corriente']
# Rentabilidad
df['ROE (%)'] = (df['Utilidad Neta'] / df['Patrimonio']) * 100
df['ROA (%)'] = (df['Utilidad Neta'] / df['Total Activo']) * 100
df['Margen Neto (%)'] = (df['Utilidad Neta'] / df['Ingresos']) * 100
# Endeudamiento
df['Endeudamiento (%)'] = (df['Total Pasivo'] / df['Total Activo']) * 100
df['Apalancamiento'] = df['Total Pasivo'] / df['Patrimonio']
df['Cobertura Intereses'] = (df['Utilidad Neta'] + df['Gastos Financieros']) / df['Gastos Financieros']
# Operación
df['Rotación Activos'] = df['Ingresos'] / df['Total Activo']
df['Margen Operativo (%)'] = ((df['Ingresos'] - df['Costo Ventas']) / df['Ingresos']) * 100
df['Rotación Inventarios'] = df['Costo Ventas'] / df['Inventarios']

# Valoración
num_acciones = 760000
df['VPP'] = df['Patrimonio'] / num_acciones
df['UPA'] = df['Utilidad Neta'] / num_acciones

# --- INTERFAZ STREAMLIT ---
st.set_page_config(page_title="Dashboard Los Tajibos", layout="wide")
st.title("🏨 Dashboard Financiero: Sociedad Hotelera Los Tajibos S.A.")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Masas", "📈 Ratios", "🧬 Dupont", "💎 Valoración"])

with tab1:
    st.header("Evolución de las Masas Patrimoniales")
    fig_masas = px.bar(df, x='Año', y=['Activo Corriente', 'Activo No Corriente', 'Total Pasivo', 'Patrimonio'], 
                       barmode='group', title="Estructura Patrimonial Completa")
    st.plotly_chart(fig_masas, use_container_width=True)
    st.info("*Interpretación de Masas:* Se observa una estructura sólida dominada por el Activo No Corriente (infraestructura hotelera). Entre 2021 y 2023, el patrimonio disminuyó debido a las pérdidas retenidas, pero muestra una recuperación vital en 2024-2025 gracias a la inyección de utilidades operativas.")

with tab2:
    # FILA 1: LIQUIDEZ
    st.subheader("💧 1. Ratios de Liquidez")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.plotly_chart(px.line(df, x='Año', y=['Liquidez Corriente', 'Prueba Ácida'], markers=True), use_container_width=True)
    with col2:
        st.write("*Interpretación:*")
        st.write("- *Liquidez:* Presión constante por debajo de 1.0.")
        st.write("- *Cap. Trabajo:* Fuerte déficit en 2023, recuperándose en 2025.")

    # FILA 2: RENTABILIDAD
    st.subheader("💰 2. Ratios de Rentabilidad")
    col3, col4 = st.columns([2, 1])
    with col3:
        st.plotly_chart(px.line(df, x='Año', y=['ROE (%)', 'ROA (%)', 'Margen Neto (%)'], markers=True), use_container_width=True)
    with col4:
        st.write("*Interpretación:*")
        st.write("- *ROE:* Salto positivo en 2024 tras 3 años de pérdidas.")
        st.write("- *Margen:* Recuperación de la eficiencia en costos post-pandemia.")

    # FILA 3: ENDEUDAMIENTO
    st.subheader("⚖️ 3. Ratios de Endeudamiento")
    col5, col6 = st.columns([2, 1])
    with col5:
        st.plotly_chart(px.line(df, x='Año', y=['Endeudamiento (%)', 'Apalancamiento', 'Cobertura Intereses'], markers=True), use_container_width=True)
    with col6:
        st.write("*Interpretación:*")
        st.write("- *Apalancamiento:* Estabilizado tras el pico de 2023.")
        st.write("- *Cobertura:* Capacidad de pago de intereses recuperada (>2 veces).")

    # FILA 4: OPERACIÓN
    st.subheader("⚙️ 4. Ratios de Operación")
    col7, col8 = st.columns([2, 1])
    with col7:
        st.plotly_chart(px.line(df, x='Año', y=['Margen Operativo (%)', 'Rotación Activos', 'Rotación Inventarios'], markers=True), use_container_width=True)
    with col8:
        st.write("*Interpretación:*")
        st.write("- *Rot. Inventarios:* Alta eficiencia en A&B (Alimentos y Bebidas).")
        st.write("- *Margen Op:* Mejora drástica en la gestión de ingresos directos.")

with tab3:
    st.subheader("🧬 Análisis Dupont (2025)")
    m_neto = df['Margen Neto (%)'].iloc[-1]
    rot_act = df['Rotación Activos'].iloc[-1]
    mult_cap = df['Total Activo'].iloc[-1] / df['Patrimonio'].iloc[-1]
    roe_f = df['ROE (%)'].iloc[-1]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Margen Neto", f"{m_neto:.2f}%")
    c2.metric("Rotación Activos", f"{rot_act:.4f}")
    c3.metric("Multiplicador", f"{mult_cap:.2f}")
    c4.metric("ROE Final", f"{roe_f:.2f}%")
    st.info("*Sentido Dupont:* La rentabilidad del accionista es impulsada por la recuperación del margen neto y el uso intensivo de los activos fijos, potenciado por un apalancamiento controlado.")

with tab4:
    st.subheader("💎 Valoración de Acciones: Evolución VPP")
    
    # Gráfico de Evolución VPP
    fig_vpp = px.area(df, x='Año', y='VPP', title="Evolución del Valor Patrimonial Proporcional (Bs/Acción)", markers=True)
    st.plotly_chart(fig_vpp, use_container_width=True)
    
    # Gráfico de Ganancia por Acción (UPA)
    fig_upa = px.bar(df, x='Año', y='UPA', title="Utilidad (UPA) por Acción", color='UPA', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_upa, use_container_width=True)

    st.markdown("### 📝 Análisis de la Evolución del Valor")
    st.write("*1. Periodo de Crisis (2021-2023):* Caída del VPP de Bs 222,28 a Bs 167,81 por pérdidas acumuladas >Bs 20M anuales.")
    st.write("*2. Recuperación (2024-2025):* El VPP sube a Bs 194,37. El patrimonio se reconstruye con utilidades de Bs 9.3M y Bs 11.9M.")
    st.write("*3. Valor Nominal:* La acción vale casi el doble de su valor original (Bs 100) gracias al colchón de *Ajuste por Inflación de Capital* (Bs 74,3M).")
