## DDD

### Основні принципи DDD

**Domain-Driven Design (DDD)** — це підхід до проєктування складних програмних систем, спрямований на чітке вираження бізнес-логіки та її ізоляцію від технічних деталей. Головна ідея DDD полягає в тому, щоб модель програми максимально відповідала реальним бізнес-процесам і була зрозумілою як для розробників, так і для експертів предметної області.

DDD складається з двох основних рівнів:

- **Стратегічний рівень**
	- Bounded Contexts — визначає межі системи та контексти, в яких певні терміни мають специфічне значення
	- Ubiquitous Language — формує єдину мову для ефективної взаємодії з бізнес-експертами та між командами
	- Context Mapping — керує відносинами між різними контекстами та їх інтеграцією
- **Тактичний рівень** - описує конкретні шаблони реалізації всередині bounded context
	- Entities — сутності з унікальною ідентичністю
	- Aggregates — кластери пов'язаних об'єктів
	- Value Objects — об'єкти без ідентичності
	- Domain Services — сервіси для бізнес-логіки, що не належить конкретній сутності

Уся бізнес-логіка зосереджена в доменному шарі, а саме в сутностях, агрегатах та Value Objects. 
Тут визначаються:

- Бізнес-інваріанти (правила, що завжди мають виконуватися)
- Допустимі переходи станів
- Валідні операції

Зміна стану та перевірка інваріантів відбуваються виключно через методи сутності, які явно виражають бізнес-зміст: `complete()`, `cancel()`, `change_owner()` тощо.

Доменні моделі не залежать від інфраструктури (ані від баз даних, ані від транспорту, ані від зовнішніх DTO), і це дозволяє повторно використовувати бізнес-логіку незалежно від того, які технології використовуються в інфраструктурному шарі. Репозиторії, адаптери, транспорт, логування, моніторинг та інша інфраструктура виносяться за межі домену й використовуються тільки в application-шарі.

Сервіси-оркестратори - це тонкий шар, який координує дії між доменними об'єктами та інфраструктурою. Він сам не містить бізнес-логіки, але керує викликами доменних методів, збором даних і збереженням результатів. Він також єдиний шар, який може спілкуватися з зовнішніми системами й взаємодіяти з репозиторіями, надсилати події, логувати тощо.

Переваги використання DDD:

- Чітке вираження бізнес-логіки — код відображає реальні бізнес-процеси
- Покращена комунікація — спільна мова з бізнес-експертами
- Модульність — чіткі межі між компонентами
- Тестованість — легко тестувати бізнес-логіку ізольовано
- Еволюційність — система легко адаптується до змін у бізнесі
- Повторне використання — доменна логіка не залежить від технологій


### Домен

Доменна модель — це сукупність структур, які виражають бізнес-правила та поведінку предметної області.

У широкому сенсі це не один конкретний тип, а сукупність:

- Entity
- Aggregate
- Value Object (VO)
- Domain Service.

**Entity (сутність)** - об'єкт предметної області з ідентичністю (ID) і життєвим циклом. Він може мати стан, бізнес-методи й брати участь в агрегатах. Декілька об'єктів з однаковими атрибутами, але різними ідентифікаторами, є різними сутностями. Навпаки, об'єкти з різними атрибутами, але однаковим ідентифікатором, розглядаються як різні стани однієї сутності.

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

**Value Object VO(Об'єкт-значення)**  - це об'єкт, який не має ідентичності й визначається лише набором своїх атрибутів. Він іммутабельний, тобто після створення його стан не змінюється, а всі зміни вносяться через створення нового екземпляра. Використовується для представлення концепцій, не будучи сутністю. Дозволяють повторно використовувати бізнес-логіку та не дублювати валідації. Два об’єкти-значення з однаковими атрибутами вважаються еквівалентними. Такий об’єкт є іммутабельним, .

Ознаки:

- Немає ID. Об'єкти вважаються рівними, якщо у них однакові значення.
- Іммутабельність. Після створення не змінюється.
- Інкапсулює валідацію. Перевіряє коректність значень на етапі створення.
- Не зберігається окремо. Не має власних таблиць/репозиторіїв.

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

**Aggregate (Агрегат)**  - це група сутностей і об'єктів-значень, які логічно пов'язані та змінюються як єдине ціле. Агрегат визначає межі консистентності й вхідну точку для операцій над пов'язаними об'єктами. Має кореневу сутність (Aggregate Root), через методи якої здійснюється доступ і модифікація даних.

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


**Domain Service**  - це компонент доменного шару, який інкапсулює бізнес-логіку, що не належить конкретній сутності або агрегату, але все ще є частиною предметної області.

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

**View/Read Model**  - це проекція доменної моделі, призначена тільки для читання, часто агрегована під конкретний use-case. Вона оптимізує читання даних, розвантажує доменну модель і дозволяє безпечно відображати агреговану інформацію.

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

**Data Transfer Object (DTO)** - тимчасова структура, що використовується для передачі даних між шарами, наприклад, між транспортом і сервісом. DTO забезпечують слабкий зв'язок між шарами й сервісами, дозволяють ізолювати зміни й формувати API-контракти.

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
