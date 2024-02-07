import telebot
from google.cloud import translate_v2 as translate
from google.cloud import texttospeech

# Initialize the translation and text-to-speech clients
translate_client = translate.Client()
text_to_speech_client = texttospeech.TextToSpeechClient()

# Telegram Bot token
TOKEN = '6821196414:AAEu-ulIbbSkm18WKtfb5JXQcXQHUTEs7bM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Translate the incoming message to English
    translated_text = translate_client.translate(message.text, target_language='en')['translatedText']

    # Convert translated text to a voice message
    synthesis_input = texttospeech.SynthesisInput(text=translated_text)
    voice_params = texttospeech.VoiceSelectionParams(language_code='en', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = text_to_speech_client.synthesize_speech(input=synthesis_input, voice=voice_params, audio_config=audio_config)

    # Send voice message back to the user
    bot.send_voice(message.chat.id, response.audio_content)

bot.polling()
