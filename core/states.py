from aiogram.fsm.state import StatesGroup, State


class CharacterCreationStatesGroup(StatesGroup):
    race_id = State()
    name = State()


class MenuStatesGroup(StatesGroup):
    main_menu = State()
    start = State()
    level_up = State()
