from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# Token del bot
TOKEN = "7351243032:AAF-VyDBV8CvNO89D0rWF1VXFA9AGZcKMbA"

# Lista de herramientas extraída de los documentos
herramientas = {
    "Telegram": "https://desktop.telegram.org/",
    "Microsoft 365": "https://signup.live.com/",
    "Clockify": "https://clockify.me/es/",
    "Odoo": "http://erp.pyxl.com.ar/",
}

# Diccionario para almacenar los nombres de los usuarios
user_data = {}

# Diccionario de preguntas y respuestas
FAQ = {
    "Qué es Telegram?": "Telegram es una aplicación de mensajería instantánea que permite enviar mensajes, fotos, videos y archivos de manera rápida y segura.",
    "Cuáles son sus utilidades dentro del equipo?": "El equipo de desarrollo se suele comunicar por Telegram, sitio donde tenemos nuestros grupos de proyecto, es muy similar a WhatsApp, pero con la diferencia de que almacena los archivos en la nube siendo una mejor opción por si tenemos que recurrir a información.",
    "Cómo gestionarlo?": "1. Descargar Telegram Desktop desde el siguiente enlace: https://desktop.telegram.org/\n2. Configurarlo con el número de telefono personal.",
    "Qué es Webmail Pyxl?": "Es un servicio por suscripción que ofrece herramientas de productividad en la nube como Word, Excel, PowerPoint, Outlook y más. Además, incluye almacenamiento en OneDrive.",
    "Cómo accedo a Webmail Pyxl?": "1. Se debe crear una cuenta en el enlace: https://signup.live.com/\n2. Comunicarse con el encargado de gestión solicitando el alta de cuenta premium al mail creado anteriormente.",
    # Agrega más preguntas y respuestas aquí
}

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update.message.reply_text(
        "¡Hola! Soy el bot de PYXL Consulting. Por favor, dime tu nombre para comenzar."
    )
    user_data[user_id] = {"name": None}

# Guardar nombre del usuario
async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    name = update.message.text
    user_data[user_id] = {"name": name}
    await update.message.reply_text(
        f"¡Encantado de conocerte, {name}! ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu(),
    )

# Menú principal
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Ver herramientas disponibles", callback_data="ver_herramientas")],
        [InlineKeyboardButton("Ver preguntas frecuentes", callback_data="ver_preguntas")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Mostrar herramientas
async def show_herramientas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(nombre, url)] for nombre, url in herramientas.items()
    ]
    keyboard.append([InlineKeyboardButton("Volver al menú", callback_data="menu_principal")])
    await query.edit_message_text(
        "HERRAMIENTAS DE GESTION: Se debe dar de alta en las siguientes plataformas. Todas las plataformas deben darse de alta con la cuenta de mail asignada por PYXL y la clave deseada. ¡Selecciona una herramienta para más información!:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Mostrar preguntas frecuentes
async def show_preguntas(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(pregunta, callback_data=f"pregunta_{pregunta}")] for pregunta in FAQ.keys()
    ]
    keyboard.append([InlineKeyboardButton("Volver al menú", callback_data="menu_principal")])
    await query.edit_message_text(
        "Selecciona una pregunta para ver la respuesta:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Mostrar respuesta a una pregunta
async def show_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    pregunta = query.data.replace("pregunta_", "")  # Extraemos la pregunta de la callback_data
    respuesta = FAQ.get(pregunta, "Lo siento, no tengo una respuesta para esa pregunta.")
    await query.answer()
    await query.edit_message_text(
        f"Pregunta: {pregunta}\n\nRespuesta: {respuesta}",
        reply_markup=main_menu(),
    )

# Volver al menú principal
async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "¿Cómo puedo ayudarte hoy?", reply_markup=main_menu()
    )

# Configuración del bot
def main() -> None:
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()

    # Agregar manejadores
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_name))
    application.add_handler(CallbackQueryHandler(show_herramientas, pattern="^ver_herramientas$"))
    application.add_handler(CallbackQueryHandler(show_preguntas, pattern="^ver_preguntas$"))
    application.add_handler(CallbackQueryHandler(show_respuesta, pattern="^pregunta_"))
    application.add_handler(CallbackQueryHandler(back_to_menu, pattern="^menu_principal$"))

    # Ejecutar el bot
    application.run_polling()

#if __name__ == "__main__":
#   main()
