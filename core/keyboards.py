from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from data.text_data import YOUTUBE_LINK, WIKI_LINK

start_inline_buttons = [
    [InlineKeyboardButton(text='Создать персонажа',
                          callback_data='create_character')],
    [InlineKeyboardButton(text='Справка',
                          callback_data='help')]]

choose_race_inline_buttons = [
    [InlineKeyboardButton(text='Человек',
                          callback_data='choose_race_human')],
    [InlineKeyboardButton(text='Голем',
                          callback_data='choose_race_golem')],
    [InlineKeyboardButton(text='Гоблин',
                          callback_data='choose_race_goblin')]
]

help_inline_buttons = [
    [InlineKeyboardButton(text='YouTube',
                          url=YOUTUBE_LINK)],
    [InlineKeyboardButton(text='Wiki',
                          url=WIKI_LINK)]]

menu_inline_buttons = [[InlineKeyboardButton(text='Добавить бота в чат',
                                             callback_data='add_bot_to_chat')],
                       [InlineKeyboardButton(text='Справка',
                                             callback_data='help')]]

stat_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=start_inline_buttons)
help_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=help_inline_buttons)
choose_race_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=choose_race_inline_buttons)
