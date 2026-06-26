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

**Клас-залежність для DRY-параметрів**

Поширений приклад - спільні query-параметри (пагінація, фільтри, сортування),
які повторюються у десятках handler'ів. Замість дублювання сигнатури в кожен
endpoint, оголошують клас, який FastAPI створює як залежність:

```python
from fastapi import Depends, FastAPI, Query

app = FastAPI()


class Pagination:
    def __init__(
        self,
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100),
    ) -> None:
        self.page = page
        self.size = size
        self.offset = (page - 1) * size


@app.get("/items")
def list_items(pg: Pagination = Depends()) -> list[ItemOut]:
    return repo.list(limit=pg.size, offset=pg.offset)


@app.get("/orders")
def list_orders(pg: Pagination = Depends()) -> list[OrderOut]:
    return repo.list_orders(limit=pg.size, offset=pg.offset)
```

OpenAPI-схема для `/items` і `/orders` отримає `page` і `size` query-параметри
з валідацією - без копіювання тіла Query-декларацій у кожен endpoint.
`Depends()` без аргументу - синтаксичне скорочення для `Depends(Pagination)`,
коли клас уже вказано в анотації типу.



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



### Sync vs async ендпоінти у FastAPI [💡19/100]

*Summary*
> `async def` handler виконується у тому самому event loop'і ASGI-сервера. `def`
> (синхронний) handler FastAPI запускає у threadpool через
> `anyio.to_thread.run_sync`, щоб не блокувати loop. Це працює, але має іншу
> вартість: GIL-серіалізує Python-виконання потоків, OS-перемикання трошки
> дорожче за await-перемикання між корутинами.

**Як FastAPI вирішує, де запускати handler**

FastAPI дивиться на сигнатуру:

- `async def` → виконується інлайн у event loop'і. Будь-яка блокуюча операція
  (синхронний HTTP, синхронна БД-бібліотека, важкий CPU-цикл) блокує **весь**
  worker - інші запити чекають.
- `def` → Starlette автоматично переносить виклик у threadpool
  (`anyio.to_thread.run_sync`, дефолтний ліміт - 40 потоків). Loop залишається
  вільним для інших запитів, але кожен синхронний handler займає слот у пулі.

**Вичерпання пулу потоків.** Слотів у пулі скінченна кількість (40 за
замовчуванням). Якщо кожен `def`-handler блокується надовго (повільний
зовнішній виклик, важкий SQL), усі слоти швидко зайняті, і нові синхронні
запити стають у чергу замість виконання. З погляду клієнта сервіс "висить":
запит не відхиляється явно, а чекає вільний слот - і часто обривається за
таймаутом проксі (типовий `proxy_read_timeout` у nginx - 60 с) ще до того, як
дістанеться worker'а. Це класичний каскад "thread-pool exhaustion": один
повільний даунстрім зупиняє всю синхронну гілку. Запобігання - тримати
синхронні handler'и короткими, виносити повільні блокуючі виклики в чергу задач
(Celery/Dramatiq) або переходити на `async def` з async-native бібліотеками,
де одне очікування I/O не займає слот пулу.

```python
@app.get("/sync")
def sync_handler():
    # Runs in threadpool — safe to call blocking psycopg2, requests, etc.
    return db.execute("SELECT 1").fetchone()


@app.get("/async")
async def async_handler():
    # Runs in event loop — MUST use async-native libs (asyncpg, httpx).
    return await async_db.fetch_one("SELECT 1")
```

**Коли який варіант**

- Працюєте з async-native бібліотекою (`asyncpg`, `httpx.AsyncClient`,
  `aioredis`) - `async def`. Loop не блокується, конкурентність дешева.
- Працюєте з суто синхронною бібліотекою без async-варіанту (`requests`,
  `psycopg2`, legacy SDK) - `def`. Threadpool ізолює блокування від loop'у.
- Найгірший варіант - `async def` з блокуючою синхронною операцією усередині:
  loop стоїть, інші запити чекають. Для разових випадків - `await
  asyncio.to_thread(blocking_call)`; для постійних - перейти на async-бібліотеку.

**Чому event loop дешевший за threadpool**

Перемикання між корутинами - це Python-`yield` усередині одного потоку: немає
syscall'у, немає роботи з kernel scheduler. Перемикання між потоками - це
OS-syscall: scheduler призупиняє один потік, відновлює інший, плюс синхронізація
через GIL. Деталі - у [`async.md`](../python/async.md) та
[`gil_threads_processes.md`](../python/gil_threads_processes.md).

Це не означає, що "async швидший за threads" універсально - обидва моделі
розв'язують I/O-bound навантаження. Поширене заблудження - що threads існують
тільки для CPU-задач; насправді більшість багатопотокових веб-фреймворків
(Django, Flask, sync FastAPI) використовують threads саме для I/O.

*Links*

- [FastAPI docs: Concurrency and async / await](https://fastapi.tiangolo.com/async/) - офіційне пояснення sync vs async вибору
- [Starlette docs: Threadpool](https://www.starlette.io/threadpool/) - як `def` handler потрапляє у threadpool



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



### Розгортання FastAPI: Uvicorn, workers [💡10/100]

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

# Production (gunicorn with UvicornWorker - better process control)
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

**Ролі Uvicorn vs Gunicorn**

Uvicorn - сам по собі ASGI-worker: приймає HTTP-запити, передає у FastAPI,
повертає response. Якщо запустити просто `uvicorn ... --workers 4`, він
підніме чотири worker-процеси, але **не моніторить** їх. Якщо worker упав
через OOM, виняток, segfault - він не перезапуститься, ємність деградує.

Gunicorn додає шар process-supervisor над worker'ами:

- Слідкує за здоров'ям кожного worker'а (heartbeat-сигнал).
- Перезапускає worker, який упав або не відповідає.
- Підтримує graceful reload (`SIGHUP` для перечитування коду без втрати
  активних з'єднань).
- Дає тонкіший контроль через `--max-requests`, `--max-requests-jitter`
  (періодичний перезапуск worker'ів для боротьби з витоками пам'яті).

Канонічна production-конфігурація поза Kubernetes:
`gunicorn main:app -k uvicorn.workers.UvicornWorker -w 4` - Gunicorn як
supervisor, Uvicorn як worker-runtime.

**Розгортання у Kubernetes - Gunicorn зайвий**

У Kubernetes роль supervisor'а виконує сам кластер: kubelet перезапускає
крашнутий контейнер, ReplicaSet тримає потрібну кількість под'ів, HPA
масштабує за CPU/RAM. Додатковий Gunicorn-шар дублює функціональність і
ускладнює лог-агрегацію (двошарова ієрархія процесів: gunicorn-master →
uvicorn-worker → handler).

Канонічний шлях у K8s: один Uvicorn-процес на под (`uvicorn main:app
--host 0.0.0.0 --port 8000`), масштабування - збільшенням `replicas`
у Deployment. Це відповідає принципу "один процес на контейнер" з
[12-factor app](https://12factor.net/processes).

**Альтернативи Uvicorn**

- [Hypercorn](https://hypercorn.readthedocs.io/) - підтримує HTTP/2 і
  HTTP/3 нативно, на відміну від Uvicorn.
- [Granian](https://github.com/emmett-framework/granian) - Rust-based ASGI
  server, конкурує з Uvicorn по швидкості.

*Links*

- [Uvicorn docs: Settings](https://www.uvicorn.org/settings/) - `--workers`, `--loop`, `--http`
- [FastAPI docs: Deployment](https://fastapi.tiangolo.com/deployment/)



### CPU-bound задачі у FastAPI: коли виносити у Celery

*Summary*
> FastAPI оптимізований під I/O-bound навантаження. Важка CPU-задача (генерація
> PDF/відео, ML-інференс, криптографія) на async-ендпоінті блокує event loop;
> на sync-ендпоінті - займає слот у threadpool і конкурує за GIL з іншими
> потоками. Канонічний шлях для тривалого CPU - винести у воркер на окремому
> процесі (Celery, Dramatiq, RQ), часто на окремому сервісі.

**Чому не запускати CPU-bound інлайн**

- **`async def` handler з CPU-циклом** блокує event loop. Інші запити в тому
  ж worker'і чекають - p99 latency злітає, RPS обвалюється до одиниць.
- **`def` handler з CPU-циклом** виконується у threadpool, але GIL серіалізує
  Python-байткод: усі потоки, що виконують Python, чекають один одного. Кілька
  паралельних важких CPU-handler'ів дають близько до однопотокової пропускної
  здатності. Виняток - C-розширення, які явно відпускають GIL (NumPy, Pandas,
  Pillow, `hashlib`); деталі - у
  [`gil_threads_processes.md`](../python/gil_threads_processes.md).
- **`asyncio.to_thread`** для CPU - той самий ефект: під GIL contention
  деградує. Корисно лише для разового виклику синхронної функції без
  паралельного навантаження.

**Канонічний шлях: окремий процес-воркер**

Винести задачу у задача-чергу (Celery, Dramatiq, RQ, ARQ):

```python
from celery import Celery

celery_app = Celery("worker", broker="redis://redis:6379/0")


@celery_app.task
def generate_report(user_id: int) -> str:
    # Heavy CPU work — runs in a Celery worker process, not in FastAPI.
    return build_pdf(user_id)


@app.post("/reports")
async def create_report(user_id: int) -> dict:
    task = generate_report.delay(user_id)
    return {"task_id": task.id, "status": "queued"}
```

Чому це працює:

- Worker - **окремий процес** (часто навіть окремий контейнер чи сервер). GIL
  worker'а ізольований від FastAPI-процесу.
- Worker'ів можна підняти `--concurrency N`, де `N ≈ кількість CPU-ядер`.
  Реальний паралелізм - стільки задач одночасно, скільки ядер.
- Worker масштабується **горизонтально незалежно від FastAPI**: важкий ML -
  потужна GPU-нода тільки для worker'а; FastAPI лишається на дешевих
  інстансах.
- Брокер (Redis, RabbitMQ) - точка зустрічі: FastAPI публікує задачу, worker
  забирає. Жодних спільних процесів чи мережевих викликів між FastAPI і
  worker'ом, окрім запису у брокер.

**Чому не `BackgroundTasks`**

`BackgroundTasks` (див. розділ вище) виконує задачу **у тому самому процесі**,
що й handler. Для CPU-bound: блокує event loop (`async def` task) або займає
слот у threadpool під GIL (`def` task) - як і інлайн-виконання. Plus немає
retry, persistence, моніторингу. Підходить тільки для дешевих fire-and-forget
операцій.

**Коли інлайн-виконання прийнятне**

- CPU-задача коротка (мс - десятки мс), нечастa, p99-вимоги м'які.
- Бібліотека з C-розширенням, що відпускає GIL (NumPy/Pandas агрегації) -
  тоді sync-handler + threadpool дає реальний паралелізм.
- Прототип / MVP, де простота важливіша за пропускну здатність.

*Links*

- [Celery docs: Introduction](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
- [FastAPI docs: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) - офіційно рекомендує Celery для тривалих/критичних задач



### Кастомні обробники винятків (`exception_handler`)

*Summary*
> `@app.exception_handler(SomeException)` реєструє функцію, яка перетворює
> виняток у `Response` замість стандартної 500-ї. Канонічні застосування:
> приховати внутрішні поля Pydantic-помилки, конвертувати domain-винятки
> у бізнес-коди, локалізувати повідомлення про помилки.

**Реалізація**

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()


class OrderNotFound(Exception):
    def __init__(self, order_id: int) -> None:
        self.order_id = order_id


@app.exception_handler(OrderNotFound)
async def handle_order_not_found(request: Request, exc: OrderNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": "order_not_found", "order_id": exc.order_id},
    )


@app.exception_handler(RequestValidationError)
async def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # Hide Pydantic internals (field paths, type names, raw input).
    return JSONResponse(
        status_code=400,
        content={"error": "invalid_request", "message": "Check the request fields"},
    )
```

**Чому приховувати дефолтну Pydantic-помилку**

Дефолтна відповідь FastAPI на `RequestValidationError`:

```json
{"detail": [{"loc": ["body", "user", "email"], "msg": "field required", "type": "value_error.missing"}]}
```

Деталі (`loc`, внутрішні `type`-токени, інколи raw-input) розкривають структуру
domain-моделі: назви полів, ієрархію об'єктів, інколи приклади валідних значень.
Для внутрішнього API це нормально; для public API часто хочуть лаконічну
відповідь без витоку схеми. Кастомний handler віддає мінімум - status + код
помилки + локалізоване повідомлення.

**Конвертація domain-винятків**

Замість того, щоб у кожному handler'і робити
`try: ... except OrderNotFound: raise HTTPException(404, ...)`, реєструють
глобальний обробник один раз. Handler-код залишається чистим - просто
`raise OrderNotFound(order_id)`.

**Інший спосіб - middleware**

Глобальний `try/except` у middleware (через `BaseHTTPMiddleware.dispatch`) дає
схожий ефект, але працює на нижчому рівні: не має доступу до Pydantic-винятків
до того, як їх обробить FastAPI. `exception_handler` - канонічний шлях для
винятків, які виникають усередині handler'а; middleware - для тих, які мають
охопити саму обробку запиту (request-id інжекція, трейсинг помилок).

*Links*

- [FastAPI docs: Custom exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#install-custom-exception-handlers)
- [FastAPI docs: Override the default exception handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers)



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
з `ASGITransport`. Декоратор `@pytest.mark.asyncio` походить з пакета
[`pytest-asyncio`](https://pytest-asyncio.readthedocs.io/) - канонічний плагін
для async-тестів у pytest; альтернативно
[`anyio-pytest`](https://anyio.readthedocs.io/en/stable/testing.html) дозволяє
запускати ті самі тести на обох async-бекендах (asyncio + trio).

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
