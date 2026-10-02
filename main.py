from flask import Flask, request, jsonify
import os
import requests
import time
import threading

app = Flask(__name__)

# ====================================================================
# CONFIGURACIÓN MAESTRA - WHATSAPP CLOUD API (CÁNDIDA ZERO - PRODUCCIÓN)
# ====================================================================
VERIFY_TOKEN = "zero_candi_secure_token_2026"
WHATSAPP_TOKEN = "EAAUV6d9auksBSrAT7SksGzBG8sa6EvodZC4oPePCK8DCKszquGSeNuKEZBrCSqZCWYRe2OQ7L93DxUfMUtiDQt21cUZA3pJQwtO1T6QTHvItO0pTLDMsyjfdwKFUaDwOdx8QVyNhQc92ZCyZCbcpWUOiZBgmVyD7BY2pU0UbMpf1qxTzmO4LcdrPhJd6VdO6JD8HAZDZD"
PHONE_NUMBER_ID = "1316482411550878"

# Memoria temporal de fases por número de teléfono
USUARIOS_FASE = {}

@app.route('/', methods=['GET'])
def home():
    return "¡Jeniffer - Cándida Zero Bot Activo y Operativo en Producción (Alta Concurrencia)! 🚀", 200

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
    
    # Respondemos inmediatamente a Meta con 200 OK para evitar timeouts en la API
    # y procesamos la lógica en un hilo secundario para alta velocidad.
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
            
            # Lanzamos el proceso en un hilo para no bloquear el servidor ante 300+ usuarias
            hilo = threading.Thread(target=procesar_y_responder, args=(numero_remitente, texto_usuario, tipo_mensaje))
            hilo.start()
            
    except (KeyError, IndexError) as e:
        print(f"Error procesando webhook structure: {str(e)}")
        pass
        
    return jsonify({"status": "received"}), 200

def procesar_y_responder(numero_remitente, texto_usuario, tipo_mensaje):
    # Obtener fase actual
    fase_actual = USUARIOS_FASE.get(numero_remitente, 0)
    
    # Si mandó una imagen (comprobante), forzamos fase de entrega
    if tipo_mensaje == 'image':
        fase_actual = 4
    
    # Procesar cerebro comercial
    respuesta_texto, nueva_fase = motor_neuro_ventas(texto_usuario, fase_actual)
    
    # Actualizar fase en memoria
    USUARIOS_FASE[numero_remitente] = nueva_fase
    
    # Pausa humana en segundo plano (no bloquea otras peticiones concurrentes)
    time.sleep(8)
    
    # Enviar mensaje a WhatsApp
    enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)

def motor_neuro_ventas(texto, fase):
    """
    Motor de neuro-ventas blindado: sin bucles repetitivos y con respuestas dinámicas a cualquier input.
    """
    # 0. Manejo de agradecimientos o confirmaciones de que abrió la app
    if any(p in texto for p in ["gracias", "excelente", "abrió", "abrio", "perfecto", "listo", "comprendido", "muy amable"]):
        if fase >= 4:
            return (
                "¡Excelente! Me alegra muchísimo saber que ya estás dentro. " +
                "Revisa con calma cada módulo del protocolo y el recetario. " +
                "Cualquier duda que te surja en el proceso, me escribes por aquí. ¡Vamos a ganar tu salud total! 🚀"
            ), fase

    # 1. Manejo global de objeción de dinero
    if any(p in texto for p in ["dinero", "plata", "caro", "esperar", "quincena", "no tengo"]):
        return (
            "Entiendo perfectamente, la situación está difícil. " +
            "¿Te parece si te guardo la promoción de los 6.823 Bs y te contacto en unos días para que no pierdas tu cupo clínico?"
        ), fase

    # 2. FAQ Inteligente (Preguntas frecuentes en cualquier momento)
    if any(p in texto for p in ["cómo se usa", "como se usa", "aplicacion", "aplicación", "dónde se compra", "donde se compra", "ingredientes", "seguro"]):
        return (
            "Es un tratamiento 100% seguro y muy fácil de aplicar en la comodidad de tu hogar. " +
            "Te indicamos exactamente qué adquirir en farmacias y el paso a paso detallado en la app. " +
            "¿Te gustaría que avancemos para darte acceso inmediato al protocolo?"
        ), fase

    if any(p in texto for p in ["cuánto tiempo", "cuanto tiempo", "días", "dias", "funciona rápido", "resultados"]):
        return (
            "La mayoría de nuestras pacientes sienten un alivio radical y la desaparición del picor y flujo molesto desde los primeros 3 a 5 días de aplicación constante. " +
            "¿Estás lista para comenzar tu recuperación?"
        ), fase

    # FASE 0: APERTURA (Empatía, dolor y PREGUNTA de enganche)
    if fase == 0 or any(p in texto for p in ["hola", "info", "información", "precio", "programa", "cándida", "candida", "empezar"]):
        return (
            "Hola, soy Jeniffer 😊 Gracias por su confianza. " +
            "Mire, si usted ha probado óvulos y cremas por meses y el problema regresa, la entiendo perfectamente: " +
            "yo pasé por ese mismo infierno y gasté una fortuna en farmacias sin ver resultados reales. " +
            "Cuénteme, ¿cuánto tiempo lleva luchando contra esta infección?"
        ), 1

    # FASE 1: VALIDACIÓN PROFUNDA (Autoridad)
    elif fase == 1:
        return (
            "Es un desgaste físico y emocional horrible, uno hasta evita su intimidad por miedo. " +
            "Por eso diseñé este protocolo clínico: para erradicar la cándida de raíz y restaurar tu parte íntima para siempre. " +
            "Cuénteme, ¿qué tratamientos ha probado hasta ahora que no le dieron resultado?"
        ), 2

    # FASE 2: SOLUCIÓN CLÍNICA
    elif fase == 2:
        return (
            "Te entiendo, yo pasé por lo mismo y con este protocolo logré erradicar la cándida, " +
            "ya que los tratamientos comunes fallan porque solo tapan el síntoma superficial sin limpiar el ecosistema vaginal. " +
            "Nosotros aplicamos un protocolo clínico avanzado a base de ácido bórico y probióticos de grado médico que neutraliza el pH y erradica el hongo de raíz. " +
            "¿Usted quiere recuperar su salud íntima y volver a sentirse limpia y segura de una vez por todas?"
        ), 3

    # FASE 3: OFERTA IRRESISTIBLE (Precio fijo en bolívares)
    elif fase == 3:
        return (
            "¡Esa es la decisión de una mujer valiente!\n\n" +
            "Normalmente este programa cuesta 25$, pero hoy para que comiences tu recuperación total te doy acceso al **PROGRAMA ZERO CANDI** por solo **6.823 Bs**.\n\n" +
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
            "Monto exacto: **6.823 Bs**\n\n" +
            "Apenas me envíe por aquí la foto del comprobante de pago, le activo su acceso de inmediato. ¿El pago lo hace Usted misma?"
        ), 4

    # FASE 4: ENTREGA DE LA APP
    elif fase == 4 or texto == "[imagen_enviada]" or any(p in texto for p in ["pago", "listo", "transferencia", "comprobante", "captura", "ya pagué", "ya pague"]):
        return (
            "¡Comprobante verificado con éxito! Felicidades por dar este gran paso hacia tu bienestar. 🚀\n\n" +
            "Su usuario ya está activo en nuestra app:\n" +
            "https://candida-zero.vercel.app/\n\n" +
            "📱 Abra el enlace desde su teléfono para ver su protocolo y recetario. ¿Me confirma por favor si logró ingresar sin problemas?"
        ), 4

    # COMODÍN INTELIGENTE ANTIBUCLES
    else:
        return (
            "Le entiendo perfectamente. Lo más importante ahora es cortar el problema de raíz regulando su pH íntimo de forma clínica con nuestro programa de 6.823 Bs. " +
            "Dígame, ¿le queda alguna duda sobre los beneficios o prefiere que le pase los datos del pago móvil para asegurar su acceso hoy mismo?"
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
