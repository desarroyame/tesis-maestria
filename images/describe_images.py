"""
Este script realiza las siguientes acciones:

1. Importa las bibliotecas necesarias: anthropic, os, dotenv, base64, PIL y io.
2. Carga las variables de entorno desde un archivo .env utilizando load_dotenv().
3. Crea una instancia del cliente de Anthropic utilizando la clave de API obtenida de las variables de entorno.
4. Solicita al usuario que ingrese la ruta de la imagen que desea procesar.
5. Abre la imagen utilizando PIL y la guarda en un objeto BytesIO para manipularla en memoria.
6. Si el tamaño de la imagen supera los 4 MB, reduce su tamaño a la mitad repetidamente hasta que su tamaño sea menor o igual a 4 MB.
7. Codifica la imagen en base64 para ser enviada a la API.
8. Determina el tipo de media de la imagen basado en su extensión de archivo.
9. Crea un mensaje para la API de Anthropic que incluye la imagen codificada en base64 y una solicitud de descripción de la imagen.
10. Envía el mensaje a la API utilizando el método client.messages.create() y imprime la respuesta en la consola.
"""

import anthropic
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

image_path = input("Por favor, ingrese la ruta de la imagen: ")

with Image.open(image_path) as img:
    img_format = img.format
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=img_format)
    img_size = img_bytes.tell()

    while img_size > 4 * 1024 * 1024:  # 4 MB
        img = img.resize((img.width // 2, img.height // 2))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img_format)
        img_size = img_bytes.tell()

    img_bytes.seek(0)
    image_data = base64.b64encode(img_bytes.read()).decode('utf-8')

if image_path.endswith(".jpg") or image_path.endswith(".jpeg"):
    image_media_type = "image/jpeg"
elif image_path.endswith(".png"):
    image_media_type = "image/png"
elif image_path.endswith(".gif"):
    image_media_type = "image/gif"
elif image_path.endswith(".bmp"):
    image_media_type = "image/bmp"
elif image_path.endswith(".tiff") or image_path.endswith(".tif"):
    image_media_type = "image/tiff"
else:
    image_media_type = "application/octet-stream"  

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=3000,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "Describe la imagen, sin apreciaciones ni interpretación. No trates de identificar o descripbor personas. Redacta de manera compacta en un solo párrafo, como si fuera el requerimiento para que artista de XR reconstruya la escena. No incluir requerimientos técnicos ni Tareas para el Artista XR. La estructura de la descripción"
                }
            ],
        }
    ],
)
print(message)