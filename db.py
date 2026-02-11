from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. Движок БД
DATABASE_URL = "sqlite+aiosqlite:///chatbot.db"

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=True,
)

# 2. Фабрика сессий
async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,  # чтобы объекты не «отваливались» после commit
    class_=AsyncSession,
)


# 3. Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# 4. Модель таблицы
class ChatRequests(Base):
    __tablename__ = "chat_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

# 5. Функция инициализации схемы
async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# 6. CRUD-функции

async def get_user_requests(ip_address: str) -> list[ChatRequests]:
    async with async_session() as session:
        stmt = select(ChatRequests).filter_by(ip_address=ip_address)
        result = await session.execute(stmt)
        return result.scalars().all()


async def add_user_data(ip_address: str, prompt: str, response: str) -> None:
    async with async_session() as session:
        new_data = ChatRequests(
            ip_address=ip_address,
            prompt=prompt,
            response=response,
        )
        session.add(new_data)
        await session.commit()
