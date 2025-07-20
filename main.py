import telebot
import time

bot = telebot.TeleBot('8039298984:AAGCrSGu3G7c92Irv8PdMo7JDKVe5V1LA2c')

# Конфигурация администратора
admin = 'imlegendoflegends'
admin_id = '2079770501'

orders = []


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.from_user.username.lower() != admin:
        # Обработка сообщений от пользователей
        bot.send_message(message.chat.id,
                         "Здравствуйте, вы можете заказать тут генерацию картинки абсолютно бесплатно. Просто отправьте свой промпт. Для повышения результата, пишите на английском. Чтобы не перенапрячь сервера, все заказы сгенерируются в течении 4 часов с 18:00 до 22:00 по мск.")


        mes = message.text

        if mes != '/start':
            orders.append({'user_id': message.from_user.id, 'order': mes})

    elif message.from_user.username.lower() == admin:
        # Команды администратора
        mes = message.text
        if mes.lower() == "заказы":
            if orders:
                orders_list = "\n".join([f"ID: {order['user_id']} Заказ: {order['order']}" for order in orders])
                bot.send_message(admin_id, f"Список заказов:\n{orders_list}")
            else:
                bot.send_message(admin_id, "Нет активных заказов.")

        elif mes.lower() == "очистить заказы":
            orders.clear()
            bot.send_message(admin_id, "Список заказов успешно очищен.")

        elif mes.startswith('ID:'):
            # Отправка фото пользователю
            parts = mes.split()
            if len(parts) >= 3 and parts[2].lower() == 'фото':
                bot.send_message(admin_id, "Теперь отправьте фото для этого пользователя.")
                bot.register_next_step_handler(message, process_photo, user_id=parts[1])


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.from_user.username.lower() == admin:
        bot.send_message(admin_id,
                         "Чтобы отправить фото пользователю, сначала введите его ID в формате: 'ID: 123456789 фото'")


def process_photo(message, user_id):
    if message.content_type == 'photo':
        try:
            file_id = message.photo[-1].file_id
            bot.send_photo(user_id, file_id)
            bot.send_message(admin_id, f"Фото успешно отправлено пользователю с ID {user_id}")
        except Exception as e:
            bot.send_message(admin_id, f"Ошибка при отправке фото: {e}")
    else:
        bot.send_message(admin_id, "Вы отправили не фото. Попробуйте снова.")


if __name__ == '__main__':
    bot.infinity_polling()