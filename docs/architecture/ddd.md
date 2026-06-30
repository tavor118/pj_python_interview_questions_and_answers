## DDD

### Основні принципи DDD [💡29/100]

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



### Домен [💡10/100]

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

На відміну від VO, рівність сутності визначають за **ідентичністю**, а не за полями:
дві сутності рівні, якщо збігаються їхні ID. У Python це задають через `__eq__`/`__hash__`
на основі ID (не всіх атрибутів):

```python
class Person:
    def __init__(self, identifier: str, name: Name):
        self.identifier = identifier
        self.name = name

    def __eq__(self, other) -> bool:
        return isinstance(other, Person) and other.identifier == self.identifier

    def __hash__(self) -> int:
        return hash(self.identifier)
```

Якщо сутність не потрібно класти в `set`/`dict`, `__hash__` лишають `None` (об'єкт
нехешований); змінювати `__hash__` без узгодження з `__eq__` не можна.

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

У Python об'єкт-значення зручно описувати через `@dataclass(frozen=True)`: декоратор
генерує `__eq__` за значенням полів, `__hash__` (тож VO можна класти в `set` чи ключі
`dict`) і блокує присвоєння атрибутів після створення - іммутабельність без ручного коду.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Name:
    first_name: str
    surname: str


assert Name("Harry", "Percival") == Name("Harry", "Percival")  # value equality
```

**Parse, don't validate.** VO - місце для "захисного програмування": замість того щоб
ганяти примітив (`float`, `str`) і перевіряти його в кожній точці використання, значення
один раз перетворюють на тип, у якому некоректний стан неможливий. Класична ціна помилки -
втрата апарата Mars Climate Orbiter (1999): одна підсистема рахувала в фунтах сили, інша -
в ньютонах. VO `Distance` з явними `from_meters()`/`from_feet()` і без неявного приведення
до числа усуває цей клас помилок на рівні типів. Цей підхід називають **string typing
проти strong typing**: представляти `email`, `discount`, `currency` рядками й числами
означає допускати у тип значення, які домен вважає невалідними (рядок без `@`, знижка
101%); VO звужує множину можливих значень до валідних.

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

І доменний, і прикладний сервіси - stateless-класи поверх сутностей і VO; різниця в тому,
**що** вони містять. **Domain Service несе доменну логіку** (бере участь у прийнятті
бізнес-рішень нарівні з сутностями), **Application Service - ні**: він лише оркеструє
рішення, прийняті доменом, і взаємодіє із зовнішнім світом.

**Тест цикломатичною складністю.** Сам факт виклику двох доменних методів поспіль ще не
робить код доменним знанням. Якщо метод лише делегує виклики й не має розгалужень
([cyclomatic complexity](../computer_science/computer_science.md) = 1), бізнес-рішення в
ньому немає - він на місці в application-сервісі. Доменним рішенням є `if`, що визначає
бізнес-результат (видавати гроші чи ні). Але навіть `if`, який лише ретранслює рішення
сутності (`if not atm.can_dispense(...): return`), лишається оркестрацією - саме рішення
приймає сутність через свою передумову.

**Виділення Domain Service.** Типовий потік прикладного сервісу - три кроки:
(1) підготувати дані (завантажити сутності зі сховища і зовнішніх джерел), (2) виконати
операцію (рішення домену, замкнуті на завантажених даних - на вході й виході лише
сутності, VO і примітиви), (3) застосувати результат до зовнішнього світу. У простому
CRUD кроку (2) немає - рішень нема, тож достатньо application-сервісу й навіть anemic
model. Domain service потрібен, коли рішення вимагає даних ззовні (відповідь
payment-gateway), яких сутність дістати не може без порушення своєї ізоляції: тоді цю
логіку віддають доменному сервісу, а не application-сервісу, щоб не розмазати доменне
знання поза межами домену.

**Pure проти impure.** Чистий (ізольований) domain service замкнутий на сутності та VO і
не залежить від зовнішнього світу - його можна впроваджувати в сутності. Нечистий (працює
з gateway/repository) ламає ізоляцію домену, тож впроваджувати його в сутність не варто -
тримати на рівні application/domain-сервісу.

*Links*

- [Enterprise Craftsmanship: Domain services vs Application services](https://enterprisecraftsmanship.com/posts/domain-vs-application-services/)
- [lyz-code blue-book: Domain Driven Design](https://lyz-code.github.io/blue-book/architecture/domain_driven_design/)



### Допоміжні елементи DDD [💡11/100]

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



### Проєктування меж і розміру агрегату

*Summary*
> Дві найскладніші проблеми агрегату - **межі** (що включати в агрегат) і **ціна**
> (великий агрегат дорого тримати в пам'яті). Межі проводять за трьома принципами:
> інваріанти, консистентність, транзакційність. Розмір лікують полегшеними структурами,
> лінивими колекціями або винесенням транзакційності в application-шар.

**Проблема меж.** Спокуса зробити "один агрегат, що править усіма" (god aggregate) -
тримати всі сутності всередині кореня, бо так найзручніше писати код. Межі агрегату
визначають трьома питаннями:

- **Інваріанти.** Якщо для дотримання бізнес-правила кореню агрегату бракує якихось
  даних - найімовірніше, ці дані мають бути всередині агрегату.
- **Консистентність.** Межа агрегату - це межа консистентності: агрегат **завжди**
  (від моменту реконструкції з репозиторію до кінця процесу) містить узгоджені дані;
  не може бути й мікросекунди, коли вони невалідні.
- **Транзакційність.** Якщо об'єкти мають змінюватися атомарно (разом або ніяк) -
  найімовірніше, вони належать одному агрегату.

Приклад: при зміні валюти нарахувань у програмі лояльності треба скинути налаштовані
рівні (бронза/срібло/золото). Якщо рівні - окремі сутності, а транзакцію тримає сервіс,
легко змінити валюту й забути скинути рівні. Включення сутності "рівень" в агрегат
"програма лояльності" задовольняє всі три принципи: інваріант (зміна валюти скидає рівні
в одному методі), консистентність (агрегат завжди валідний), транзакційність (рівні й
програма зберігаються атомарно).

**Проблема ціни.** Якщо агрегат тримає в пам'яті десятки тисяч дочірніх сутностей (усі
картки лояльності, уся історія списань), завантажувати його цілком стає надто дорого або
неможливо. Маркери того, що це **не один агрегат, а кілька**: бажання додати paging,
lazy-loading чи batch-update до дочірньої колекції. Order з тисячами позицій - не єдиний
агрегат; інваріанти таких "розщеплених" агрегатів забезпечують
[доменними подіями](#domain-events-доменні-події).

**Способи знизити ціну:**

- **Полегшені структури замість колекцій.** Замість повної колекції об'єктів агрегат
  тримає лише метадані (`id`, ключові поля). Транзакційність нових елементів забезпечують
  доменними подіями і службовим класом, що акумулює зміни (зберігаються разом з коренем
  в одній транзакції).
- **Винесення транзакційності в Application-шар.** Корінь декларує операції над дочірньою
  сутністю (`accrue(card, order)`), але фізично не тримає всі дочірні об'єкти; завантажити
  потрібний об'єкт і обгорнути збереження в транзакцію доручають application-сервісу.
  Простіше в реалізації, але частина логіки (наприклад, перевірка унікальності)
  піднімається в application-шар - ціна у вигляді нижчого cohesion і відступу від DDD.
- **Лінива колекція.** Колекція тримає лише `id` елементів і підвантажує конкретний
  елемент на вимогу (`get_by_id`). Оскільки домен не може звертатися до інфраструктури
  напряму, підвантаження роблять через доменну подію, яку обробляє інфраструктурний
  підписник.

**Чотири правила Вернона** ("Effective Aggregate Design") - канонічне формулювання
сказаного вище плюс два правила про зв'язки **між** агрегатами:

1. **Моделювати інваріанти в межах консистентності** - те саме, що три принципи меж вище.
2. **Проєктувати малі агрегати** - те саме, що проблема ціни вище.
3. **Посилатися на інші агрегати за ідентичністю**, а не тримати об'єктне посилання:
   `order.customer_id`, не `order.customer`. Зменшує розмір агрегату й розриває жорсткий
   зв'язок між межами.
4. **Оновлювати інші агрегати через eventual consistency** - одна транзакція змінює **один**
   агрегат; зміни в інших проводять асинхронно (доменна подія -> обробник), а не в тій
   самій транзакції.

**Хибний агрегат: концепт, що охоплює кілька контекстів.** Окремий випадок - не завеликий
агрегат у межах одного контексту, а сутність із моделі користувача (умовний `Product`,
`ShoppingCart`), чиї атрибути належать **різним** bounded context'ам: ціною володіє Sales,
наявністю - Warehouse, назвою й описом - Marketing, терміном доставки - Shipping. Зібрати
все це в один агрегат означає змусити один контекст диктувати поведінку іншому й повернути
сильну зв'язність. Правильніше: кожен контекст володіє своїм зрізом, спільний між ними лише
`id`, а цілісну картину для користувача збирають у UI (composite UI /
[`microservices.md`](microservices.md) - BFF). Орієнтир той самий, що й для меж усередині
контексту: дані, що змінюються разом, лишаються разом (транзакційна межа); атрибути, що
змінюються незалежно й мають різних власників, - сигнал різних контекстів, а не одного
агрегату.

*Links*

- [Vaughn Vernon: Effective Aggregate Design (PDF, 3 частини)](https://www.dddcommunity.org/library/vernon_2011/)
- [Habr: Проєктування доменного агрегату (проблема меж і ціни)](https://habr.com/ru/articles/954688/)
- [Habr: Байки про тактичні патерни DDD](https://habr.com/ru/articles/933588/)



### Rich vs Anemic Domain Model [💡17/100]

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

**Переваги anemic-підходу**

Anemic + service layer має реальні плюси, через які він поширений: його легко зрозуміти й
реалізувати на старті, легко контролювати на code-review (навіть джуніор бачить
відхилення), він структурованіший за повну відсутність підходу і добре лягає на дефолтну
структуру фреймворків (Entity/Controller/Repository/Service). Ціна виявляється згодом:
бізнес-логіку важко каталогізувати (легко не помітити наявний сервіс і обійти правило), а
повторне використання веде або до дублювання, або до заплутаного інжекту одних сервісів в
інші - звідси вищий coupling, нижчий cohesion і зламана інкапсуляція.

**Рефакторинг anemic -> rich** (за Хоріковим) - два кроки: (1) **сувора типізація** через
Value Objects (замість `str`/`Decimal` - `Email`/`Discount`, які не допускають невалідного
стану); (2) **зменшення кількості публічних методів, що міняють стан** - логіку переносять
із сервісів у сутності, а із сутностей - у VO. Орієнтир-піраміда: VO (низ) -> Entity
(середина) -> Service (верх); логіку штовхають якомога нижче, бо VO іммутабельні й з ними
найпростіше працювати. Ознака недостатньої інкапсуляції - коли для однієї бізнес-цілі
клієнту треба викликати два методи поспіль (додати ордер, потім оновити статус); після
рефакторингу ціль досягається одним викликом, а інваріант тримає сама сутність.

**Функціональний поділ даних і операцій - не anemic.** Розділення даних і функцій над ними
у ФП виглядає як anemic, але ним не є, бо дані **іммутабельні**: їх неможливо привести в
неконсистентний стан, тож інкапсуляція не потрібна (валідація одноразова, у конструкторі).
Майкл Фезерс: ООП робить код зрозумілим, **інкапсулюючи** рухомі частини, ФП - **мінімізуючи**
їх. Anemic-антипатерн - це змінювані дані з логікою назовні; ФП прибирає саму змінюваність.

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



### DDD-трилема: інкапсуляція, ізоляція, швидкодія

*Summary*
> Сформульована Володимиром Хоріковим: одночасно досягти **повної інкапсуляції** доменної
> моделі, її **ізоляції** від зовнішніх залежностей і максимальної **швидкодії** не можна -
> доступні лише два з трьох. Рекомендація: жертвувати швидкодією; якщо не можна - обирати
> ізоляцію над інкапсуляцією.

**Ізоляція доменної моделі** - це її незалежність від позапроцесних (база даних, зовнішні
сервіси) і волатильних залежностей. Критерій - **референційна прозорість**
([referential transparency](../python/functions.md)): виклик можна замінити його
результатом без зміни поведінки. Тому `datetime.now()` усередині доменного методу ламає
ізоляцію (щоразу інше значення) - поточний час передають аргументом ззовні. З тієї ж
причини [Active Record](../python_framework/sqlalchemy.md) (сутність сама себе зберігає)
не ізольований - змішує бізнес-логіку і доступ до БД.

**Конфлікт інкапсуляції та ізоляції.** Нехай з'являється інваріант "email кастомера
унікальний". Щоб перевірити, потрібні дані поза агрегатом - усі кастомери. Виникає дилема:

- Перевірити в контролері/хендлері - домен лишається **ізольованим**, але втрачає
  **інкапсуляцію** (не всі інваріанти всередині моделі).
- Впровадити репозиторій у сутність - домен лишається **інкапсульованим**, але втрачає
  **ізоляцію** (явна залежність на БД). Заміна `CustomerRepository` на інтерфейс
  `ICustomerRepository` нічого не міняє: залежність усе одно не референційно прозора.
- Передати в метод усіх наявних кастомерів для перевірки - зберігає й інкапсуляцію, й
  ізоляцію, але вбиває **швидкодію** (завантаження всієї таблиці).

Це і є трилема: три варіанти - три пари властивостей, повний набір недосяжний. Цей самий
інваріант унікальності окремо розглянуто в [Specification pattern](#specification-pattern).

**Рекомендація вибору.** Якщо швидкодією можна пожертвувати - жертвувати нею, бо й ізоляція,
і інкапсуляція важливі. Якщо ні - обирати **ізоляцію над інкапсуляцією**: неізольований
домен набирає зайвих відповідальностей (доступ до БД) і переускладнюється, а доменна модель
і так складна. Цей самий вибір роблять функціональне програмування (працює лише з
референційно прозорими типами) і юніт-тестування (ізольована модель тестується без моків) -
обидва ставлять ізоляцію вище за інкапсуляцію.

*Links*

- [Vladimir Khorikov: Domain-driven design (доповідь)](https://www.youtube.com/watch?v=JOy_SNK3qj4)
- [Enterprise Craftsmanship: Domain model isolation](https://enterprisecraftsmanship.com/posts/domain-model-isolation/)



### Repository vs DAO [💡18/100]

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

**Каталог патернів доступу (Fowler PoEAA)**

Повний каталог патернів роботи зі сховищем ділиться на дві групи. Перша **відділяє**
операції від даних і може повністю приховати організацію сховища: **DAO** (Table Data
Gateway) повертає RecordSet/DTO без логіки й без стану; **Data Mapper** робить
двосторонню синхронізацію моделей зі сховищем (може містити Identity Map);
**Repository** - це Data Mapper для кореневих сутностей. Друга група **змішує** дані й
роботу зі сховищем: **Row Data Gateway** (екземпляр на рядок плюс окремий Finder) і
**Active Record** (Row Data Gateway з бізнес-логікою, не абстрагований від сховища).

Багато Python-ORM реалізують Active Record (з неявним контролем з'єднань і транзакцій),
тоді як SQLAlchemy - Data Mapper (вищий рівень абстракції, `map_imperatively`); деталі -
[Active Record проти Data Mapper](../python_framework/sqlalchemy.md). Звідси й поділ
підходів: орієнтація на **стан у пам'яті** (Active Record / Data Mapper / Unit of Work:
завантажити -> змінити -> зберегти; спрощує тестування, але потребує Identity Map і
блокувань) проти орієнтації на **дії над станом у БД** (DAO: ефективніше, але частина
логіки переїжджає в запити).

**Generic Repository як анти-патерн**

Узагальнений `Repository[T]` з готовим CRUD-набором (`get_all`, `find_by`, `add`,
`update`, `delete`) виглядає зручно, але (за Беном Моррісом) це **протікаюча
абстракція**: обгортка над ORM пропускає залежність від технології у прикладний код, по
суті нічого не приховуючи. Вона **занадто узагальнена** (мало моделей обслуговуються
однаковим набором методів) і дає **беззмістовний контракт**:

```python
def find(self, query: Any) -> Iterable[T]: ...                        # meaningless contract
def find_customer_by_name(self, name: str) -> Iterable[Customer]: ...  # clear contract
```

Специфічні репозиторії з осмисленими методами кращі; узагальнений доречний лише як
внутрішня деталь реалізації конкретного репозиторію (через вкладення), де дає
перевикористання коду без втрати чіткого контракту.

*Links*

- [Martin Fowler: PoEAA - Repository](https://martinfowler.com/eaaCatalog/repository.html) - канонічний опис патерну
- [Vaughn Vernon: Implementing DDD - Repositories chapter](https://www.amazon.com/Implementing-Domain-Driven-Design-Vaughn-Vernon/dp/0321834577) - збереження aggregate'ів
- [Microsoft docs: Designing the infrastructure persistence layer (DDD)](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design)
- [Patterns Implemented by SQLAlchemy (Mike Bayer)](https://techspot.zzzeek.org/2012/02/07/patterns-implemented-by-sqlalchemy/)
- [Martin Fowler: PoEAA - Data Mapper](https://martinfowler.com/eaaCatalog/dataMapper.html)
- [Ben Morris: Why the generic repository is just a lazy anti-pattern](https://www.ben-morris.com/why-the-generic-repository-is-just-a-lazy-anti-pattern/)



### Next Identity: генерація ідентичності Entity

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



### Domain Events (доменні події)

*Summary*
> Доменна подія - факт того, що в домені **щось сталося** (`OrderConfirmed`,
> `MoneyDeposited`, минулий час). Тактичний патерн, що послаблює зв'язність: сутність
> фіксує подію, не знаючи, хто і чи взагалі її обробить. Доменні події **внутрішні**
> (в межах процесу, не зберігаються) - на відміну від integration events, що йдуть у
> шину через [Outbox](architecture_patterns.md).

**Проблема, яку вирішує.** Метод сутності інколи має спричинити побічний ефект - надіслати
email, звернутися до зовнішнього сервісу, запустити сценарій над іншим агрегатом. Прямий
виклик інфраструктури з домену зламав би ізоляцію
([трилема](#ddd-трилема-інкапсуляція-ізоляція-швидкодія)). Доменна подія розриває цей
зв'язок: сутність лише **публікує факт**, а обробник (в application-шарі) вирішує, що робити.

```python
class Order:  # Aggregate Root
    def confirm(self) -> None:
        if not self._items:
            raise ValueError("Cannot confirm empty order")
        self._status = "confirmed"
        self._events.append(OrderConfirmed(self._id))  # record the fact
```

**Час обробки.** Події обробляють **не в момент публікації**, а після завершення методу -
коли агрегат уже в узгодженому стані. Канонічна реалізація: на коміті
[Unit of Work](../python_framework/sqlalchemy.md) збирають накопичені події з усіх змінених
сутностей, обробляють (рекурсивно, бо обробники можуть породжувати нові події) і лише потім
підтверджують транзакцію - усе за принципом "все або нічого".

**Обробники - в application-шарі.** Попри назву "доменні", обробники подій належать
application-шару: вони часто роблять речі, не пов'язані з доменною логікою (публікація
integration event у шину, виклик стороннього сервісу). Сама сутність не повинна знати, чи
подія взагалі обробляється.

**Domain Events проти Integration Events.** Доменні - внутрішні, синхронні, не серіалізуються
й не залишають процес. Integration events призначені для інших контекстів, їх надсилають у
шину (надійно - через [Transactional Outbox](architecture_patterns.md)); типово обробник
доменної події і публікує integration event.

*Links*

- [Habr: Байки про тактичні патерни DDD](https://habr.com/ru/articles/933588/)
- [Martin Fowler: Domain Event](https://martinfowler.com/eaaDev/DomainEvent.html)



### Specification pattern

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
- **Впровадити репозиторій в Entity** - працює, але ламає **ізоляцію** домену:
  доменний об'єкт отримує інфраструктурну залежність, домен дотягується до
  бази, шари перемішуються (інкапсуляція при цьому збережена - усі інваріанти
  всередині моделі; це і є компроміс з [DDD-трилеми](#ddd-трилема-інкапсуляція-ізоляція-швидкодія)).
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

- **Валідація** - перевірити, чи кандидат задовольняє правило (як `EmailIsUnique`).
- **Вибірка (selection)** - відібрати зі сховища об'єкти, що задовольняють
  специфікацію (фактично умова відбору для запиту).
- **Побудова під замовлення (building to order)** - згенерувати об'єкт, який
  від початку задовольняє специфікацію.

**Перевірка в пам'яті проти виразу-запиту.** Форма `is_satisfied_by(candidate) -> bool`
виконується **в пам'яті**: годиться для валідації одного кандидата, але для **вибірки зі
сховища** її довелося б застосувати до кожного рядка вже після завантаження всієї таблиці.
Щоб відбір зробила сама СУБД, специфікація має повертати **вираз-запит**, який ORM
транслює в `WHERE` (у SQLAlchemy - вираз на кшталт `Product.quantity > 0`, що
підставляється в `select().where(...)`). Комбінування (`and`/`or`/`not`) зберігається в
обох формах, але перенести фільтр у саму базу можуть лише виразні специфікації, а не
булеві перевірки в пам'яті. Це і робить Specification зручнішим за набір ad-hoc методів
репозиторію (`get_available`, `get_available_by_name`): спільну умову задають один раз і
комбінують, не дублюючи її в кожному методі.

Specification не обов'язковий: для тривіального правила перевірка в хендлері
простіша, і це нормально. Цінність зростає, коли правило складне, повторюване
або має комбінуватися з іншими. Як і будь-який патерн, він працює лише коли
команда домовилася його застосовувати - інакше та сама логіка розповзеться
методами Entity, хендлерами і специфікаціями одночасно.

**Конфлікт із CQRS.** Найбільша цінність Specification - повторно використати **те саме**
правило і для валідації (запис), і для вибірки (читання), уникнувши дублювання доменного
знання (DRY). Але це прямо суперечить [CQRS](architecture_patterns.md), який навмисно
розділяє моделі читання й запису заради слабкої зв'язності. Це класичний конфлікт DRY проти
слабкої зв'язності, і **у переважній більшості випадків перемагає слабка зв'язність**.
Спільна специфікація для читань змушує опускатися до "найменшого спільного знаменника" - не
дає ефективно використати рідні засоби запитів сховища; натомість дублювання знання між
читанням і записом - менше зло. Тому Specification для вибірки виправданий лише в простих
сценаріях; у великих системах сторону читання будують окремо (за CQRS).

*Links*

- [Eric Evans & Martin Fowler: Specifications (PDF)](https://martinfowler.com/apsupp/spec.pdf) - оригінальний опис патерну
- [Specification pattern - Wikipedia](https://en.wikipedia.org/wiki/Specification_pattern) - поєднання правил через булеву логіку



### DDD і масові операції (bulk operations)

*Summary*
> DDD добре працює для транзакційної обробки малих обсягів (OLTP) і **погано - для масових
> операцій**. **Масова операція** (bulk update) - оновлення великого обсягу даних за один
> прохід до БД. Об'єктна модель DDD (завантажити сутності → змінити → зберегти) тут дає
> забагато roundtrip'ів. Підходів три; обирають за компромісом DRY проти продуктивності.

**Три підходи**

- **Послідовна обробка** (об'єкт за об'єктом): завантажити сутності, змінити кожну в домені,
  зберегти. Доменне знання лишається в домені (DRY), але повільно - один roundtrip на кожне
  оновлення. Для 30 000 рядків неприйнятно.
- **Сирий SQL** (`UPDATE ... WHERE ...`): швидко й просто, але порушує DRY - правило "яким
  задачам можна ставити дату" дублюється у SQL (`is_completed = false`) і в домені
  (`can_set_execution_date()`). Для простих проєктів часто прийнятно.
- **Specification + Command**: і DRY, і швидко, ціною складності. Доцільно, коли доменна
  логіка нетривіальна й має повторно використовуватися між in-memory і масовими оновленнями.

**Масове оновлення - четверте застосування Specification.** Окрім валідації, вибірки й
побудови під замовлення, специфікація може генерувати не лише вираз для запиту, а й
SQL-фільтр для `UPDATE` (метод `to_sql()` + параметри). На відміну від вибірки (читання,
що конфліктує з CQRS), масове оновлення - це **запис**, тож повторне
використання специфікації для in-memory-валідації й bulk-update відбувається в межах
write-моделі й CQRS не порушує.

**Command-патерн: розділення "що" і "як".** Специфікація каже, **які** рядки оновити
(`WHERE`), але не **як** (`SET ...`); інакше логіка присвоєння та її передумови дублюються
між сутністю і репозиторієм. Патерн **Command** (у термінах GoF) інкапсулює спосіб оновлення
і вбудовує передумови всередину себе, тож обійти їх неможливо. У цьому й суть інкапсуляції:
не покладатися на коректність кожного виклику, а усунути саму можливість некоректного.

> Термін **command** перевантажений: у [CQRS](architecture_patterns.md) це високорівнева
> операція застосунку; у CQS - будь-який метод зі side-effect (зміною стану); у GoF - клас,
> що інкапсулює всю інформацію для дії над об'єктом. У контексті bulk-операцій ідеться про
> GoF-значення.

Для більшості проєктів сирий SQL часто лишається кращим вибором через простоту, навіть ціною
DRY. Зв'язка Specification + Command виправдана для складної доменної логіки, яку хочеться
тримати в одному місці.



### У чому різниця між стратегічним і тактичним рівнями DDD?

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



### Що таке Light DDD і чому це анти-патерн?

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

**Споріднений антипатерн - механічне моделювання.** Шаблонний підхід "на кожну сутність -
репозиторій + доменний сервіс + фабрика" однаково шкідливий: доменна модель завжди має
аспекти, що не лягають у шаблон, а генерація однакового набору класів додає коду, який
згодом важко підтримувати. Доменну модель пишуть з нуля під конкретну задачу, а не
штампують генератором за шаблоном.



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

**DDD Starter Modeling Process**

П'ять кроків вище - стиснута суть; DDD-crew формалізує детальніший **ітеративний**
гайд (це орієнтир, не жорстка процедура - усі кроки опційні, їх корисність залежить від
складності й масштабу):

1. **Understand** - бізнес-модель з висоти 10 000 футів: хто користувачі, яку цінність дає продукт (Business Model Canvas).
2. **Discover** - дослідження домену з експертами (Event Storming, Domain Storytelling, Example Mapping); тут народжується Ubiquitous Language.
3. **Decompose** - виділення субдоменів: групувати те, що змінюється разом (cohesion), щоб знизити когнітивне навантаження.
4. **Connect** - зв'язки й залежності між субдоменами (Domain Message Flow Modeling, Context Mapping); перевірити, що розбиття дає слабку зв'язність.
5. **Strategize** - класифікація субдоменів за пріоритетом (Core Domain Chart).
6. **Organize** - межі команд, а не лише технічні (Team Topologies); subdomain-розбиття має лягати на структуру команд (Conway's Law).
7. **Define** - фіксація меж і відповідальностей кожного контексту (Bounded Context Canvas), документація (C4).
8. **Code** - тактичні патерни всередині контексту; для core - захисні стилі ([Hexagonal/Onion](architecture_patterns.md)).

Кроки ітеративні: відкриття на пізньому етапі повертає до раннього. Вихід процесу -
**соціально-технічна архітектура**: межі модулів і межі команд проєктують разом, а не
лише технічний поділ.

**Core Domain Chart** (Nick Tune) - інструмент кроку Strategize: субдомени розкладають
на квадранті *складність проти конкурентної переваги*. Core - висока перевага: туди
скеровують найдосвідченіших інженерів; generic - низька перевага: беруть готове рішення.
Інструмент допомагає не розпорошувати зусилля на не-core частини.

**Назва контексту як сигнал проблеми.** Уже саме найменування Bounded Context виявляє
дефекти дизайну: контекст зі словом "Manager" у назві або з описом "робить X, і Y, і
Z" вказує на розмиту відповідальність, яку варто розділити.

*Links*

- [DDD Crew: DDD Starter Modelling Process](https://github.com/ddd-crew/ddd-starter-modelling-process) - канонічний гайд з усіма кроками й інструментами
- [DDD Crew: Core Domain Charts](https://github.com/ddd-crew/core-domain-charts)



### Коли застосовувати DDD

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

**Core пишуть руками, generic беруть готовим.** Орієнтир, куди не вкладати зусиль:
**generic-піддомени** (бухгалтерія, нотифікації, SSO, платежі) - уже розв'язані проблеми,
для них беруть коробкове рішення (умовний 1С/SAP) - дешевше й швидше, ніж писати своє.
**Core-піддомен** (те, що дає конкурентну перевагу) навпаки **завжди** пишуть кастомно:
коробкове рішення для core - антипатерн, бо ніколи не дає точної відповідності
бізнес-вимогам, тягне багато непотрібного коду, а понятійний розрив (свій "клієнт роздробу"
проти чужого "діловий партнер") додає когнітивного навантаження.

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



### Event Storming

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



### Що таке Bounded Context і як він пов'язаний з Ubiquitous Language? [💡19/100]

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

**Subdomain проти Bounded Context.** Subdomain - частина *простору проблеми* (що треба
вирішити), Bounded Context - частина *простору рішення* (код, що вирішує). Ідеал - **один
до одного**: один контекст обслуговує один піддомен. Допустимо **один до багатьох**
(кілька контекстів на піддомен - часто в legacy, де поділ важко переробити). Найгірше -
**багато до багатьох**, коли контекст вирішує задачі кількох піддоменів одночасно; такого
перетину уникають.

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

**Спільні сутності й майстер-контекст.** Той самий `Customer` часто присутній у кількох
контекстах (sales і support). Код доменної моделі **не перевикористовують** між контекстами - це
підвищило б їхню зв'язність; натомість сутність дублюють, бо кожен контекст дивиться на неї
під своїм кутом (sales - як продати, support - як вирішити проблему). Дублювання йде і на
рівні БД (різні таблиці). Щоб уникнути конфліктів запису, кожен атрибут має
**майстер-контекст** - єдиний, хто його змінює; решта тримають read-only-репліку,
синхронізовану через інтеграцію. Наприклад, sales володіє `id` та `name` кастомера,
support - рівнем підтримки; кожен читає чуже, але міняє лише своє.



### Anti-Corruption Layer (ACL)

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

**Анатомія ACL.** Усередині ACL зазвичай виділяють кілька частин:

- **Інтерфейси й моделі даних** з боку бізнес-логіки - вимоги до взаємодії,
  виражені у власних термінах, лише про потрібні аспекти зовнішньої системи.
- **Клієнтський фасад** - тонка обгортка над чужим API, виражена в **термінах
  чужої системи**. Спрощує читабельність зовнішнього API (суворіші типи,
  конкретніші сигнатури, групування викликів), але не транслює виклики в доменні
  сутності. Якщо чужий API вже достатньо зручний, фасад не потрібен.
- **Адаптер** - реалізує власний інтерфейс через виклики фасаду; перекладає виклики
  з власних термінів у чужі. На одне звернення може робити кілька викликів чужого API.
- **Транслятори** - перетворюють форму даних між моделями; окремі об'єкти або методи
  адаптера.

ACL перекладає **словник домену**, а не протокол: це не проміжний шар про HTTP чи
формати серіалізації, а доменно-обізнаний переклад чужої мови у власну на межі
застосунку.



### Open Host Service (OHS) і Published Language

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


### Як обрати: ACL чи OHS?

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



### Інші Context Mapping патерни: Shared Kernel, Customer/Supplier, Conformist, Partnership

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
