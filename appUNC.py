import streamlit as st
import pandas as pd
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión de Alumnos",
    page_icon="📚",
    layout="wide"
)

# Inicializar session_state
if 'df_final_inscriptos' not in st.session_state:
    st.session_state.df_final_inscriptos = None
if 'df_final_notas' not in st.session_state:
    st.session_state.df_final_notas = None
if 'promocionados_file' not in st.session_state:
    st.session_state.promocionados_file = None

# Función para procesar archivo de inscriptos
def procesar_inscriptos(uploaded_file, nombre_docente, df_promocionados):
    """Procesa un archivo de inscriptos y añade columna de docente y detalle"""
    try:
        # Leer el archivo Excel con header en fila 3
        df = pd.read_excel(uploaded_file, sheet_name='Reporte')
        
        # Eliminar filas vacías
        df = df.dropna(subset=['Legajo'])
        
        # Añadir columna de docente
        df['Docente'] = nombre_docente
        
        # Convertir columnas a string
        df['Legajo'] = df['Legajo'].astype(str).str.strip()
        
        if df_promocionados is not None:
            df_promocionados['DNI'] = df_promocionados['DNI'].astype(str).str.strip()
            dni_promocionados = set(df_promocionados['DNI'].unique())
            
            # Crear columna Detalle
            df['Detalle'] = df['Legajo'].apply(
                lambda x: 'Promocionado' if x in dni_promocionados else 'Regular'
            )
        else:
            df['Detalle'] = 'Regular'
        
        return df, None
    except Exception as e:
        return None, str(e)

# Función para procesar archivo de notas
def procesar_notas(uploaded_file, nombre_docente):
    """Procesa un archivo de notas y añade columna de docente"""
    try:
        df = pd.read_excel(uploaded_file)
        df['Docente'] = nombre_docente
        return df, None
    except Exception as e:
        return None, str(e)

# Función para convertir DataFrame a Excel en memoria
def to_excel(df):
    """Convierte un DataFrame a un archivo Excel en memoria"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    output.seek(0)
    return output

# Menú de navegación
st.sidebar.title("📚 Sistema de Gestión")
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "📋 Carga de Inscriptos", "📝 Carga de Notas", "📥 Descargas"]
)

# ==================== PÁGINA DE INICIO ====================
if pagina == "🏠 Inicio":
    st.title("📚 Sistema de Gestión de Alumnos UNC")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 📋 Carga de Inscriptos\nCarga archivos de inscripción de diferentes docentes y combínalos en una base unificada.")
    
    with col2:
        st.info("### 📝 Carga de Notas\nCarga archivos de notas de diferentes docentes para procesamiento posterior.")
    
    with col3:
        st.info("### 📥 Descargas\nVisualiza y descarga los archivos procesados en formato Excel.")
    
    st.markdown("---")
    st.markdown("""
    ### 📖 Instrucciones de uso:
    
    1. **Carga de Inscriptos**: 
       - Primero carga el archivo de promocionados (opcional)
       - Luego carga hasta 3 archivos Excel de inscripción
       - Para cada archivo, ingresa el nombre del docente
       - El sistema generará un archivo consolidado
    
    2. **Carga de Notas**: 
       - Carga hasta 3 archivos Excel con notas
       - Asigna el docente correspondiente a cada archivo
       - Los archivos se unificarán automáticamente
    
    3. **Descargas**: 
       - Visualiza los datos procesados
       - Personaliza el nombre del archivo
       - Descarga en formato Excel
    """)

# ==================== PÁGINA 1: CARGA DE INSCRIPTOS ====================
elif pagina == "📋 Carga de Inscriptos":
    st.title("📋 Carga de Inscriptos")
    st.markdown("---")
    
    # Sección para cargar archivo de promocionados
    st.subheader("📂 Paso 1: Cargar archivo de Promocionados (Opcional)")
    promocionados_file = st.file_uploader(
        "Selecciona el archivo de promocionados 2025",
        type=['xlsx', 'xls'],
        key='promocionados'
    )
    
    if promocionados_file:
        try:
            df_promocionados = pd.read_excel(promocionados_file)
            st.success(f"✅ Archivo cargado: {len(df_promocionados)} promocionados")
            st.session_state.promocionados_file = df_promocionados
        except Exception as e:
            st.error(f"❌ Error al cargar archivo: {str(e)}")
            df_promocionados = None
    else:
        df_promocionados = st.session_state.promocionados_file
    
    st.markdown("---")
    st.subheader("📂 Paso 2: Cargar archivos de Inscripción")
    
    # Crear 3 secciones para cargar archivos
    dataframes_list = []
    
    for i in range(1, 4):
        with st.expander(f"📄 Archivo {i} - Inscriptos", expanded=(i==1)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                uploaded_file = st.file_uploader(
                    f"Selecciona archivo Excel {i}",
                    type=['xlsx', 'xls'],
                    key=f'inscriptos_{i}'
                )
            
            with col2:
                nombre_docente = st.text_input(
                    f"Nombre del Docente",
                    key=f'docente_{i}',
                    placeholder="Ej: Prof. García"
                )
            
            if uploaded_file and nombre_docente:
                df, error = procesar_inscriptos(uploaded_file, nombre_docente, df_promocionados)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success(f"✅ Archivo procesado correctamente")
                    
                    # Análisis breve
                    total = len(df)
                    promocionados = (df['Detalle'] == 'Promocionado').sum()
                    regulares = (df['Detalle'] == 'Regular').sum()
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Total Alumnos", total)
                    col_b.metric("Promocionados", f"{promocionados} ({promocionados/total*100:.1f}%)")
                    col_c.metric("Regulares", f"{regulares} ({regulares/total*100:.1f}%)")
                    
                    # Vista previa
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    dataframes_list.append(df)
    
    # Botón para consolidar archivos
    st.markdown("---")
    if st.button("🔄 Consolidar Archivos", type="primary", use_container_width=True):
        if len(dataframes_list) > 0:
            # Concatenar todos los DataFrames
            df_consolidado = pd.concat(dataframes_list, ignore_index=True)
            st.session_state.df_final_inscriptos = df_consolidado
            
            st.success(f"✅ Archivos consolidados exitosamente: {len(df_consolidado)} registros totales")
            
            # Análisis consolidado
            st.subheader("📊 Resumen Consolidado")
            total = len(df_consolidado)
            promocionados = (df_consolidado['Detalle'] == 'Promocionado').sum()
            regulares = (df_consolidado['Detalle'] == 'Regular').sum()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Alumnos", total)
            col2.metric("Promocionados", promocionados)
            col3.metric("Regulares", regulares)
            col4.metric("Docentes", df_consolidado['Docente'].nunique())
            
            # Vista previa consolidada
            st.dataframe(df_consolidado, use_container_width=True)
            
            # Análisis por docente
            st.subheader("👥 Análisis por Docente")
            resumen_docentes = df_consolidado.groupby('Docente').agg({
                'Legajo': 'count',
                'Detalle': lambda x: (x == 'Promocionado').sum()
            }).rename(columns={'Legajo': 'Total', 'Detalle': 'Promocionados'})
            resumen_docentes['Regulares'] = resumen_docentes['Total'] - resumen_docentes['Promocionados']
            st.dataframe(resumen_docentes, use_container_width=True)
        else:
            st.warning("⚠️ No hay archivos para consolidar. Por favor, carga al menos un archivo.")

# ==================== PÁGINA 2: CARGA DE NOTAS ====================
elif pagina == "📝 Carga de Notas":
    st.title("📝 Carga de Notas")
    st.markdown("---")
    
    st.subheader("📂 Cargar archivos de Notas")
    
    dataframes_notas = []
    
    for i in range(1, 4):
        with st.expander(f"📄 Archivo {i} - Notas", expanded=(i==1)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                uploaded_file = st.file_uploader(
                    f"Selecciona archivo Excel {i}",
                    type=['xlsx', 'xls'],
                    key=f'notas_{i}'
                )
            
            with col2:
                nombre_docente = st.text_input(
                    f"Nombre del Docente",
                    key=f'docente_notas_{i}',
                    placeholder="Ej: Prof. García"
                )
            
            if uploaded_file and nombre_docente:
                df, error = procesar_notas(uploaded_file, nombre_docente)
                
                if error:
                    st.error(f"❌ Error: {error}")
                else:
                    st.success(f"✅ Archivo procesado correctamente")
                    
                    # Análisis breve
                    total = len(df)
                    col_a, col_b = st.columns(2)
                    col_a.metric("Total Registros", total)
                    col_b.metric("Columnas", len(df.columns))
                    
                    # Vista previa
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    dataframes_notas.append(df)
    
    # Botón para consolidar archivos de notas
    st.markdown("---")
    if st.button("🔄 Consolidar Archivos de Notas", type="primary", use_container_width=True):
        if len(dataframes_notas) > 0:
            # Concatenar todos los DataFrames
            df_consolidado_notas = pd.concat(dataframes_notas, ignore_index=True)
            st.session_state.df_final_notas = df_consolidado_notas
            
            st.success(f"✅ Archivos consolidados exitosamente: {len(df_consolidado_notas)} registros totales")
            
            # Análisis consolidado
            st.subheader("📊 Resumen Consolidado")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Registros", len(df_consolidado_notas))
            col2.metric("Docentes", df_consolidado_notas['Docente'].nunique())
            col3.metric("Columnas", len(df_consolidado_notas.columns))
            
            # Vista previa consolidada
            st.dataframe(df_consolidado_notas, use_container_width=True)
            
            # Análisis por docente
            st.subheader("👥 Análisis por Docente")
            resumen_docentes = df_consolidado_notas.groupby('Docente').size().reset_index(name='Total Registros')
            st.dataframe(resumen_docentes, use_container_width=True)
        else:
            st.warning("⚠️ No hay archivos para consolidar. Por favor, carga al menos un archivo.")

# ==================== PÁGINA 3: DESCARGAS ====================
elif pagina == "📥 Descargas":
    st.title("📥 Descargas")
    st.markdown("---")
    
    # Descargar archivo de Inscriptos
    st.subheader("📋 Archivo de Inscriptos Consolidado")
    
    if st.session_state.df_final_inscriptos is not None:
        df = st.session_state.df_final_inscriptos
        
        # Análisis breve
        total = len(df)
        promocionados = (df['Detalle'] == 'Promocionado').sum()
        regulares = (df['Detalle'] == 'Regular').sum()
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Alumnos", total)
        col2.metric("Promocionados", f"{promocionados} ({promocionados/total*100:.1f}%)")
        col3.metric("Regulares", f"{regulares} ({regulares/total*100:.1f}%)")
        col4.metric("Docentes", df['Docente'].nunique())
        
        # Vista previa
        st.dataframe(df, use_container_width=True)
        
        # Nombre del archivo y descarga
        col_a, col_b = st.columns([3, 1])
        with col_a:
            nombre_archivo_inscriptos = st.text_input(
                "Nombre del archivo (sin extensión)",
                value="Inscriptos_Consolidado",
                key='nombre_inscriptos'
            )
        
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            excel_data = to_excel(df)
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data,
                file_name=f"{nombre_archivo_inscriptos}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
    else:
        st.info("ℹ️ No hay datos de inscriptos para descargar. Por favor, procesa archivos en la página de 'Carga de Inscriptos'.")
    
    st.markdown("---")
    
    # Descargar archivo de Notas
    st.subheader("📝 Archivo de Notas Consolidado")
    
    if st.session_state.df_final_notas is not None:
        df_notas = st.session_state.df_final_notas
        
        # Análisis breve
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Registros", len(df_notas))
        col2.metric("Docentes", df_notas['Docente'].nunique())
        col3.metric("Columnas", len(df_notas.columns))
        
        # Vista previa
        st.dataframe(df_notas, use_container_width=True)
        
        # Nombre del archivo y descarga
        col_a, col_b = st.columns([3, 1])
        with col_a:
            nombre_archivo_notas = st.text_input(
                "Nombre del archivo (sin extensión)",
                value="Notas_Consolidado",
                key='nombre_notas'
            )
        
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            excel_data_notas = to_excel(df_notas)
            st.download_button(
                label="📥 Descargar Excel",
                data=excel_data_notas,
                file_name=f"{nombre_archivo_notas}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary"
            )
    else:
        st.info("ℹ️ No hay datos de notas para descargar. Por favor, procesa archivos en la página de 'Carga de Notas'.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Sistema UNC")
st.sidebar.markdown("Versión 1.0")