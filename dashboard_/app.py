import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mapa de Calor Turístico", layout="wide")

st.markdown("""
# **Mapa de Calor y Demanda Turística**
Visualiza la distribución de sitios turísticos y la demanda por municipio.
""")

BASE_URL = "http://127.0.0.1:8000"

def obtener_sitios(dep):
    if not dep:
        return pd.DataFrame()
    try:
        resp = requests.get(f"{BASE_URL}/foursquare/sities_clean?departamento={dep}", timeout=10)
        resp.raise_for_status()
        return pd.DataFrame(resp.json().get("sitios", []))
    except:
        return pd.DataFrame()

def obtener_reseñantes(dep):
    if not dep:
        return pd.DataFrame()
    try:
        resp = requests.get(f"{BASE_URL}/foursquare/reseñantes?departamento={dep}", timeout=10)
        resp.raise_for_status()
        return pd.DataFrame(resp.json().get("reseñantes", []))
    except:
        return pd.DataFrame()

with st.sidebar:
    st.header("⚙️ Filtro del Departamento")
    departamento = st.text_input(" Departamento:", placeholder="Ejemplo: Atlántico")

if departamento:
    df_sities = obtener_sitios(departamento)
    df_reviewers = obtener_reseñantes(departamento)

    if df_sities.empty:
        st.warning(" No se encontraron sitios para este departamento.")
    else:
        df_sities = df_sities.dropna(subset=["latitude", "longitude"])
        df_sities["num_sitios"] = 1

        total_sitios = len(df_sities)
        total_reseñantes = len(df_reviewers)
        total_categorias = df_sities["categoria"].nunique() if "categoria" in df_sities.columns else 0

        st.markdown("### 📊 Indicadores Generales")
        c1, c2, c3 = st.columns(3)
        c1.metric(label="🏖️ Total de Sitios", value=f"{total_sitios:,}")
        c2.metric(label="💬 Total de Reseñantes", value=f"{total_reseñantes:,}")
        c3.metric(label="🏷️ Categorías", value=f"{total_categorias:,}")
        st.markdown("---")

        # ===============================
        # LAYOUT PRINCIPAL (Mapa + Top Categorías)
        # ===============================
        col1, col2 = st.columns([2.8, 1.0])  # <-- col2 más estrecha para el top

        # --- Mapa de calor (ahora usando density_map moderno)
        with col1:
            fig_map = px.density_map(
                df_sities,
                lat="latitude",
                lon="longitude",
                z="num_sitios",
                radius=18,
                hover_name="nombre",
                hover_data={"categoria": True, "num_sitios": True},
                color_continuous_scale="rainbow",
                title=f" Mapa de Calor - {departamento}",
                height=500
            )
            fig_map.update_layout(
                margin=dict(l=0, r=0, t=40, b=0),
                coloraxis_colorbar=dict(
                    title=dict(text="Sitios", side="right")  # ✅ reemplazo de titleside
                ),
            )
            st.plotly_chart(fig_map, use_container_width=True)

       # --- Top Categorías (en cuadro tipo tarjeta)
        with col2:
            if "categoria" in df_sities.columns:
                df_top = (
                    df_sities.groupby("categoria")
                    .size()
                    .reset_index(name="cantidad")
                    .sort_values("cantidad", ascending=False)
                    .head(10)
                )

                # Paleta de colores (10 colores)
                colors = [
                    "#00B3A4", "#F39C12", "#E74C3C", "#9B59B6", "#3498DB",
                    "#1ABC9C", "#2ECC71", "#E67E22", "#16A085", "#7F8C8D"
                ]

                # Título con estilo uniforme (sin fondo ni sombreado)
                st.markdown("""
                    <h5 style="text-align:center; color:#333; margin-bottom:15px; font-weight:600;">
                         Top Categorías 
                    </h5>
                """, unsafe_allow_html=True)

                # Estilo CSS con tooltip
                st.markdown("""
                    <style>
                        .bar-container {
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                            margin-bottom: 8px;
                        }
                        .bar-label {
                            flex: 1;
                            text-align: left;
                            font-size: 13px;
                            color: #333;
                            padding-right: 6px;
                        }
                        .bar-wrapper {
                            position: relative;
                            flex: 3;
                            height: 14px;
                            background-color: #f2f2f2;
                            border-radius: 6px;
                        }
                        .bar {
                            height: 100%;
                            border-radius: 6px;
                            transition: opacity 0.2s;
                        }
                        .bar:hover {
                            opacity: 0.8;
                        }
                        .bar::after {
                            content: attr(data-tooltip);
                            position: absolute;
                            top: -24px;
                            left: 50%;
                            transform: translateX(-50%);
                            background-color: rgba(0, 0, 0, 0.75);
                            color: white;
                            font-size: 11px;
                            padding: 2px 6px;
                            border-radius: 4px;
                            opacity: 0;
                            pointer-events: none;
                            transition: opacity 0.2s;
                        }
                        .bar-wrapper:hover .bar::after {
                            opacity: 1;
                        }
                        .bar-value {
                            width: 40px;
                            text-align: right;
                            font-size: 13px;
                            color: #333;
                            margin-left: 6px;
                        }
                    </style>
                """, unsafe_allow_html=True)

                # Crear barras de colores
                max_val = df_top["cantidad"].max()
                for i, row in enumerate(df_top.itertuples(), start=0):
                    color = colors[i % len(colors)]  # Cicla los colores si hay más de 10
                    width = (row.cantidad / max_val) * 100
                    st.markdown(
                        f"""
                        <div class="bar-container">
                            <div class="bar-label">{row.categoria}</div>
                            <div class="bar-wrapper">
                                <div class="bar" style="width:{width}%; background-color:{color};" data-tooltip="{row.cantidad} sitios"></div>
                            </div>
                            <div class="bar-value">{row.cantidad}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("No hay datos de categorías para este departamento.")



        # ===============================
        # GRÁFICA DE DEMANDA TURÍSTICA (debajo del mapa)
        # ===============================
        st.markdown("---")
        st.markdown(f"### Demanda Turística por Municipio - {departamento}")

        if df_reviewers.empty:
            st.warning("No se encontraron reseñantes para este departamento.")
        else:
            # Agrupar los datos por municipio
            df_count = df_reviewers.groupby("municipio").size().reset_index(name="valor")
            df_count = df_count.sort_values("valor", ascending=False)

            # Crear gráfico de barras
            fig_demand = px.bar(
                df_count,
                x="municipio",
                y="valor",
                color="municipio",
                text="valor",  # 🔹 Muestra los valores sobre las barras
                title="Demanda Turística por Municipio",
                height=500,
                color_discrete_sequence=px.colors.qualitative.Set2  # 🔹 Colores suaves y variados
            )

            # Ajustes estéticos
            fig_demand.update_traces(
                textposition="outside",
                textfont_size=12
            )

            fig_demand.update_layout(
                xaxis_title="",  # 🔹 Sin etiqueta en eje X
                yaxis_title="valor",
                xaxis_tickangle=-45,
                legend_title="municipio",
                margin=dict(l=20, r=20, t=50, b=100),
                plot_bgcolor="white"
            )

            # Mostrar gráfico en Streamlit
            st.plotly_chart(fig_demand, use_container_width=True)