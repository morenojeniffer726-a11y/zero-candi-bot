from flask import Flask, request, jsonify
import os
import requests
import time

app = Flask(__name__)

# ====================================================================
# CONFIGURACIÓN MAESTRA - WHATSAPP CLOUD API (CÁNDIDA ZERO)
# ====================================================================
VERIFY_TOKEN = "zero_candi_secure_token_2026"
WHATSAPP_TOKEN = "EAAUV6d9auksBSrAT7SksGzBG8sa6EvodZC4oPePCK8DCKszquGSeNuKEZBrCSqZCWYRe2OQ7L93DxUfMUtiDQt21cUZA3pJQwtO1T6QTHvItO0pTLDMsyjfdwKFUaDwOdx8QVyNhQc92ZCyZCbcpWUOiZBgmVyD7BY2pU0UbMpf1qxTzmO4LcdrPhJd6VdO6JD8HAZDZD"
PHONE_NUMBER_ID = "1316482411550878"

# Historial de chat por número de teléfono para memoria fluida y continua
# Estructura: { "numero": [ {"role": "user"/"assistant", "content": "mensaje"}, ... ] }
HISTORIAL_CONVERSACIONES = {}

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Inteligente Activo 24/7!", 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if token == VERIFY_TOKEN and challenge:
        return challenge, 200
    return 'Error de verificación de token', 403

@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get_json()
    
    try:
        changes = data['entry'][0]['changes'][0]['value']
        if 'messages' in changes:
            mensaje_entrada = changes['messages'][0]
            numero_remitente = mensaje_entrada['from']
            
            tipo_mensaje = mensaje_entrada.get('type')
            texto_usuario = ""
            
            if tipo_mensaje == 'text':
                texto_usuario = mensaje_entrada['text']['body'].strip()
            elif tipo_mensaje == 'image':
                texto_usuario = "[El cliente ha enviado una imagen o comprobante de pago]"
            
            print(f"[{tipo_mensaje.upper()}] Recibido de {numero_remitente}: {texto_usuario}")
            
            # Inicializar historial si no existe
            if numero_remitente not in HISTORIAL_CONVERSACIONES:
                HISTORIAL_CONVERSACIONES[numero_remitente] = []
            
            # Agregar mensaje del usuario al historial
            HISTORIAL_CONVERSACIONES[numero_remitente].append({"role": "user", "content": texto_usuario})
            
            # Mantener solo los últimos 15 intercambios para rendimiento extremo
            if len(HISTORIAL_CONVERSACIONES[numero_remitente]) > 30:
                HISTORIAL_CONVERSACIONES[numero_remitente] = HISTORIAL_CONVERSACIONES[numero_remitente][-30:]
            
            # Procesar cerebro comercial con inteligencia artificial y contexto
            respuesta_texto = motor_neuro_ventas_ia(HISTORIAL_CONVERSACIONES[numero_remitente])
            
            # Agregar respuesta al historial
            HISTORIAL_CONVERSACIONES[numero_remitente].append({"role": "assistant", "content": respuesta_texto})
            
            # Pausa humana de 12 segundos para máxima naturalidad
            print("Aplicando pausa humana de 12 segundos...")
            time.sleep(12)
            
            # Enviar mensaje a WhatsApp
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError) as e:
        print(f"Error procesando webhook: {str(e)}")
        pass
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas_ia(historial):
    """
    Cerebro comercial avanzado inspirado en Margarita Pasos y la experiencia personal de Jeniffer.
    Utiliza el historial completo para mantener contexto continuo y responder con empatía y precisión.
    """
    
    # Prompt del Sistema (Directrices Maestras para el Bot)
    system_prompt = """
    Eres Jeniffer, creadora del programa 'Cándida Zero' y experta en salud íntima femenina y neuro-ventas.
    Te comunicas por WhatsApp con mujeres de Venezuela que sufren de infecciones vaginales recurrentes (cándida, flujo blanco, picazón, etc.).
    
    TUS DIRECTRICES DE ORO:
    1. HISTORIA DE AUTORIDAD Y EMPATÍA: Habla desde la experiencia real. Di siempre que tú pasaste por ese mismo infierno, gastaste dinero en farmacias y cremas sin ver resultados, hasta que creaste este protocolo. Valida exactamente lo que la clienta te diga (si dice 6 meses, menciona sus 6 meses con empatía).
    2. TONO: Cercano, cálido, firme, empoderador y de absoluta confianza (como una hermana mayor o una mentora que ya venció el problema).
    3. MANEJO DE DUDAS Y SOPORTE TOTAL: Puedes responder cualquier duda técnica o clínica que tenga la clienta (cómo usar los óvulos de ácido bórico, el recetario anti-cándida, la alimentación, etc.) con base en medicina natural y bienestar.
    4. FLUJO COMERCIAL Y CIERRE:
       - Si muestra interés o dolor, profundiza en la solución.
       - Si pregunta el precio o muestra disposición, presenta la oferta irresistible: El PROGRAMA ZERO CANDI completo (Protocolo exacto de Ácido Bórico + Recetario Anti-Cándida de 15 opciones + Checklist diario + Garantía blindada de 20 días) por solo 7.99$ (Tasa BCV) (Precio regular 25$).
       - Cuando acepten comprar (con un "sí", "estoy lista", etc.), dales de inmediato los datos de pago móvil:
         Banco: Mercantil
         Cédula: 25771166
         Teléfono: 04121582154
         Monto: 7.99$
         Y pídeles el comprobante.
       - Si envían un comprobante o foto, felicítalas y entrégales el enlace de acceso a la app: https://candida-zero.vercel.app/
    5. GESTIÓN DE POST-VENTA Y AGRADECIMIENTOS: Si la clienta dice "gracias", responde con calidez, recuérdale que estás para apoyarla en su sanación y pregúntale si pudo ingresar a la app o si tiene alguna duda sobre cómo aplicarse los óvulos. Nunca repitas un mensaje automatizado de forma robótica si ya pagó; lee el contexto y responde de forma natural.
    6. OBJECIONES DE DINERO: Si dicen que no tienen dinero o deben esperar quincena, muéstrate comprensiva y ofréceles apartarles el cupo promocional para esa fecha.
    7. BREVEDAD PARA WHATSAPP: Usa párrafos cortos, viñetas limpias y emojis moderados para una lectura rápida en el móvil.
    """

    # Construir payload para la API de IA (puedes conectar OpenAI o Google AI Studio aquí)
    # Por seguridad y estabilidad, simularemos la llamada estructurada con el contexto integrado o endpoint LLM.
    # Nota: Si usas OpenAI o Google Gemini API en tu servidor, insertas tu cliente aquí.
    # Ejemplo de estructura de mensajes para enviar al modelo:
    
    mensajes_completos = [{"role": "system", "content": system_prompt}] + historial
    
    # Si tienes configurada tu API Key de OpenAI o Gemini, puedes hacer la petición real. 
    # Para asegurar que tu bot funcione de inmediato con la lógica exacta, aquí tienes el conector robusto o puedes usar la API de OpenAI/Gemini:
    
    try:
        # Ejemplo usando OpenAI (puedes cambiar la URL o SDK según prefieras)
        openai_api_key = os.environ.get("OPENAI_API_KEY", "")
        if openai_api_key:
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": mensajes_completos,
                "temperature": 0.7,
                "max_tokens": 500
            }
            response = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=20)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        
        # Fallback inteligente con heurística de contexto si no está activa la API key de LLM en este segundo:
        ultimo_mensaje = historial[-1]["content"].lower()
        
        if "gracias" in ultimo_mensaje or "gracia" in ultimo_mensaje:
            return "¡De nada con todo el corazón! Recuerda que no estás sola en esto. Dime, ¿pudiste abrir el enlace de la app o tienes alguna duda con la aplicación de los óvulos?"
        
        if "óvulo" in ultimo_mensaje or "ovulo" in ultimo_mensaje or "aplicar" in ultimo_mensaje:
            return "Los óvulos de ácido bórico de grado médico se colocan preferiblemente en la noche antes de dormir, bien arriba en la vagina. Te ayudan a equilibrar el pH de forma inmediata y eliminar el hongo. ¿Tienes alguna duda sobre cómo prepararlos o conseguirlos?"
            
        return (
            "Te entiendo perfectamente, yo pasé por ese mismo infierno de infecciones recurrentes y sé lo agotador que es. " +
            "Por eso diseñé Cándida Zero: para ir a la raíz del problema y devolverte tu tranquilidad íntima. " +
            "Cuéntame, ¿qué síntoma es el que más te incomoda en este momento para darte la solución exacta?"
        )

    except Exception as e:
        print(f"Error en motor IA: {str(e)}")
        return "¡Hola! Estoy aquí para ayudarte a recuperar tu salud íntima de raíz. Cuéntame, ¿cuánto tiempo llevas lidiando con esta infección?"

def enviar_mensaje_whatsapp(destinatario, texto):
    url = f"https://graph.facebook.com/v26.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario,
        "type": "text",
        "text": {
            "body": texto
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Respuesta enviada a Meta: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error al enviar mensaje a WhatsApp: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
