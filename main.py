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
# Estados: 0=Inicio/Apertura, 1=Validación Profunda, 2=Autoridad y Solución, 3=Oferta Irresistible, 4=Cierre de Pago, 5=Entrega de Plataforma
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
            texto_usuario = mensaje_entrada['text']['body'].lower().strip()
            
            print(f"Mensaje recibido de {numero_remitente}: {texto_usuario}")
            
            # Obtener o inicializar la fase del usuario
            fase_actual = USUARIOS_FASE.get(numero_remitente, 0)
            
            # Procesar el cerebro comercial de Jeniffer según la fase
            respuesta_texto, nueva_fase = motor_neuro_ventas(texto_usuario, fase_actual)
            
            # Actualizar la fase del cliente
            USUARIOS_FASE[numero_remitente] = nueva_fase
            
            # Retraso humano de 15 segundos para máxima naturalidad
            print("Aplicando pausa humana de 15 segundos...")
            time.sleep(15)
            
            # Enviar respuesta por la API Cloud de Meta
            enviar_mensaje_whatsapp(numero_remitente, respuesta_texto)
            
    except (KeyError, IndexError):
        pass
        
    return jsonify({"status": "received"}), 200

def motor_neuro_ventas(texto, fase):
    """
    Motor consultivo de ventas con el guión exacto de Jeniffer y progresión por fases.
    """
    # Manejo de objeción de dinero o dudas puntuales en cualquier momento
    if "dinero" in texto or "plata" in texto or "caro" in texto or "esperar" in texto or "quincena" in texto:
        return (
            "Entiendo perfectamente, la situación está difícil. " +
            "¿Te parece si te guardo la promoción y te contacto en la quincena para que no pierdas tu cupo clínico?"
        ), fase

    # FASE 1: APERTURA (Si saluda o pide info por primera vez)
    if fase == 0 or any(p in texto for p in ["hola", "info", "información", "precio", "programa", "cándida", "candida", "empezar"]):
        return (
            "Hola, soy Jeniffer 😊 Gracias por su confianza. " +
            "Mire, si usted ha probado óvulos, cremas y tratamientos médicos por más de 5 meses y el problema siempre regresa, " +
            "créame que la entiendo a la perfección porque yo viví ese mismo desgaste físico y emocional. " +
            "Cuénteme con confianza... ¿Siente que gasta dinero en farmacias y el ardor o la picazón jamás se van por completo?"
        ), 1

    # FASE 2: VALIDACIÓN PROFUNDA (El desahogo íntimo tras la respuesta de la fase 1)
    elif fase == 1:
        return (
            "Es desesperante, ¿verdad? Uno llega a un punto de frustración donde ya ni disfruta de su intimidad por miedo al dolor o al rechazo. " +
            "Cuénteme, ¿cómo es ese flujo que le molesta y cuánto tiempo lleva atrapada en este ciclo?"
        ), 2

    # FASE 3: LA AUTORIDAD Y LA SOLUCIÓN CLÍNICA
    elif fase == 2:
        return (
            "Mire, la razón por la que los tratamientos comunes fallan es porque solo tapan el síntoma superficial sin limpiar el ecosistema vaginal. " +
            "Nosotros aplicamos un protocolo avanzado a base de ácido bórico de grado médico que neutraliza el pH y erradica el hongo de raíz. " +
            "¿Usted quiere recuperar su salud íntima y volver a sentirse limpia y segura de una vez por todas?"
        ), 3

    # FASE 4: LA OFERTA IRRESISTIBLE
    elif fase == 3 or any(p in texto for p in ["sí", "si", "quiero", "claro", "estoy lista", "seguro"]):
        oferta_texto = (
            "Perfecto, esa es la decisión de una mujer valiente que no se resigna a vivir a medias\n\n" +
            "Normalmente este programa clínico especializado cuesta 25$. Pero hoy para que Usted comience su recuperación total, le daré acceso al **PROGRAMA ZERO CANDI** por solo 7.99$ (tasa BCV).\n\n" +
            "🧬 **PROGRAMA ZERO CANDI**. Incluye acceso a:\n\n" +
            "✅ **Protocolo de Limpieza:** Acceso a nuestro programa donde te enseñamos exactamente qué comprar, cómo preparar y cómo utilizar los componentes de ácido bórico para limpiar y restaurar tu vagina de forma segura.\n" +
            "🥗 **Recetario Exclusivo Anti-Cándida (15 Opciones):** Opciones deliciosas y prácticas libres de azúcares y harinas para cortar el alimento del hongo desde la cocina.\n" +
            "📋 **Checklist Diario de Control:** Una bitácora interactiva para que lleves el seguimiento exacto del día a día y no se te olvide ningún paso clave.\n" +
            "💡 **Sesión de Consejos Fundamentales:** Guía de hábitos esenciales para garantizar que todo el protocolo funcione al 100%.\n\n" +
            "POR TAN SOLO: 7.99$ (BCV)\n\n" +
            "🔓 Todo respaldado con una Garantía Blindada de 20 días (Cero riesgo para su bolsillo).\n\n" +
            "Dígame una sola cosa con el corazón en la mano... ¿Sí o sí está lista para asegurar hoy mismo una solución definitiva y dejar atrás este tormento?"
        )
        return oferta_texto, 4

    # FASE 5: CIERRE DE PAGO Y DATOS BANCARIOS
    elif fase == 4 and any(p in texto for p in ["sí", "si", "estoy", "listas", "comprar", "pago", "datos"]):
        pago_texto = (
            "¡Esa es la actitud! Usted no arriesga absolutamente nada, yo misma la respaldo. Aquí tiene los datos para el pago móvil:\n\n" +
            "🏦 Mercantil\n" +
            "🪪 25771166\n" +
            "📞 04121582154\n\n" +
            "Apenas me envíe la foto del comprobante por aquí, le activo su acceso inmediato a nuestra plataforma. ¿El pago lo hace Usted misma o se lo hace alguien más?"
        )
        return pago_texto, 5

    # FASE 6: LÓGICA DE ENTREGA (Tras recibir el comprobante o confirmación de pago)
    elif fase == 5 or any(p in texto for p in ["pago", "listo", "transferencia", "comprobante", "captura", "ya pagué"]):
        entrega_texto = (
            "¡Felicidades por dar este gran paso hacia su bienestar! Su usuario ya está activo en nuestra app innovadora de alta tecnología. Puede ingresar directamente aquí:\n" +
            "https://candida-zero.vercel.app/\n\n" +
            "📱 **Indicaciones de uso:**\n" +
            "1. Abra el enlace desde su teléfono móvil.\n" +
            "2. Explore de inmediato todo el contenido: el protocolo de limpieza y restauración vaginal, descargue su checklist diario, revise las 15 recetas y lea los consejos fundamentales.\n\n" +
            "Así recuperé mi salud desde casa. ¿Me confirma por favor si logró ingresar y abrir la plataforma sin problemas?"
        )
        return entrega_texto, 5

    # Comodín en caso de desvío
    else:
        return (
            "¿Vio por qué los tratamientos tradicionales son solo un parche temporal y regular el pH vaginal de raíz es lo único que frena la infección para siempre? " +
            "Dígame qué le pareció para explicarle cómo nuestro sistema logra ese mismo efecto clínico desde casa."
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
