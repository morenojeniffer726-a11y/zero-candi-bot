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
            
            tipo_mensaje = mensaje_entrada.get('type')
            texto_usuario = ""
            
            if tipo_mensaje == 'text':
                texto_usuario = mensaje_entrada['text']['body'].lower().strip()
            elif tipo_mensaje == 'image':
                texto_usuario = "[imagen_enviada]"
            
            print(f"[{tipo_mensaje.upper()}] Recibido de {numero_remitente}: {texto_usuario}")
            
            # Obtener fase actual
            fase_actual = USUARIOS_FASE.get(numero_remitente, 0)
            
            # Si mandó una imagen (comprobante), forzamos fase de entrega
            if tipo_mensaje == 'image':
                fase_actual = 4
            
            # Procesar cerebro comercial
            respuesta_texto, nueva_fase = motor_neuro_ventas(texto_usuario, fase_actual)
            
            # Actualizar fase en memoria
            USUARIOS_FASE[numero_remitente] = nueva_fase
            
            # Retraso humano de 15 segundos para máxima naturalidad
            print("Aplicando pausa humana de 15 segundos...")
            time.sleep(15)
            
            # Enviar mensaje a WhatsApp
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError) as e:
        print(f"Error procesando webhook: {str(e)}")
        pass
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas(texto, fase):
    """
    Motor de neuro-ventas con historia de autoridad, oferta equilibrada y transiciones blindadas.
    """
    # Manejo global de objeción de dinero
    if any(p in texto for p in ["dinero", "plata", "caro", "esperar", "quincena"]):
        return (
            "Entiendo perfectamente, la situación está difícil. " +
            "¿Te parece si te guardo la promoción y te contacto en la quincena para que no pierdas tu cupo clínico?"
        ), fase

    # FASE 0: APERTURA (Empatía y dolor)
    if fase == 0 or any(p in texto for p in ["hola", "info", "información", "precio", "programa", "cándida", "candida", "empezar"]):
        return (
            "Hola, soy Jeniffer 😊 Gracias por su confianza. " +
            "Mire, si usted ha probado óvulos y cremas por meses y el problema regresa, la entiendo perfectamente: " +
            "yo pasé por ese mismo infierno y gasté una fortuna en farmacias sin ver resultados reales."
        ), 1

    # FASE 1: VALIDACIÓN PROFUNDA (Autoridad y origen del protocolo)
    elif fase == 1:
        return (
            "Es un desgaste físico y emocional horrible, uno hasta evita su intimidad por miedo. " +
            "Por eso diseñé este protocolo clínico: para erradicar la cándida de raíz y restaurar tu parte íntima para siempre. " +
            "Cuénteme, ¿cuánto tiempo lleva atrapada en este ciclo de infecciones?"
        ), 2

    # FASE 2: SOLUCIÓN CLÍNICA
    elif fase == 2:
        return (
            "7 meses (o el tiempo que lleve) es demasiado tiempo cargando con ese tormento. " +
            "Los tratamientos comunes fallan porque solo tapan el síntoma. Nuestro sistema de ácido bórico de grado médico equilibra el pH y sella tu microbiota. " +
            "¿Usted quiere recuperar su salud íntima y sentirse limpia y segura de una vez por todas?"
        ), 3

    # FASE 3: OFERTA IRRESISTIBLE (Equilibrada: ni muy larga ni muy corta, con explicaciones claras)
    elif fase == 3:
        # Si el usuario responde afirmativamente a la pregunta anterior, entregamos la oferta y avanzamos a fase 3.5
        return (
            "¡Esa es la decisión de una mujer valiente!\n\n" +
            "Normalmente este programa cuesta 25$, pero hoy para que comiences tu recuperación total te doy acceso al **PROGRAMA ZERO CANDI** por solo **7.99$ (Tasa BCV)**.\n\n" +
            "🧬 **Lo que incluye tu acceso inmediato:**\n\n" +
            "✅ **Protocolo exacto de Ácido Bórico:** Te enseñamos qué comprar y cómo usarlo de forma segura para limpiar y restaurar tu zona íntima.\n" +
            "🥗 **Recetario Anti-Cándida (15 opciones):** Comidas deliciosas sin azúcares ni harinas para cortar el alimento del hongo desde la cocina.\n" +
            "📋 **Checklist Diario de Control:** Tu bitácora interactiva para seguir el paso a paso sin perderte.\n" +
            "🔓 **Garantía Blindada de 20 días:** Cero riesgo para tu bolsillo; si no ves mejoría radical, te devuelvo tu dinero.\n\n" +
            "Dígame una sola cosa con el corazón en la mano... ¿Sí o sí está lista para asegurar hoy su solución definitiva?"
        ), 35

    # FASE 3.5: CAPTURA DEL "SÍ" A LA OFERTA E INMEDIATO PASE A DATOS DE PAGO
    elif fase == 35 and any(p in texto for p in ["sí", "si", "estoy", "lista", "claro", "seguro", "comprar"]):
        return (
            "¡Excelente! Usted no arriesga absolutamente nada, yo misma la respaldo.\n\n" +
            "🏦 *Datos para Pago Móvil (Mercantil)*\n" +
            "🪪 25771166\n" +
            "📞 04121582154\n" +
            "Monto: 7.99$ (en bolívares tasa BCV).\n\n" +
            "Apenas me envíe por aquí la foto del comprobante de pago, le activo su acceso de inmediato. ¿El pago lo hace Usted misma?"
        ), 4

    # FASE 4: ENTREGA DE LA APP (Al recibir la foto del comprobante o confirmación)
    elif fase == 4 or texto == "[imagen_enviada]" or any(p in texto for p in ["pago", "listo", "transferencia", "comprobante", "captura", "ya pagué"]):
        return (
            "¡Comprobante verificado con éxito! Felicidades por dar este gran paso hacia tu bienestar. 🚀\n\n" +
            "Su usuario ya está activo en nuestra app:\n" +
            "https://candida-zero.vercel.app/\n\n" +
            "📱 Abra el enlace desde su teléfono para ver su protocolo y recetario. ¿Me confirma por favor si logró ingresar sin problemas?"
        ), 4

    # Comodín inteligente si se desvía en la fase de oferta
    else:
        return (
            "¿Vio por qué los tratamientos tradicionales son solo un parche temporal y regular el pH vaginal de raíz es lo único que frena la infección para siempre? " +
            "Dígame, ¿le queda alguna duda sobre el protocolo en casa para avanzar?"
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
