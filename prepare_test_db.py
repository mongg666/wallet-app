import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base

async def main():
    engine = create_async_engine(
        "postgresql+asyncpg://wallet_user:wallet_pass@localhost:5432/test_wallet_db",
        echo=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

asyncio.run(main())