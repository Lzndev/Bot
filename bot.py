import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

# Substitua 'TOKEN' pelo token real do seu bot do Telegram
bot = telebot.TeleBot("6083889471:AAFz0csB6XG_w-_OKE1R6PKAeP27AFjpFD8")

# Estados para a conversa
LINK_STATE = 1

# Função para iniciar a conversa
@bot.message_handler(commands=['anime'])
def start(message):
    bot.send_message(message.chat.id, "Envie o ID do anime no seguinte formato: /anime {id}")
    bot.register_next_step_handler(message, receive_id)

# Função para receber o ID do anime
def receive_id(message):
    link = message.text

    # Extrair o ID do anime do texto fornecido
    parts = link.split("_")
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Por favor, envie o ID do anime no formato correto.")
        return

    anime_id = parts[1]

    # Montar o link com base no ID recebido
    assistir_link = f"https://animesflix.net/assistir/{anime_id}"

    # Extrair informações do link usando BeautifulSoup
    try:
        response = requests.get(assistir_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            capa = soup.find('img', {'alt': 'Image Naruto'})['src']
            descricao = soup.find('div', {'class': 'description'}).find('p').text.strip()

            # Obter a imagem em formato binário
            image_response = requests.get(capa)
            image_data = image_response.content

            # Montar a mensagem com a descrição e o botão
            message_text = f"Descrição: {descricao}\nClique no botão abaixo para assistir dublado:"
            markup = types.InlineKeyboardMarkup()
            assistir_button = types.InlineKeyboardButton("🈂️ Assistir Dublado", url="https://t.me/anim_club_md")
            markup.add(assistir_button)

            # Enviar a mensagem com a imagem, descrição e botão
            bot.send_photo(message.chat.id, photo=("image.jpg", image_data), caption=message_text, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Não foi possível acessar o link. Verifique o ID do anime e tente novamente.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ocorreu um erro: {str(e)}")

# Função para cancelar a conversa
@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, "Conversa cancelada.")

# Iniciar o bot
bot.polling()