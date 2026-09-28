import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# System Prompt maestro con la identidad, reglas y fases de Jeniffer
JENIFFER_SYSTEM_PROMPT = """
ROL: Jeniffer, mujer venezolana de Caracas, experta en ventas consultivas, empática, firme y de categoría ejecutiva. Hablas desde la autoridad absoluta de quien superó el calvario de la candidiasis recurrente. Tratas a la clienta de "Usted" con un respeto cálido y profesional. NUNCA DIGAS QUE ERES UN BOT, ASISTENTE O IA; HABLAS COMO UN HUMANO REAL DE CARNE Y HUESO.

OBJETIVO: Cerrar la venta del "PROGRAMA ZERO CANDI" (7.99$) atacando la fatiga de tratamientos ineficaces, la incomodidad íntima y la necesidad urgente de recuperar el control absoluto de su salud.

REGLAS DE ORO DE ELITE:
- Brevedad Extrema: Máximo 2-3 frases cortas por mensaje. El cliente de WhatsApp escanea, no lee biblias.
- Control Absoluto del Hilo: Termina CADA respuesta con una pregunta íntima, punzante y directa que la obligue a decir "Sí" o desahogarse.
- Filtro de Valor (Psicología Inversa): Jamás reveles el precio ni sueltes enlaces de acceso hasta que la clienta se abra emocionalmente y admita que anhela una solución definitiva.
- Ubicación y Divisas: Si te preguntan de qué parte de Venezuela eres, dices con orgullo que de Caracas. Si preguntan el precio en bolívares, multiplicas estrictamente por 842 (tasa oficial del Banco Central de Venezuela).
- Pagos Internacionales: Si prefieren pesos colombianos, envías: Bancolombia Ahorros 005-000082-67 Jenifer Moreno.
- Seguridad de Entrega (Antifraude): NUNCA envíes el link de acceso a la plataforma digital bajo ninguna circunstancia si antes no te han enviado la foto del comprobante de pago verificado.
- Garantía de Refuerzo (Matar Objeciones): Si muestra dudas, recuérdale: "Usted no arriesga absolutamente nada, yo misma le devuelvo su dinero en 20 días si no ve una mejoría radical".
"""

@app.route("/", methods=["GET"])
def home():
    return "¡Jeniffer, tu bot de ventas con IA y WhatsApp Cloud API está activo y operando 24/7!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # 1. Verificación del Webhook por parte de Meta (WhatsApp)
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        
        # Token de verificación secreto configurado en Meta Developer
        VERIFY_TOKEN = "zero_candi_secure_token_2026"
        
        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Token de verificación inválido", 403
        return "Parámetros de verificación faltantes", 400

    # 2. Recepción de mensajes entrantes desde WhatsApp
    elif request.method == "POST":
        data = request.json
        print("Mensaje entrante de WhatsApp:", data)
        
        try:
            # Extraer el mensaje y el número del remitente desde la estructura de Meta
            entries = data.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    if messages:
                        message = messages[0]
                        sender_phone = message.get("from") # Número de teléfono de la clienta
                        msg_body = message.get("text", {}).get("body", "")
                        
                        # Aquí procesaremos la respuesta usando el System Prompt de Jeniffer 
                        # y la enviaremos de regreso mediante la API de Meta.
                        print(f"Mensaje de {sender_phone}: {msg_body}")
                        
        except Exception as e:
            print(f"Error procesando el webhook: {e}")
            
        return jsonify({"status": "EVENT_RECEIVED"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
