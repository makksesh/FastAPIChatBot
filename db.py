from fastapi import FastAPI
from sqlalchemy import create_engine, ForeignKey, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url="sqlite:///chatbot.db")
session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

# class Users(Base):
#     __tablename__ = "users"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column()
#     email: Mapped[str] = mapped_column()
#     ip: Mapped[str] = mapped_column(index=True)

class ChatRequests(Base):
    __tablename__ = "chat_requests"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

def get_user_requests(ip_address: str) -> list[ChatRequests]:
    with session() as new_session:
        query = select(ChatRequests).filter_by(ip_address=ip_address)
        result = new_session.execute(query)
        return result.scalars().all()

def add_user_data(ip_address: str, prompt: str, response: str) -> None:
    with session() as new_session:
        new_data = ChatRequests(
            ip_address=ip_address,
            prompt=prompt,
            response=response
        )
        new_session.add(new_data)
        new_session.commit()
