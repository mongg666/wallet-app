from decimal import Decimal
import uuid
import threading
from fastapi.testclient import TestClient


def test_operation_wallet_not_found(client: TestClient):
    fake_id = str(uuid.uuid4())
    response = client.post(
        f"/api/v1/wallets/{fake_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 100},
    )
    assert response.status_code == 404


def test_deposit_and_get_balance(client: TestClient):
    create_resp = client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet_id = create_resp.json()["wallet_id"]

    # Депозит 500
    resp = client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": 500},
    )
    assert resp.status_code == 200
    # Баланс возвращается как строка, преобразуем в Decimal
    balance = Decimal(resp.json()["balance"])
    assert balance == Decimal("500.00")

    # Получение баланса
    get_resp = client.get(f"/api/v1/wallets/{wallet_id}")
    assert get_resp.status_code == 200
    assert Decimal(get_resp.json()["balance"]) == Decimal("500.00")


def test_withdraw_insufficient_funds(client: TestClient):
    create_resp = client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet_id = create_resp.json()["wallet_id"]

    resp = client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": 200},
    )
    assert resp.status_code == 402


def test_concurrent_deposits(client: TestClient):
    create_resp = client.post("/api/v1/wallets")
    assert create_resp.status_code == 201
    wallet_id = create_resp.json()["wallet_id"]

    results = []
    lock = threading.Lock()

    def deposit(amount):
        resp = client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={"operation_type": "DEPOSIT", "amount": amount},
        )
        with lock:
            results.append(resp)

    threads = []
    for _ in range(20):
        t = threading.Thread(target=deposit, args=(50,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    assert all(r.status_code == 200 for r in results)

    get_resp = client.get(f"/api/v1/wallets/{wallet_id}")
    assert get_resp.status_code == 200
    # Ожидаем 20 * 50 = 1000.00
    assert Decimal(get_resp.json()["balance"]) == Decimal("1000.00")