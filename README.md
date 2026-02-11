# 📚 Sistema de Gestión de Alumnos UNC

Aplicación web desarrollada con Streamlit para la gestión de inscriptos y notas de alumnos.

## 🚀 Instalación

### 1. Instalar Python
Asegúrate de tener Python 3.8 o superior instalado en tu sistema.

### 2. Instalar dependencias
Abre una terminal en la carpeta del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- Streamlit (framework web)
- Pandas (procesamiento de datos)
- OpenPyXL (lectura/escritura de Excel)
- XLRD (soporte para archivos .xls)

## 🎯 Cómo ejecutar la aplicación

1. Abre una terminal en la carpeta donde guardaste `app_streamlit.py`

2. Ejecuta el siguiente comando:
```bash
streamlit run app_streamlit.py
```

3. La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Guía de uso

### Página 1: Carga de Inscriptos 📋

1. **Paso 1**: (Opcional) Carga el archivo de promocionados 2025
   - Formato: Excel (.xlsx o .xls)
   - Debe contener una columna "DNI"

2. **Paso 2**: Carga hasta 3 archivos de inscripción
   - Para cada archivo:
     - Selecciona el archivo Excel
     - Ingresa el nombre del docente
     - El sistema procesará automáticamente
   - Los archivos deben tener la estructura:
     - Sheet: "Reporte"
     - Columnas: Legajo, Alumno, Instancia, Estado
     - Headers en la fila 3

3. **Paso 3**: Haz clic en "Consolidar Archivos"
   - Se generará un archivo unificado
   - Se añadirá columna "Docente" y "Detalle" (Promocionado/Regular)
   - Verás análisis estadísticos por docente

### Página 2: Carga de Notas 📝

1. Carga hasta 3 archivos de notas en formato Excel
2. Para cada archivo, ingresa el nombre del docente
3. Haz clic en "Consolidar Archivos de Notas"
4. Se generará un archivo unificado con columna "Docente"

### Página 3: Descargas 📥

1. **Inscriptos Consolidado**:
   - Vista previa del archivo procesado
   - Análisis estadístico (total, promocionados, regulares)
   - Personaliza el nombre del archivo
   - Descarga en formato Excel

2. **Notas Consolidado**:
   - Vista previa del archivo procesado
   - Análisis por docente
   - Personaliza el nombre del archivo
   - Descarga en formato Excel

## 📊 Características principales

✅ Procesamiento de múltiples archivos Excel simultáneamente
✅ Identificación automática de alumnos promocionados vs regulares
✅ Asignación de docente a cada conjunto de datos
✅ Consolidación automática de múltiples fuentes
✅ Análisis estadístico en tiempo real
✅ Vista previa de datos antes de descargar
✅ Nombres de archivo personalizables
✅ Interfaz intuitiva y moderna

## 🔧 Solución de problemas

### Error: "KeyError: 'Legajo'"
- Verifica que el archivo Excel tenga el formato correcto
- Los headers deben estar en la fila 3
- El sheet debe llamarse "Reporte"

### Error al instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### La aplicación no se abre en el navegador
Abre manualmente: http://localhost:8501

## 📝 Estructura de archivos esperada

### Archivo de Inscriptos:
```
Sheet: "Reporte"
Fila 3 (headers): Legajo | Alumno | Instancia | Estado
```

### Archivo de Promocionados:
```
Columna: DNI
```

## 🆘 Soporte

Si encuentras algún problema:
1. Verifica que todos los archivos tengan el formato correcto
2. Revisa que las dependencias estén instaladas
3. Consulta los mensajes de error en la aplicación

---

**Versión**: 1.0
**Desarrollado con**: Streamlit + Pandas
