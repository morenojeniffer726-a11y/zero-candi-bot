from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "¡Jeniffer, tu bot de ventas está activo y operando 24/7!", 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificación del Webhook de Meta
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        # Coloca aquí el token de verificación que inventarás
        VERIFY_TOKEN = "micodigosecreto123"

        if mode and token:
            if mode == "subscribe" and token == VERIFY_TOKEN:
                return challenge, 200
            else:
                return "Token inválido", 403
        return "Error de verificación", 400

    elif request.method == "POST":
        # Aquí recibiremos los mensajes de las clientas de WhatsApp
        data = request.json
        print(data)
        return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
