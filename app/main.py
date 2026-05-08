from contextlib import asynccontextmanager
import uuid
from fastapi import FastAPI, HTTPException
from app.database import init_db, async_session_maker
from app.schemas import OperationRequest, WalletResponse
from app import crud
from app.models import Wallet


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Всегда создаём таблицы при старте
    await init_db()
    yield


app = FastAPI(title="Wallet API", lifespan=lifespan)


@app.post("/api/v1/wallets", status_code=201, response_model=WalletResponse)
async def create_wallet():
    async with async_session_maker() as session:
        async with session.begin():
            wallet = Wallet()
            session.add(wallet)
            await session.flush()
            return WalletResponse(wallet_id=str(wallet.id), balance=wallet.balance)


@app.post("/api/v1/wallets/{wallet_uuid}/operation")
async def change_balance(wallet_uuid: uuid.UUID, op: OperationRequest):
    result = await crud.operate_wallet(wallet_uuid, op.operation_type.value, op.amount)
    if result is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if result == "insufficient_funds":
        raise HTTPException(status_code=402, detail="Insufficient funds")
    if result == "invalid_operation":
        raise HTTPException(status_code=400, detail="Invalid operation type")
    return WalletResponse(wallet_id=str(result.id), balance=result.balance)


@app.get("/api/v1/wallets/{wallet_uuid}", response_model=WalletResponse)
async def get_balance(wallet_uuid: uuid.UUID):
    wallet = await crud.get_wallet(wallet_uuid)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return WalletResponse(wallet_id=str(wallet.id), balance=wallet.balance)
