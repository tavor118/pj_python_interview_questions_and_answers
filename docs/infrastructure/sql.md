## SQL

### Що таке SQL

**SQL (Structured Query Language)** — це мова для роботи з реляційними базами даних,
що використовується для створення, модифікації, управління та отримання даних.
Вона є стандартом для більшості сучасних реляційних СУБД, таких як MySQL, PostgreSQL,
SQLite та інші.

- SQL дозволяє створювати структуру бази даних через команди створення таблиць, індексів, та зв’язків між таблицями.
- Основні операції SQL включають `SELECT` для вибірки даних, `INSERT` для додавання, `UPDATE` для оновлення та `DELETE` для видалення записів.
- SQL підтримує складні запити за допомогою умов `WHERE`, сортування `ORDER BY`, агрегації даних `GROUP BY`, а також функцій для роботи з підзапитами та об'єднання таблиць (`JOIN`).
- Мова SQL є декларативною, тобто користувач описує, що він хоче отримати або змінити, а не як саме це потрібно зробити.
- У сучасних застосунках SQL часто використовується через ORM (Object-Relational Mapping) інструменти, такі як SQLAlchemy для Python, що дозволяє взаємодіяти з базою даних через об'єкти класів замість прямого написання SQL-коду.

Приклад базового запиту SQL для вибірки всіх користувачів з бази даних:

```sql
SELECT * FROM users WHERE age > 18 ORDER BY name ASC;
```



### Оператори `SELECT`, `INSERT`, `UPDATE` та `DELETE` [❄️1/100]

Призначення операторів

- `SELECT` для вибірки даних
- `INSERT` для додавання записів
- `UPDATE` для оновлення записів
- `DELETE` для видалення записів

Оператор `SELECT` використовується для вилучення даних з бази даних.
Він дозволяє вибирати певні стовпці з таблиці, фільтрувати дані за умовами,
сортувати, групувати і виконувати інші операції над даними. 

```sql
SELECT column1, column2 FROM table_name WHERE condition;
```

Оператор `INSERT` використовується для вставки нових даних у таблицю.
Він дозволяє вказувати значення для стовпців або вставляти значення з іншої таблиці. 

```sql
INSERT INTO table_name (column1, column2) VALUES (value1, value2);
```

Оператор `UPDATE` використовується для зміни даних у таблиці.
Він дозволяє оновлювати значення стовпців у певних рядках таблиці.
Можна вказувати умови для фільтрації даних, які потрібно оновити. 

```sql
UPDATE table_name SET column1 = value1, column2 = value2 WHERE condition;
```

Оператор `DELETE` використовується для видалення даних з таблиці.
Він дозволяє видаляти певні рядки таблиці на основі умов.

```sql
DELETE FROM table_name WHERE condition
```



### SQL Constraints

**Обмеження (Constraints)** використовуються для визначення правил для даних у таблиці.

Обмеження використовуються для обмеження типу даних, які можуть входити в таблицю.
Це забезпечує точність і достовірність даних у таблиці.
Якщо існує будь-який конфлікт між обмеженням і дією з даними, дія переривається.

Обмеження можуть бути на рівні стовпця або таблиці.
Обмеження рівня стовпця застосовуються до стовпця, а обмеження рівня таблиці застосовуються до всієї таблиці.

Перелік обмежень

- `NOT NULL` - гарантує, що стовпець не може мати значення `NULL`
- `UNIQUE` – гарантує, що всі значення в стовпці відрізняються
- `PRIMARY KEY` - комбінація `NOT NULL` і `UNIQUE`. Унікально визначає кожен рядок у таблиці
- `FOREIGN KEY` - однозначно ідентифікує рядок/запис в іншій таблиці
- `CHECK` - гарантує, що всі значення в стовпці задовольняють певну умову



### PK - Primary Key, FK -Foreign Key, UNIQUE - Unique constraint [❄️1/100]

**Primary Key (Первинний Ключ)** - це унікальний ідентифікатор (стовпець або комбінація 
стовпців), який визначає конкретний запис в базі даних.
Він гарантує унікальність кожного запису в таблиці і дозволяє ефективно виконувати пошук
та звертатися до конкретних даних. Кожна таблиця може мати лише один первинний ключ.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255)
);
```

**Foreign Key (Зовнішній Ключ)** - це поле в таблиці бази даних, яке вказує
на Primary Key іншої таблиці.
Він встановлює зв'язок між двома таблицями, дозволяючи одній таблиці посилатися на дані 
в іншій.
Це використовується для створення зв'язків між таблицями та забезпечення цілісності даних 
в базі даних.
Таблиця може мати кілька зовнішніх ключів, що вказують на її зв'язок із різними таблицями.

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id)
);
```

`UNIQUE` – обмеження гарантує унікальність значень - всі значення стовпця відрізняються 
один від одного.
Обмеження первинного ключа має автоматичне обмеження на унікальність.
В таблиці можна мати багато унікальних обмежень, але тільки одне обмеження
первинного ключа таблиці.

```sql
CREATE TABLE users (
 id int NOT NULL,
 email varchar(255) UNIQUE, -- all the emails shoud be unique
 CONSTRAINT pk_user PRIMARY KEY (id)
);
```



### Оператор та види `JOIN` [❄️3/100]

Оператор `JOIN` в SQL використовується для об'єднання даних з двох або більше таблиць
на основі визначених умов.
`JOIN` дозволяє комбінувати дані з різних таблиць в один результат.

Умова з'єднання вказується в реченні `ON`.
Ця умова визначає, які рядки двох вихідних таблиць вважаються "відповідними" один одному.

Слова `INNER` та `OUTER` не є обов'язковими у всіх формах.
За замовчуванням передбачається INNER` `(внутрішнє з'єднання), а при вказанні 
`LEFT`, `RIGHT` і `FULL` - зовнішнє з'єднання.

Види джойнів

- `JOIN` (`INNER JOIN`)
- `LEFT JOIN` (`LEFT OUTER JOIN`)
- `RIGHT JOIN` (`RIGHT OUTER JOIN`)
- `FULL JOIN` (`FULL OUTER JOIN`)
- `CROSS JOIN`

- `INNER JOIN` - Повертає ті рядки, які мають відповідні значення в обох таблицях.

```sql
SELECT Orders.order_id, Customers.customer_name
FROM Orders
JOIN Customers ON Orders.customer_id = Customers.customer_id;
```

- `LEFT OUTER JOIN` - Повертає всі рядки з лівої (першої) таблиці та відповідні значення з правої (другої) таблиці. Якщо відповідних значень немає, повертається `NULL`.

```sql
SELECT Customers.customer_name, Orders.order_id
FROM Customers
LEFT JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

- `RIGHT OUTER JOIN` - Повертає всі рядки з правої (другої) таблиці та відповідні значення з лівої (першої) таблиці. Якщо відповідних значень немає, повертається `NULL`. Це з'єднання є протилежним до лівого (`LEFT JOIN`).

```sql
SELECT Customers.customer_name, Orders.order_id 
FROM Customers 
RIGHT JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

- `FULL OUTER JOIN` - Повертає всі рядки з обох таблиць, і якщо відповідних значень немає, повертається `NULL`. Фактично це одночасний `LEFT` та `RIGHT JOIN`.

```sql
SELECT Customers.customer_name, Orders.order_id 
FROM Customers 
FULL JOIN Orders ON Customers.customer_id = Orders.customer_id;
```

- `CROSS JOIN` - Повертає декартовий добуток (комбінацію) всіх рядків із першої таблиці та всіх рядків із другої таблиці.

```sql
SELECT Customers.customer_name, Products.product_name 
FROM Customers 
CROSS JOIN Products;
```

Латеральний JOIN, (`LATERAL JOIN`) дозволяє використовувати результати попереднього запиту 
як джерело даних для подальших операцій JOIN, що дозволяє створювати більш складні
і гнучкі запити.

Основна властивість латерального JOIN полягає в тому, що він дозволяє включати підзапити, 
які "бачать" дані з рядків, отриманих від зовнішніх таблиць.
Це дозволяє використовувати значення з поточного рядка як параметр для підзапиту,
що в свою чергу дозволяє гнучко маніпулювати даними.

```sql
SELECT e.employee_name, t.task_name
FROM employees e
LEFT JOIN LATERAL (
    SELECT task_name
    FROM tasks
    WHERE tasks.employee_id = e.employee_id
    LIMIT 5 -- Limit the number of tasks per employee, for example
) t ON true;
```



### Підзапити

**Підзапити SQL** - це запити, вкладені всередині інших запитів.

Підзапити можуть бути використані для створення складних і гнучких запитів,
які вимагають більш складної логіки або операцій з даними.
Підзапити можуть використовуватися в різних частинах SQL-запиту,
таких як `SELECT`, `FROM`, `WHERE`, `HAVING` та інших.

Підзапити можуть бути менш ефективними з точки зору продуктивності,
особливо під час роботи з великими обсягами даних.
Вони можуть призвести до підвищеного часу виконання запитів та навантаження на базу даних.
В таких випадках можна спробувати замінити підзапит на `JOIN`.

Підзапит в операторі `SELECT`

```sql
SELECT product_name, (SELECT AVG(price) FROM prices WHERE product_id = products.id) as avg_price
FROM products;
```

Підзапит в операторі `FROM`

```sql
SELECT product_name, price
FROM products
JOIN (SELECT product_id, AVG(price) as avg_price FROM prices GROUP BY product_id) as subquery
ON products.id = subquery.product_id
WHERE price > subquery.avg_price;
```

Підзапит в операторі `WHERE`

```sql
SELECT order_id, customer_id
FROM orders
WHERE customer_id IN (SELECT customer_id FROM customers WHERE customer_type = 'premium');
```



### Агрегатні функції і `GROUP BY`

Агрегатні функції SQL використовуються для обчислення агрегатних значень на основі даних
в стовпцях таблиці. 

Основні агрегатні функції SQL

- `COUNT`
- `SUM`
- `AVG`
- `MIN`
- `MAX`

`COUNT`
Повертає кількість рядків або значень у стовпці. Може використовуватися з модифікатором `DISTINCT` для розрахунку унікальних значень.

```sql
SELECT COUNT(*) AS total_orders
FROM Orders;
```

`SUM`
Повертає суму значень у стовпці. Може використовуватись лише з числовими стовпцями.

```sql
SELECT SUM(order_total) AS total_sales
FROM Orders;
```

`AVG`
Повертає середнє значення значень у стовпці. Може використовуватись лише з числовими стовпцями.

```sql
SELECT AVG(order_total) AS avg_order_total
FROM Orders;
```

`MIN`
Повертає мінімальне значення у стовпці. Може використовуватись з будь-яким типом даних.

```sql
SELECT MIN(order_date) AS earliest_order_date
FROM Orders;
```

`MAX`
Повертає максимальне значення у стовпці. Може використовуватись з будь-яким типом даних.

```sql
sqlCopy code
SELECT MAX(order_date) AS latest_order_date
FROM Orders;
```

Оператори GROUP BY, HAVING використовуються спільно з агрегатними функціями 
для виконання агрегації на рівні груп або для створення зведених звітів.

`GROUP BY`
Використовується для угруповання результатів по одному або декільком стовпцям.

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM Orders
GROUP BY customer_id;
```

`HAVING`
Використовується для фільтрації груп після застосування GROUP BY на основі умов,
заданих у HAVING.

```sql
SELECT customer_id, COUNT(*) AS order_count
FROM Orders
GROUP BY customer_id
HAVING COUNT(*) > 5;
```



### У чому різниця між операторами `HAVING` та `WHERE`?

Оператор `HAVING` використовується у зв'язці з `GROUP BY`, щоб фільтрувати рядки
на основі агрегатних функцій.
У свою чергу оператор `WHERE` фільтрує рядки перед групуванням.
Простіше кажучи `WHERE` використовується для звуження пошуку на рівні рядків,
а `HAVING` вибирає конкретні результати після групування.

```sql
SELECT department, COUNT(*) AS total_employees
FROM employees
GROUP BY department
HAVING total_employees > 10;
```



### `UNION` та `UNION ALL`

`UNION` та `UNION ALL` використовуються для об’єднання результатів кількох запитів у один набір даних.

- `UNION` видаляє дублікати зі з'єднаного набору результатів. Використовується, коли потрібен унікальний список значень, при цьому виконує додаткову перевірку для усунення дублікатів, що може уповільнити виконання запиту на великих наборах даних.
- `UNION ALL` зберігає всі записи, включаючи дублікати.

Обидва оператори вимагають, щоб кількість і типи стовпців у всіх запитах, що об'єднуються, збігалися. 

```sql
-- Union example, duplicates will be removed
SELECT column_name FROM table1
UNION
SELECT column_name FROM table2;

-- Union All example, duplicates will be kept
SELECT column_name FROM table1
UNION ALL
SELECT column_name FROM table2;
```



### Функції в SQL

Рядкові функції

- `CONCAT()`
	- Об'єднання двох або більше рядків.
	- `SELECT CONCAT('Hello', 'World');` -- Результат: 'HelloWorld'
- `LENGTH()`
	- Повертає довжину рядка.
	- `SELECT LENGTH('Hello');` -- Результат: 5
- `UPPER()`
	- Перетворення рядка у верхній регістр.
	- `SELECT UPPER('hello');` -- Результат: 'HELLO'
- `LOWER()`
	- Перетворення рядка на нижній регістр.
	- `SELECT LOWER('WORLD');` -- Результат: 'world'
- `SUBSTRING()`
	- Вилучення підрядка з рядка.
	- `SELECT SUBSTRING('HelloWorld', 6, 5);` -- Результат: 'World'

Математичні функції

- `ABS()`
	- Повертає абсолютне значення числа.
	- `SELECT ABS(-5); `-- Результат: 5
- `ROUND()`
	- Округлення числа до заданої кількості знаків після коми.
	- `SELECT ROUND (3.14159, 2);` -- Результат: 3.14
- `CEILING()`
	- Округлення числа у велику сторону до найближчого цілого.
	- `SELECT CEILING (3.2);` -- Результат: 4
- `FLOOR()`
	- Округлення числа в меншу сторону до найближчого цілого.
	- `SELECT FLOOR(3.8);` -- Результат: 3
- `RAND()`
	- Генерація випадкового числа.
	- `SELECT RAND();` -- Результат: випадкове число від 0 до 1

Інші функції

- `COALESCE()`
	- Повертає перше ненульове значення зі списку значень.
	- `SELECT COALESCE(column1, column2, column3, 'N/A') FROM table1;`
- `NULLIF()`
	- Повертає NULL, якщо два значення дорівнюють.
	- `SELECT NULLIF(column1, 0) FROM table1;`
- `CASE()`
	- Виконує умовну логіку SQL запиту.
	- `SELECT column1, CASE WHEN column1 > 0 THEN 'Positive' ELSE 'Negative' END FROM table1;`



### `UPSERT`

`UPSERT` (update or insert) у SQL — це операція, яка дозволяє вставляти нові рядки 
у таблицю або оновлювати існуючі, якщо такі вже присутні.
Це корисно для забезпечення цілісності даних та уникнення дублювання записів.
Залежно від бази даних, синтаксис UPSERT може відрізнятися. 

- У PostgreSQL UPSERT реалізується через `INSERT ... ON CONFLICT`. Ви вказуєте, що робити у разі конфлікту (наприклад, оновити дані).
- У MySQL використовують `INSERT ... ON DUPLICATE KEY UPDATE`. Це оновлює рядок, якщо ключ уже існує.
- У SQLite UPSERT доступний через `INSERT ... ON CONFLICT`.
- У Oracle використовують `MERGE` для реалізації UPSERT-поведінки.

Приклад для PostgreSQL

```sql
INSERT INTO users (id, name, email) 
VALUES (1, 'John Doe', 'john.doe@example.com') 
ON CONFLICT (id)  -- identifies the field causing the conflict
DO UPDATE SET 
    name = EXCLUDED.name,
    email = EXCLUDED.email;
    
-- "EXCLUDED" is a special reference to the data being attempted to be inserted
```

Цей запит вставить новий запис, якщо `id` не існує, або оновить `name` та `email`,
якщо запис із таким `id` уже присутній.



### `TRUNCATE` vs `DELETE` [❄️2/100]

*Summary*
> `DELETE` видаляє рядки по одному за умовою `WHERE`, пише per-row записи в WAL, тригери
> ON DELETE спрацьовують, місце на диску звільняє лише `VACUUM`. `TRUNCATE` миттєво
> скидає вміст таблиці на metadata-рівні, без per-row логування, одразу повертає місце
> ОС. У Postgres `TRUNCATE` транзакційна (можна відкотити в межах транзакції) - у
> MySQL/Oracle це DDL з implicit commit.

**Принцип роботи `DELETE`**

`DELETE FROM t WHERE …` обходить таблицю, для кожного рядка позначає його як
"мертвий" (видимий для старих snapshot'ів через MVCC), записує per-row запис у WAL,
запускає тригери `BEFORE`/`AFTER DELETE` і оновлює індекси. Фізично рядки лишаються
у файлах таблиці, поки `VACUUM` не звільнить місце; до того часу таблиця і її індекси
зберігають попередній розмір.

```sql
DELETE FROM orders WHERE status = 'cancelled' AND created_at < '2025-01-01';
-- builds WAL records per row, fires ON DELETE triggers,
-- space reclaimed only after VACUUM
```

**Принцип роботи `TRUNCATE`**

`TRUNCATE TABLE t` працює як швидке скидання вмісту: за документацією, "видаляє всі
рядки з набору таблиць ... оскільки не сканує таблиці, працює швидше [за `DELETE`].
Крім того, одразу повертає дисковий простір, не вимагаючи `VACUUM`". Тригери `ON
DELETE` не запускаються, окремі рядки не обходяться.

```sql
TRUNCATE TABLE staging_events;                       -- single table
TRUNCATE TABLE orders, order_items CASCADE;          -- + tables referencing via FK
TRUNCATE TABLE counters RESTART IDENTITY;            -- reset sequences (Postgres)
```

**Транзакційність у Postgres**

Ключовий нюанс, на якому часто плутаються кандидати: у **Postgres** `TRUNCATE` -
транзакційна команда. Її можна викликати всередині `BEGIN … ROLLBACK` і таблиця
повернеться до попереднього стану:

```sql
BEGIN;
TRUNCATE TABLE orders;
-- still inside transaction
ROLLBACK;  -- table is back to its original contents
```

У **MySQL** і **Oracle** `TRUNCATE` - DDL з implicit commit: транзакція автоматично
завершується перед виконанням, відкатити неможливо.

**Тригери**

- `DELETE` запускає row-level тригери `BEFORE/AFTER DELETE` на кожен рядок.
- `TRUNCATE` запускає statement-level тригер `BEFORE/AFTER TRUNCATE` (один раз на
  команду). Row-level `ON DELETE` тригери **не** спрацьовують - типове джерело
  тонких багів при міграції з `DELETE` на `TRUNCATE`.

**Сценарії застосування**

- **`TRUNCATE`:** очистка staging-таблиці перед ETL-завантаженням, скидання тестових
  фікстур між прогонами, повне очищення журналу. Великий виграш у швидкості для
  таблиць з мільйонами рядків (за документацією Postgres - саме тому, що не сканує
  рядки).
- **`DELETE`:** умовне видалення (за `WHERE`), коли потрібні row-level тригери,
  коли репліка/CDC має отримати per-row події, коли є FK без `CASCADE` і видалення
  має відбутися лише для частини рядків.

**Обмеження**

- `TRUNCATE` вимагає окремого `TRUNCATE` privilege на таблиці; `DELETE` - `DELETE`
  privilege. **Row-level security (RLS) до `TRUNCATE` не застосовується** ("operations
  that apply to the whole table, such as `TRUNCATE` and `REFERENCES`, are not subject
  to row security" - з документації Postgres), тоді як `DELETE` повністю підпадає
  під RLS-політики.
- `TRUNCATE` бере на таблиці lock рівня `ACCESS EXCLUSIVE`, що блокує всі конкурентні
  операції (включно з `SELECT`). `DELETE` бере `ROW EXCLUSIVE` на таблицю - не
  блокує читачів (звичайні `SELECT` беруть `ACCESS SHARE`, який сумісний з
  `ROW EXCLUSIVE`).

*Links*

- [Postgres docs: TRUNCATE](https://www.postgresql.org/docs/current/sql-truncate.html) - privileges, transactional behavior, `ON TRUNCATE` triggers, `RESTART IDENTITY`
- [Postgres docs: Explicit Locking](https://www.postgresql.org/docs/current/explicit-locking.html) - lock modes (`ACCESS EXCLUSIVE`, `ROW EXCLUSIVE`)
- [Postgres docs: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) - "`TRUNCATE` and `REFERENCES` are not subject to row security"



### Що робить SELECT FOR UPDATE? [❄️5/100]

`SELECT FOR UPDATE` – це SQL-конструкція, яка використовується для блокування рядків,
що вибираються під час виконання запиту, щоб уникнути конкурентних змін даних.
Ця конструкція зазвичай застосовується в транзакціях для забезпечення консистентності даних.

Вона виконує ексклюзивне блокування рядків, які відповідають умовам запиту,
і дозволяє тільки одному процесу або транзакції читати або змінювати ці рядки.
Інші транзакції, що спробують виконати `SELECT FOR UPDATE` для цих же рядків,
будуть чекати, поки поточна транзакція завершиться (коміт або ролбек).

Зазвичай використовується, коли є потреба прочитати дані, провести певні обчислення
та потім оновити ці дані без ризику, що інша транзакція зможе змінити їх між читанням
і записом.
Це важливо для уникнення проблем, таких як race conditions.

Недоліком є те, що використання `SELECT FOR UPDATE` може призвести до зменшення 
швидкодії за рахунок блокування ресурсів та можливих deadlock-ів.
Тому його треба застосовувати з обережністю в системах з високою конкуренцією запитів.

  ```sql
  BEGIN;

  -- Selecting rows for update
  SELECT * FROM orders
  WHERE status = 'pending'
  FOR UPDATE;

  -- Performing update based on previous select
  UPDATE orders
  SET status = 'processing'
  WHERE status = 'pending';

  COMMIT;
  ```

**Сценарії застосування**

- **Грошові перекази, робота з рахунками.** Щоб уникнути "подвійного списання", блокується рядок балансу до коміту.
- **Редагування критичних бізнес-сутностей** (контракт, налаштування), які не можна змінювати паралельно.
- **Розбір черг у БД** - типовий патерн `SELECT ... FOR UPDATE SKIP LOCKED` для воркерів, які беруть наступне необроблене завдання.

**Обмеження**

- Якщо читається багато рядків, а змінюється лише один - блокувати все буде надмірно.
- Якщо конфлікти трапляються часто і система масштабується - краще оптимістична блокування через `version` / `updated_at` (`WHERE ... AND version = ?`).
- Якщо важлива висока паралельність - `FOR UPDATE` може спричиняти дедлоки і простої.

**Типи локів**

- **`FOR UPDATE`** - **X-lock** (exclusive): блокує і читання `FOR UPDATE` / `FOR SHARE`, і запис іншими транзакціями. Звичайний `SELECT` без локу далі читає снапшот через MVCC.
- **`FOR SHARE`** - **S-lock** (shared): дозволяє іншим читати з `FOR SHARE`, але блокує `FOR UPDATE` та запис. Кілька shared-локів співіснують.
- **`FOR NO KEY UPDATE`** - слабший за `FOR UPDATE`: не заважає FK-перевіркам в інших транзакціях.
- **`FOR KEY SHARE`** - слабший за `FOR SHARE`: блокує лише зміну ключа (саме цей режим автоматично використовують FK-перевірки), дозволяючи звичайні `UPDATE` неключових полів. Як і інші row-locks, тримається до кінця транзакції.

**Опції при конфлікті**

- За замовчуванням транзакція **чекає**, поки lock зніметься.
- **`NOWAIT`** - одразу повертає помилку замість чекати.
- **`SKIP LOCKED`** - пропускає вже заблоковані рядки.

Концептуально оптимістичне vs песимістичне блокування (з порівнянням trade-off-ів,
MVCC і retry з exponential backoff + jitter) - див.
[`architecture/system_design.md`](../architecture/system_design.md).



### Що таке віконні функції і як вони працюють?

**Віконні функції** - це засіб в SQL, який дозволяє виконувати обчислення на підмножині 
рядків з результатами запиту і керувати їх порядком та групуванням.
Вони корисні для виконання аналізу даних на рівні рядків і дозволяють враховувати 
взаємозв'язані дані при обчисленнях.

У PostgreSQL можна використовувати віконні функції, використовуючи ключове слово `OVER`. 
Наприклад, є таблиця `orders` зі стовпцями `order_date`, 
`customer_id` і `order_amount`. Можна використовувати віконну функцію `SUM` для 
обчислення кумулятивної суми замовлень для кожного клієнта впродовж часу.

```sql
SELECT 
    order_date,
    customer_id,
    order_amount,
    SUM(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date) AS cumulative_order_amount
FROM 
    orders;
```

У цьому запиті ми використовуємо функцію 
`SUM(order_amount) OVER (PARTITION BY customer_id ORDER BY order_date)`.
Частина `PARTITION BY customer_id` розділяє дані на групи
за `customer_id`, а `ORDER BY order_date` визначає порядок сортування за датою замовлення.

Таким чином, для кожного рядка ми отримаємо значення кумулятивної суми суми замовлень
для відповідного клієнта на даний момент.

Досягти того ж результату, що і у вище наведеному прикладі, можна використовуючи `GROUP BY`.

```sql
SELECT 
    order_date,
    customer_id,
    order_amount,
    SUM(order_amount) AS cumulative_order_amount
FROM 
    orders
GROUP BY 
    customer_id, order_date, order_amount
ORDER BY 
    customer_id, order_date;
```

Обидва запити дають однаковий результат - кумулятивну суму сум замовлень
для кожного клієнта на основі дати замовлення.
Однак, використання віконних функцій дозволяє уникнути необхідності вказувати всі стовпці 
з запиту в розділі `GROUP BY`.
Використання `OVER` і `PARTITION BY` дозволяє більш гнучко визначити,
як розподілити дані для обчислень, і отримати більш зрозумілий і компактний код.

В більшості випадків використання віконних функцій є більш ефективним та швидким способом 
порівняно з використанням `GROUP BY`, особливо при роботі з великими наборами даних.
Віконні функції дозволяють виконувати обчислення на підмножині рядків без потреби 
створювати окремі групи.
Це може призвести до кращої продуктивності, оскільки система управління базами даних
може оптимізувати розрахунки в межах віконного фрейму.

При використанні підходу `GROUP BY` база даних має створювати відмінні групи на основі 
стовпців групування, що може включати додаткові кроки сортування та агрегації.
Цей процес може стати більш витратним з точки зору ресурсів зі збільшенням обсягу даних.



### Агрегатні віконні функції `ROW_NUMBER`, `RANK`, `DENSE_RANK`

**Агрегатні віконні функції** SQL дозволяють агрегувати дані всередині певного вікна
або діапазону рядків, визначеного за допомогою віконного виразу.
Віконні функції можуть бути корисними для аналізу даних, таких як ранжування,
обчислення відмінностей між значеннями, знаходження першого або останнього значення 
всередині вікна та інших аналітичних операцій.

Віконні функції

- `ROW_NUMBER`
- `RANK`
- `DENSE_RANK`

`ROW_NUMBER()`
Повертає порядковий номер рядка всередині вікна. Нумерація починається з першої.

Наступний запит обирає ідентифікатор, ім'я та оцінку студентів з таблиці "students"
та призначає їм порядкові номери всередині вікна, відсортованого за зменшенням оцінок.

```sql
SELECT id, name, score, ROW_NUMBER() OVER (ORDER BY score DESC) AS row_num
FROM students
```

`RANK()`
Повертає ранг (порядковий номер) рядка всередині вікна, пропускаючи дублікати, 
та пропускаючи наступний порядковий номер у разі, якщо кілька рядків
мають одне й те саме значення.

Наступний запит обирає ідентифікатор, ім'я та оцінку студентів з таблиці "students"
і призначає їм ранги всередині вікна, відсортованого за спаданням оцінок,
пропускаючи дублікати оцінок.

```sql
SELECT id, name, score, RANK() OVER (ORDER BY score DESC) AS rank_num
FROM students
```

`DENSE_RANK()`
Повертає щільний ранг (порядковий номер) рядка всередині вікна, не пропускаючи дублікати, 
і не пропускаючи наступний порядковий номер у випадку, якщо кілька рядків мають
те саме значення.

Наступний запит обирає ідентифікатор, ім'я та оцінку студентів з таблиці "students"
та призначає їм щільні ранги всередині вікна, відсортованого за спаданням оцінок,
без пропуску дублікатів оцінок.

```sql
sqlCopy code
SELECT id, name, score, DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank_num
FROM students
```



### SQL ін'єкції - що таке, як захиститись?

**SQL-ін'єкції** — це один із найпоширеніших типів атак на базу даних, коли зловмисник 
вставляє шкідливий SQL-код у запит, що виконується сервером.
Це може призвести до витоку даних, модифікації бази або навіть повного видалення даних.

Основна причина SQL-ін'єкцій — неправильна обробка даних, які надходять від користувача,
та їх безпосереднє використання у SQL-запитах.
Наслідки атак можуть бути дуже серйозними: викрадення конфіденційної інформації, 
несанкціоновані зміни даних, створення облікових записів з підвищеними привілеями тощо.

Приклад небезпечного коду

```python
user_input = "1; DROP TABLE users;"  # Malicious input
query = f"SELECT * FROM users WHERE id = {user_input};"
cursor.execute(query)  # This executes malicious SQL code
```

Методи захисту:

- Використання параметризованих запитів або підготовлених виразів (prepared statements). Це дозволяє відокремити дані від SQL-логіки.

```python
user_input = "1; DROP TABLE users;"  # This will now be treated as plain data
query = "SELECT * FROM users WHERE id = %s;"
cursor.execute(query, (user_input,))  # Using parameterized query to prevent SQL injection
```

- Застосування ORM (наприклад, Django ORM або SQLAlchemy), яке автоматично обробляє вхідні дані.

```python
user = User.objects.filter(id=user_input).first()  # ORM escapes input automatically
```

- Валідація та фільтрація вхідних даних. Обмеження типів даних (наприклад, числові значення).
- Мінімізація прав користувачів бази даних. Акаунт, через який додаток підключається до бази, повинен мати лише необхідні привілеї.
- Використання веб-фаєрволів (WAF) для моніторингу та блокування шкідливих запитів.
- Логування та моніторинг запитів допоможуть вчасно виявити підозрілу активність.


### View, Materialised View [❄️1/100]

У SQL **View** (представлення) та **Materialized View** (матеріалізоване представлення) — 
це способи роботи з даними, що полегшують доступ до складних запитів
або великих наборів даних.
Вони мають схожість, але виконують різні завдання.

Ключові відмінності

- View завжди показує актуальні дані, тоді як Materialized View може відображати застарілі дані до моменту рефрешу.
- View не займає додаткового місця в пам’яті, а Materialized View зберігає результати фізично.
- Materialized View краще підходить для великих обсягів даних, якщо запит часто повторюється і важливіша швидкість, ніж актуальність.

**View**

- View — це віртуальна таблиця, яка базується на результаті SQL-запиту. Дані у View завжди актуальні, оскільки витягуються з базової таблиці під час виконання запиту.
- View не зберігає дані фізично, а лише визначення запиту.
- Використовується для спрощення складних запитів, підвищення безпеки (обмеження доступу до певних колонок або рядків) та створення абстракцій над базою даних.
- Оновлення даних через View можливе, якщо виконуються певні умови (наприклад, відсутність агрегатів у запиті).

```sql
CREATE VIEW active_users AS
SELECT id, name, email
FROM users
WHERE is_active = true;

-- Query the view
SELECT * FROM active_users;
```

**Materialized View**

- Materialized View — це таблиця, яка зберігає результат SQL-запиту фізично. Дані в Materialized View не оновлюються автоматично; потрібно виконувати рефреш для їх оновлення.
- Використовується для покращення продуктивності, особливо для часто виконуваних складних запитів або агрегатів на великих наборах даних.
- Рефреш може бути виконаний вручну або автоматично залежно від налаштувань.
- Materialized View може мати індекси для прискорення запитів.

```sql
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT product_id, SUM(sales) AS total_sales
FROM sales
GROUP BY product_id;

REFRESH MATERIALIZED VIEW monthly_sales; -- Refresh Materialized View
SELECT * FROM monthly_sales; -- Query Materialized View
```



### `EXPLAIN` та `EXPLAIN ANALYZE` [❄️2/100]

`EXPLAIN` - це команда, яка надає інформацію про план виконання запиту.
Вона показує, як база даних планує виконати запит, включаючи індекси,
порядок виконання операцій та очікувані витрати, що допомагає в оптимізації запитів.
Сам запит у разі не виконується.

`EXPLAIN ANALYZE` виконує пояснюваний вираз, навіть якщо це insert, update або delete.

Приклад використання команди `EXPLAIN`

```sql
EXPLAIN SELECT * FROM employees WHERE age > 30;

Seq Scan on employees (cost=0.00..12.50 rows=3 width=100)
 Filter: (age > 30)
```

База даних буде виконувати послідовне сканування (Seq Scan) таблиці employees
і застосовувати фільтр age > 30.
Поле cost показує передбачувані витрати виконання операції термінах часу і ресурсів.

`EXPLAIN` допомагає виявити потенційні проблеми у запитах, такі як відсутність індексного
сканування, що може вказувати на необхідність додавання індексів
або переписування запитів для покращення продуктивності.

Використання `EXPLAIN` особливо корисне при роботі зі складними запитами
або великими обсягами даних, оскільки дозволяє заздалегідь зрозуміти,
як виконуватиметься запит, і які оптимізації можуть знадобитися.



### PostgreSQL Row-Level Security [❄️1/100]

*Summary*
> Row-Level Security (RLS) - вбудований у Postgres механізм фільтрації рядків
> на рівні ядра БД за політиками (`CREATE POLICY`). На відміну від
> `WHERE`-фільтрації в application-коді, RLS застосовується завжди, незалежно
> від запиту, і дає кінцеву гарантію ізоляції даних (наприклад, між тенантами
> у multi-tenant SaaS).

**Призначення**

RLS вирішує дві задачі: ізоляцію даних між тенантами у shared-schema
multi-tenant архітектурі (див. [`architecture/architecture_patterns.md`](../architecture/architecture_patterns.md)
розділ "Multi-tenancy: моделі ізоляції даних") і застосовну ізоляцію за ролями
(одна таблиця `documents`, користувач бачить лише свої документи).

Доступна з Postgres 9.5 (2016). Працює для `SELECT`, `INSERT`, `UPDATE`,
`DELETE`; не застосовується до `TRUNCATE` і `REFERENCES` (див.
[`TRUNCATE` vs `DELETE`](#truncate-vs-delete)).

**Принцип роботи**

RLS складається з трьох елементів:

1. **Увімкнення на таблиці** через `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`.
   Без цього прапорця policy не застосовується. Окрема директива `FORCE ROW
   LEVEL SECURITY` поширює policy і на власника таблиці (без неї власник їх
   обходить).
2. **Політики** - правила фільтрації `CREATE POLICY ... USING (...)
   WITH CHECK (...)`. `USING` обмежує, які рядки видимі для `SELECT`/`UPDATE`/
   `DELETE`; `WITH CHECK` валідує, які рядки можна записати через `INSERT`/
   `UPDATE`. Якщо `WITH CHECK` опущений - використовується вираз з `USING`.
3. **Контекст** - значення, на яке посилається policy. Стандартний спосіб
   передачі контексту - сесійні налаштування через `SET LOCAL` /
   `set_config()`, які зчитуються з policy через `current_setting()`.

**Реалізація**

Tenant-isolation policy на таблиці `orders`:

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_orders ON orders
FOR ALL
USING (
    tenant_id = current_setting('app.tenant_id', true)
)
WITH CHECK (
    tenant_id = current_setting('app.tenant_id', true)
);
```

Другий аргумент `current_setting('app.tenant_id', true)` - `missing_ok`: повертає
`NULL` замість помилки, якщо GUC не виставлено. Без `true` policy впаде з
`ERROR: unrecognized configuration parameter` для будь-якого запиту без
налаштованого контексту.

Передача `tenant_id` у контекст транзакції через `set_config` з local-scope
(аналог `SET LOCAL`):

```sql
BEGIN;
SELECT set_config('app.tenant_id', '42', true);  -- true = local to transaction
SELECT * FROM orders;  -- returns only tenant_id = '42' rows
COMMIT;  -- app.tenant_id reset
```

Подробиці про scope і pool-poisoning - у розділі
[`SET LOCAL` vs `SET`](#set-local-vs-set-contamination-pool).

**Перевірка контексту**

```sql
SELECT current_setting('app.tenant_id', true);
```

Корисно при дебазі - запит повертає менше рядків, ніж очікувалося, перевіряти
саме цей GUC.

**Cross-tenant запити: роль з `BYPASSRLS`**

Системні задачі (аналітика, міграції, адмін-операції) потребують доступу через
тенанти. Postgres підтримує атрибут ролі `BYPASSRLS`:

```sql
CREATE ROLE analytics_readonly WITH BYPASSRLS LOGIN PASSWORD '...';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analytics_readonly;
-- Cover tables created later (existing GRANT applies only to current tables):
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO analytics_readonly;
```

Запити цієї ролі ігнорують усі policy. Усі звернення через таку роль логуються
в окремий audit log на рівні застосунку - якщо доступ використано неправомірно,
це фіксується в логах.

**Перформанс**

RLS додає предикат `USING` до плану запиту. Без індексу на `tenant_id` Postgres
змушений сканувати таблицю і фільтрувати. З composite-індексом
`(tenant_id, <колонка з основним фільтром>)` оверхед стає незначним - 5-10% за
бенчмарками практиків ([Crunchy Data: Row-Level Security in
PostgreSQL](https://www.crunchydata.com/blog/row-level-security-for-tenants-in-postgres)).

Обов'язкове правило: індекс на `tenant_id` (або на `(tenant_id, ...)`) на кожній
таблиці з policy. Без нього семантика збережена, але перформанс деградує.

**Обмеження**

- `TRUNCATE` і `REFERENCES` не підпадають під RLS (див. розділ "`TRUNCATE` vs
  `DELETE`"). `TRUNCATE` очищує таблицю повністю - у multi-tenant контексті це
  означає видалення даних усіх тенантів, тому права на `TRUNCATE` мають бути
  обмежені окремою policy на рівні `GRANT`.
- Власник таблиці і суперюзер обходять policy за замовчуванням. `FORCE ROW
  LEVEL SECURITY` поширює policy і на власника, але суперюзер обходить завжди.
- Помилка у policy (наприклад, `USING (true)` через недогляд) перетворює RLS
  на no-op. Інтеграційні тести мають перевіряти ізоляцію явно (крос-тенант
  запит повертає 0 рядків).

*Links*

- [Postgres docs: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html) - повний опис семантики
- [Postgres docs: CREATE POLICY](https://www.postgresql.org/docs/current/sql-createpolicy.html) - синтаксис і приклади
- [Postgres docs: CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html) - атрибут `BYPASSRLS`
- [Postgres 9.5 release notes](https://www.postgresql.org/docs/release/9.5.0/) - перший реліз з RLS (січень 2016)



### `SET LOCAL` vs `SET`: contamination з'єднання у pool [❄️1/100]

*Summary*
> `SET LOCAL` встановлює GUC лише до кінця поточної транзакції; `SET` (без
> `LOCAL`) - до кінця сесії. У застосунках з connection pool використання
> `SET` без явного скидання призводить до того, що наступний клієнт отримує
> з'єднання з налаштуваннями попереднього - cross-request state leak.

**Принцип роботи**

Postgres GUC-параметри (включно з користувацькими `app.*`) мають scope:

- **Session-level (`SET name = value` або `set_config(name, value, false)`)** -
  значення зберігається до кінця сесії (= до `DISCARD ALL` або закриття
  з'єднання).
- **Transaction-level (`SET LOCAL name = value` або `set_config(name, value,
  true)`)** - значення скидається на `COMMIT` або `ROLLBACK`. `SET LOCAL` поза
  транзакцією видає `WARNING: SET LOCAL can only be used in transaction blocks`
  і не діє.

Команда `set_config(name, value, is_local)` - програмний еквівалент `SET` /
`SET LOCAL`, повертає встановлене значення; зручна, бо параметризується через
`$1`/`$2` у звичайному `prepared statement`.

**Проблема pool contamination**

Connection pool (pgbouncer у режимі `transaction` або застосунковий
`SQLAlchemy QueuePool`, `asyncpg.Pool`) повертає з'єднання між запитами без
закриття. Якщо запит виконав `SET app.tenant_id = '42'` без `LOCAL`:

1. Транзакція завершується, з'єднання повертається у pool.
2. Наступний запит від іншого тенанта чекає з'єднання з того ж pool, отримує
   це саме з'єднання з налаштованим `app.tenant_id = '42'`.
3. RLS policy фільтрує дані як для `tenant_id = '42'` - cross-tenant data leak.

Та сама проблема для будь-яких сесійних GUC: `search_path`, `role`,
`statement_timeout`. Аналогічно небезпечні сесійні об'єкти - тимчасові таблиці,
prepared statements: вони переживають закінчення транзакції і залишаються на
з'єднанні до кінця сесії.

**Безпечні патерни**

Варіант 1 - встановлення всередині транзакції з `local=true`:

```python
async with pool.acquire() as conn:
    async with conn.transaction():
        await conn.execute(
            "SELECT set_config('app.tenant_id', $1, true)",
            tenant_id,
        )
        result = await conn.fetch("SELECT * FROM orders")
        # COMMIT resets app.tenant_id automatically
```

Варіант 2 - встановлення поза транзакцією з `local=false`, явний `RESET` у
`finally`:

```python
async with pool.acquire() as conn:
    try:
        await conn.execute(
            "SELECT set_config('app.tenant_id', $1, false)",
            tenant_id,
        )
        result = await conn.fetch("SELECT * FROM orders")
    finally:
        await conn.execute("RESET app.tenant_id")
```

Варіант 1 безпечніший: Postgres гарантує скидання навіть при незловленому
винятку всередині транзакції. Варіант 2 коректний лише за умови, що `finally`
точно виконається; будь-який crash процесу між встановленням і `RESET` залишає
з'єднання забрудненим.

**Перевірка**

Інтеграційний тест pool contamination:

```python
async def test_tenant_context_not_leaked_across_acquires(pool):
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                "SELECT set_config('app.tenant_id', 'A', true)"
            )
    # Acquire again - either same connection or another from pool
    async with pool.acquire() as conn:
        value = await conn.fetchval(
            "SELECT current_setting('app.tenant_id', true)"
        )
        assert value in (None, "")  # no leak from previous transaction
```

*Links*

- [Postgres docs: SET](https://www.postgresql.org/docs/current/sql-set.html) - семантика session vs transaction scope
- [Postgres docs: set_config()](https://www.postgresql.org/docs/current/functions-admin.html#FUNCTIONS-ADMIN-SET) - програмна форма з `is_local`
- [pgbouncer pooling modes](https://www.pgbouncer.org/features.html) - несумісність `transaction` pooling із сесійними GUC
