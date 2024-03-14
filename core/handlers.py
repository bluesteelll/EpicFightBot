from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
import core.keyboards
import data.text_data
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from utils.sql_connector import SQliteConnector


class CharacterCreationStatesGroup(StatesGroup):
    race_id = State()
    name = State()


router = Router()
sql_connector = SQliteConnector('data/sql/test.db')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        data.text_data.START_TEXT,
        reply_markup=core.keyboards.stat_inline_keyboard_markup,
    )


@router.callback_query(F.data == 'help')
async def callback_help(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text(text='help',
                                     reply_markup=core.keyboards.help_inline_keyboard_markup)


@router.callback_query(F.data == 'create_character')
async def callback_create_character(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.edit_text(text='Выберите расу',
                                     reply_markup=core.keyboards.choose_race_inline_keyboard_markup)
    await state.set_state(CharacterCreationStatesGroup.race_id)


async def _accept_race(callback: CallbackQuery, state: FSMContext, race_id):
    await state.update_data(race_id=race_id)
    await callback.message.edit_text(text='Введите имя вашего персонажа')
    await state.set_state(CharacterCreationStatesGroup.name)


@router.callback_query(F.data == 'choose_race_human')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 1)


@router.callback_query(F.data == 'choose_race_golem')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 2)


@router.callback_query(F.data == 'choose_race_goblin')
async def callback_choose_race_human(callback: CallbackQuery, state: FSMContext):
    await _accept_race(callback, state, 3)


@router.message(CharacterCreationStatesGroup.name)
async def input_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    character_data = await state.get_data()

    await message.answer(f'Ваш персонаж:\n{character_data}')
    await state.clear()
    await sql_connector.add_user(message.from_user.id, character_data['name'], character_data['race_id'])


@router.message(F.text == 'hi')
async def hi(message: Message):
    await message.answer('hello')



