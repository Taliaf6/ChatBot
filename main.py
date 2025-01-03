
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.ext import ContextTypes

# Token del bot
TOKEN = "7351243032:AAFzXHmBTaQjgq5ZGDFGn38AHrd6x0VUcSo"

# Lista de herramientas extraída de los documentos
herramientasG = {
    "Telegram": "https://desktop.telegram.org/",
    "Microsoft 365": "https://signup.live.com/",
    "Clockify": "https://clockify.me/es/",
    "Odoo": "http://erp.pyxl.com.ar/",
    "Gather": "https://app.gather.town/app",
}

herramientasT = {
    "Norton": "https://ar.norton.com/",
    "Visual Studio Code": "https://code.visualstudio.com/",
    "Android Studio": "https://developer.android.com/studio?hl=es-419#get-android-studio",
    "GitHub": "https://github.com/",
    "GitHub Desktop": "https://desktop.github.com/download/",
    "Postman": "https://www.postman.com/",
    "MySQL": "https://dev.mysql.com/downloads/workbench/",
    "PostgreSQL": "https://www.postgresql.org/download/",
    "Notepad++": "https://notepad-plus-plus.org/downloads/",
    "Notion": "https://www.notion.so/es/desktop",
    "OBS": "https://obsproject.com/es",
    "VLC": "https://www.videolan.org/vlc/",
    "ChatGPT": "https://chatgpt.com/",
}

# Diccionario para almacenar los nombres de los usuarios
user_data = {}

# Diccionario de preguntas y respuestas
FAQ = {
    "telegram": {
    "Qué es Telegram?": "Telegram es una aplicación de mensajería instantánea que permite enviar mensajes, fotos, videos y archivos de manera rápida y segura.",
    "Cuáles son sus utilidades dentro del equipo?": "El equipo de desarrollo se suele comunicar por Telegram, sitio donde tenemos nuestros grupos de proyecto, es muy similar a WhatsApp, pero con la diferencia de que almacena los archivos en la nube siendo una mejor opción por si tenemos que recurrir a información.",
    "Cómo gestionarlo?": "1. Descargar Telegram Desktop desde el siguiente enlace: https://desktop.telegram.org/\n2. Configurarlo con el número de telefono personal.",
    "Qué es Webmail Pyxl?": "Es un servicio por suscripción que ofrece herramientas de productividad en la nube como Word, Excel, PowerPoint, Outlook y más. Además, incluye almacenamiento en OneDrive.",
    "Cómo accedo a Webmail Pyxl?": "1. Se debe crear una cuenta en el enlace: https://signup.live.com/\n2. Comunicarse con el encargado de gestión solicitando el alta de cuenta premium al mail creado anteriormente.",
    },
    "clockify": {
        "¿Cómo iniciar un temporizador en Clockify?": "Para iniciar un temporizador en Clockify, ve a la página principal y haz clic en 'Iniciar'.",
        "¿Cómo ver el historial en Clockify?": "Puedes ver tu historial de tiempo haciendo clic en 'Historial'..."
    },
    "odoo": {
        "¿Cómo crear un nuevo producto en Odoo?": "Para crear un nuevo producto, ve a la sección de 'Inventario' y selecciona 'Productos'.",
        "¿Cómo generar un reporte en Odoo?": "Para generar un reporte, ve a la sección 'Reportes' y selecciona el tipo de reporte..."
    },
    "gather": {
        "¿Cómo crear una reunión en Gather?": "Para crear una reunión en Gather, haz clic en 'Crear' y selecciona 'Reunión'.",
        "¿Cómo invitar a personas a Gather?": "Puedes invitar a personas a tu reunión generando un enlace desde la opción 'Invitar'..."
    }
}
# Función de inicio que pregunta por el nombre del usuario
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    await update.message.reply_text(
        "¡Hola! Soy el bot de PYXL Consulting. Por favor, dime tu nombre para comenzar."
    )
    context.user_data["name"] = None

# Función para guardar el nombre del usuario
async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    name = update.message.text
    context.user_data["name"] = name
    await update.message.reply_text(
        f"¡Encantado de conocerte, {name}! ¿Cómo puedo ayudarte hoy?",
        reply_markup=main_menu(),
    )

# Función para mostrar el menú principal
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Ver Herramientas Gestión", callback_data="ver_herramientasG")],
        [InlineKeyboardButton("Ver Herramientas Trabajo", callback_data="ver_herramientasT")],
        [InlineKeyboardButton("Preguntas frecuentes", callback_data="show_faq_main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Mostrar herramientas de gestión
async def show_herramientasG(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(nombre, url=url)] for nombre, url in herramientasG.items()
    ]
    keyboard.append([InlineKeyboardButton("Volver al menú", callback_data="main_menu")])
    await query.edit_message_text(
        "HERRAMIENTAS DE GESTION: Se debe dar de alta en las siguientes plataformas...",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
# Función para mostrar las herramientas de trabajo
async def show_herramientasT(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(nombre, url=url)] for nombre, url in herramientasT.items()
    ]
    keyboard.append([InlineKeyboardButton("Volver al menú", callback_data="main_menu")])
    await query.edit_message_text(
        "HERRAMIENTAS DE TRABAJO: Aquí están las herramientas que puedes usar...",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

# Función para manejar las preguntas frecuentes
async def show_faq_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Telegram", callback_data="telegram")],
        [InlineKeyboardButton("Clockify", callback_data="clockify")],
        [InlineKeyboardButton("Odoo", callback_data="odoo")],
        [InlineKeyboardButton("Gather", callback_data="gather")],
        [InlineKeyboardButton("Volver al menú principal", callback_data="main_menu")],
    ]
    await query.edit_message_text( "Selecciona una opción para obtener más información:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


    
# Configuración del bot
def main() -> None:
    application = Application.builder().token("7351243032:AAFzXHmBTaQjgq5ZGDFGn38AHrd6x0VUcSo").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_name))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_name))
    application.add_handler(CallbackQueryHandler(show_herramientasG, pattern="ver_herramientasG"))
    application.add_handler(CallbackQueryHandler(show_herramientasT, pattern="ver_herramientasT"))
    application.add_handler(CallbackQueryHandler(show_faq_main_menu, pattern="show_faq_main_menu"))
    application.add_handler(CallbackQueryHandler(main_menu, pattern="main_menu"))

# Llamada a la función principal
if __name__ == "__main__":
    main()
