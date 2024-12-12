import streamlit as st
from simplekml import Kml, Types
from PIL import Image
import base64
from io import BytesIO
from css import css

def create_kmz(image_data):
    kml = Kml()
    for idx, (img, lat, lon, comm) in enumerate(image_data):
        if img is not None:
            lat_decimal = convert_to_decimal(lat)
            lon_decimal = convert_to_decimal(lon)
            
            # Abrir la imagen con PIL y redimensionarla a 1920x1080
            pil_image = Image.open(img)
            pil_image = pil_image.resize((1920, 1080))
            
            # Guardar la imagen redimensionada en un buffer
            buffer = BytesIO()
            pil_image.save(buffer, format='JPEG')
            buffer.seek(0)
            
            # Obtener los bytes de la imagen redimensionada
            image_data_bytes = buffer.getvalue()
            
            # Codificar la imagen en base64
            image_base64 = base64.b64encode(image_data_bytes).decode('utf-8')
            
            # Crear punto en el KML
            pnt = kml.newpoint(name=f"Imagen {idx + 1}", coords=[(lon_decimal, lat_decimal)])
            pnt.description = f"<img src='data:image/jpeg;base64,{image_base64}' width='400' /><br>{comm}"
            # Especificar el ícono
            pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
    
    # Guardar KML en un buffer
    buffer = BytesIO()
    kml.savekmz(buffer)
    buffer.seek(0)
    return buffer

def convert_to_decimal(deg_min_sec):
    # Convierte grados, minutos y segundos a decimal
    degrees, minutes, seconds = deg_min_sec
    return (degrees + (minutes / 60) + (seconds / 3600))*-1 # Hemisferior sur son valores negativos

def main():
    st.set_page_config(page_title='IMG a KMZ', layout = 'centered', page_icon = 'world_map', initial_sidebar_state = 'auto')
    st.title('Generador de KMZ de fotos Georeferenciadas 🗺️')
    st.header('Aplicación genera un archivo KMZ a partir de fotos subidas con sus respectivas coordenadas')
    st.markdown(css, unsafe_allow_html=True)
    
    # Inicializar lista de imágenes, coordenadas y comentarios si no existen en session_state
    if 'image_data' not in st.session_state:
        st.session_state.image_data = []

    with st.form(key='uploader_form'):
        # Número de sets de imágenes y coordenadas para subir
        num_sets = st.number_input('**Número de imágenes a subir, presionar enter después indicar cantidad de imágenes**', min_value=1, max_value=10, value=len(st.session_state.image_data) or 1)
        
        new_image_data = []
        for i in range(int(num_sets)):
            st.write(f'### **Imagen {i + 1}:**')
            uploaded_image = st.file_uploader(f'**Seleccionar imagen {i + 1}**', type=['png', 'jpg', 'jpeg'], key=f'file_uploader_{i}')
            
            # Coordenadas
            st.write('**Latitud:** Para nuestra región la latitud casi siempre comienza con 42')
            col1, col2, col3 = st.columns(3)
            with col1:
                lat_grados = st.number_input('Grados', min_value=-0, max_value=90, key=f'lat_grados_{i}')
            with col2:
                lat_minutos = st.number_input('Minutos', min_value=0, max_value=59, key=f'lat_minutos_{i}')
            with col3:
                lat_segundos = st.number_input('Segundos', min_value=0.0, max_value=59.999, format="%.3f", key=f'lat_segundos_{i}')
            st.write('**Longitud:** Para nuestra región la longitud casi siempre comienza con 73')
            col4, col5, col6 = st.columns(3)
            with col4:
                lon_grados = st.number_input('Grados', min_value=0, max_value=180, key=f'lon_grados_{i}')
            with col5:
                lon_minutos = st.number_input('Minutos', min_value=0, max_value=59, key=f'lon_minutos_{i}')
            with col6:
                lon_segundos = st.number_input('Segundos', min_value=0.0, max_value=59.999, format="%.3f", key=f'lon_segundos_{i}')
            
            # Comentario
            comentario = st.text_area('**Comentario fotografía**', max_chars=250, key=f'comentario_{i}')

            new_image_data.append((uploaded_image, (lat_grados, lat_minutos, lat_segundos), (lon_grados, lon_minutos, lon_segundos), comentario))
        
        submit_button = st.form_submit_button('Guardar datos')

    if submit_button:
        st.session_state.image_data = new_image_data  # Actualiza el estado global con los nuevos datos
        kmz_buffer = create_kmz(st.session_state.image_data)  # Crear archivo KMZ
        st.download_button(label="Descargar KMZ", data=kmz_buffer, file_name="fotos_georeferenciadas.kmz", mime="application/vnd.google-earth.kmz")
        st.success('Archivo KMZ creado y listo para descargar!')

    # Visualizar imágenes, coordenadas y comentarios subidos
    if st.session_state.image_data:
        st.write('Imágenes, coordenadas y comentarios subidos:')
        for idx, (img, lat, lon, comm) in enumerate(st.session_state.image_data, start=1):
            if img is not None:
                st.write(f"Imagen {idx}: {img.name}, Coordenadas: Latitud {lat}, Longitud {lon}, Comentario: {comm}")
            else:
                st.write(f"Imagen {idx}: No subida, Coordenadas: Latitud {lat}, Longitud {lon}, Comentario: {comm}")


    st.markdown("""
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    <div class="centered-text">
    Diseñado y programado por Manuel Cano N., Castro, 2024
    </div>
    """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
