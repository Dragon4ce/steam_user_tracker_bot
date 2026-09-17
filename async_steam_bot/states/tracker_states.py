from aiogram.fsm.state import State, StatesGroup

class UserTrackerState(StatesGroup):
    steam_link = State()
    track_type = State()
