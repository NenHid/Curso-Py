"""
demo_03_asistente_email_llm.py
------------------------------
Automatización Avanzada: Integración de IMAP (Lectura de Gmail) + LLM (OpenAI/Groq).
1. Lee el último correo no leído de Gmail.
2. Un LLM analiza el contenido, detecta la urgencia y redacta una respuesta sugerida.
3. Imprime el análisis en consola (y opcionalmente puede enviar la respuesta automáticamente).
"""

import os
import json
from openai import OpenAI

# Importamos las funciones de los scripts anteriores
from demo_02_leer_email import leer_ultimos_correos
from demo_01_enviar_email import enviar_correo

# Cargar variables de entorno
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Inicializar cliente OpenAI
# TIP: Si usas Groq (gratis), agrega: base_url="https://api.groq.com/openai/v1", api_key="gsk_..."
client = OpenAI()

def analizar_correo_con_ia(remitente: str, asunto: str, cuerpo: str):
    """
    Envía el contenido del correo a un LLM para extraer categoría, urgencia y redactar respuesta.
    """
    prompt_sistema = """
    Eres un asistente virtual de correo electrónico para un profesional.
    Tu tarea es leer el correo entrante y generar un análisis estructurado en formato JSON con las siguientes claves:
    {
        "categoria": "cliente" | "urgente" | "spam" | "informativo" | "facturacion",
        "urgencia": "alta" | "media" | "baja",
        "resumen": "Resumen conciso en 1 o 2 oraciones",
        "respuesta_sugerida": "Borrador de respuesta formal, empática y lista para enviar"
    }
    Responde ÚNICAMENTE con el objeto JSON válido.
    """

    contenido_usuario = f"""
    Remitente: {remitente}
    Asunto: {asunto}
    Contenido del correo:
    {cuerpo}
    """

    try:
        respuesta = client.chat.completions.create(
            model="gpt-4o-mini", # O si usas Groq: "llama-3.3-70b-versatile"
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": contenido_usuario}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(respuesta.choices[0].message.content)
    except Exception as e:
        print(f"❌ Error al consultar el LLM: {e}")
        return None

def ejecutar_flujo_asistente():
    print("=== ASISTENTE INTELIGENTE DE CORREO (GMAIL + LLM) ===")
    
    # 1. Obtenemos el correo más reciente
    print("\n Buscando el último correo en Gmail...")
    correos = leer_ultimos_correos(limite=5, solo_no_leidos=False)
    
    if not correos:
        print("No se encontraron correos para procesar.")
        return

    # correo_a_procesar = correos[0]
    for correo in correos:
        print(f"\n Procesando correo: '{correo['asunto']}' de {correo['remitente']}")

        # 2. Análisis con Inteligencia Artificial
        print(" Consultando al LLM para analizar y redactar respuesta...")
        analisis = analizar_correo_con_ia(
            remitente=correo["remitente"],
            asunto=correo["asunto"],
            cuerpo=correo["cuerpo"]
        )

        if not analisis:
            print("❌ No se pudo obtener el análisis del LLM.")
            return

        # 3. Mostrar el resultado
        print("\n" + "="*60)
        print(" RESULTADO DEL ANÁLISIS DE LA IA:")
        print("="*60)
        print(f"• Categoría:          {analisis.get('categoria').upper()}")
        print(f"• Nivel de Urgencia:  {analisis.get('urgencia').upper()}")
        print(f"• Resumen:            {analisis.get('resumen')}")
        print("\n📝 Borrador de respuesta generado:")
        print("-" * 60)
        print(analisis.get('respuesta_sugerida'))
        print("-" * 60)
    
        # 4. (Opcional) Auto-respuesta si no es spam
        # if analisis.get("categoria") != "spam":
        #     enviar_correo(
        #         destinatario=correo_a_procesar["remitente"],
        #         asunto=f"Re: {correo_a_procesar['asunto']}",
        #         cuerpo_texto=analisis.get("respuesta_sugerida")
        #     )

if __name__ == "__main__":
    ejecutar_flujo_asistente()
