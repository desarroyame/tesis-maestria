from dotenv import load_dotenv
import os
import base64
from PIL import Image
import io
import anthropic

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)

image_path = "./2011 Nicolas Van Hemelryck - San Juan sin Dios055.jpg"

with Image.open(image_path) as img:
    img_format = img.format
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=img_format)
    img_size = img_bytes.tell()

    while img_size > 2 * 1024 * 1024:  
        img = img.resize((int(img.width * 0.8), int(img.height * 0.8)))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img_format, quality=90)
        img_size = img_bytes.tell()

    img_bytes.seek(0)
    image_data = base64.b64encode(img_bytes.read()).decode('utf-8')

metodologia = """La metodología de análisis de la imagen se basa en Didi-Huberman sobre el método de montaje de Walter Benjamin y el modelo M12 de Rubén Dittus. A continuación, te presento el diagrama mermaid que agrupa los elementos visibles en la imagen de acuerdo con las categorías: anacronismo e imagen-síntoma."""

if image_path.lower().endswith(('.jpg', '.jpeg')):
    image_media_type = "image/jpeg"
elif image_path.lower().endswith('.png'):
    image_media_type = "image/png"
else:
    image_media_type = "application/octet-stream"

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data
                    }
                },
                {
                    "type": "text", 
                    "text": f"""Describe en español académico la imagen objetivamente en un párrafo compacto. Sin crear conceptos direrentes a los enunciados en la{metodologia}. El diagrama mermaid debe ser presentado en la siguiente estrucura:
                    graph TD
                        A[[Anacronismo]]
                        B[[Imagen-Síntoma]]
                        
                        A --> A1[Elementos temporales distorsionados]
                        A --> B2[Contradicciones de época]
                        
                        B --> B1[Reflejo de la sociedad]
                        B --> B2[Condiciones del presente]
                        B --> B3[Fenómenos ocultos que se revelan]
                    """
                }
            ]
        }
    ]
)

print(message.content)
