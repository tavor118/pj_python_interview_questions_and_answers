## FastAPI

### Переваги та недоліки FastAPI

Переваги FastAPI

- Швидкість і ефективність: FastAPI заснований на асинхронному програмуванні, що дозволяє обробляти велику кількість запитів на секунду.
- Простота і зручність використання: FastAPI має простий та інтуїтивно зрозумілий інтерфейс, який дозволяє швидко і легко створювати веб-додатки.
- Автоматична документація: FastAPI автоматично генерує документацію для API на основі анотацій Python, що спрощує роботу з API.
- Підтримка OpenAPI і JSON Schema: FastAPI підтримує стандарти OpenAPI і JSON Schema, що дозволяє використовувати різні інструменти для роботи з API.
- FastAPI використовує особливості мови Python, такі як анотації типів, для підвищення продуктивності та зручності розробки. 

Недоліки FastAPI

- Необхідність вивчення асинхронного програмування: FastAPI використовує асинхронне програмування, що може бути складним для новачків у Python.
- Відсутність підтримки деяких функцій: FastAPI ще не підтримує деякі функції, які доступні в інших веб-фреймворках. Кількість бібліотек менша ніж в екосистемі Django.



### Що приймає `Depends()` у FastAPI? Якого типу об'єкт це з погляду Python?

*Summary*
> `Depends()` приймає будь-який `callable` (функцію, корутину, клас, об'єкт з `__call__`)
> і повертає примірник внутрішнього класу `fastapi.params.Depends`.
> Це маркер, який FastAPI шукає у сигнатурах ендпоінтів і за яким будує граф залежностей.

`Depends()` сам по собі **не викликає** передану функцію - він лише обгортає її 
в маркерний об'єкт.
Виклик відбувається пізніше, коли FastAPI розв'язує залежності для кожного запиту.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

@app.get("/items")
def list_items(db = Depends(get_db)):
    return db.query(Item).all()
```

**Що можна передати у `Depends()`:**

- Звичайну функцію або корутину (`async def`).
- Клас - FastAPI створить екземпляр на кожен запит.
- Об'єкт із реалізованим `__call__`.
- Інший об'єкт `Depends` (вкладені залежності).
- `Depends(None)` - placeholder, корисний у тестах, коли залежність підставляється через `app.dependency_overrides`.

**Що робить `Depends` під капотом:**

- Реєструє залежність у графі - FastAPI обходить його рекурсивно.
- Підтримує `async`/`sync`, генератори (для setup/teardown через `yield`), `BackgroundTasks`, `Request`, `Response`.
- Кешує результат у межах одного запиту (`use_cache=True` за замовчуванням) - корисно, якщо одна залежність підставляється у кілька інших.



### Різниця між `Depends()` та параметром `dependencies=[...]`

*Summary*
> `Depends()` як аргумент функції повертає результат і дає до нього доступ у
> тілі handler'а. `dependencies=[Depends(...)]` на рівні path-операції чи
> `APIRouter` запускає залежність як guard - результат не повертається, але
> виняток у залежності завершує запит.

**Призначення кожного варіанту**

`Depends()` як параметр функції - класичний DI: результат потрібен у тілі
(наприклад, екземпляр `Session`, об'єкт користувача, налаштування).

`dependencies=[Depends(check_admin), Depends(rate_limit)]` - guard: залежність
виконується перед handler'ом, її результат відкидається. Підходить для
перевірок, де важливий side effect (валідація токена, перевірка дозволу,
вичерпання rate-limit квоти), а не повернене значення.

**Реалізація**

```python
from fastapi import Depends, FastAPI, HTTPException, Header, APIRouter

app = FastAPI()


def get_current_user(token: str = Header(...)) -> User:
    user = decode_token(token)
    if user is None:
        raise HTTPException(401, "Invalid token")
    return user


def require_admin(user: User = Depends(get_current_user)) -> None:
    if not user.is_admin:
        raise HTTPException(403, "Admin only")


# Result-providing dependency: user is available in the body.
@app.get("/me")
def me(user: User = Depends(get_current_user)) -> UserSchema:
    return UserSchema.model_validate(user)


# Guard dependency: require_admin runs before the handler; its return value
# is discarded but an exception inside it aborts the request.
admin_router = APIRouter(
    prefix="/admin", dependencies=[Depends(require_admin)]
)


@admin_router.get("/stats")
def admin_stats() -> StatsSchema:
    return collect_stats()
```

**Спільна поведінка**

- Кешування (`use_cache=True` за замовчуванням) діє в обох випадках - якщо одна
  й та сама залежність використовується і як аргумент, і як guard у тому самому
  запиті, вона виконається один раз.
- Граф залежностей будується незалежно від того, як `Depends` оголошено.
  Вкладені `Depends` працюють однаково.

**Антипатерн**

Передавати у `dependencies=[Depends(...)]` залежність, чий результат потім
потрібен у тілі - це повторне виконання (FastAPI не може автоматично перенести
результат з guard-списку в аргументи). Якщо потрібен результат - оголошувати
як аргумент handler'а.

*Links*

- [FastAPI docs: Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/) - `dependencies=` на рівні `FastAPI()` і `APIRouter`
- [FastAPI docs: Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)



### `BackgroundTasks` у FastAPI

*Summary*
> `BackgroundTasks` - вбудований механізм запуску задач після надсилання
> response клієнту. Задачі виконуються в тому самому процесі: `async def`
> задача йде в event loop, синхронна `def` - у threadpool. Це **не фоновий
> worker і не окремий потік** для async-задач.

**Принцип роботи**

Імпортується клас `BackgroundTasks` з `fastapi`. Інстанс отримується як
параметр handler'а - FastAPI створює його на кожен запит. Задачі додаються
через `tasks.add_task(callable, *args, **kwargs)`. Після завершення тіла
handler'а і надсилання response Starlette проходить чергу і виконує задачі
послідовно.

Виконання залежить від того, чи задача оголошена як `async def` чи звичайна
`def`:

- `async def` - запускається у тому самому event loop, що й handler. Якщо
  задача робить блокуючий syscall - блокує event loop.
- `def` (синхронна) - запускається у threadpool через
  `starlette.concurrency.run_in_threadpool`, який всередині викликає
  `anyio.to_thread.run_sync`.

Окремий потік задіюється тільки для синхронних `def`-задач; `async def` задача
виконується у тому самому event loop, що й основний handler.

**Реалізація**

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


async def send_email(to: str, body: str) -> None:
    async with httpx.AsyncClient() as client:
        await client.post("https://api.mailer/send", json={"to": to, "body": body})


@app.post("/orders")
async def create_order(
    order: OrderIn,
    tasks: BackgroundTasks,
    repo: OrderRepo = Depends(get_repo),
) -> OrderOut:
    saved = await repo.insert(order)
    tasks.add_task(send_email, order.customer_email, f"Order {saved.id} created")
    return OrderOut.model_validate(saved)
```

Response повертається клієнту одразу після `return`; `send_email` стартує
вже після цього і не впливає на латентність endpoint'а.

**Обмеження**

- **Процес-локальні.** Задача живе в межах процесу, який обробив запит. Якщо
  процес перезавантажується (deploy, OOM-kill) - задача втрачається.
- **Без retry, без persistence.** Падіння задачі не призводить до повторного
  виконання. Logging винятків лежить на самій задачі або на global exception
  handler.
- **Без backpressure.** Велика кількість задач у пам'яті процесу не обмежена;
  при сплеску може вичерпати RAM або thread pool.
- **Послідовне виконання у межах одного запиту.** Задачі з одного
  `BackgroundTasks` йдуть одна за одною, не паралельно.

Для задач, які мають переживати рестарт процесу, мати retry/idempotency,
розподіляти навантаження і збирати метрики - канонічний шлях: винести в окремий
worker (Celery, RQ, ARQ, Dramatiq) і публікувати завдання у MQ. `BackgroundTasks`
підходить для дешевих fire-and-forget операцій (логування, надсилання
телеметрії, інвалідація кешу).

*Links*

- [FastAPI docs: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Starlette source: BackgroundTasks](https://github.com/encode/starlette/blob/master/starlette/background.py) - `await run_in_threadpool(self.func, *self.args, **self.kwargs)` для sync-функцій
- [Starlette source: run_in_threadpool](https://github.com/encode/starlette/blob/master/starlette/concurrency.py) - тонкий wrapper над `anyio.to_thread.run_sync`



### FastAPI під капотом

*Summary*
> FastAPI - тонкий шар поверх двох незалежних бібліотек: Starlette (ASGI
> toolkit з routing, middleware, websockets) і Pydantic (валідація та
> серіалізація). Сам FastAPI не має ні HTTP-сервера, ні event loop'а - запуск
> виконує зовнішній ASGI-сервер (Uvicorn / Hypercorn / Granian).

**Внесок Starlette**

- Routing (`@app.get`, `@app.post`, ...) - FastAPI обгортає decorators
  Starlette з додаванням dependency-graph і OpenAPI-метаданих.
- Middleware-stack, `Request`/`Response` об'єкти.
- WebSocket support, Server-Sent Events.
- Сесії, GZip, CORS, TrustedHost - як стандартні middleware.
- `BackgroundTasks`, `StreamingResponse`, `FileResponse`.
- `TestClient` (синхронний адаптер навколо `httpx`).

**Внесок Pydantic**

- `BaseModel` для опису request/response схем.
- Автоматична валідація вхідних даних: FastAPI парсить тіло запиту відповідно
  до сигнатури handler'а і повертає `422 Unprocessable Entity` із детальним
  списком помилок при невалідних даних.
- Серіалізація вихідних даних через `model_dump()`.
- Генерація OpenAPI-схеми з типів - саме звідси автодокументація `/docs`
  і `/redoc`.

**Внесок самого FastAPI**

- Граф залежностей (`Depends`, `dependencies=`), див. розділ
  [`Depends()`](#depends-fastapi-python).
- Сполучення Starlette-routing'у з Pydantic-валідацією і автогенерацією
  OpenAPI.
- `APIRouter` для модуляризації.
- Конвенції для security-схем (`OAuth2PasswordBearer`, `APIKeyHeader`).

**Поза межами FastAPI**

- HTTP-сервер. Запускати треба ASGI-сервером: `uvicorn main:app --workers 4`
  або через gunicorn з `UvicornWorker`. Деталі - у розділі
  [розгортання](#fastapi-uvicorn-workers).
- Event loop. FastAPI делегує управління event loop'ом ASGI-серверу і
  стандартному `asyncio` (або `uvloop`, якщо встановлений).
- ORM. SQLAlchemy / Tortoise / SQLModel - окремі бібліотеки; FastAPI не
  нав'язує жодну.

**Практичні наслідки шарування**

Розуміння шарів пояснює перформанс-характеристики і обмеження:

- Швидкість FastAPI на синтетичних тестах - це переважно швидкість Starlette
  і Uvicorn (C-розширення `httptools`, `uvloop`); FastAPI додає невелику
  накладну витрату на dependency-resolution і Pydantic-валідацію.
- Багато можливостей FastAPI - це Starlette-фічі (BackgroundTasks, WebSocket,
  middleware). Документація Starlette часто детальніша за документацію
  FastAPI для цих API.

*Links*

- [FastAPI docs: How FastAPI is built on top of Starlette and Pydantic](https://fastapi.tiangolo.com/features/)
- [Starlette docs](https://www.starlette.io/)
- [Pydantic docs](https://docs.pydantic.dev/)



### Middleware у FastAPI

*Summary*
> FastAPI підтримує два рівні middleware: pure ASGI middleware (рекомендовано
> для високого навантаження) і `BaseHTTPMiddleware` зі Starlette (зручніший
> API, але має overhead через обгортання у фонову task). Реєструються через
> `app.add_middleware(MiddlewareClass, **opts)`.

**Стандартні middleware**

Усе зі Starlette, готове до використання:

- `CORSMiddleware` - обробка cross-origin запитів, див.
  [CORS](#cors-fastapi).
- `GZipMiddleware` - стиснення відповідей з `Content-Length` понад мінімум.
- `TrustedHostMiddleware` - захист від host-header injection.
- `SessionMiddleware` - cookie-based session storage.
- `HTTPSRedirectMiddleware` - примусовий редирект з HTTP на HTTPS.

**Реалізація кастомного middleware**

Канонічний шлях для бізнес-логіки - `BaseHTTPMiddleware`. Перевизначається
метод `dispatch(request, call_next)`:

```python
import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Response-Time-Ms"] = f"{duration * 1000:.1f}"
        return response


app.add_middleware(RequestTimingMiddleware)
```

`call_next(request)` запускає решту middleware-stack'у і handler; повертає
`Response`. Все, що до `await call_next` - "перед запитом", після -
"після відповіді". Виняток у `call_next` піде через `except`.

**ASGI middleware (для перформансу)**

`BaseHTTPMiddleware` обгортає кожен запит у проміжну `anyio` task для
підтримки streaming body. На високих RPS цей overhead помітний (десятки
мікросекунд + додаткова алокація). Pure ASGI middleware пишеться як ASGI
application (приймає `scope`, `receive`, `send`):

```python
class RequestIdMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        request_id = generate_request_id()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                message["headers"].append(
                    (b"x-request-id", request_id.encode())
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)


app.add_middleware(RequestIdMiddleware)
```

Pure ASGI потребує знання ASGI-протоколу і не має зручних `Request`/`Response`
обгорток, але уникає накладних витрат `BaseHTTPMiddleware`.

**Порядок виконання**

Middleware виконуються в зворотному порядку реєстрації для request і у
прямому для response - "матрьошка" обгорток. Останній зареєстрований
`add_middleware` - найзовнішній (виконується першим на вході, останнім на
виході).

*Links*

- [Starlette docs: Middleware](https://www.starlette.io/middleware/) - повний перелік стандартних і API `BaseHTTPMiddleware`
- [Starlette source: BaseHTTPMiddleware](https://github.com/encode/starlette/blob/master/starlette/middleware/base.py) - реалізація через `anyio` task



### CORS у FastAPI

*Summary*
> CORS (Cross-Origin Resource Sharing) - механізм браузера для контролю
> запитів між різними origin'ами. `CORSMiddleware` зі Starlette додає
> відповідні response-заголовки і обробляє preflight (`OPTIONS`) запити;
> сам CORS - це браузерна політика, не серверний firewall.

**Реалізація**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com", "https://admin.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=600,
)
```

`allow_origins` - точний перелік дозволених origin'ів (схема + host + port).
`max_age` - як довго браузер кешує preflight-результат (зменшує OPTIONS
трафік).

**Обмеження wildcard з credentials**

Специфікація CORS забороняє комбінацію `Access-Control-Allow-Origin: *` з
`Access-Control-Allow-Credentials: true`. Якщо потрібні credentials (cookies,
Authorization-header) - `allow_origins` має бути явним списком, не `["*"]`.

`CORSMiddleware` валідує це у момент відповіді: при `allow_origins=["*"]`
і `allow_credentials=True` хедер `Access-Control-Allow-Credentials` не
надсилається, і браузер відкине куки.

**Preflight (OPTIONS)**

Для non-simple запитів (методи поза GET/HEAD/POST, custom-хедери,
JSON-Content-Type) браузер спершу надсилає `OPTIONS` запит з заголовками
`Access-Control-Request-Method`/`-Headers`. `CORSMiddleware` відповідає на
нього сам - handler не запускається.

**Межі CORS**

CORS не захищає сервер від несанкціонованого доступу. Запит, який не пройшов
CORS-перевірку, **доходить до сервера**: браузер блокує доступ до response на
стороні клієнта, але сервер вже виконав handler і змінив стан. Безпека
покладається на автентифікацію (токени, сесії) і авторизацію - CORS лише
контролює, який JavaScript може **читати** відповідь.

*Links*

- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) - повна специфікація політики
- [Starlette docs: CORSMiddleware](https://www.starlette.io/middleware/#corsmiddleware)



### Pydantic-схеми у FastAPI

*Summary*
> Pydantic-схема (підклас `BaseModel`) описує форму даних на вході або виході
> handler'а. FastAPI використовує її для двох речей: валідації request body
> (вхід) і `response_model` для серіалізації результату (вихід).

**Серіалізація і десеріалізація**

- **Серіалізація** - перетворення Python-об'єкта у транспортний формат
  (JSON, bytes). У FastAPI - `model.model_dump_json()` / `jsonable_encoder()`.
- **Десеріалізація** - зворотне: з JSON у Python-об'єкт. Це робить
  `model_validate_json(raw_bytes)` (Pydantic v2).
- **Валідація** - перевірка типів, обмежень (range, regex, custom validators)
  під час десеріалізації. У Pydantic відбувається одночасно з десеріалізацією.

**Request body**

```python
from pydantic import BaseModel, Field
from fastapi import FastAPI

app = FastAPI()


class OrderIn(BaseModel):
    customer_id: int
    items: list[str] = Field(min_length=1)
    note: str | None = None


@app.post("/orders")
async def create_order(order: OrderIn) -> dict:
    # `order` is already validated. Invalid input never reaches here -
    # FastAPI returns 422 with a per-field error list automatically.
    return {"received": order.model_dump()}
```

**`response_model` для виходу**

```python
class OrderOut(BaseModel):
    id: int
    customer_id: int
    items: list[str]
    # `internal_notes` intentionally absent from output schema


@app.post("/orders", response_model=OrderOut)
async def create_order(order: OrderIn) -> Order:
    saved = await repo.insert(order)
    return saved  # SQLAlchemy Order with extra fields
```

`response_model=OrderOut` робить дві важливі речі:

- **Фільтрація.** Поля, відсутні у `OrderOut`, не потраплять у відповідь -
  навіть якщо `saved` має `internal_notes`, `password_hash` чи інші чутливі
  атрибути. Захищає від витоку PII при випадковому додаванні полів у domain
  model.
- **Документація.** OpenAPI-схема `/docs` відображає саме `OrderOut`, а не
  domain-модель.

Поведінкові опції: `response_model_exclude_unset=True` (повертати лише поля,
які явно встановили на екземплярі моделі), `response_model_exclude={"field"}`,
`response_model_include={"field"}`.

**Антипатерн: domain model як response_model**

Спокуса використовувати SQLAlchemy-модель або domain entity напряму як
схему вводу-виводу спричиняє витоки полів і змішує транспортний контракт з
доменом. Канонічний шлях - окремі Pydantic-схеми (`OrderIn`, `OrderOut`,
`OrderUpdate`) і явне перетворення між ними і domain-об'єктами через
`model_validate` (див. наступний розділ).

*Links*

- [FastAPI docs: Response Model](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Pydantic docs: Models](https://docs.pydantic.dev/latest/concepts/models/)



### `model_validate` у Pydantic v2

*Summary*
> `model_validate(obj)` - канонічний метод Pydantic v2 для побудови моделі з
> довільного об'єкта (dict, ORM entity, dataclass). Замінив v1-методи
> `parse_obj` і `from_orm`. Опція `from_attributes=True` у `model_config`
> дозволяє читати дані з атрибутів об'єкта (а не лише з dict-ключів).

**v1 → v2 відповідність**

| Pydantic v1 | Pydantic v2 |
| --- | --- |
| `Model.parse_obj(d)` | `Model.model_validate(d)` |
| `Model.parse_raw(s)` | `Model.model_validate_json(s)` |
| `Model.from_orm(obj)` | `Model.model_validate(obj)` з `from_attributes=True` |
| `model.dict()` | `model.model_dump()` |
| `model.json()` | `model.model_dump_json()` |
| `Config.orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |

**Реалізація**

```python
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str


def get_user(session: Session, user_id: int) -> UserOut:
    user_row = session.get(User, user_id)  # SQLAlchemy ORM object
    return UserOut.model_validate(user_row)
```

Без `from_attributes=True` `model_validate` очікує `dict`-подібний об'єкт
(`__getitem__`); з ним - читає через `getattr`, що покриває ORM-моделі,
`@dataclass`, `attrs`-класи, NamedTuple.

**Переваги над `**user_row.__dict__`**

- Працює коректно з lazy-завантаженими relationship'ами SQLAlchemy: доступ
  через `getattr` спрацьовує тригером загрузки (на відміну від `__dict__`,
  який лише дає immediate state).
- Виконує валідацію типів - якщо домен-модель має `int`, а схема очікує
  `str`, отримаємо `ValidationError`, а не silent type mismatch.
- Підтримує `field validators` і `model validators` зі схеми.

*Links*

- [Pydantic v2 migration guide](https://docs.pydantic.dev/latest/migration/) - повний перелік перейменувань
- [Pydantic docs: `model_validate`](https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel.model_validate)



### Розгортання FastAPI: Uvicorn, workers

*Summary*
> FastAPI запускається ASGI-сервером. Канонічний вибір - Uvicorn (опційно
> з `uvloop` і `httptools`). Для багатопроцесового деплою використовують
> `uvicorn ... --workers N` або gunicorn з `UvicornWorker`. Кожен worker -
> окремий процес з власним event loop'ом, не потік.

**Запуск**

```bash
# Local dev
uvicorn main:app --reload

# Production (single host, multiple workers)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Production (gunicorn з UvicornWorker - кращий control над процесами)
gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:8000
```

`--reload` і `--workers` взаємно виключні: reload-режим тримає лише один
процес з watchdog'ом.

**Worker = окремий процес**

Кожен worker - окремий ОС-процес з власним:

- Event loop'ом (`asyncio` або `uvloop`).
- Connection pool'ом до БД, кешу, MQ.
- Кешем у пам'яті процесу.
- Лічильниками метрик (якщо не централізовані).

Процеси не діляться пам'яттю - in-memory кеш у одному worker'і не видно
іншим. Це наслідок Python GIL: щоб використати кілька CPU-ядер, потрібні
окремі процеси, не потоки.

**Кількість workers**

Стандартна евристика для IO-bound (типовий FastAPI-API): `2 * cpu_count + 1`
(відображає gunicorn-конвенцію). Для CPU-bound навантажень - близько до
`cpu_count`. Реальна цифра підбирається бенчмарками з контролем p99 latency
і CPU utilization.

**Альтернативи Uvicorn**

- [Hypercorn](https://hypercorn.readthedocs.io/) - підтримує HTTP/2 і
  HTTP/3 нативно, на відміну від Uvicorn.
- [Granian](https://github.com/emmett-framework/granian) - Rust-based ASGI
  server, конкурує з Uvicorn по швидкості.

*Links*

- [Uvicorn docs: Settings](https://www.uvicorn.org/settings/) - `--workers`, `--loop`, `--http`
- [FastAPI docs: Deployment](https://fastapi.tiangolo.com/deployment/)



### Тестування FastAPI: `TestClient` і `dependency_overrides`

*Summary*
> `TestClient` (з `fastapi.testclient`) - синхронний клієнт, який викликає
> ASGI-застосунок напряму без HTTP-сокета. Реалізований через `httpx`.
> `app.dependency_overrides` дозволяє підміняти будь-яку `Depends`-залежність
> у тестах без зміни production-коду.

**`TestClient`**

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

`TestClient` запускає lifespan startup при вході в контекст-менеджер:
`with TestClient(app) as client: ...`. Без `with` lifespan не виконається, що
часто плутає при ініціалізації global state. Канонічний шлях оголошення
startup/shutdown - `lifespan` async context manager, переданий у
`FastAPI(lifespan=...)`; FastAPI 0.93.0 (2023-03-07) додав підтримку
`lifespan` і позначив `@app.on_event("startup"/"shutdown")` як попередній
підхід, що `lifespan` витісняє; у документації вони тепер у розділі
"Alternative Events (deprecated)".

З FastAPI 0.87.0 (2022-11-13) `TestClient` побудований на `httpx` після
апгрейду Starlette до 0.21.0 (раніше - на `requests`). API сумісне у
більшості випадків, але є відмінності у тімаутах і обробці redirect'ів.

**Async-aware тестування**

Для тестів, які мають викликати `async`-функції напряму або перевіряти
async-середовище більш контрольовано, використовують `httpx.AsyncClient`
з `ASGITransport`:

```python
import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_create_order() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/orders", json={"customer_id": 1, "items": ["a"]})
    assert response.status_code == 201
```

Це обов'язковий шлях, якщо тест викликає async-fixture'и, які не
підтримуються синхронним `TestClient`.

**`app.dependency_overrides`**

Канонічний механізм підміни залежностей у тестах:

```python
from fastapi.testclient import TestClient


def fake_db():
    return InMemoryDb()


def test_list_items() -> None:
    app.dependency_overrides[get_db] = fake_db
    try:
        client = TestClient(app)
        response = client.get("/items")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()
```

Скидання після тесту обов'язкове - інакше override залишається активним для
наступного тесту, який ділить той самий `app`. У pytest зручно через
fixture з `yield`:

```python
@pytest.fixture
def override_db():
    app.dependency_overrides[get_db] = fake_db
    yield
    app.dependency_overrides.clear()
```

Підмінити можна будь-яку залежність на будь-якому рівні графа: верхньорівневу
(`get_db`), вкладену (`get_current_user`, що сам залежить від `get_db`),
guard з `dependencies=[Depends(...)]`. Це робить `dependency_overrides`
основним інструментом для unit-тестування handler'ів без mock-бібліотек.

*Links*

- [FastAPI docs: Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI docs: Async Tests](https://fastapi.tiangolo.com/advanced/async-tests/) - `httpx.AsyncClient` з `ASGITransport`
- [FastAPI docs: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
