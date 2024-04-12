# CHONQUE DEL MONTE
![Chonque del Monte](/static/img/LOGO.png)

# Aplicación para generar KMZ a partir de fotos y coordenadas

Este repositorio contiene una simple aplicación para facilitar un flujo de trabajo consistente en generar una ayuda visual a una actividad de terreno. 

## Descripción general

A partir de una fotografía y sus respectivas coordenadas geográficas, es posible obtener un archivo KMZ útil para visualizar dichas imágenes en Google Earth. Adicionalmente se le puede incorporar un comentario para acompañar la fotografía resultante. Acepta una o muchas fotografías.

### Características principales

- **Streamlit** Framework de Python pusado para crear la interfaz web con el Chatbot
- **simplekml** Librería (package) para Python, para crear o generar archivos KML o KMZ

### Pre requisitos

- Python 3.10
- Streamlit
- simplekml

## Uso

Indicar la cantidad de imágenes a georeferenciar, pueden ser tantas como sea necesario. Luego, indicar las coordenadas de dicha foto. Para mayor claridad de uso se recomienda utilizar la aplicación **Timestamp** de android que incorpora la coordenada a la foto como un overlay. Finalmente se agrega un comentario. Cuando se tenga lista la información se aprieta en "Guardar datos" y luego en "Generar KMZ". El navegador entrega de forma automática un archivo KMZ llamado "fotos_georeferenciadas.kmz"

## A tener en consideración y ToDo:

Se pueden incorporar mayores funcionalidades, incluido un tutorial.
