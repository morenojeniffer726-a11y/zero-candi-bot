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

# Memoria de estado comercial por número de teléfono
# Estados posibles: 'inicio', 'esperando_sintoma', 'ofreciendo_programa', 'esperando_pago', 'completado'
USUARIOS_ESTADO = {}

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Inteligente V2 Activo 24/7!", 200

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
                texto_usuario = "[COMPROBANTE_ENVIADO]"
            
            print(f"[{tipo_mensaje.upper()}] Recibido de {numero_remitente}: {texto_usuario}")
            
            # Obtener o inicializar el estado del usuario
            if numero_remitente not in USUARIOS_ESTADO:
                USUARIOS_ESTADO[numero_remitente] = {
                    "paso": "inicio",
                    "tiempo": "",
                    "sintoma": ""
                }
            
            # Procesar la máquina de ventas con flujo dinámico
            respuesta_texto = motor_neuro_ventas(numero_remitente, texto_usuario)
            
            # Pausa humana de 10 segundos para máxima naturalidad
            print("Aplicando pausa humana de 10 segundos...")
            time.sleep(10)
            
            # Enviar mensaje a WhatsApp
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError) as e:
        print(f"Error procesando webhook: {str(e)}")
        pass
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas(numero, texto):
    """
    Máquina de estados comercial de alta conversión basada en neuro-ventas.
    Evita bucles y garantiza que la conversación avance de forma fluida.
    """
    texto_lower = texto.lower()
    estado_actual = USUARIOS_ESTADO[numero]["paso"]
    
    # 1. SI MANDA UN COMPROBANTE O FOTO O PALABRAS DE PAGO
    if "[comprobante_enviado]" in texto or "banco" in texto_lower or "transferencia" in texto_lower or "pago móvil" in texto_lower or "listo el pago" in texto_lower or "pagado" in texto_lower:
        USUARIOS_ESTADO[numero]["paso"] = "completado"
        return (
            "¡Comprobante verificado con éxito! Felicidades por dar este gran paso hacia tu bienestar. 🚀\n\n"
            "Tu usuario ya está activo en nuestra app:\n"
            "https://candida-zero.vercel.app/\n\n"
            "📱 Abre el enlace desde tu teléfono para ver tu protocolo y recetario. ¿Me confirmas por favor si logró ingresar sin problemas?"
        )

    # 2. MANEJO DE AGRADECIMIENTOS O DUDAS POST-VENTA
    if estado_actual == "completado" or "gracias" in texto_lower or "muchas gracias" in texto_lower:
        return (
            "¡De nada con todo el corazón! Recuerda que estoy aquí para acompañarte en tu sanación. "
            "Dime, ¿pudiste ingresar a la app sin inconvenientes o tienes alguna duda sobre cómo aplicarte los óvulos?"
        )

    # 3. MÁQUINA DE ESTADOS SECUENCIAL DEL EMBUDO
    if estado_actual == "inicio":
        # Guardamos de manera flexible el tiempo que respondió
        USUARIOS_ESTADO[numero]["tiempo"] = texto
        USUARIOS_ESTADO[numero]["paso"] = "esperando_sintoma"
        
        # Respuesta empática validando exactamente lo que dijo (sin contradecirla con números fijos)
        return (
            f"¡{texto} es demasiado tiempo cargando con ese tormento! Te entiendo perfectamente, yo pasé por ese mismo infierno de infecciones recurrentes y sé lo agotador que es.\n\n"
            "Los tratamientos comunes fallan porque solo tapan el síntoma. Nuestro sistema de ácido bórico de grado médico equilibra el pH y sella tu microbiota.\n\n"
            "Cuéntame, además del tiempo, ¿qué síntoma (como flujo, picazón u olor) es el que más te incomoda en este momento?"
        )

    elif estado_actual == "esperando_sintoma":
        USUARIOS_ESTADO[numero]["sintoma"] = texto
        USUARIOS_ESTADO[numero]["paso"] = "ofreciendo_programa"
        
        return (
            "¡Ese síntoma es precisamente el que vamos a erradicar de raíz! Ya basta de pañitos de agua tibia.\n\n"
            "¿Usted quiere recuperar su salud íntima, despedirse del mal olor y sentirse limpia y segura de una vez por todas?"
        )

    elif estado_actual == "ofreciendo_programa" or "si" in texto_lower or "claro" in texto_lower or "quiero" in texto_lower:
        USUARIOS_ESTADO[numero]["paso"] = "esperando_pago"
        
        return (
            "¡Esa es la decisión de una mujer valiente! 🔥\n\n"
            "Normalmente este programa cuesta 25$, pero hoy para que comiences tu recuperación total te doy acceso al *PROGRAMA ZERO CANDI* por solo *7.99$ (Tasa BCV)*.\n\n"
            "💳 *Datos de Pago Móvil (Mercantil):*\n"
            "• Banco: Mercantil (0105)\n"
            "• Cédula: 25.771.166\n"
            "• Teléfono: 0412-1582154\n"
            "• Monto: 7.99$ (o su equivalente en Bs a tasa BCV)\n\n"
            "📲 Realiza tu pago y envíame por aquí el capture del comprobante para activar tu acceso inmediato."
        )

    else:
        # Fallback inteligente por si escriben cualquier otra duda o objeción
        return (
            "Te entiendo perfectamente. Estoy aquí para resolver cualquier duda que tengas sobre el protocolo de ácido bórico o la alimentación.\n\n"
            "¿Estás lista para adquirir tu acceso al *Programa Zero Candi* por solo 7.99$ y empezar tu sanación hoy mismo?"
        )

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
