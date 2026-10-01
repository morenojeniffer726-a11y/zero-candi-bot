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

# Memoria temporal de fases por número de teléfono
USUARIOS_FASE = {}

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Activo y Operativo 24/7!", 200

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
            
            # Detectar si es texto o imagen (comprobante)
            tipo_mensaje = mensaje_entrada.get('type')
            texto_usuario = ""
            
            if tipo_mensaje == 'text':
                texto_usuario = mensaje_entrada['text']['body'].lower().strip()
            elif tipo_mensaje == 'image':
                texto_usuario = "[imagen_enviada]"
            
            print(f"[{tipo_mensaje.upper()}] Recibido de {numero_remitente}: {texto_usuario}")
            
            # Obtener o inicializar la fase del usuario
            fase_actual = USUARIOS_FASE.get(numero_remitente, 0)
            
            # Si mandó una imagen, forzamos la fase de validación de pago / entrega
            if tipo_mensaje == 'image':
                fase_actual = 5
            
            # Procesar el cerebro comercial de Jeniffer
            respuesta_texto, nueva_fase = motor_neuro_ventas(texto_usuario, fase_actual)
            
            # Actualizar la fase
            USUARIOS_FASE[numero_remitente] = nueva_fase
            
            # Retraso humano de 15 segundos
            print("Aplicando pausa humana de 15 segundos...")
            time.sleep(15)
            
            # Enviar respuesta por WhatsApp
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError) as e:
        print(f"Error procesando webhook: {str(e)}")
        pass
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas(texto, fase):
    """
    Motor optimizado: Textos cortos, directos al pulgar y manejo de imágenes.
    """
    # Manejo de objeción de dinero
    if any(p in texto for p in ["dinero", "plata", "caro", "esperar", "quincena"]):
        return (
            "Entiendo perfectamente, la situación está difícil. " +
            "¿Te parece si te guardo la promoción y te contacto en la quincena para que no pierdas tu cupo clínico?"
        ), fase

    # FASE 0: APERTURA
    if fase == 0 or any(p in texto for p in ["hola", "info", "información", "precio", "programa", "cándida", "candida", "empezar"]):
        return (
            "Hola, soy Jeniffer 😊 Gracias por su confianza. " +
            "Mire, si usted ha probado óvulos y cremas por más de 5 meses y el problema regresa, la entiendo porque viví ese mismo desgaste. " +
            "Cuénteme... ¿Siente que gasta dinero en farmacias y el ardor o la picazón no se van?"
        ), 1

    # FASE 1: VALIDACIÓN PROFUNDA
    elif fase == 1:
        return (
            "Es desesperante, ¿verdad? Uno ya ni disfruta de su intimidad por miedo al dolor. " +
            "Cuénteme, ¿cómo es ese flujo que le molesta y cuánto tiempo lleva atrapada en este ciclo?"
        ), 2

    # FASE 2: SOLUCIÓN CLÍNICA
    elif fase == 2:
        return (
            "Los tratamientos comunes fallan porque solo tapan el síntoma sin limpiar el ecosistema. " +
            "Nuestro protocolo de ácido bórico de grado médico neutraliza el pH y erradica el hongo de raíz. " +
            "¿Usted quiere recuperar su salud íntima de una vez por todas?"
        ), 3

    # FASE 3: OFERTA IRRESISTIBLE (Versión corta de alto impacto)
    elif fase == 3 or any(p in texto for p in ["sí", "si", "quiero", "claro", "estoy lista", "seguro"]):
        return (
            "¡Excelente decisión! No se resigne a vivir a medias.\n\n" +
            "El **PROGRAMA ZERO CANDI** incluye:\n" +
            "✅ Protocolo exacto de Ácido Bórico.\n" +
            "🥗 Recetario Anti-Cándida (15 opciones).\n" +
            "📋 Checklist interactivo diario.\n" +
            "🔓 Garantía Blindada de 20 días.\n\n" +
            "🔥 **Precio especial hoy: 7.99$ (Tasa BCV)** en lugar de 25$.\n\n" +
            "¿Sí o sí está lista para asegurar hoy su solución definitiva?"
        ), 4

    # FASE 4: DATOS DE PAGO
    elif fase == 4 and any(p in texto for p in ["sí", "si", "estoy", "listas", "comprar", "pago", "datos", "explícame", "explicame"]):
        return (
            "¡Así se habla! Usted no arriesga nada, yo la respaldo.\n\n" +
            "🏦 *Pago Móvil Mercantil*\n" +
            "🪪 25771166\n" +
            "📞 04121582154\n" +
            "Monto: 7.99$ (o su equivalente en Bs tasa BCV).\n\n" +
            "Apenas me envíe la foto del comprobante aquí, le activo su acceso de inmediato. ¿El pago lo hace Usted?"
        ), 5

    # FASE 5: ENTREGA DE PLATAFORMA (Se activa con texto o cuando mandan la foto)
    elif fase == 5 or texto == "[imagen_enviada]" or any(p in texto for p in ["pago", "listo", "transferencia", "comprobante", "captura", "ya pagué"]):
        return (
            "¡Comprobante recibido con éxito! Felicidades por dar este gran paso. 🚀\n\n" +
            "Su usuario ya está activo en nuestra app:\n" +
            "https://candida-zero.vercel.app/\n\n" +
            "Abra el enlace desde su teléfono para ver su protocolo y recetario. ¿Me confirma si logró ingresar sin problemas?"
        ), 5

    # Comodín
    else:
        return (
            "¿Vio por qué regular el pH vaginal de raíz es lo único que frena la infección para siempre? " +
            "Dígame, ¿le quedan dudas sobre el protocolo en casa?"
        ), fase

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
