import os
import base64
import mimetypes
import json
import re
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image
import requests
from typing import Optional, Dict, Any, List


# API Configuration
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def get_api_keys() -> Dict[str, str]:
    """Obtiene las API keys disponibles desde variables de entorno."""
    load_dotenv()
    keys = {}
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        keys["openai"] = openai_key
        
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key:
        keys["deepseek"] = deepseek_key
    
    return keys


def validate_image_file(image_path):
    """Validar que el archivo sea un formato de imagen soportado."""
    try:
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
        file_extension = Path(image_path).suffix.lower()
        
        if file_extension not in valid_extensions:
            print(f"Error: Formato no soportado {file_extension}. Soportados: JPG, PNG, WEBP, GIF.")
            return False
        
        # Verificar que el archivo se pueda abrir como imagen
        with Image.open(image_path) as img:
            width, height = img.size
            if width > 2048 or height > 2048:
                print(f"Advertencia: Imagen {width}x{height} es muy grande. Recomendado: máximo 2048x2048")
                
        # Verificar tamaño de archivo (límite 20MB)
        file_size = os.path.getsize(image_path)
        if file_size > 20 * 1024 * 1024:  # 20MB
            print(f"Advertencia: Archivo {file_size/1024/1024:.1f}MB es muy grande")
            
        return True
    except Exception as e:
        print(f"Error validando imagen: {e}")
        return False


def encode_image_to_base64(image_path):
    """Codificar imagen a base64 para transmisión API."""
    try:
        # Optimizar imagen si es muy grande
        with Image.open(image_path) as img:
            if img.size[0] > 2048 or img.size[1] > 2048:
                print(f"📏 Redimensionando imagen de {img.size[0]}x{img.size[1]} a máximo 2048x2048")
                img.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
                
                # Guardar imagen redimensionada temporalmente
                temp_path = f"/tmp/temp_resized_{Path(image_path).name}"
                img.save(temp_path, format=img.format or 'JPEG', quality=85, optimize=True)
                image_path = temp_path
        
        # Codificar a base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Limpiar archivo temporal si se creó
        if 'temp_resized_' in image_path:
            os.remove(image_path)
            
        return encoded_string
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


def get_mime_type(image_path):
    """Obtener tipo MIME para el archivo de imagen."""
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type and mime_type.startswith('image/'):
        return mime_type
    
    # Fallback basado en extensión
    extension = Path(image_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
        '.gif': 'image/gif'
    }
    return mime_types.get(extension, 'image/jpeg')


def analyze_image_with_openai(image_path: str, custom_prompt: Optional[str] = None,
                              model: str = "gpt-4o", api_key: str = None) -> Optional[Dict[str, Any]]:
    """Analiza imagen usando OpenAI GPT-4 Vision."""
    
    if not custom_prompt:
        custom_prompt = (
            "Describe detalladamente lo que observas en esta imagen. "
            "Sé específico sobre los elementos visibles, colores, composición, "
            "personas, objetos, texto, y cualquier detalle relevante. "
            "Mantén la descripción objetiva y basada únicamente en lo que puedes ver directamente. "
            "Al final, proporciona un JSON con las entidades detectadas usando este formato: "
            '{ "entidades": [ { "tipo": "persona|objeto|lugar|texto|forma|color", "nombre": "string", "confianza": 0-1, "detalles": "descripción" } ], "elementos_visuales": { "colores_principales": [], "composicion": "descripción", "iluminacion": "descripción" } }'
        )

    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return None
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": custom_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 4000,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_text = response.text[:300]
            print(f"❌ Error OpenAI {response.status_code}: {error_text}")
            return None
            
    except Exception as e:
        print(f"💥 Error llamando OpenAI: {e}")
        return None


def analyze_image_with_deepseek_text(image_path: str, custom_prompt: Optional[str] = None,
                                   api_key: str = None) -> Optional[Dict[str, Any]]:
    """Analiza metadatos de imagen usando DeepSeek (sin visión)."""
    
    try:
        with Image.open(image_path) as img:
            w, h = img.size
            fmt = img.format or "Unknown"
    except Exception:
        w, h, fmt = ("?", "?", "?")

    meta_prompt = (
        f"[ANÁLISIS DE METADATOS DE IMAGEN]\n"
        f"Nombre: {Path(image_path).name}\n" 
        f"Formato: {fmt}\n"
        f"Dimensiones: {w}x{h}\n\n"
        f"LIMITACIÓN: No tengo capacidad de visión para ver el contenido real de la imagen.\n\n"
        f"Como experto en análisis de imágenes, explica:\n"
        f"1. Qué información específica faltaría para hacer un análisis objetivo completo\n"
        f"2. Qué metodología usarías si pudieras ver la imagen\n"
        f"3. Proporciona un framework JSON de ejemplo de cómo estructurarías el análisis\n\n"
        f"Instrucciones adicionales del usuario: {custom_prompt or 'Análisis estándar'}"
    )
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": meta_prompt}],
        "temperature": 0.1,
        "max_tokens": 3000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            error_text = response.text[:300]
            print(f"❌ Error DeepSeek {response.status_code}: {error_text}")
            return None
            
    except Exception as e:
        print(f"💥 Error llamando DeepSeek: {e}")
        return None


def analyze_image(image_path: str, custom_prompt: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Analiza imagen usando el mejor API disponible."""
    
    if not validate_image_file(image_path):
        return None
        
    api_keys = get_api_keys()
    
    if not api_keys:
        print("❌ No se encontraron API keys configuradas")
        print("💡 Configura al menos una de estas variables de entorno:")
        print("   - OPENAI_API_KEY (recomendado para análisis de imágenes)")
        print("   - DEEPSEEK_API_KEY (solo metadatos)")
        return None
    
    print(f"🔍 APIs disponibles: {list(api_keys.keys())}")
    
    # Priorizar OpenAI para análisis de imágenes real
    if "openai" in api_keys:
        print("→ Usando OpenAI GPT-4 Vision para análisis completo de imagen")
        result = analyze_image_with_openai(image_path, custom_prompt, api_key=api_keys["openai"])
        if result:
            return result
        print("⚠️  OpenAI falló, intentando con DeepSeek...")
    
    # Fallback a DeepSeek para análisis de metadatos
    if "deepseek" in api_keys:
        print("→ Usando DeepSeek para análisis de metadatos (sin visión)")
        return analyze_image_with_deepseek_text(image_path, custom_prompt, api_key=api_keys["deepseek"])
    
    return None


def extract_json_block(text: str) -> Optional[Dict[str, Any]]:
    """Intenta extraer un bloque JSON del texto de la respuesta."""
    if not text:
        return None
        
    # Busca el primer '{' que abra un JSON hasta su cierre balanceado
    brace_stack = []
    start_idx = None
    
    for i, ch in enumerate(text):
        if ch == '{':
            if start_idx is None:
                start_idx = i
            brace_stack.append('{')
        elif ch == '}':
            if brace_stack:
                brace_stack.pop()
                if not brace_stack and start_idx is not None:
                    candidate = text[start_idx:i+1]
                    try:
                        return json.loads(candidate)
                    except json.JSONDecodeError:
                        pass
    return None


def display_response(response: Optional[Dict[str, Any]]):
    """Muestra la respuesta formateada e intenta extraer JSON de entidades."""
    if not response:
        print("❌ No response received")
        return
        
    if not response.get('choices'):
        print("❌ Respuesta sin 'choices':", list(response.keys()))
        return
        
    choice = response['choices'][0]
    content = choice['message'].get('content')
    
    if not content:
        print("❌ Contenido vacío en la respuesta")
        return
    
    print("\n" + "="*60)
    print("🖼️  ANÁLISIS DE IMAGEN")
    print("="*60)
    print(content)
    print("="*60)
    
    # Intentar extraer JSON de entidades
    json_block = extract_json_block(content)
    if json_block:
        print("\n🏷️  ENTIDADES DETECTADAS (JSON):")
        print(json.dumps(json_block, ensure_ascii=False, indent=2))
    
    # Mostrar información del modelo
    model_used = choice.get('model', 'unknown')
    print(f"\n🤖 Modelo usado: {model_used}")
    
    # Mostrar información de uso si está disponible
    if 'usage' in response:
        usage = response['usage']
        total_tokens = usage.get('total_tokens', 'N/A')
        print(f"📊 Tokens usados: {total_tokens}")


def get_user_image_path():
    """Obtener ruta de imagen del usuario con validación."""
    while True:
        image_path = input("\n📁 Ingresa la ruta completa de la imagen: ").strip()
        
        if not image_path:
            print("⚠️  Por favor ingresa una ruta válida")
            continue
            
        if not os.path.exists(image_path):
            print("❌ El archivo no existe. Verifica la ruta.")
            continue
        
        return image_path


def get_custom_prompt():
    """Obtener prompt personalizado del usuario."""
    print("\n❓ ¿Deseas usar un prompt personalizado para el análisis?")
    print("(Presiona Enter para usar el prompt optimizado por defecto)")
    custom_prompt = input("Prompt personalizado: ").strip()
    
    return custom_prompt if custom_prompt else None


def main():
    """Punto de entrada principal."""
    try:
        print("🔬 Analizador de Imágenes con IA")
        print("="*40)
        print("🎯 Prioridad: OpenAI GPT-4 Vision > DeepSeek")
        print("📸 Soporta: JPG, PNG, WEBP, GIF")
        
        image_path = get_user_image_path()
        print(f"✅ Imagen seleccionada: {Path(image_path).name}")
        
        custom_prompt = get_custom_prompt()
        
        print("\n⏳ Analizando imagen...")
        response = analyze_image(image_path, custom_prompt)
        
        display_response(response)
        
        if response:
            save_option = input("\n💾 ¿Deseas guardar el análisis en un archivo? (s/n): ").strip().lower()
            if save_option == 's':
                save_analysis_to_file(response, image_path)
        
    except KeyboardInterrupt:
        print("\n👋 Análisis cancelado por el usuario")
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()


def save_analysis_to_file(response: Optional[Dict[str, Any]], image_path: str):
    """Guarda el análisis en un archivo."""
    try:
        if not response or 'choices' not in response:
            print("❌ No hay análisis para guardar")
            return
            
        content = response['choices'][0]['message'].get('content')
        if not content:
            print("❌ No se pudo extraer contenido para guardar")
            return
        
        image_name = Path(image_path).stem
        output_filename = f"analisis_imagen_{image_name}.txt"
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(f"ANÁLISIS DE IMAGEN: {Path(image_path).name}\n")
            f.write("="*60 + "\n\n")
            f.write(content + "\n\n")
            
            # JSON si está disponible
            json_block = extract_json_block(content)
            if json_block:
                f.write("JSON ESTRUCTURADO:\n")
                f.write(json.dumps(json_block, ensure_ascii=False, indent=2))
                f.write("\n\n")
            
            # Información técnica
            model_used = response['choices'][0].get('model', 'unknown')
            f.write(f"Modelo usado: {model_used}\n")
            
            if 'usage' in response:
                usage = response['usage']
                f.write(f"Tokens utilizados: {usage.get('total_tokens', 'N/A')}\n")
            
            f.write(f"\nGenerado el: {os.popen('date').read().strip()}\n")
        
        print(f"✅ Análisis guardado en: {output_filename}")
        
    except Exception as e:
        print(f"💥 Error guardando archivo: {e}")


if __name__ == "__main__":
    main()