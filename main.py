from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# ====================================================================
# CONFIGURACIÓN MAESTRA - WHATSAPP CLOUD API (CÁNDIDA ZERO)
# ====================================================================
VERIFY_TOKEN = "zero_candi_secure_token_2026"
WHATSAPP_TOKEN = "EAAUV6d9auksBSrAT7SksGzBG8sa6EvodZC4oPePCK8DCKszquGSeNuKEZBrCSqZCWYRe2OQ7L93DxUfMUtiDQt21cUZA3pJQwtO1T6QTHvItO0pTLDMsyjfdwKFUaDwOdx8QVyNhQc92ZCyZCbcpWUOiZBgmVyD7BY2pU0UbMpf1qxTzmO4LcdrPhJd6VdO6JD8HAZDZD"
PHONE_NUMBER_ID = "1316482411550878"

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Activo y Operativo 24/7!", 200

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # Validación oficial de Meta para mantener el webhook conectado
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if token == VERIFY_TOKEN and challenge:
        return challenge, 200
    return 'Error de verificación de token', 403

@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get_json()
    
    try:
        # Extracción segura del mensaje entrante del prospecto
        changes = data['entry'][0]['changes'][0]['value']
        if 'messages' in changes:
            mensaje_entrada = changes['messages'][0]
            numero_remitente = mensaje_entrada['from']
            texto_usuario = mensaje_entrada['text']['body'].lower()
            
            print(f"Mensaje recibido de {numero_remitente}: {texto_usuario}")
            
            # Cerebro comercial de Jeniffer (Neuro-ventas)
            respuesta_texto = generar_respuesta_comercial(texto_usuario)
            
            # Disparo automático de respuesta por la API Cloud de Meta
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError):
        # Ignora eventos secundarios de entrega o lectura de WhatsApp
        pass
        
    return jsonify({"status": "received"}), 200

def generar_respuesta_comercial(texto):
    """
    Motor de persuasión adaptado al Programa Clínico Cándida Zero.
    Ataca dolores críticos: fatiga crónica, ansiedad por carbohidratos e inflamación.
    """
    texto = texto.strip()
    
    # Intención: Saludo o información general del programa
    if any(palabra in texto for palabra in ["hola", "info", "información", "precio", "programa", "cándida", "candida"]):
        return (
            "¡Hola! Qué gusto saludarte. Soy Jeniffer, asesora oficial del *Programa Clínico Cándida Zero*.\n\n" +
            "¿Sientes fatiga constante, inflamación o una ansiedad incontrolable por los azúcares que no te deja avanzar? " +
            "No estás sola, y tiene solución. Nuestro método clínico está diseñado para devolverte la energía vital y resetear tu salud digestiva de raíz.\n\n" +
            "Escríbeme cuál es el síntoma que más te afecta hoy (ej. *hinchazón*, *cansancio* o *ansiedad por dulces*) para darte el plan exacto que necesitas."
        )
    
    # Dolor: Ansiedad por azúcar / carbohidratos
    elif any(palabra in texto for palabra in ["azucar", "dulce", "ansiedad", "carbohidratos", "comida"]):
        return (
            "Esa ansiedad voraz es el hongo de la cándida exigiendo combustible. ¡Es hora de cortar ese ciclo de raíz!\n\n" +
            "Con el *Programa Clínico Cándida Zero* reprogramamos tu metabolismo en pocas semanas para eliminar esos antojos sin pasar hambre.\n\n" +
            "¿Te gustaría conocer los detalles de nuestros paquetes y comenzar tu transformación esta misma semana? Responde *SÍ* para enviarte la guía de inicio."
        )
        
    # Dolor: Cansancio / Fatiga crónica
    elif any(palabra in texto for palabra in ["cansancio", "fatiga", "energia", "cansada", "sin fuerza"]):
        return (
            "La fatiga crónica es la señal de alerta número uno de que tu microbiota está desbalanceada. " +
            "Recuperar tu energía y claridad mental es totalmente posible con nuestro protocolo clínico guiado.\n\n" +
            "¿Estás lista para volver a despertar con vitalidad? Responde *QUIERO MI CAMBIO* y te indico los pasos para acceder al programa."
        )
        
    # Dolor: Inflamación / Problemas estomacales
    elif any(palabra in texto for palabra in ["inflamacion", "hinchazon", "estomago", "abdomen", "digestión", "gases"]):
        return (
            "Esa inflamación y pesadez estomacal después de comer son el reflejo directo de la disbiosis intestinal. " +
            "El *Programa Cándida Zero* sella tu intestino y elimina el sobrecrecimiento bacteriano de forma natural.\n\n" +
            "Imagina volver a sentir ligereza y bienestar todos los días. Escribe *VALOR* para conocer cómo iniciar hoy mismo."
        )
        
    # Cierre / Interés en adquirir
    elif any(palabra in texto for palabra in ["sí", "si", "quiero", "valor", "comprar", "precio"]):
        return (
            "¡Excelente decisión! El éxito no es un accidente y dar este paso cambiará tu salud para siempre.\n\n" +
            "Para entregarte el acceso inmediato al *Programa Clínico Cándida Zero* y activar tu acompañamiento personalizado, haz clic en el siguiente enlace de inscripción segura o dime a qué hora prefieres que te contactemos por aquí."
        )
        
    # Respuesta por defecto empática (Mantiene el gancho comercial)
    else:
        return (
            "Te entiendo perfectamente. Cada cuerpo nos habla a su manera, y en el *Programa Clínico Cándida Zero* tenemos el protocolo exacto para ti.\n\n" +
            "Cuéntame brevemente: ¿cuánto tiempo llevas luchando con estos síntomas? Estoy aquí para ayudarte a recuperar tu bienestar."
        )

def enviar_mensaje_whatsapp(destinatario, texto):
    """
    Envía la respuesta utilizando la API Cloud oficial de Meta v26.0 con autenticación Bearer permanente.
    """
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
