## SQLAlchemy

### SQLAlchemy: Core та ORM [💡18/100]

*Summary*
> SQLAlchemy - бібліотека Python для роботи з реляційними базами даних. Має
> два рівні абстракції: Core (низькорівневий construction layer для SQL)
> і ORM (мапінг таблиць у класи з identity-map і unit-of-work).

**SQLAlchemy Core**

Низькорівневий рівень, що дозволяє конструювати SQL-вирази через Python-об'єкти
без обов'язкового мапінгу у класи.

- Об'єктне представлення таблиць, колонок і типів через `Table`, `Column`,
  `MetaData`.
- Декларативний конструктор запитів (`select`, `insert`, `update`, `delete`).
- Виконання через `Connection` з явним керуванням транзакціями.

```python
from sqlalchemy import (
    Column, Integer, MetaData, String, Table, create_engine, select,
)

engine = create_engine("sqlite:///example.db")
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("age", Integer),
)

metadata.create_all(engine)

with engine.connect() as connection:
    connection.execute(
        users.insert(),
        [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}],
    )

with engine.connect() as connection:
    result = connection.execute(select(users.c.name, users.c.age))
    for row in result:
        print(row)
```

**SQLAlchemy ORM**

Високорівневий шар над Core: мапінг таблиць у класи, identity map, unit of
work через `Session` (див. [`Session` vs
`sessionmaker`](#session-vs-sessionmaker)).

- Розробник оперує об'єктами-моделями замість рядків таблиць.
- Декларативний стиль через успадкування від `DeclarativeBase` (2.0+).
- `Session` керує життєвим циклом об'єктів, транзакціями і flush'ом змін.

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


engine = create_engine("sqlite:///example.db")
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

with SessionLocal() as session:
    session.add_all([User(name="Alice", age=25), User(name="Bob", age=30)])
    session.commit()

with SessionLocal() as session:
    for user in session.scalars(select(User)):
        print(user.name, user.age)
```

**Сценарії застосування**

- **Core** - складна аналітика, batch-операції, ETL, кейси з нестандартними
  SQL-конструкціями де ORM-абстракція заважає; коли об'єктний мапінг не
  потрібен.
- **ORM** - типова доменна логіка, де об'єкт-домен природньо мапиться у
  таблиці; коли потрібен identity map і unit of work.

Обидва шари сумісні в одному застосунку: ORM під капотом виконує запити через
Core.

**Використання ORM проти Core.** Якщо застосовувати моделі алхімії, але викликати
`insert`/`update`, ORM фактично не використовується. Так роблять для оптимізації
окремих навантажених ділянок, але не як основний спосіб роботи. Ознака ORM-підходу:
завантаження сутностей цілком (`session.get`, `select(Model)`), додавання через
`session.add`, зміни через мутацію об'єкта плюс `commit`, видалення через
`session.delete` - усе спирається на Identity Map і Unit of Work сесії.

**Три підходи до доменних сутностей.** Окрема помилка - тримати доменні сутності й
ORM-моделі паралельно: доводиться писати складні маппери, що часто не враховують
Identity Map і Unit of Work, ламаючи логіку збереження. Натомість обирають один із
трьох підходів:

- **Не використовувати ORM.** Писати сутності як зручно й зберігати через Core.
  Втрачається вбудований Unit of Work, але немає й конфлікту з ним.
- **ORM-моделі як бізнес-сутності.** Сутності виглядають трохи "брудніше" (несуть
  метадані ORM), але ці метадані в бізнес-логіці не використовуються.
- **Датакласи з imperative mapping.** Доменна сутність лишається звичайним класом, а
  `Table` описують окремо (див. [Imperative mapping](#imperative-mapping-відокремити-доменну-сутність-від-orm)).
  Повністю кастомні маппери для окремих моделей недоступні, зате доступні всі
  можливості алхімії.

Складні `select`-запити (пошук, зведена інформація) ховають усередині патерну
[Repository](../architecture/ddd.md), спираючись на сесію як Unit of Work. Для запитів
читання, що віддають клієнту певний зріз даних, реалізують простий DAO на Core або
альтернативні моделі з imperative mapping на ті самі таблиці.



### Active Record проти Data Mapper

*Summary*
> Два патерни доступу до даних (за Фаулером). **Active Record**: об'єкт-модель сам знає, як
> себе зберегти - дані й логіка persistence в одному класі (`user.save()`). **Data Mapper**:
> окремий шар (mapper / session) переносить дані між об'єктом і БД, а доменний об'єкт нічого
> не знає про сховище. **Django ORM - це Active Record, SQLAlchemy - Data Mapper.**

- **Active Record (Django).** Модель успадковує всю persistence-логіку; `obj.save()`,
  `obj.delete()`, `Model.objects.filter(...)` живуть на самій моделі. Швидко й зручно для
  CRUD, але домен злитий з ORM - важче тримати чисту доменну модель і тестувати без БД.
- **Data Mapper (SQLAlchemy).** Persistence винесено у `Session` (unit of work):
  `session.add(obj)`, `session.commit()`. Сам клас може лишатися звичайним об'єктом
  (особливо з imperative mapping), тож домен не залежить від інфраструктури.
  Ціна - більше церемоній, ніж в Active Record.

Саме тому в Django транзакцію відкривають зовні (`transaction.atomic`), а в SQLAlchemy за
коміт відповідає `Session` (`session.commit()`): за збереження відповідають різні сутності,
бо це різні патерни.



### Imperative mapping: відокремити доменну сутність від ORM

*Summary*
> Декларативний стиль (`class User(Base)`) прив'язує доменний клас до SQLAlchemy -
> він успадковує `Base`, тобто домен залежить від інфраструктури. **Imperative
> mapping** (`registry.map_imperatively(Class, table)`) лишає доменну сутність
> **звичайним класом без жодного імпорту SQLAlchemy**, а таблицю описує окремо. Це
> класичний прийом чистої архітектури / DDD - домен не знає про ORM.

При декларативному мапінгу клас = таблиця і прив'язаний до фреймворку (успадковує
`Base`, поля - `Mapped[...]`). Якщо ж домен має бути незалежним від сховища, сутність
визначають як plain-клас, а зв'язок із таблицею задають імперативно:

```python
from dataclasses import dataclass
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import registry

# 1. Domain entity - a plain class, zero SQLAlchemy imports in its definition
@dataclass
class User:
    id: int | None
    name: str

# 2. Table described separately (infrastructure layer)
metadata = MetaData()
user_table = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)

# 3. Imperative mapping wires them from the outside
mapper_registry = registry()
mapper_registry.map_imperatively(User, user_table)
```

Тепер `session.scalars(select(User))` повертає екземпляри **доменного** `User`, а не
окремого ORM-класу, тоді як уся прив'язка до SQLAlchemy зосереджена в інфраструктурі.
Альтернатива - тримати окремі ORM-моделі й конвертувати їх у доменні сутності/DTO на
межі шару (розділ "ORM-об'єкти - не DTO" нижче).



### Lazy vs Eager loading: стратегії завантаження relationship

*Summary*
> `relationship()` у SQLAlchemy за замовчуванням завантажується **ліниво** -
> окремим SQL-запитом при першому доступі до атрибута. Це генерує проблему
> N+1: ітерація по 100 батьківських записах з доступом до relationship
> породжує 101 запит. Eager-стратегії (`joined`, `selectin`, `subquery`)
> завантажують relationship разом з основним запитом.

**Стратегії**

| Стратегія | Поведінка | Сценарії |
| --- | --- | --- |
| `lazy='select'` (default) | Окремий `SELECT` при першому доступі | Дані часто не потрібні; many-to-one з рідкісним доступом |
| `lazy='joined'` | `LEFT OUTER JOIN` з основним запитом | one-to-one, many-to-one (один запит) |
| `lazy='selectin'` | Один додатковий `SELECT ... WHERE parent_id IN (?, ?, ...)` після основного | Рекомендовано для one-to-many, many-to-many |
| `lazy='subquery'` | Підзапит у `FROM` основного запиту | Історично; `selectin` зазвичай кращий |
| `lazy='raise'` | Доступ кидає `InvalidRequestError` | Захист від випадкового lazy-завантаження в async-коді |
| `lazy='noload'` | Завжди порожньо | Колекції, які навмисно не вантажати |

`selectin` зазвичай швидший за `joined` для one-to-many: `joined` дублює
батьківські рядки (по одному на кожну дитину), а `selectin` робить два
окремих запити без декартового добутку.

Поза стандартними стратегіями ORM існує **array/json-агрегація**: замість збільшення
кількості рядків зв'язані дані збирають агрегувальними функціями (`array_agg`,
`json_agg`) у масив чи json-поле. Вимагає підтримки таких типів від СУБД і теж дублює
дані при many-to-one. Інколи цим формують у БД готову до відправки структуру - це
анти-патерн, бо змішує доступ до даних із формуванням відповіді.

**Per-query override**

Стратегію в `relationship()` варто залишати дефолтною (`lazy='select'`) і
обирати завантаження на рівні конкретного запиту через `.options()`:

```python
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, raiseload


# Eager-load author for each post in one query (LEFT JOIN)
stmt = select(Post).options(joinedload(Post.author))

# Eager-load comments via separate SELECT IN (...)
stmt = select(Post).options(selectinload(Post.comments))

# Combine: author via join, comments via selectin, ban lazy on tags
stmt = select(Post).options(
    joinedload(Post.author),
    selectinload(Post.comments),
    raiseload(Post.tags),
)
```

Це робить контракт явним: запит, який очікує relationship, оголошує це
сам.

**Обмеження lazy loading в async-режимі**

В `AsyncSession` lazy-завантаження за замовчуванням падає з
`MissingGreenlet`/`StatementError`. Причина: атрибут-доступ синхронний
(`post.comments`), а під ним має статися SQL-запит, який у async-режимі
потребує `await`. Тому в async-коді:

- Усі relationship'и, які реально читаються, завантажуються через
  `selectinload`/`joinedload` у `.options()`.
- На решту ставлять `lazy='raise'` на рівні `relationship()` - щоб помилка
  була явною на етапі розробки, а не silent N+1 під час дебагу production.

**Зв'язок з Django ORM**

Концептуально відповідає `select_related` (≈ `joinedload`) і
`prefetch_related` (≈ `selectinload`) у Django (див.
[`django.md`](django.md) розділ "Різниця між `select_related` та
`prefetch_related`").

*Links*

- [SQLAlchemy docs: Relationship Loading Techniques](https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html)
- [SQLAlchemy docs: Loading Relationships in Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#preventing-implicit-io-when-using-asyncsession)



### `Session` vs `sessionmaker`

*Summary*
> `Session` - unit of work, що тримає identity map, трекає зміни і flush'ить
> їх на commit. Один `Session` живе одну логічну транзакцію (типово - один
> HTTP-запит). `sessionmaker(bind=engine, ...)` - factory, що повертає
> `Session`-екземпляри з пресетованими параметрами, щоб не повторювати їх у
> кожному `Session(engine, ...)` виклику.

**Функції `Session`**

- **Identity map.** У межах сесії одна і та сама row з БД відповідає одному
  Python-об'єкту. Повторний `session.get(User, 1)` повертає той самий
  екземпляр, не новий.
- **Unit of work.** Зміни об'єктів акумулюються у session і flush'аться
  одним пакетом (при commit, явному `flush()`, або при наступному `SELECT`).
- **Transaction boundary.** `session.commit()` фіксує транзакцію,
  `session.rollback()` скасовує всі pending-зміни.
- **Expire on commit.** За замовчуванням після commit усі атрибути об'єктів
  expired - наступний доступ робить SQL-запит для перезавантаження. Зручно
  у sync-коді, але **проблема в async** (потрібен `expire_on_commit=False`).

**`sessionmaker` як factory**

```python
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("postgresql://user:pass@localhost/db")

# Pre-set parameters once
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

`SessionLocal()` повертає новий `Session` з прив'язаним engine та опціями.
Альтернатива - щоразу писати `Session(engine, autoflush=False,
expire_on_commit=False)`, що швидко стає шумом.

**Канонічний патерн у FastAPI**

Один `Session` на запит через `Depends(get_db)` з `yield` для cleanup
(див. розділ [Depends() у FastAPI](fast_api.md#depends-fastapi-python)). Це
гарантує, що сесія закриється навіть при винятку у handler'і.

**Async-варіант**

```python
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # critical for async
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as db:
        yield db
```

`expire_on_commit=False` критично для async: при `expire_on_commit=True`
(default) після commit об'єкти позначаються expired, і будь-який наступний
доступ до атрибута тригерить sync lazy-refresh, який у async-режимі видасть
`MissingGreenlet`. Стандартна рекомендація для async-додатків - вимикати
expire on commit.

**Unit of Work як патерн**

`Session` реалізує патерн **Unit of Work**: відстежує зміни об'єктів і потім
скоординовано зберігає їх у БД. Спершу реєструють зміни (`register_new`,
`register_dirty`, `register_deleted`), а в певний момент зберігають усе разом
(`commit`). Це не просто керування транзакцією: UoW накопичує зміни перед відправкою,
може об'єднувати вставки в один запит і контролювати цілісність (оптимістичні
блокування). У БД він звертається через об'єкти [Data Mapper](../architecture/ddd.md)
(кожен працює з моделями одного класу) і тісно пов'язаний з **Identity Map** - реєстром
завантажених екземплярів за їхніми ідентифікаторами. У SQLAlchemy зміни потрапляють у БД
у момент `session.flush()`/`session.commit()`.

*Links*

- [SQLAlchemy docs: Session Basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [SQLAlchemy docs: `sessionmaker`](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.sessionmaker)
- [SQLAlchemy docs: Asyncio](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Martin Fowler: PoEAA - Unit of Work](https://martinfowler.com/eaaCatalog/unitOfWork.html)
- [Patterns Implemented by SQLAlchemy (Mike Bayer)](https://techspot.zzzeek.org/2012/02/07/patterns-implemented-by-sqlalchemy/)



### ORM-об'єкти - не DTO

*Summary*
> ORM-екземпляр SQLAlchemy виглядає як `dataclass` (ті самі поля), але це не
> пасивний DTO: він **мутабельний** і прив'язаний до `Session` (identity map +
> unit of work). Зміна атрибута persistent-об'єкта позначає його "брудним", і на
> `commit` сесія сама вистрілює `UPDATE` - навіть якщо зміна була випадковою. Тому
> ORM-об'єкти не передають крізь шари: на межі їх конвертують у простий DTO.

**Ризик випадкового `UPDATE`.** Запит через ORM повертає об'єкт із заповненими
полями, тож спокусливо передати його далі по ланцюжку викликів як звичайні дані. Але
`Session` трекає всі завантажені об'єкти: змінив поле persistent-об'єкта (хай навіть
помилково, гадаючи що це DTO) - на наступному `commit`/`flush` у БД полетить
`UPDATE`. Жодного явного `save()` для цього не треба.

```python
user = session.get(User, 42)   # persistent, tracked by the session
dto = user                     # looks like plain data, but it is the live ORM object
dto.name = "typo"              # meant to touch a DTO - actually marks the row dirty
session.commit()               # UPDATE "Users" SET name='typo' WHERE id=42  (!)
```

Інші відмінності від DTO:

- **Detached після закриття сесії.** Коли сесія закрита, доступ до незавантажених атрибутів чи relationship кидає `DetachedInstanceError`.
- **Lazy-relationship.** Звернення до не-eager relationship мовчки робить запит у БД - класичне джерело проблеми N+1 (див. розділ "Lazy vs Eager loading" вище).

**Рішення: конвертувати на межі шару.** Data-шар повертає ORM-об'єкт лише всередині
себе, а назовні (в use-case, презентацію) віддає **plain DTO** (`dataclass` чи
Pydantic-модель), зібраний з потрібних полів. Тоді зміни DTO нікого не торкаються, а
поведінка сесії не "тече" у бізнес-логіку. Це та сама причина, чому Repository не
віддає ORM-моделі - див. [`architecture/ddd.md`](../architecture/ddd.md) розділ
"Repository vs DAO".



### Connection pool: `pool_size`, `max_overflow`, `pool_recycle`

*Summary*
> `Engine` за замовчуванням використовує `QueuePool` з `pool_size=5` і
> `max_overflow=10` - до 15 одночасних з'єднань на процес. Для SQLite
> default інший: з версії 2.0 файлова SQLite (sync) теж використовує
> `QueuePool`, а `:memory:` SQLite - `SingletonThreadPool`. Параметри пулу
> налаштовуються через `create_engine(..., pool_*)`.

**Default poolclass за діалектом**

| Діалект | Pool за замовчуванням |
| --- | --- |
| PostgreSQL, MySQL, MSSQL, Oracle | `QueuePool` (`pool_size=5`, `max_overflow=10`) |
| SQLite файлова (sync, з 2.0) | `QueuePool` (раніше - `NullPool`) |
| SQLite `:memory:` (sync) | `SingletonThreadPool` (одне з'єднання на потік) |
| SQLite файлова (async) | `AsyncAdaptedQueuePool` |
| SQLite `:memory:` (async) | `StaticPool` (одне з'єднання на engine) |
| Інші async-engines (`asyncpg`, `aiomysql`) | `AsyncAdaptedQueuePool` |

`StaticPool` за замовчуванням не використовується для синхронного SQLite; його
застосовують свідомо для multi-thread сценарію спільного in-memory.

Перевизначається через `create_engine(..., poolclass=NullPool)` - наприклад,
якщо engine ділять кілька процесів через `fork()` і їм небезпечно
успадковувати TCP-з'єднання.

**Параметри `QueuePool`**

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=10,         # permanent connections kept in pool
    max_overflow=20,      # additional connections beyond pool_size on demand
    pool_timeout=30,      # seconds to wait for a free connection before TimeoutError
    pool_recycle=1800,    # close + reopen connections older than 30 min
    pool_pre_ping=True,   # TCP health check before handing out a connection
)
```

- `pool_size` - постійний резерв з'єднань. Pool ніколи не опускається нижче.
- `max_overflow` - скільки додаткових з'єднань можна відкрити понад
  `pool_size` під час сплеску. Закриваються після повернення.
- `pool_timeout` - скільки чекати вільне з'єднання, поки `pool_size +
  max_overflow` вичерпано.
- `pool_recycle` - примусове перевідкриття з'єднання після N секунд. Захист
  від MySQL `wait_timeout` (default 8 годин) і від PgBouncer/load-balancer,
  які можуть рвати idle-з'єднання після TTL.
- `pool_pre_ping=True` - перед видачею з'єднання Engine виконує `SELECT 1`;
  якщо невдало, відкидає stale-з'єднання і відкриває нове. Невелика накладна
  витрата, але страховка від stale connections після rolling restart БД або
  network blip'у.

**Sizing у production**

Загальний підхід:

1. `pool_size` ≈ кількість одночасно оброблюваних запитів (RPS × середній
   час БД-операції в секундах). Для типового FastAPI-сервіса з кількома
   воркерами по 100 RPS і 20 мс DB time - близько 2 з'єднання на worker,
   тобто `pool_size=5` достатньо.
2. `max_overflow` ≈ запас на сплеск (2-3× pool_size).
3. Сумарно `(pool_size + max_overflow) × workers` має не перевищувати
   `max_connections` БД. Postgres default `max_connections=100`; 4 worker'и
   × 15 = 60 - OK; 16 × 15 = 240 - вичерпає Postgres.

**Серверний connection pooler (PgBouncer)**

При багатьох worker-процесах (особливо у Kubernetes з горизонтальним
скейлінгом) загальна кількість з'єднань швидко б'є в стелю Postgres. Тоді
використовують **серверний** connection pooler (PgBouncer у `transaction`
mode), який мультиплексує тисячі application-з'єднань на сотню реальних до
Postgres. Деталі - у [`infrastructure/database.md`](../infrastructure/database.md)
розділ про connection pooler і у [`infrastructure/sql.md`](../infrastructure/sql.md)
розділ "`SET LOCAL` vs `SET`" (transaction-mode pooling має нюанси з
session-scoped GUC).

*Links*

- [SQLAlchemy docs: Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html) - типи пулів, параметри, поведінка
- [SQLAlchemy docs: Engine Disposal](https://docs.sqlalchemy.org/en/20/core/connections.html#engine-disposal) - чому `engine.dispose()` обов'язковий при `fork()`



### Прогрів пула (pool warm-up)

*Summary*
> Прогрів пула - явне відкриття `pool_size` з'єднань до того, як прийде
> перший запит користувача. Усуває "холодний старт" перших handler'ів і дає
> ранню діагностику невалідної конфігурації БД.

**Призначення**

За замовчуванням SQLAlchemy ліниво відкриває з'єднання - перше реальне
з'єднання створюється на першому `engine.connect()`/`Session()`. Перший
запит несе вартість TCP-handshake, TLS, автентифікації, потенційного
DNS lookup'у. На startup-критичних сервісах (короткі health-check вікна,
autoscaler, який вмикає pod у трафік одразу після `readinessProbe`) це
дає latency-spike на перші N запитів.

Прогрів дає:

- меншу хвостову латенсію на перших запитах після старту;
- ранню діагностику - якщо БД недоступна, credentials невірні або
  hostname не резолвиться, помилка вилазить на startup-етапі, а не на
  першому користувацькому трафіку;
- передбачуване споживання з'єднань до моменту, коли почне приходити
  трафік (важливо при autoscaling, де новий pod не повинен генерувати
  cold-connection sturm у момент входження в LB-ротацію).

**Реалізація**

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg://user:pass@host/db",
    pool_size=10,
    max_overflow=5,
)


def warm_up_pool() -> None:
    """Open and immediately return `pool_size` baseline connections."""
    conns = [engine.connect() for _ in range(engine.pool.size())]
    for conn in conns:
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    warm_up_pool()
    yield


app = FastAPI(lifespan=lifespan)
```

Закриття `conn.close()` повертає з'єднання у pool (не рве TCP), тому після
циклу всі `pool_size` з'єднань уже відкриті й чекають на handler-и.

Зазвичай прогрів виконують у lifespan startup для FastAPI або еквівалентному
startup-хуку для іншого фреймворку. Особливо актуально для high-load
сервісів і коротких health-check вікон, де перші N запитів можуть зловити
SLA-violation через cold-start latency.

**Обмеження**

- Прогрів закриває проблему latency для перших запитів, але не масштабує
  pool вище за `pool_size`. Під реальний пік навантаження все одно
  буде розширення через `max_overflow`.
- Якщо БД фізично далеко (cross-region), warm-up не зменшує round-trip
  time на запитах - він лише прибирає одноразову вартість встановлення
  з'єднання.



### SQLite: `foreign_keys` PRAGMA вимкнено за замовчуванням

*Summary*
> SQLite з історичних причин **не перевіряє зовнішні ключі за замовчуванням** -
> доти, доки на кожному з'єднанні не виконано `PRAGMA foreign_keys=ON`. На відміну
> від PostgreSQL/MySQL, де FK-обмеження діють завжди.

Без увімкненого прапорця вставка рядка з посиланням на неіснуючий ключ та видалення
"батьківського" рядка з наявними нащадками **проходять без помилки**, лишаючи неузгоджені
дані. Прапорець діє в межах одного з'єднання, тому в пулі його треба виставляти на кожному
новому з'єднанні - у SQLAlchemy це роблять через обробник події `connect`.

```python
from sqlalchemy import event
from sqlalchemy.engine import Engine

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")   # per-connection, enforce FKs
    cursor.close()
```

Поширений наслідок при використанні SQLite у тестах: схема ідентична продакшену на
PostgreSQL, але FK-порушення, які впали б на проді, у тестах на SQLite проходять без помилки.



### Alembic: тонкощі та анти-патерни

*Summary*
> `Alembic` - інструмент міграцій реляційної БД, тісно інтегрований із SQLAlchemy.
> Типові підводні камені: пакет не імпортується, генеруються порожні міграції,
> згенерована міграція видаляє БД, міграції неповні. Базове правило: усю структуру БД
> створює саме alembic, кожну міграцію генерують від попереднього стану, а згенероване
> завжди перевіряють і редагують вручну.

- **Alembic не може імпортувати пакет.** Робота імпортів залежить від того, який
  скрипт запущено. Правильно - зробити пакет встановлюваним: після встановлення він
  імпортується як стороння бібліотека, незалежно від розташування скрипта.
- **Генеруються порожні міграції** або частина моделей не потрапляє в міграцію. Це
  буває, коли код створення класів моделей не виконувався. У застосунку проблеми немає
  (класи імпортуються для використання), але в alembic зазвичай імпортують лише базову
  модель. Зручне рішення - імпортувати класи в `__init__.py` пакета з моделями.
- **Міграція видаляє БД.** Інструменти міграцій розраховані на те, що саме ними
  створюється вся структура. Кожна міграція переводить БД з попереднього стану
  (отриманого через alembic) у новий. Першу міграцію генерують від порожньої БД,
  міграцію `M` - від стану після `M-1`. Зміни в обхід механізму міграцій ламають
  генерацію й застосування.
- **Міграції некоректні або неповні.** Жоден інструмент не вирішує задачу повністю -
  згенероване завжди перевіряють і правлять. Часті пропуски: не оновлюється чи не
  видаляється Enum, не змінюється тип поля, не пересоздаються індекси.
- **Іменування constraint/index.** Задати `naming_convention` для `MetaData`: інакше
  alembic може не згенерувати назву обмеження/індексу, і downgrade не спрацює; крім
  того, при оновленні SQLAlchemy вбудовані угоди про іменування можуть змінитися.
- **Порядок файлів міграцій.** Він неочевидний; можна задати власні правила іменування
  (дата й час у назві), але при злитті гілок інколи доводиться правити імена вручну
  (окрім `down_revision`).
- **Не імпортувати основний код застосунку в міграціях.** Він змінюється, що ламає
  старі міграції; міграція ж не повинна змінювати поведінку після створення. За потреби
  невелику частину коду копіюють у конкретну міграцію, не маючи спільного коду між
  міграціями.
- **Тестувати міграції.** Перевіряти після створення, але не включати в регрес:
  випущені міграції зазвичай не змінюють. Корисно розгортати тестову БД міграціями й
  видаляти відкатом, а також перевіряти єдиний `head` і повторне застосування після
  відкату.

*Links*

- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/)
