import os
import threading
from flask import Flask, request, jsonify
import telebot

# =============================
# DADOS FIXOS (FORNECIDOS POR VOCÊ)
# =============================
BOT_TOKEN = "7767214512:AAHVGTipD03AgwRH2qRnNHg2vV0Gite3uT0"
PADDLE_PRODUCT_ID = "pro_01kg2q7nwe8bqkvhtvm5015m7j"
CHAT_ID = "-1003550834121"

# Link do grupo privado (troque se necessário)
PRIVATE_GROUP_LINK = "https://t.me/+SEULINKPRIVADO"

# =============================
# INICIALIZAÇÕES
# =============================
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# =============================
# COMANDO /start
# =============================
@bot.message_handler(commands=["start"])
def start(message):
    text = (
        "🔥 ACESSO EXCLUSIVO\n\n"
        "💰 Valor único: R$ 21,90\n\n"
        "Clique abaixo para realizar o pagamento.\n"
        "Após a confirmação, você receberá o acesso ao conteúdo privado."
    )

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            "🔓 Acessar o conteúdo aqui",
            url=f"https://checkout.paddle.com/checkout/{PADDLE_PRODUCT_ID}"
        )
    )

    bot.send_message(message.chat.id, text, reply_markup=markup)

# =============================
# WEBHOOK PADDLE
# =============================
@app.route("/paddle/webhook", methods=["POST"])
def paddle_webhook():
    data = request.form.to_dict()

    # Paddle pode variar o nome do evento
    event_type = data.get("event_type") or data.get("alert_name")

    if event_type in ["payment_succeeded", "payment_completed"]:
        customer_email = data.get("customer_email", "email_nao_informado")

        # Envia acesso automaticamente (exemplo direto)
        bot.send_message(
            CHAT_ID,
            f"✅ Novo pagamento confirmado!\n📧 {customer_email}"
        )

    return jsonify({"status": "ok"}), 200

# =============================
# HEALTH CHECK (Railway)
# =============================
@app.route("/")
def home():
    return "Bot + Paddle Webhook rodando corretamente 🚀", 200

# =============================
# THREAD DO BOT
# =============================
def run_bot():
    bot.infinity_polling(skip_pending=True)

# =============================
# MAIN (RAILWAY)
# =============================
if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )

