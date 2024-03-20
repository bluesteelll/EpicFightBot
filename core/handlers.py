from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
import core.keyboards
import data.text_data
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from utils.sql_connector import SQliteConnector
from utils.giphy_connector import GiphyConnector
from datetime import datetime
from config import DB_PATH
from core.states import CharacterCreationStatesGroup, MenuStatesGroup

# Setup router and utilities
router = Router()
sql_connector = SQliteConnector(DB_PATH)
giphy_connector = GiphyConnector()


# Support functions

async def _accept_race(callback: CallbackQuery, state: FSMContext, race_id):
    await state.update_data(race_id=race_id)
    await callback.message.edit_text(text='Введите имя вашего персонажа')
    await state.set_state(CharacterCreationStatesGroup.name)


async def _get_user_profile_str(user_id):
    user = await sql_connector.get_user(user_id)
    return f'''Ваш профиль\n
            Персонаж: {user['name']}
            Уровень: {user['level']}
            Очков улучшения: {user['level_points']}
            Здоровье: {user['health']}
            Максимальное здоровье: {user['max_health']}
            Урон: {user['damage']}
            Убийства: {user['kills']}
            '''


async def _open_main_menu(message: Message, state: FSMContext, user_id, new_message=False):
    menu_text = await _get_user_profile_str(user_id)
    if new_message:
        await message.answer(text=menu_text,
                             reply_markup=core.keyboards.main_menu_keyboard_markup)
    else:
        await message.edit_text(text=menu_text,
                                reply_markup=core.keyboards.main_menu_keyboard_markup)

    await state.set_state(MenuStatesGroup.main_menu)


async def _open_level_up_menu(callback: CallbackQuery):
    user = await sql_connector.get_user(callback.from_user.id)

    await callback.message.edit_text(f'''
    У вас {user['level_points'] if user['level_points'] != 0 else 'нет'} очков улучшения\n
         Максимальное здоровье: {user['max_health']}
         Урон: {user['damage']}''',
                                     reply_markup=core.keyboards.level_up_keyboard_markup)


# Handlers

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        data.text_data.START_TEXT,
        reply_markup=core.keyboards.stat_inline_keyboard_markup)

    await state.set_state(MenuStatesGroup.start)


@router.callback_query(F.data == 'help')
async def callback_help(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text='''''',
                                     reply_markup=core.keyboards.help_inline_keyboard_markup)


@router.callback_query(F.data == 'create_character')
async def callback_create_character(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(text='Выберите расу',
                                     reply_markup=core.keyboards.choose_race_inline_keyboard_markup)
    await state.set_state(CharacterCreationStatesGroup.race_id)


@router.callback_query(F.data == 'choose_race_human')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 1)


@router.callback_query(F.data == 'choose_race_golem')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 2)


@router.callback_query(F.data == 'choose_race_goblin')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 3)


@router.callback_query(F.data == 'back', MenuStatesGroup.start)
async def callback_choose_race_human(callback: CallbackQuery):
    await callback.message.edit_text(data.text_data.START_TEXT,
                                     reply_markup=core.keyboards.stat_inline_keyboard_markup)


@router.callback_query(F.data == 'open_level_up')
async def callback_choose_race_human(callback: CallbackQuery):
    await _open_level_up_menu(callback)


@router.callback_query(F.data == 'back', MenuStatesGroup.main_menu)
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _open_main_menu(callback.message, state, callback.from_user.id)


@router.message(CharacterCreationStatesGroup.name)
async def input_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    character_data = await state.get_data()
    await sql_connector.add_user(message.from_user.id, character_data['name'], character_data['race_id'])
    await _open_main_menu(message, state, message.from_user.id, new_message=True)


@router.message(F.text.lower() == 'видра')
async def cat(message: Message, state: State, bot: Bot):
    await message.answer_animation(animation=giphy_connector.get_random_url('otter'))


@router.message(F.text.lower() == 'котик')
async def cat(message: Message, state: State, bot: Bot):
    await message.answer_animation(animation=giphy_connector.get_random_url('cat'))


@router.message(F.text.lower() == 'атака')
async def attack(message: Message, state: State, bot: Bot):
    attacker_dead_until = await sql_connector.user_is_dead(message.from_user.id)
    if attacker_dead_until:
        await message.reply(text=f'''Ты не можешь атокавать когда мертв!
Жди возраждения в {attacker_dead_until}''')

    elif await sql_connector.user_is_dead(message.reply_to_message.from_user.id):
        await message.reply(text=f'''Ты не можешь атокавать мертвого игрока!''')
    else:
        level_up = await sql_connector.attack(message.from_user.id, message.reply_to_message.from_user.id)
        if level_up:
            await bot.send_message(chat_id=message.from_user.id,
                                   text='У вас новый уровень!',
                                   reply_markup=core.keyboards.main_menu_keyboard_markup)
        defender = await sql_connector.get_user(message.reply_to_message.from_user.id)
        attacker = await sql_connector.get_user(message.from_user.id)
        if datetime.fromisoformat(defender['dead_until']) > datetime.now():
            await message.answer(text=f'''
                        Ой ой ой!
                        {await sql_connector.get_race_name(attacker['rid'])} {attacker['name']} УБИЛ
                        {await sql_connector.get_race_name(defender['rid'])}а {defender['name']}!
                        
                        Теперь у {attacker['name']} {attacker['kills']} убийств!
                        ''')
        else:
            await message.answer(text=f'''
            Вау!
            {await sql_connector.get_race_name(attacker['rid'])} {attacker['name']} напал на
            {await sql_connector.get_race_name(defender['rid'])}а {defender['name']}

            Теперь у {defender['name']} {defender['health']} здоровья!

            ''')


@router.message(F.text.lower() == 'профиль')
async def callback_profile(message: Message):
    # user = await sql_connector.get_user(message.from_user.id)
    await message.reply(text=await _get_user_profile_str(message.from_user.id))


@router.message(Command('wipe'))
async def callback_profile(message: Message, bot: Bot):
    if await sql_connector.is_admin(message.from_user.id):
        # user = await sql_connector.get_user(message.from_user.id)
        for i in await sql_connector.get_users_id():
            await bot.send_message(chat_id=i['id'], text='''Сейчас будет происходить вайп!
            ваши данные удалятся и вам придется регистрироваться заново!''')
        await sql_connector.clear_users()
    else:
        await message.reply(text='Это каманда доступна только аддминам')


@router.callback_query(F.data == 'profile')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _open_main_menu(callback.message, state, callback.from_user.id)


@router.callback_query(F.data == 'upgrade_health')
async def callback_upgrade_health(callback: CallbackQuery, state: FSMContext):
    if await sql_connector.get_level_points(callback.from_user.id) != 0:
        await sql_connector.add_max_health(callback.from_user.id, 50)
        await sql_connector.reduce_level_points(callback.from_user.id)
        await _open_level_up_menu(callback)


@router.callback_query(F.data == 'upgrade_damage')
async def callback_upgrade_health(callback: CallbackQuery, state: FSMContext):
    if await sql_connector.get_level_points(callback.from_user.id) != 0:
        await sql_connector.add_damage(callback.from_user.id, 25)
        await sql_connector.reduce_level_points(callback.from_user.id)
        await _open_level_up_menu(callback)
