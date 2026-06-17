## DDD

### Основні принципи DDD [❄️5/100]

**Domain-Driven Design (DDD)** — це підхід до проєктування складних програмних систем, 
спрямований на чітке вираження бізнес-логіки та її ізоляцію від технічних деталей. 
Головна ідея DDD полягає в тому, щоб модель програми максимально відповідала реальним 
бізнес-процесам і була зрозумілою як для розробників, так і для експертів предметної області.

DDD складається з двох основних рівнів:

**Стратегічний рівень**

- Bounded Contexts — визначає межі системи та контексти, в яких певні терміни мають специфічне значення
- Ubiquitous Language — формує єдину мову для ефективної взаємодії з бізнес-експертами та між командами
- Context Mapping — керує відносинами між різними контекстами та їх інтеграцією

**Тактичний рівень** - описує конкретні шаблони реалізації всередині bounded context

- Entities — сутності з унікальною ідентичністю
- Aggregates — кластери пов'язаних об'єктів
- Value Objects — об'єкти без ідентичності
- Domain Services — сервіси для бізнес-логіки, що не належить конкретній сутності

Уся бізнес-логіка зосереджена в доменному шарі, а саме в сутностях, агрегатах та Value Objects. 
Тут визначаються:

- Бізнес-інваріанти (правила, що завжди мають виконуватися)
- Допустимі переходи станів
- Валідні операції

Зміна стану та перевірка інваріантів відбуваються виключно через методи сутності, 
які явно виражають бізнес-зміст: `complete()`, `cancel()`, `change_owner()` тощо.

Доменні моделі не залежать від інфраструктури (ані від баз даних, ані від транспорту, 
ані від зовнішніх DTO), і це дозволяє повторно використовувати бізнес-логіку 
незалежно від того, які технології використовуються в інфраструктурному шарі. 
Репозиторії, адаптери, транспорт, логування, моніторинг та інша інфраструктура виносяться 
за межі домену й використовуються тільки в application-шарі.

Сервіси-оркестратори - це тонкий шар, який координує дії між доменними об'єктами та 
інфраструктурою. 
Він сам не містить бізнес-логіки, але керує викликами доменних методів, збором даних
і збереженням результатів. 
Він також єдиний шар, який може спілкуватися з зовнішніми системами й взаємодіяти 
з репозиторіями, надсилати події, логувати тощо.

Переваги використання DDD:

- Чітке вираження бізнес-логіки — код відображає реальні бізнес-процеси
- Покращена комунікація — спільна мова з бізнес-експертами
- Модульність — чіткі межі між компонентами
- Тестованість — легко тестувати бізнес-логіку ізольовано
- Еволюційність — система легко адаптується до змін у бізнесі
- Повторне використання — доменна логіка не залежить від технологій



### Домен [❄️3/100]

Доменна модель — це сукупність структур, які виражають бізнес-правила та поведінку 
предметної області.

У широкому сенсі це не один конкретний тип, а сукупність:

- Entity
- Aggregate
- Value Object (VO)
- Domain Service.

**Entity (сутність)** - об'єкт предметної області з ідентичністю (ID) і життєвим циклом.
Він може мати стан, бізнес-методи й брати участь в агрегатах. 
Декілька об'єктів з однаковими атрибутами, але різними ідентифікаторами, 
є різними сутностями. 
Навпаки, об'єкти з різними атрибутами, але однаковим ідентифікатором, розглядаються 
як різні стани однієї сутності.

Ознаки:

- Має ID, за яким визначається унікальність.
- Може мати змінюваний стан.
- Інкапсулює бізнес-інваріанти.
- Може бути частиною агрегату або його коренем (Aggregate Root).

Сутність і її інваріанти

```python
# domain/tasks/entity.py
class Task:
    def __init__(self, id: str, status: str, owner_id: str):
        self.id = id
        self.status = status
        self.owner_id = owner_id

    def complete(self):
        if self.status != "in_progress":
            raise ValueError("Invalid status transition")
        return Task(self.id, "completed", self.owner_id)
	
    def assign_to(self, new_owner_id: str): 
        if self.status == "completed": 
            raise ValueError("Unable to change the owner of a completed task") 
        return Task(self.id, self.status, new_owner_id)
```

**Value Object VO(Об'єкт-значення)** - це об'єкт, який не має ідентичності й визначається 
лише набором своїх атрибутів. Він іммутабельний, тобто після створення його стан 
не змінюється, а всі зміни вносяться через створення нового екземпляра. 
Використовується для представлення концепцій, не будучи сутністю. 
Дозволяють повторно використовувати бізнес-логіку та не дублювати валідації. 
Два об’єкти-значення з однаковими атрибутами вважаються еквівалентними. 
Такий об’єкт є іммутабельним.

Ознаки:

- Немає ID. Об'єкти вважаються рівними, якщо у них однакові значення.
- Іммутабельність. Після створення не змінюється.
- Інкапсулює валідацію. Перевіряє коректність значень на етапі створення.
- Групує дані, що належать разом. Гроші - це `amount` + `currency`, координата - `lat` + `lon`, період - `date_from` + `date_to`. Окремо ці поля сенсу не мають (Martin Fowler називає це Whole Value / Quantity).
- Інкапсулює операції над значенням. Порівняння, арифметику, конвертацію тримають усередині VO, щоб логіка не дублювалася по сервісах.
- Не зберігається окремо. Не має власних таблиць/репозиторіїв.

Типові VO: `Money`, `Email`, `Address`, `DateRange`, `Credentials`. Для грошей
не використовують `float` (похибка подвійної точності спотворює суми) - беруть
`Decimal` або ціле число мінімальних одиниць (центи).

```python       
# domain/value_objects.py
class Email:
    def __init__(self, value: str):
        if not self._is_valid_email(value):
            raise ValueError("Invalid email")
        self.value = value
    
    def _is_valid_email(self, email: str) -> bool:
        return "@" in email and "." in email.split("@")[1]
    
    def __eq__(self, other):
        return isinstance(other, Email) and self.value == other.value
    
    def __str__(self):
        return self.value
```

**Aggregate (Агрегат)** - це група сутностей і об'єктів-значень, які логічно пов'язані
та змінюються як єдине ціле. 
Агрегат визначає межі консистентності й вхідну точку для операцій над пов'язаними об'єктами. 
Має кореневу сутність (Aggregate Root), через методи якої здійснюється доступ 
і модифікація даних.

Ознаки:

- Має Aggregate Root - головну сутність для доступу до агрегату. Тільки через неї здійснюється доступ до інших даних.
- Гарантія інваріантів. Будь-яка операція зберігає внутрішню узгодженість.
- Визначає межі транзакції. Все всередині агрегату змінюється в рамках однієї транзакції.
- Не розкриває вкладені сутності назовні напряму. Зовнішній доступ тільки через Aggregate Root.

```python
# domain/orders/aggregate.py
class Order:  # Aggregate Root
    def __init__(self, id: str, customer_id: str):
        self.id = id
        self.customer_id = customer_id
        self.items = []
        self.status = "draft"
    
    def add_item(self, product_id: str, quantity: int, price: Money):
        if self.status != "draft":
            raise ValueError("Unable to add product to inactive order")
        item = OrderItem(product_id, quantity, price)
        self.items.append(item)
    
    def confirm(self):
        if not self.items:
            raise ValueError("Unable to confirm empty order")
        self.status = "confirmed"
```


**Domain Service**  - це компонент доменного шару, який інкапсулює бізнес-логіку,
що не належить конкретній сутності або агрегату, але все ще є частиною предметної області.

Використовується, коли логіка:

- неприродно лягає на одну конкретну сутність
- потребує координації кількох об'єктів
- при цьому залишається всередині одного домену.

Ознаки:

- Містить бізнес-логіку
- Не має власного стану (stateless)
- Не є сутністю чи Value Object
- Працює з кількома доменними моделями
- Не залежить від інфраструктури

```python
# domain/services/pricing_service.py
class PricingService:
    def calculate_discount(self, customer: Customer, order: Order) -> Money:
        discount_rate = 0.0
        
        if customer.is_vip():
            discount_rate += 0.1
        
        if order.total_amount() > Money(1000, "USD"):
            discount_rate += 0.05
        
        return order.total_amount() * discount_rate
```

**Application Service**

```python
# application/task_service.py
class TaskService:
    def __init__(self, task_repo: TaskRepository, event_publisher: EventPublisher):
        self.task_repo = task_repo
        self.event_publisher = event_publisher
    
    def complete_task(self, task_id: str, user_id: str):
        task = self.task_repo.get_by_id(task_id)  # Get data
        
        if task.owner_id != user_id:  # Check access rights
            raise ValueError("Insufficient rights to complete task")
        
        completed_task = task.complete()  # Call domain logic
        
        self.task_repo.save(completed_task)  # Save the result
        
        self.event_publisher.publish(TaskCompletedEvent(completed_task.id))  # Publish the event
```

Domain Service vs Application Service

- Domain Service - операція стосується однієї сутності або агрегату.
- Application Service - потрібна координація кількох доменів або інфраструктурних компонентів.



### Допоміжні елементи DDD

**View/Read Model** - це проекція доменної моделі, призначена тільки для читання, 
часто агрегована під конкретний use-case. 
Вона оптимізує читання даних, розвантажує доменну модель і дозволяє безпечно 
відображати агреговану інформацію.

Ознаки:

- Не є частиною домену.
- Не містить бізнес-логіки. Якщо у View з'являється поведінка, то розмивається межа між Domain Model і View Model, що порушує SRP. Виняток: методи, які не змінюють стан і не виконують бізнес-логіку, наприклад `__str__()`, `format()`.
- Використовується для відображення, звітів, API-відповідей тощо.
- Може містити агреговані дані з кількох джерел.

```python
# views/task_view.py
class TaskSummaryView:
    def __init__(self, id: str, title: str, status: str, owner_name: str, created_at: datetime):
        self.id = id
        self.title = title
        self.status = status
        self.owner_name = owner_name
        self.created_at = created_at
    
    def format_for_display(self) -> str:
        return f"{self.title} ({self.status}) - {self.owner_name}"
```

**Data Transfer Object (DTO)** - тимчасова структура, що використовується для передачі 
даних між шарами, наприклад, між транспортом і сервісом. 
DTO забезпечують слабкий зв'язок між шарами й сервісами, дозволяють ізолювати зміни
й формувати API-контракти.

Ознаки:

- Не має поведінки й бізнес-логіки.
- Використовується в транспортному шарі (gRPC, HTTP), мапиться до/з Entity/VO через конвертери. Ізолює зовнішній API від внутрішніх моделей.
- Може бути двостороннім (RequestDTO ↔ ResponseDTO).

```python
# dto/task_dto.py
class CreateTaskRequest:
    def __init__(self, title: str, description: str, owner_id: str):
        self.title = title
        self.description = description
        self.owner_id = owner_id

class TaskResponse:
    def __init__(self, id: str, title: str, status: str, owner_id: str):
        self.id = id
        self.title = title
        self.status = status
        self.owner_id = owner_id
```



### Rich vs Anemic Domain Model [❄️4/100]

*Summary*
> **Rich Model** - доменна модель, де бізнес-логіка живе всередині сутностей
> (`order.cancel()`, `account.withdraw(amount)`). **Anemic Model** - сутність
> має лише дані (поля + getter/setter), а вся бізнес-логіка винесена в
> сервіси (`OrderService.cancel(order)`). Anemic Model описаний Мартіном
> Фаулером як **антипатерн** для DDD: модель перетворюється на типізований
> dict, а Service Layer стає transaction script - DDD з нього зникає.

**Anemic Model: симптоми**

Клас з лише полями і `getX()`/`setX()`-методами, без жодної бізнес-операції.
Усю логіку виконує "сервіс":

```python
# Anemic — anti-pattern in DDD context
class Order:
    def __init__(self, id, customer_id, status, items):
        self.id = id
        self.customer_id = customer_id
        self.status = status
        self.items = items
    # ... 20+ getters/setters, no behavior


class OrderService:
    def cancel(self, order: Order, reason: str) -> None:
        if order.status == "completed":
            raise ValueError("Cannot cancel completed order")
        if order.status == "cancelled":
            raise ValueError("Already cancelled")
        order.status = "cancelled"
        order.cancellation_reason = reason
        # ... emit DomainEvent, etc.

    def add_item(self, order: Order, item: Item) -> None:
        if order.status != "draft":
            raise ValueError("Cannot modify non-draft order")
        order.items.append(item)
```

Проблеми:
- **Бізнес-правила розпорошені.** `OrderService`, `OrderValidator`, `OrderHelper`
  - усі знають правила Order. Зміна правила вимагає правок у кількох місцях.
- **Інваріанти не захищені.** Будь-хто може `order.status = "completed"`
  напряму, обійшовши `OrderService.complete()`. Encapsulation зламана.
- **Однакова логіка дублюється.** Те саме правило про "cannot cancel
  completed" з'являється у двох сервісах і поступово розходиться.

**Rich Model: бізнес-логіка у сутності**

```python
class Order:  # Rich Model — invariants enforced
    def __init__(self, id, customer_id, items):
        self._id = id
        self._customer_id = customer_id
        self._status = "draft"
        self._items = list(items)
        self._events: list[DomainEvent] = []

    def cancel(self, reason: str) -> None:
        if self._status == "completed":
            raise OrderCannotBeCancelled("Completed order cannot be cancelled")
        if self._status == "cancelled":
            raise OrderCannotBeCancelled("Already cancelled")
        self._status = "cancelled"
        self._events.append(OrderCancelled(self._id, reason))

    def add_item(self, item: Item) -> None:
        if self._status != "draft":
            raise OrderImmutable("Cannot modify non-draft order")
        self._items.append(item)
```

Бізнес-операції - методи з осмисленими іменами (`cancel`, `add_item`,
`apply_discount`), не `setStatus`/`setItems`. Інваріанти перевіряються
всередині методу - неможливо порушити стан, обійшовши контракт.

**Коли Anemic виправдане**

- **DTO/Read Model**: об'єкти для транспорту або відображення (response_model
  у FastAPI, ViewModel у UI) природно anemic - вони не модель домену, лише
  носій даних. Дивіться [Допоміжні елементи DDD](#допоміжні-елементи-ddd).
- **CRUD-сервіс без бізнес-інваріантів**: проста таблиця "tags", де
  єдина операція - додати/видалити - не потребує rich model. У такій частині
  системи DDD не застосовується взагалі.

**Зв'язок з Application Service**

Application service не зникає у Rich Model - він координує: дістає aggregate
з репозиторію, викликає бізнес-метод, зберігає назад, публікує події.
Просто **не містить** бізнес-правил - вони у сутності.

```python
class CancelOrderHandler:
    def __init__(self, repo: OrderRepository):
        self._repo = repo

    def execute(self, order_id: str, reason: str) -> None:
        order = self._repo.get(order_id)
        order.cancel(reason)  # business rules live inside Order
        self._repo.save(order)
```

*Links*

- [Martin Fowler: AnemicDomainModel](https://martinfowler.com/bliki/AnemicDomainModel.html) - канонічна стаття-критика
- [Vaughn Vernon: Implementing DDD (book)](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) - детально про Rich Aggregate



### Repository vs DAO [❄️5/100]

*Summary*
> **Repository** і **DAO** часто плутають, але це два різні патерни.
> Repository - доменна абстракція, що **імітує колекцію** aggregate'ів:
> `orders.add(order)`, `orders.get(id)`. DAO (Data Access Object) -
> інфраструктурний примітив над таблицею: `OrderDAO.insert_row()`,
> `OrderDAO.update_status()`. Repository інкапсулює DAO, плюс ORM,
> плюс кеш, але говорить **мовою домену**, а не SQL.

**DAO: data access primitive**

DAO відображає схему БД на CRUD-методи. Один-до-одного з таблицею.

```python
class OrderDAO:
    def __init__(self, db: Connection):
        self._db = db

    def insert(self, row: dict) -> int:
        return self._db.execute("INSERT INTO orders (...) VALUES (...)", row).lastrowid

    def update_status(self, order_id: int, status: str) -> None:
        self._db.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))

    def find_by_customer(self, customer_id: int) -> list[dict]:
        return self._db.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,)).fetchall()
```

API DAO - набір SQL-операцій, повертає `dict` або `Row`. Це **не модель
домену** - тільки технічна доставка даних.

**Repository: domain collection**

Repository працює з aggregate'ами (домен-об'єктами), не з рядками.
"Виглядає" як in-memory колекція - `add`, `remove`, `get` - але насправді
звертається до сховища.

```python
from abc import ABC, abstractmethod
from domain.orders import Order


class OrderRepository(ABC):
    @abstractmethod
    def add(self, order: Order) -> None: ...

    @abstractmethod
    def get(self, order_id: OrderId) -> Order: ...

    @abstractmethod
    def find_open_for_customer(self, customer_id: CustomerId) -> list[Order]: ...


class SqlOrderRepository(OrderRepository):
    def __init__(self, dao: OrderDAO, items_dao: OrderItemDAO):
        self._dao = dao
        self._items_dao = items_dao

    def add(self, order: Order) -> None:
        row = order.to_persistence()
        order_id = self._dao.insert(row)
        for item in order.items:
            self._items_dao.insert({**item.to_persistence(), "order_id": order_id})

    def get(self, order_id: OrderId) -> Order:
        order_row = self._dao.find(order_id)
        item_rows = self._items_dao.find_by_order(order_id)
        return Order.from_persistence(order_row, item_rows)  # reconstitute aggregate
```

Repository:
- **Одна репо на aggregate root**, не на таблицю. Order з 5 пов'язаними
  таблицями (`orders`, `order_items`, `order_addresses`, ...) - одна
  `OrderRepository`, не п'ять.
- **Реконструює aggregate** з даних (load + items + invariants).
- **Зберігає aggregate цілком** як один transactional act.
- **Говорить мовою домену**: `find_open_for_customer` (бізнес-запит), не
  `select_where_status_in`.

**Ключові відмінності**

| Властивість | DAO | Repository |
| --- | --- | --- |
| Рівень | Інфраструктура | Доменний шар |
| Одиниця | Рядок таблиці / `dict` | Aggregate |
| API | CRUD-методи з SQL-семантикою | Колекціє-подібний (`add`, `get`, `find`) |
| Скільки на сутність | Одне DAO на таблицю | Одне Repository на aggregate root |
| Знає про SQL/ORM? | Так, прямо | Інкапсулює DAO/ORM усередині |
| Інтерфейс | Конкретний клас | Абстракція (ABC), мокується у тестах |

**Чому плутання шкодить**

Якщо репозиторій по факту повертає `dict` чи ORM-моделі з 30 полями і
методом `.save()` - це DAO з іменем "Repository". Доменний шар тоді знає
про ORM-деталі (lazy loading, session, mapping), а Aggregate стає
двійником ORM-моделі замість самостійної доменної структури.

Симптом: у domain-коді з'являються `if order.payment is None: order.payment_id`
(перевірка lazy-load). Це означає, що Repository не реконструював
повний Aggregate - повернув proxy.

**Коли DAO достатньо**

Якщо застосунок - простий CRUD без бізнес-інваріантів і без DDD-aggregate'ів,
вводити Repository поверх DAO - оверкіл. Це повертає до питання
[Light DDD як анти-патерн](#що-таке-light-ddd-і-чому-це-анти-патерн):
тактичні патерни без потреби додають складність.

**Сусідній патерн: Gateway**

Repository і DAO - про **власні** дані застосунку. Для **зовнішніх** ресурсів
(чужий REST/gRPC API, черга, файл, message broker) є окремий патерн **Gateway**
(PoEAA): адаптер, що ізолює інтеграційні деталі - протокол, формати, таймаути,
retry, circuit breaker - від бізнес-логіки і віддає узгоджений DTO. Тобто DAO/ORM
закривають доступ до свого сховища, Gateway - до зовнішнього світу, а Repository
може збирати доменну сутність із кількох таких джерел.

*Links*

- [Martin Fowler: PoEAA - Repository](https://martinfowler.com/eaaCatalog/repository.html) - канонічний опис патерну
- [Vaughn Vernon: Implementing DDD - Repositories chapter](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) - збереження aggregate'ів
- [Microsoft docs: Designing the infrastructure persistence layer (DDD)](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)



### Next Identity: генерація ідентичності Entity [❄️1/100]

*Summary*
> Хто і коли присвоює Entity її унікальний ID. Vaughn Vernon виділяє чотири
> стратегії: ідентичність надає користувач, генерує застосунок (UUID), генерує
> сховище (`AUTO_INCREMENT`) або вона приходить з іншого Bounded Context. DDD
> тяжіє до варіанта "генерує застосунок": ID відомий до збереження, тож агрегат
> повноцінний і консистентний ще в пам'яті, без раунд-тріпу в БД. Технічний
> прийом - метод репозиторію `next_identity()`.

**Чотири стратегії присвоєння ідентичності** (Vaughn Vernon, *Implementing DDD*):

- **Користувач надає** - природний ключ, який вводить людина (email, ISBN,
  номер договору). Ризик: значення може бути помилковим, а ключ доводиться
  робити змінюваним.
- **Застосунок генерує** - доменний код створює ID сам, як правило UUID, ще до
  персистенції. Канонічний вибір для DDD.
- **Сховище генерує** - `AUTO_INCREMENT` чи `SEQUENCE` присвоює ID під час
  INSERT. Просте рішення, але ID невідомий, доки рядок не збережено.
- **Інший Bounded Context** - ID уже визначений деінде, цей контекст лише
  приймає його через інтеграцію (див. [Anti-Corruption Layer](#anti-corruption-layer-acl)).

**Обмеження auto-increment у DDD.** Якщо ID присвоює база, агрегат до
збереження не має ідентичності: не можна порівняти дві сутності, побудувати
посилання між агрегатами чи опублікувати доменну подію з `aggregate_id`, поки
не відбулося звернення до БД. Міграція legacy-схеми з `AUTO_INCREMENT` на DDD
упирається саме в це - цілісність на рівні об'єктів вимагає ID наперед.

**Прийом Next Identity.** Репозиторій видає наступний ID на вимогу, методом
`next_identity()`. Application-код отримує ID перед створенням агрегату, тож
сутність створюється одразу повною.

```python
class OrderRepository(ABC):
    @abstractmethod
    def next_identity(self) -> OrderId: ...   # hand out an ID up front

    @abstractmethod
    def add(self, order: Order) -> None: ...


class SqlOrderRepository(OrderRepository):
    def next_identity(self) -> OrderId:
        return OrderId(str(uuid4()))          # app-generated, no DB round-trip


# application layer
order_id = repo.next_identity()
order = Order(order_id, customer_id)          # aggregate is complete in memory
repo.add(order)
```

У MySQL, де немає окремих sequence-об'єктів, той самий ефект дають UUID-ключі
або емуляція sequence окремою таблицею; у PostgreSQL - `SEQUENCE` чи
`gen_random_uuid()`. Принципове одне: ID відомий **до** INSERT.

*Links*

- [Vaughn Vernon: Implementing DDD - Entities](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) - розділ про стратегії генерації ідентичності
- [Matthias Noback: When and where to determine the ID of an entity](https://matthiasnoback.nl/2018/05/when-and-where-to-determine-the-id-of-an-entity/)



### Specification pattern [❄️1/100]

*Summary*
> Specification - окремий клас-правило, який перевіряє, чи задовольняє кандидат
> певний критерій, методом `is_satisfied_by(candidate) -> bool` (Evans & Fowler).
> Розв'язує питання "де має жити інваріант, що для перевірки потребує зовнішніх
> даних" (унікальність email): не в методі Entity, не через репозиторій,
> впроваджений у домен, а окремою специфікацією доменного шару. Три
> застосування: валідація, вибірка, побудова під замовлення; специфікації
> комбінуються булевою логікою.

**Проблема розміщення інваріанта.** Частину інваріантів сутність перевіряє сама
(сума не від'ємна, валідні переходи статусу). Але є правила, для перевірки яких
потрібні дані поза агрегатом - класичне "не можна зареєструвати двох
користувачів з однаковим email": щоб перевірити, треба звернутися до сховища
всіх користувачів. Де ця перевірка має жити?

- **У методі Entity** - не виходить: щоб дізнатися про інших користувачів,
  сутність мусила б мати доступ до БД.
- **Впровадити репозиторій в Entity** - працює, але ламає інкапсуляцію:
  доменний об'єкт отримує інфраструктурну залежність, домен дотягується до
  бази, шари перемішуються.
- **Перевірити в application-хендлері** - валідний варіант: хендлер бере
  репозиторій, питає `exists_by_email`, кидає виняток. Мінус - інваріант
  від'єднаний від домену, сутність більше не є єдиним джерелом своїх правил.

**Specification як третій варіант.** Винести правило в окремий доменний клас.
Інтерфейс специфікації належить домену; його реалізація, що звертається до
сховища, - інфраструктурі.

```python
# domain/specifications.py
class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool: ...


class EmailIsUnique(Specification):
    def __init__(self, users: UserRepository):
        self._users = users

    def is_satisfied_by(self, email: Email) -> bool:
        return not self._users.exists_by_email(email)
```

Правило іменоване, тестоване ізольовано і повторно використовуване - і у
валідації при реєстрації, і деінде. Специфікації **комбінуються** булевою
логікою (`and`/`or`/`not`), тож складні критерії збираються з простих.

**Три застосування** (Evans & Fowler):

- **Валідація** - перевірити, чи кандидат задовольняє правило (приклад вище).
- **Вибірка (selection)** - відібрати зі сховища об'єкти, що задовольняють
  специфікацію (фактично умова відбору для запиту).
- **Побудова під замовлення (building to order)** - згенерувати об'єкт, який
  від початку задовольняє специфікацію.

Specification не обов'язковий: для тривіального правила перевірка в хендлері
простіша, і це нормально. Цінність зростає, коли правило складне, повторюване
або має комбінуватися з іншими. Як і будь-який патерн, він працює лише коли
команда домовилася його застосовувати - інакше та сама логіка розповзеться
методами Entity, хендлерами і специфікаціями одночасно.

*Links*

- [Eric Evans & Martin Fowler: Specifications (PDF)](https://martinfowler.com/apsupp/spec.pdf) - оригінальний опис патерну
- [Specification pattern - Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern) - поєднання правил через булеву логіку



### У чому різниця між стратегічним і тактичним рівнями DDD? [❄️3/100]

*Summary*
> Стратегічний рівень - про межі та мову (domain, subdomain, Bounded Context, Ubiquitous Language); 
> тактичний - про реалізацію всередині цих меж (Aggregate, Entity, VO, Repository, Factory, Domain Event).
> Основна цінність DDD - саме стратегічний рівень.

**Стратегічний рівень** працює зі складністю на рівні бізнесу та архітектури:

- **Domain / Subdomain** - виділення предметної області та її поділ на core/supporting/generic піддомени.
- **Ubiquitous Language** - єдина мова між розробниками та бізнес-експертами, спільна для коду, документації та розмов.
- **Bounded Context** - явна межа, всередині якої терміни Ubiquitous Language мають однозначне значення.
- **Context Mapping** - опис відносин між контекстами (Customer/Supplier, Conformist, Anti-Corruption Layer тощо).

**Тактичний рівень** - це низькорівневі ООП-патерни всередині одного Bounded Context:

- Aggregate, Aggregate Root
- Entity
- Value Object
- Repository
- Factory
- Domain Service / Domain Event

Найбільший ефект в управлінні складністю проєкту дає саме стратегічний рівень. 
Тактичні патерни - це інструмент реалізації, а не самоціль.



### Що таке Light DDD і чому це анти-патерн? [❄️1/100]

*Summary*
> Light DDD - застосування лише тактичних патернів (Aggregate, Entity, VO, Repository, Factory) без стратегічного аналізу. Код виглядає як DDD, але не вирішує головної задачі - керування складністю та узгодження з бізнесом.

Типовий сценарій: розробник прочитав Еванса, побачив перелік патернів і почав писати ООП-код, у якому є агрегати, value objects, фабрики, репозиторії - усе як у книжці. 
Код працює, його можна запустити в проді. 
Але це **не DDD**, а Light DDD - карго-культ.

Чому це проблема:

- Немає виділених доменів і піддоменів - незрозуміло, де core-логіка, а де generic.
- Немає Bounded Context - терміни розпливаються по всій системі, той самий `Order` означає різне в різних місцях.
- Немає Ubiquitous Language - розробники говорять однією мовою, бізнес - іншою; модель не відображає реальні процеси.
- Тактичні патерни прикладаються до випадково нарізаних модулів, межі агрегатів не узгоджені з бізнес-інваріантами.

Результат: формально "правильні" класи, але та сама стара заплутаність, заради боротьби з якою DDD і вигадували.



### Який правильний порядок застосування DDD?

*Summary*
> Спочатку стратегія (домени → субдомени → Ubiquitous Language → Bounded Contexts), потім тактика всередині кожного контексту.

Послідовність кроків:

1. **Виділити домен** - предметну область системи в цілому.
2. **Поділити на субдомени** - визначити core (де лежить конкурентна перевага), supporting (потрібне, але не унікальне) і generic (готові рішення на ринку).
3. **Сформувати Ubiquitous Language** - разом з бізнес-експертами зафіксувати терміни для кожного піддомену.
4. **Виділити Bounded Contexts** - провести межі, в яких мова та модель залишаються однозначними; описати відносини між ними (Context Map).
5. **Застосувати тактичні патерни** - усередині кожного Bounded Context спроєктувати Aggregates, Entities, Value Objects, Repositories, Factories, Domain Services, Domain Events.

Якщо пропустити кроки 1-4 і одразу стрибнути в тактику, отримаємо Light DDD. 
Якщо зробити лише 1-4 без тактики - отримаємо хорошу архітектурну карту без робочої реалізації. 
Цінність дає саме поєднання в правильному порядку.



### Коли застосовувати DDD [❄️2/100]

*Summary*
> DDD - інвестиція у складність моделювання, не у швидкий вихід на ринок.
> Виправдана на доменах з нетривіальною бізнес-логікою (Healthcare,
> Fintech, Insurance, Logistics, Education) і при тісній співпраці з
> доменними експертами. **Не виправдана** для CRUD-додатків, простих
> інтернет-магазинів, MVP-стартапів - накладні витрати DDD там вб'ють
> time-to-market без компенсації у вигляді розв'язку складності.

**Коли DDD дає цінність**

- **Складний домен з нетривіальними правилами.** Healthcare (правила
  вакцинації за вагою/історією), Fintech (compliance, anti-fraud,
  багаторівневі account-структури), Insurance (актуарні розрахунки),
  Logistics (маршрутизація, тарифи). Якщо логіка непомітно складна -
  domain experts мають бути у команді, і DDD дає спільну мову.
- **Великі enterprise-системи з багатьма subdomains.** Маркетплейс із
  каталогом + замовлення + логістика + білінг + аналітика - кожен
  bounded context з власною мовою. DDD ділить мегасистему на керовані
  частини.
- **Legacy refactoring.** Стара система з домішаною бізнес-логікою у
  контролерах/скриптах добре сприймає DDD-аналіз: воркшопи з доменими
  експертами виявляють процеси, які вже працюють, формалізують їх,
  допомагають реорганізувати код без зміни поведінки.
- **Ріст команди + bus factor.** Розподіл коду за bounded context'ами
  означає чіткий "ownership-границь" - команда billing володіє своїм
  контекстом, нова людина у команді onboardиться у конкретну мову.
- **Тривалий життєвий цикл.** Якщо система буде еволюціонувати 5-10 років -
  початкова інвестиція в DDD окупається. Якщо це разовий MVP на півроку - ні.

**Коли DDD - оверкіл**

- **Простий CRUD без бізнес-правил.** Інтернет-магазин з товарами,
  кошиком, оплатою через готовий gateway - бізнес-правила тривіальні
  (`if quantity > stock: error`), не потрібна доменна модель.
- **MVP / стартап на стадії product-market fit.** Time-to-market критичний,
  domain ще не сформований - кодова база міняється радикально щотижня.
  DDD-моделювання тут перетворюється на витрачені сесії, бо моделі
  застаріють раніше, ніж досягнуть production.
- **Команда без досвіду DDD.** Перший проєкт - багато помилок моделювання,
  тактичні патерни без стратегії = Light DDD антипатерн (див.
  [Що таке Light DDD](#що-таке-light-ddd-і-чому-це-анти-патерн)).
- **Немає доменних експертів.** DDD працює лише з людьми, які глибоко
  знають домен і доступні для тривалих воркшопів. Без них Ubiquitous
  Language ніколи не з'явиться.

**DDD ≠ Microservices**

Поширена омана - "1 Bounded Context = 1 мікросервіс". Це **не так**.
DDD - design approach до моделювання домену; мікросервіси - архітектурний
стиль деплою. Реальні комбінації:

- **Моноліт з модулями за bounded contexts** - найпростіша валідна
  форма. Часто кращий старт, ніж мікросервіси.
- **Один мікросервіс містить кілька bounded contexts** - якщо
  contexts маленькі і деплояться разом.
- **Один bounded context розщеплений на кілька мікросервісів** - якщо
  компоненти контексту мають різні характеристики масштабування або
  команд-власників.

Розбиття на мікросервіси - окреме архітектурне рішення, базоване на:
- Нефункціональних вимогах (масштабованість, ізоляція збоїв, частота розгортання).
- Структурі команд (Conway's Law).
- Operational complexity (мережа, observability, distributed transactions).

Bounded Context дає **межі модулів**; мікросервіси - **межі деплою**.
Вони можуть співпадати, але не зобов'язані.

**DDD у Legacy**

Окремий поширений сценарій: успадкована система з 5-15+ років роботи,
де бізнес-логіка розпорошена. Як починати:

1. **Воркшопи з доменими експертами** - які процеси ще працюють, які
   застаріли, що насправді приносить гроші. Це інформація, яка часто
   зникла з документації.
2. **Strangler Fig pattern** - нові bounded contexts створюються
   поряд із legacy, поступово перехоплюючи запити (через проксі/router)
   до повного заміщення.
3. **Anti-Corruption Layer** ([деталі](#anti-corruption-layer-acl)) -
   ізолює нову доменну модель від legacy-схеми; жоден legacy-концепт
   не "тече" у новий код.

*Links*

- [Eric Evans: DDD Reference (PDF)](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) - оригінальне довідкове резюме
- [Vaughn Vernon: Implementing Domain-Driven Design](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) - практичний посібник
- [Martin Fowler: BoundedContext](https://martinfowler.com/bliki/BoundedContext.html) - канонічна замітка



### Event Storming [❄️2/100]

*Summary*
> **Event Storming** - воркшоп-технологія для дослідження домену, придумана
> Alberto Brandolini (~2013). Команда з доменими експертами і розробниками
> біля великої дошки (фізичної або Miro) розкладає **події домену**
> хронологічно за допомогою стікерів. За кілька годин видно процеси,
> кандидати на bounded context, "гарячі точки" (hotspots) і прогалини у
> розумінні. Канонічний інструмент стратегічного DDD-discovery.

**Три рівні Event Storming**

1. **Big Picture** - усе підприємство за 3-4 години. Шукають **доменні
   події** ("OrderPlaced", "PaymentReceived", "ShipmentDispatched") і
   викладають хронологічно. Outcome: верхньорівнева мапа процесів,
   гарячі точки, кандидати на bounded contexts.
2. **Process Modeling** - детальний розбір одного процесу: команди
   (`PlaceOrder`), агенти (`Customer`, `WarehouseStaff`), політики
   (`when payment received → reserve stock`).
3. **Software Design** - переходить у тактичне моделювання: aggregates,
   read models, external systems. Зазвичай за участю більшого
   технічного складу.

**Кольорова конвенція стікерів**

Brandolini'євська канонічна палітра:

- 🟧 **Помаранчевий** - доменна подія (`OrderPlaced`, минулий час).
- 🟦 **Блакитний** - команда (`PlaceOrder`, наказова форма).
- 🟨 **Жовтий** - актор (хто ініціює команду).
- 🟪 **Фіолетовий** - політика/правило ("щоразу коли X → виконати Y").
- 🟥 **Червоний** - гаряча точка (hotspot): невідомість, конфлікт,
  неперевершене питання, до якого треба повернутися.
- 🟩 **Зелений** - read model / view (що користувач бачить, щоб
  прийняти рішення).

**Коли Event Storming доречний**

- Початок нового проєкту з нетривіальним доменом.
- Onboarding нової команди на існуючу систему (legacy discovery).
- Інтеграція 2-3 систем після злиття компаній.
- Виявлення прогалин розуміння у вже працюючій системі.

**Коли він зайвий**

- Простий CRUD без процесних бізнес-правил.
- Команда без досвідченого фасилітатора (як у Scrum майстер) - сесія
  розповзеться у обговорення без структури.
- Доменні експерти недоступні - без них воркшоп безглуздий.
- Часовий тиск, де sequence-діаграми + Miro board дають 80% результату
  за 20% часу. Це не зменшує цінність повноцінного Event Storming -
  просто визнає, що він не єдина опція discovery.

**Хто фасилітує**

Фасилітатор - окрема роль (як scrum-майстер у scrum'і). Тримає фокус,
не дає сесії скочуватися у дискусії про деталі реалізації. Часто
це досвідчений архітектор/консультант, рідше - product manager. Нова
команда без фасилітатора з досвідом часто отримує "лоп" одних і тих
же дискусій.

*Links*

- [Alberto Brandolini: Introducing EventStorming (book)](https://www.eventstorming.com/book/) - канонічна книга
- [eventstorming.com](https://www.eventstorming.com/) - офіційний сайт з прикладами
- [Martin Fowler: EventStorming](https://martinfowler.com/articles/event-storming.html) - короткий огляд



### Що таке Bounded Context і як він пов'язаний з Ubiquitous Language? [❄️5/100]

*Summary*
> Bounded Context - це зона узгодженості Ubiquitous Language: межа, всередині якої кожен термін має одне чітке значення для бізнесу й коду.

**Ubiquitous Language (єдина мова)** - словник термінів предметної області, якими 
однаково оперують і бізнес, і розробники. Бізнес висловлює концепції певними 
мовними конструкціями, а розробники розуміють той самий термін так само й переносять 
його в код один-в-один.

Для Еванса Ubiquitous Language і Bounded Context - дві нерозривні опори DDD: модель 
не існує поза контекстом, а контекст визначається саме мовою, узгодженою в його межах.
Тактичні конструкції (агрегати, сутності, value objects) реалізують цю мову й похідні 
від неї.

**Конфлікт термінів при масштабуванні.** Коли в проєкті з'являється багато 
стейкхолдерів, ті самі слова починають означати різні речі. "Клієнт" у відділі 
продажів - це лід або потенційний покупець з контактами; "Клієнт" у білінгу - 
платник із договором і балансом; "Клієнт" у підтримці - користувач з тікетами. 
Назва одна, сутність - різна.

Якщо неможливо вигадати окремий унікальний термін, який задовольнить усіх, 
виділяють **Bounded Context** - окрему зону, в якій термін "Клієнт" означає 
щось одне й конкретне. У сусідньому контексті це буде інша сутність зі своїм 
набором атрибутів і поведінки, навіть якщо називається так само.

Це дозволяє не створювати "божественну" сутність з мільярдом атрибутів на всі 
випадки життя, а тримати кожну модель сфокусованою на своєму контексті.

**Природа межі: мова, не команда**

У самій назві ключове слово - **обмежений** (bounded). Як мінімум це межа 
узгодженості Ubiquitous Language: усередині контексту кожен термін має одне 
значення. Це необхідна умова - якщо мова в одному місці ламається, контекст 
обов'язково треба виділити. Як максимум - це межа коду, команд, релізного циклу 
та бази даних; часто контексти збігаються з мікросервісами та з командами, 
які їх розробляють.

За Евансом мовний конфлікт - **мінімальний** критерій поділу. Але ділити можна 
й далі, навіть без мовних конфліктів, - за іншими ознаками:

- Розмір концепції: маркетинг і продажі можуть не перетинатися термінами, але 
  бути настільки великими, що зручніше винести їх окремо.
- Організаційна структура: над різними частинами працюють різні команди, які 
  хочуть незалежний реліз і власну кодову базу.
- Масштабованість: різний профіль навантаження або різні SLA.

**У коді: одна назва, дві моделі**

Один і той самий "Customer" - дві різні моделі в різних контекстах, з різними 
полями та поведінкою; між ними - явне мапування за ID.

```python
# contexts/sales/customer.py - Sales Bounded Context
class Customer:
    def __init__(self, id: str, lead_source: str, contact: Email):
        self.id = id
        self.lead_source = lead_source   # marketing-specific attribute
        self.contact = contact

    def qualify_as_lead(self) -> bool: ...
```

```python
# contexts/billing/customer.py - Billing Bounded Context
class Customer:
    def __init__(self, id: str, tax_id: str, balance: Money, contract_id: str):
        self.id = id
        self.tax_id = tax_id             # billing-specific attribute
        self.balance = balance
        self.contract_id = contract_id

    def charge(self, amount: Money) -> None: ...
```

Назва класу однакова, але це **різні сутності** в різних модулях/сервісах. 
Зв'язок між ними - через спільний `customer_id` і явний контракт інтеграції 
(Context Map: events, anti-corruption layer, shared kernel тощо), а не через 
спільну "товсту" модель.

**Виключення**

Якщо мова всередині концепції узгоджена і одна команда тримає її повністю - 
окремий контекст не обов'язковий:

- Терміни ніде не перетинаються з іншими значеннями - мова консистентна.
- Над концепцією працює одна команда, поділ не дасть організаційного виграшу.
- Концепція мала, винесення в окремий контекст додасть більше інфраструктурних 
  витрат (мапування, інтеграція, окреме сховище), ніж дасть ясності.

У такому разі концепція спокійно живе разом з іншими в межах одного контексту - 
це не порушення DDD.

*Links*

- [Eric Evans. Domain-Driven Design](https://www.domainlanguage.com/ddd/)
- [Martin Fowler. BoundedContext](https://martinfowler.com/bliki/BoundedContext.html)



### Як інтегрувати різні bounded contexts?

*Summary*
> Коли два мікросервіси живуть у різних bounded contexts, на межі потрібен переклад мови: **ACL** ставлять на стороні споживача, щоб захистити власну модель, **OHS** - на стороні постачальника, щоб опублікувати стабільний контракт для багатьох клієнтів.

Всередині одного bounded context сервіси розмовляють спільною Ubiquitous Language, тож DTO 
серіалізуються однаково. Коли сервіс A з одного контексту мусить надсилати дані сервісу B 
з іншого контексту, `Customer` у A і `Customer` у B - це різні концепції з різною семантикою. 
Прямий маппінг моделей псує домен: чужа мова "протікає" всередину й деформує власні інваріанти. 
Тому між контекстами потрібен **transformation boundary** - шар, який перекладає одну мову 
на іншу.

Вибір транспорту (HTTP, брокер, gRPC) вторинний відносно того, **на чиєму боці стоїть 
шар перекладу** й **хто під кого підлаштовується** - хоча сам по собі транспорт впливає 
на coupling (синхронний RPC vs асинхронні події дають різну семантику для споживачів).



### Anti-Corruption Layer (ACL) [❄️3/100]

*Summary*
> ACL - це шар-фасад на стороні споживача, який перекладає зовнішню модель у внутрішню, 
> щоб чужа мова не "коррумпувала" власний домен.

Споживач не може (або не хоче) впливати на постачальника - наприклад, legacy-система, 
зовнішній вендор, інша команда зі своїм релізним циклом. Щоб не тягнути їхній словник 
у власний домен, споживач будує адаптер: приймає вхідний DTO/event у "чужому" форматі 
й конвертує його у власні Entity/VO. Якщо постачальник змінить контракт, ламається лише ACL, 
а доменна модель залишається стабільною.

```python
# acl/billing_acl.py
# Upstream "Billing" service speaks its own language: invoices, line_items, gross_total.
# Our "Orders" context speaks: Order, OrderItem, Money.

class BillingACL:
    def to_order(self, payload: dict) -> Order:
        # Translate foreign vocabulary into our Ubiquitous Language
        order = Order(id=payload["invoice_id"], customer_id=payload["payer_ref"])
        for li in payload["line_items"]:
            order.add_item(
                product_id=li["sku"],
                quantity=li["qty"],
                price=Money(li["gross"], li["ccy"]),  # -> our VO
            )
        return order
```

Коли застосовувати:

- Інтеграція з legacy чи зовнішнім API, який ми не контролюємо.
- Upstream-команда диктує свій формат, а ми хочемо ізолювати свій домен від його змін.
- Потрібно адаптувати кілька різних upstream-постачальників до однієї внутрішньої моделі.


### Open Host Service (OHS) і Published Language [❄️2/100]

*Summary*
> У Еванса це дві парні, але окремі речі: **OHS** - сам сервіс/протокол, який постачальник 
> відкриває багатьом споживачам; **Published Language** - стабільна задокументована мова 
> (схема, контракт), якою цей сервіс розмовляє. Зазвичай вони застосовуються разом: OHS 
> публікує контракт у форматі Published Language.

Постачальник обслуговує багато клієнтів і не хоче зв'язуватися з кожним окремо. Він відкриває 
**OHS** - єдиний публічний сервіс/API/потік подій - і формалізує його контракт як 
**Published Language**: event schema, OpenAPI чи proto-визначення, що не повторює внутрішню 
модель один-в-один. Внутрішній `Order` перекладається в зовнішній `OrderPublished` 
з полями, придатними для зовнішнього світу. Усі споживачі говорять цією Published Language; 
зміна внутрішньої моделі постачальника не ламає клієнтів, доки контракт стабільний.

```python
# ohs/order_published_language.py
# Internal aggregate stays rich; the published event is a flat, stable contract.

class OrderPublisher:
    def publish_confirmed(self, order: Order) -> None:
        event = {
            "event": "order.confirmed",
            "version": "1",
            "order_id": order.id,
            "customer_id": order.customer_id,
            "items": [
                {"sku": i.product_id, "qty": i.quantity, "amount": str(i.price)}
                for i in order.items
            ],
        }
        self.broker.publish("orders", event)  # -> Published Language
```

Коли застосовувати:

- Один сервіс-постачальник з багатьма споживачами (типова шина подій).
- Команда-постачальник хоче зафіксувати контракт і еволюціонувати його версіоновано.
- Внутрішня модель надто багата чи нестабільна, щоб віддавати її "як є".


### Як обрати: ACL чи OHS? [❄️1/100]

*Summary*
> Питання не "який кращий", а "хто кого змушений підлаштовуватися": хто абсорбує зміни 
> контракту, той і ставить у себе шар перекладу.

- **ACL** - коли upstream "вище за рангом" і диктує мову, а downstream змушений адаптуватися. 
  Перекладач живе у downstream.
- **OHS** - коли постачальник свідомо стає платформою для багатьох клієнтів і бере на себе 
  стабільність контракту. Перекладач живе в upstream, у вигляді published language.
- На практиці патерни часто комбінуються: постачальник публікує OHS, а конкретний споживач 
  додатково обгортає його своїм ACL, бо хоче ізолювати власний домен навіть від стабільного, 
  але чужого словника.

Це два з кількох патернів Context Mapping за Evans (поряд із Shared Kernel, Customer/Supplier, 
Conformist, Partnership) - кожен описує іншу політику відносин між командами та контекстами.



### Інші Context Mapping патерни: Shared Kernel, Customer/Supplier, Conformist, Partnership [❄️2/100]

*Summary*
> Окрім ACL/OHS, Evans описав ще чотири канонічні патерни Context Mapping,
> які формалізують **організаційні і кодові відносини** між командами,
> що володіють різними bounded contexts. Кожен патерн - кодифікований
> компроміс між автономією, узгодженістю і координацією.

**Shared Kernel**

Дві команди погоджуються розділити **спільну** малу підмодель (kernel) -
зазвичай ядро доменних типів (`Money`, `Address`, `CustomerId`), у яких
зміна вимагає погодження обох сторін.

```python
# shared_kernel/money.py — imported by Billing AND Sales
class Money:
    def __init__(self, amount: Decimal, currency: str): ...
    def __add__(self, other: "Money") -> "Money": ...
```

- **Переваги:** не дублюється фундаментальна логіка, обидві команди
  використовують одні й ті самі типи напряму, без перетворень.
- **Недоліки:** жорстка зв'язаність - зміна Kernel вимагає узгодженого
  релізу обох команд; еволюція гальмується.
- **Коли:** дві команди близькі організаційно (одна функціональна група),
  високий рівень довіри, малий розмір kernel (~10-20% коду).

**Customer/Supplier**

Чітко визначена асиметрія: **supplier** (upstream) команда орієнтує
план розвитку частково на потреби **customer** (downstream) команд.
Customer впливає на пріоритети supplier'а через формальний процес
(запити, SLA, governance).

- **Приклад:** платформова команда (auth, notifications, payments) -
  supplier; продуктові команди - customers. Customer'и можуть впливати
  на API supplier'а, але не міняють його напряму.
- **Переваги:** баланс - supplier зберігає автономію, customer впливає
  на пріоритети.
- **Недоліки:** вимагає формального процесу пріоритезації; без нього
  supplier ігнорує customer.
- **Коли:** платформові/інфраструктурні команди обслуговують кілька
  продуктових.

**Conformist**

Downstream-команда **повністю приймає** модель upstream'а як свою, без
ACL і без переговорів. Жодного перекладу - просто використати ту мову,
яку дає upstream.

- **Приклад:** інтеграція з зовнішнім SaaS (Stripe, Salesforce, Shopify) -
  ви приймаєте їхні концепти як є, бо у вас нуль впливу на їхній API.
- **Переваги:** мінімум коду, нуль витрат на підтримку перекладу.
- **Недоліки:** ваш домен забруднюється чужими концептами; зміна upstream =
  зміна вашого коду.
- **Коли:** upstream стабільний, "чужий" словник прийнятний у вашому
  домені, ACL не виправданий.
- **Контраст з ACL:** ACL = "я хочу свою модель і перекладаю"; Conformist =
  "беру чужу модель як є".

**Partnership**

Дві команди визнають взаємозалежність і працюють як один колектив:
координують цикли релізів, спільно еволюціонують контракти, не
вибудовують перекладних шарів між собою.

- **Приклад:** два сервіси, що разом дають єдину бізнес-функцію
  (Booking + Pricing завжди ходять разом для рендера ціни).
- **Переваги:** немає накладних витрат формальних контрактів - просто
  разом планують реліз.
- **Недоліки:** масштабується лише до невеликої кількості команд; пара
  partnership = два team-meeting'и/тиждень, шість partnerships = непідйомно.
- **Коли:** малі команди з частою взаємодією, недоцільність формальних API.

**Зведення: вибір патерну**

| Патерн | Хто адаптується | Перекладач | Coordination | Коли застосовувати |
| --- | --- | --- | --- | --- |
| **Shared Kernel** | Обидві сторони (до Kernel) | Немає | Висока | Спільні фундаментальні типи |
| **Customer/Supplier** | Supplier учитавши customer | Опціональний | Помірна (через план розвитку) | Платформа vs продукти |
| **Conformist** | Downstream | Немає | Низька | Стабільний зовнішній SaaS |
| **Partnership** | Обидві сторони | Немає | Дуже висока | Малі команди з тісною взаємодією |
| **ACL** ([↑](#anti-corruption-layer-acl)) | Downstream | Так, у downstream | Низька | Захист доменного ядра від upstream |
| **OHS** ([↑](#open-host-service-ohs-і-published-language)) | Upstream (готує contract) | Так, у upstream | Висока (для контракту) | Платформа для багатьох споживачів |

На практиці патерни **комбінуються**: команда може бути Customer для
auth-platform і одночасно Conformist для Stripe, плюс мати Shared Kernel
з сусідньою командою. Context Map - візуалізація цих відносин по всій
системі.

*Links*

- [Eric Evans: Domain-Driven Design (Chapter 14)](https://www.amazon.com/Domain-Driven-Design-Tackling-Complexity-Software/dp/0321125215) - оригінальна типологія
- [DDD Crew: Context Mapping](https://github.com/ddd-crew/context-mapping) - сучасний practical-guide зі схемами
- [Martin Fowler: BoundedContext](https://martinfowler.com/bliki/BoundedContext.html)
