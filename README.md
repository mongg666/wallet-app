 **Требования**

> ● **Docker** и **docker-compose** (рекомендуется для запуска) ●
> **Python** **3.12** (если запуск тестов планируется локально)

 **Cтарт**

**1.** **Клонируйте** **репозиторий**

git clone

\[https://github.com/your-username/wallet-app.git\](https://github.com/your-username/wallet-app.g
it)

cd wallet-app

**2.** **Запустите** **приложение** **через** **Docker**

docker-compose up --build -d

> ● **API** **доступен** **по** **адресу:** http://localhost:8000
>
> ● **Swagger-документация** **(OpenAPI):** http://localhost:8000/docs

📑 **Примеры** **использования** **(curl)**

**Создать** **кошелёк**

curl -X POST http://localhost:8000/api/v1/wallets

*В* *ответе* *придет* *wallet_id* *(UUID)* *и* *balance:* *0.00.*

**Пополнить** **баланс** **(DEPOSIT)**

*(Замените* *{wallet_id}* *на* *реальный* *UUID)*

curl -X POST http://localhost:8000/api/v1/wallets/{wallet_id}/operation
\\ -H "Content-Type: application/json" \\

> -d '{"operation_type": "DEPOSIT", "amount": 500.00}'

**Снять** **средства** **(WITHDRAW)**

curl -X POST http://localhost:8000/api/v1/wallets/{wallet_id}/operation
\\ -H "Content-Type: application/json" \\

> -d '{"operation_type": "WITHDRAW", "amount": 200.00}'

**Проверить** **баланс**

curl http://localhost:8000/api/v1/wallets/{wallet_id}

 **Запуск** **тестов**

**1.** **Подготовка** **тестовой** **БД**

Убедитесь, что контейнер с PostgreSQL запущен, и создайте базу для
тестов: docker exec -it wallet-app-db-1 psql -U wallet_user -d wallet_db
-c "CREATE DATABASE test_wallet_db;"

**2.** **Установка** **зависимостей** **и** **запуск**

\# Создание venv python -m venv venv

source venv/bin/activate \# Для Windows: venv\\Scripts\\activate

\# Установка и запуск

pip install -r requirements.txt pytest -v

**Примечание:** Таблицы в тестовой базе создаются автоматически при
старте тестов через SQLAlchemy.

**Что** **проверяют** **тесты:**

> ● Создание кошелька (201 Created).
>
> ● Валидация типов операций (DEPOSIT/WITHDRAW).
>
> ● Проверка на "недостаточно средств" (402 Payment Required).
>
> ● **Конкурентность:** выполнение 20 параллельных запросов на
> пополнение одного кошелька без потери данных.

 **API** **Endpoints**

||
||
||
||
||
||

**Формат** **JSON** **для** **операций:**

{

> "operation_type": "DEPOSIT", "amount": 1000.00

}

> ● amount: Положительное число (Decimal).
>
> ● balance: В ответах возвращается строкой для предотвращения потери
> точности на стороне фронтенда.

