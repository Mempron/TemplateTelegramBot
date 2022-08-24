from typing import Dict, Any

from aiogram.dispatcher.router import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..keyboards.user import kb_inline_builder_confirm

user_router = Router()


class UserRegister(StatesGroup):
    input_name = State()
    input_age = State()


@user_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(f'Привет, <b>{message.from_user.full_name}!</b>\n/register - зарегистрироваться')


@user_router.message(Command(commands=['register']))
async def process_name(message: Message, state: FSMContext, **kwargs) -> None:
    user: User = kwargs.get('user')

    if user:
        await message.answer('Вы и так уже зарегистрированы!')
        return

    await message.answer(f'Возможно, <b>{message.from_user.full_name}</b> твоё ненастоящее имя.\nТак '
                         f'что напиши, пожалуйста, как тебя действительно зовут на самом деле.')
    await state.set_state(UserRegister.input_name)


@user_router.message(UserRegister.input_name)
async def process_age(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(f'А сколько тебе лет, <b>{message.text}</b>?')
    await state.set_state(UserRegister.input_age)


@user_router.message(UserRegister.input_age)
async def foo(message: Message, state: FSMContext) -> None:
    age = int(message.text)
    data = await state.update_data(age=age)
    await show_summary(message, data)


async def show_summary(message: Message, data: Dict[str, Any]) -> None:
    name = data.get('name')
    age = data.get('age')
    text = f'Тебя зовут <b>{name}</b> и тебе <b>{age}</b>?'
    await message.answer(text=text, reply_markup=kb_inline_builder_confirm.as_markup())


@user_router.callback_query(text='yes')
async def finish_registration(callback: CallbackQuery, state: FSMContext, **kwargs) -> None:
    await callback.answer('Ваша регистрация успешно завершена')
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    session: AsyncSession = kwargs.get('session')

    user = User(telegram_id=callback.from_user.id, name=name, age=age)
    session.add(user)
    await session.commit()

    await state.clear()


@user_router.callback_query(text='no')
async def finish_registration(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
