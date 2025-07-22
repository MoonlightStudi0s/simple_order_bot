import telebot

bot = telebot.TeleBot('8039298984:AAGCrSGu3G7c92Irv8PdMo7JDKVe5V1LA2c')

# Конфигурация администратора
admin = 'imlegendoflegends'
admin_id = '2079770501'

flag = 0

def write_order(mes, id):
    with open("order.txt", 'a') as file:
        file.write(f"ID: {id} Заказ: {mes}\n")

def delete_orders():
    with open("order.txt", 'w'):
        pass

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global flag
    if message.from_user.username.lower() != admin:
        bot.send_message(message.chat.id,
                         "Здравствуйте, вы можете заказать тут генерацию картинки абсолютно бесплатно. Просто отправьте свой промпт. Для повышения результата, пишите на английском. Чтобы не перенапрячь сервера, все заказы сгенерируются в течении 4 часов с 18:00 до 22:00 по мск.")

        mes = message.text
        id = message.from_user.id
        if mes != '/start':
            write_order(mes, id)
            flag = 1

    else:
        mes = message.text
        if mes.lower() == "заказы":
            with open("order.txt", 'r') as file:
                content = file.read()
                if content:
                    bot.send_message(admin_id, content)
                else:
                    bot.send_message(admin_id, "Нет доступных заказов")
        elif mes.lower() == "очистить заказы":
            delete_orders()
            flag = 0
            bot.send_message(admin_id, "Список заказов успешно очищен.")

        elif mes.startswith('ID:'):
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
