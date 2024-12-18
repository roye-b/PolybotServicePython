import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from polybot.img_proc import Img


class Bot:

    def __init__(self, token, bot_app_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{bot_app_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')

        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ImageProcessingBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')
        try:
            my_img = None
            if msg["caption"] == "Salt and pepper":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                my_img.salt_n_pepper()
            elif msg["caption"] == "Segment":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                my_img.segment()
            elif msg["caption"] == "Contour":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                my_img.contour()
            elif msg["caption"] == "Blur":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                my_img.blur()
            if msg["caption"] == "Concat":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                image_path2 = self.download_user_photo(msg)
                another_img = Img(image_path2)
                my_img.concat(another_img)
            if msg["caption"] == "Rotate":
                image_path = self.download_user_photo(msg)
                my_img = Img(image_path)
                my_img.rotate()

            if my_img is not None:
                self.send_photo(msg["chat"]["id"], my_img.save_img())
        except KeyError as ke:
            logger.error(f"Missing key in message: {ke}")
            self.send_text(msg["chat"]["id"], "An error occurred: Missing required data in the message.")
        except FileNotFoundError as fnfe:
            logger.error(f"File not found: {fnfe}")
            self.send_text(msg["chat"]["id"], "An error occurred: Unable to find the file.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            self.send_text(msg["chat"]["id"], "An unexpected error occurred. Please try again.")







            
            
