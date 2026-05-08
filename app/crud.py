import uuid
from decimal import Decimal
from sqlalchemy import select
from app.database import async_session_maker
from app.models import Wallet


async def get_wallet(wallet_id: uuid.UUID) -> Wallet | None:
    """Получить кошелёк по ID (без блокировки)."""
    async with async_session_maker() as session:
        result = await session.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalar_one_or_none()


async def operate_wallet(
    wallet_id: uuid.UUID, operation_type: str, amount: Decimal
) -> Wallet | str | None:
    """
    Изменить баланс кошелька.
    Возвращает:
        - объект Wallet при успехе,
        - None если кошелёк не найден,
        - "insufficient_funds" при нехватке средств.
    """
    async with async_session_maker() as session:
        async with session.begin():
            # Блокируем строку для безопасного конкурентного обновления
            result = await session.execute(
                select(Wallet)
                .where(Wallet.id == wallet_id)
                .with_for_update()
            )
            wallet = result.scalar_one_or_none()
            if not wallet:
                return None

            if operation_type == "DEPOSIT":
                wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if wallet.balance < amount:
                    return "insufficient_funds"
                wallet.balance -= amount
            else:
                return "invalid_operation"

            # При выходе из session.begin() транзакция закоммитится
            return wallet