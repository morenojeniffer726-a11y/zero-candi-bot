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
USUARIOS_ESTADO = {}

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Activo y Blindado 24/7!", 200

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
    print(f"📥 WEBHOOK RECIBIDO: {data}")
    
    try:
        # Validar estructura estándar de WhatsApp Cloud API
        if 'entry' in data and data['entry'][0].get('changes'):
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
                else:
                    texto_usuario = "[OTRO_TIPO_MENSAJE]"
                
                print(f"💬 Mensaje extraído de {numero_remitente}: {texto_usuario}")
                
                # Inicializar estado si es un usuario nuevo
                if numero_remitente not in USUARIOS_ESTADO:
                    USUARIOS_ESTADO[numero_remitente] = {
                        "paso": "inicio",
                        "tiempo": "",
                        "sintoma": ""
                    }
                
                # Procesar respuesta comercial
                respuesta_texto = motor_neuro_ventas(numero_remitente, texto_usuario)
                
                # Pausa humana táctica de 3 segundos para evitar bloqueos por velocidad
                time.sleep(3)
                
                # Enviar respuesta a WhatsApp
                enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
                
    except Exception as e:
        print(f"❌ Error crítico procesando webhook: {str(e)}")
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas(numero, texto):
    texto_lower = texto.lower()
    estado_actual = USUARIOS_ESTADO[numero]["paso"]
    
    print(f"🔄 Estado actual de {numero}: {estado_actual} | Mensaje: {texto}")

    # 1. SI ENVÍA UN COMPROBANTE DE PAGO
    if "[comprobante_enviado]" in texto or "banco" in texto_lower or "transferencia" in texto_lower or "pago móvil" in texto_lower or "listo el pago" in texto_lower or "pagado" in texto_lower:
        USUARIOS_ESTADO[numero]["paso"] = "completado"
        return (
            "¡Comprobante verificado con éxito! Felicidades por dar este gran paso hacia tu bienestar. 🚀\n\n"
            "Su usuario ya está activo en nuestra app:\n"
            "https://candida-zero.vercel.app/\n\n"
            "📱 Abra el enlace desde su teléfono para ver su protocolo y recetario. ¿Me confirma por favor si logró ingresar sin problemas?"
        )

    # 2. MANEJO DE AGRADECIMIENTOS O SOPORTE POST-VENTA
    if estado_actual == "completado" or "gracias" in texto_lower or "muchas gracias" in texto_lower:
        return (
            "¡De nada con todo el corazón! Recuerde que no está sola en este proceso. "
            "¿Pudiste ingresar a la app sin inconvenientes o tienes alguna duda sobre cómo aplicarte los óvulos?"
        )

    # 3. FLUJO COMERCIAL PASO A PASO
    if estado_actual == "inicio":
        USUARIOS_ESTADO[numero]["tiempo"] = texto
        USUARIOS_ESTADO[numero]["paso"] = "esperando_sintoma"
        
        return (
            f"¡{texto} es demasiado tiempo cargando con ese tormento! Los tratamientos comunes fallan porque solo tapan el síntoma. "
            "Nuestro sistema de ácido bórico de grado médico equilibra el pH y sella tu microbiota.\n\n"
            "¿Usted quiere recuperar su salud íntima y sentirse limpia y segura de una vez por todas?"
        )

    elif estado_actual == "esperando_sintoma":
        USUARIOS_ESTADO[numero]["sintoma"] = texto
        USUARIOS_ESTADO[numero]["paso"] = "ofreciendo_programa"
        
        return (
            "¡Esa es la decisión de una mujer valiente! 🔥\n\n"
            "Normalmente este programa cuesta 25$, pero hoy para que comiences tu recuperación total te doy acceso al *PROGRAMA ZERO CANDI* por solo *7.99$ (Tasa BCV)*."
        )

    elif estado_actual == "ofreciendo_programa" or "si" in texto_lower or "claro" in texto_lower or "quiero" in texto_lower:
        USUARIOS_ESTADO[numero]["paso"] = "esperando_pago"
        
        return (
            "💳 *Datos de Pago Móvil (Mercantil):*\n"
            "• Banco: Mercantil (0105)\n"
            "• Cédula: 25.771.166\n"
            "• Teléfono: 0412-1582154\n"
            "• Monto: 7.99$ (o su equivalente en Bs a tasa BCV)\n\n"
            "📲 Realiza tu pago y envíame por aquí el capture del comprobante para activar tu acceso inmediato."
        )

    else:
        # Manejo de objeciones / Dudas sobre el producto
        if "que es" in texto_lower or "vending" in texto_lower or "vendes" in texto_lower or "programa" in texto_lower or "consiste" in texto_lower or "entiendo" in texto_lower:
            return (
                "Te explico con todo detalle: el *PROGRAMA ZERO CANDI* es un protocolo clínico digital diseñado para erradicar la cándida de raíz.\n\n"
                "Incluye:\n"
                "1️⃣ Protocolo exacto de óvulos de ácido bórico.\n"
                "2️⃣ Recetario anti-cándida para cortar el alimento del hongo.\n"
                "3️⃣ Acceso privado a la app 24/7.\n\n"
                "Todo por solo 7.99$. ¿Deseas los datos de pago móvil para comenzar hoy?"
            )
        
        return (
            "Te entiendo perfectamente. Yo pasé por ese mismo infierno y sé lo importante que es sanar de raíz.\n\n"
            "El *Programa Zero Candi* te entrega el paso a paso exacto en nuestra app por solo 7.99$. "
            "¿Deseas que te comparta los datos de pago móvil para activar tu acceso?"
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
        print(f"📤 Resultado envío Meta: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error al enviar mensaje a WhatsApp: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
