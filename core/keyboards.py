from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton)
from config import YOUTUBE_LINK, WIKI_LINK

# Keyboards and markups

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
                          url=WIKI_LINK)],
    [InlineKeyboardButton(text='Назад',
                          callback_data='back')]
]

main_menu_inline_buttons = [[InlineKeyboardButton(text='Обновить профиль',
                                                  callback_data='profile')],
                            [InlineKeyboardButton(text='Увеличить уровень',
                                                  callback_data='open_level_up')],
                            [InlineKeyboardButton(text='Справка',
                                                  callback_data='help')]]

level_up_buttons = [[InlineKeyboardButton(text='Здоровье',
                                          callback_data='upgrade_health')],
                    [InlineKeyboardButton(text='Урон',
                                          callback_data='upgrade_damage')],
                    [InlineKeyboardButton(text='Назад',
                                          callback_data='back')]]

stat_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=start_inline_buttons)
help_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=help_inline_buttons)
choose_race_inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=choose_race_inline_buttons)
level_up_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=level_up_buttons)
main_menu_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=main_menu_inline_buttons)
