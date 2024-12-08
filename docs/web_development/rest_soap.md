## REST & SOAP

### Що таке REST?

*Summary*
> **REST (Representational State Transfer, "передача стану представлення")** - це архітектурний стиль для розподілених систем. Іншими словами - це набір правил того, як програмісту організувати написання коду серверної програми, щоб усі системи легко обмінювалися даними і програму можна було масштабувати. Під REST часто розуміють так звані HTTP REST API. Зазвичай це веб-додаток з набором URL-адрес - кінцевих точок. URL-адреси приймають та повертають дані у форматі JSON. REST є альтернативою RPC.

REST не накладає правил на реалізацію на низькому рівні, а лише надає високорівневі рекомендації та залишає вам волю для власної реалізації.

Основні поняття REST

- Ресурс - будь-який об’єкт або дані, з якими взаємодіє клієнт через сервер. Ресурс може бути будь-чим: користувач, файл, замовлення, продукт тощо. У REST API ресурси ідентифікуються через унікальні URL-адреси (Uniform Resource Locator), тобто посилання.
- Посилання - URL (уніфікований локатор ресурсу) є унікальним ідентифікатором ресурсу в REST API. Він слугує як шлях до конкретного ресурсу або його колекції. URL має бути інтуїтивно зрозумілим і відображати структуру та ієрархію ресурсів.
	- `/users` — колекція всіх користувачів
	- `/users/123` — конкретний користувач із ідентифікатором 123
- Версіонування - можливість підтримки кількох версій сервісу для різних клієнтів або застосунків. Можливі варіанти версіонування
	- версія у URL - `GET /v1/users`, `GET /v2/users`
	- версія у заголовках - `Accept: application/vnd.myapi.v1+json`
	- версія у параметрах запиту - `GET /users?version=1`
- HATEOAS (Hypermedia as the Engine of Application State) — використання гіпермедіа для управління станом застосунку. Гіпермедіа тут означає використання гіперпосилань у відповідях API для надання клієнту можливості переходити між різними станами або ресурсами системи.

REST API будується на кількох ключових принципах. Якщо ці принципи дотримані, інтерфейс сервісу можу називатися RESTful.

Основні принципи REST

- Stateless -Відсутність стану - кожен HTTP-запит відбувається в повній ізоляції
- Client-Server - Клієнт-сервер  - автономність клієнта і сервера та їх взаємодія
- Uniform Interface - Однорідний інтерфейс - підтримка однорідного інтерфейсу
- Cacheable - Кешування - підтримка кешування
- Layered System - Шари абстракції - поділ на шари
- Code on Demand - Код на запит - необов’язкове обмеження, що дозволяє завантажувати код клієнта


Операції визначаються HTTP-методами, тому не варто використовувати дієслова в URL. Метод запиту HTTP визначає тип операції

- `GET` - отримати об'єкт або список об'єктів
- `POST` - створити об'єкт
- `PUT` - оновити існуючий об'єкт
- `PATCH` - частково оновити існуючий об'єкт
- `DELETE` - видалити об'єкт
- `HEAD` - отримати метадані об'єкта

REST-архітектура активно використовує можливості протоколу HTTP, щоб уникнути власних рішень. Наприклад, параметри кешування передаються стандартними заголовками `Cache`, `If-Modified-Since`, `ETag`. Аутентифікація здійснюється за допомогою заголовка `Authentication`.

*Links*

- [Повний огляд REST: нюанси, поради, приклади](https://dou.ua/forums/topic/50364/)


### Що таке RESTful API?

**RESTful** -API, побудоване з дотриманням REST (тобто відповідає принципам REST).

На відміну від веб-сервісів на основі SOAP, для RESTful веб-API не існує "офіційного" стандарту. Оскільки REST - це архітектурний стиль, тоді як SOAP - це протокол.

REST визначає 6 архітектурних принципів, виконання яких дозволить створити RESTful API

- Uniform Interface - Однорідний інтерфейс
- Client-Server - Клієнт-сервер
- Stateless -Відсутність стану
- Cacheable - Кешування
- Layered System - Шари абстракції 
- Code on Demand - Код на запит

**Однорідний інтерфейс**
Всі компоненти в архітектурі REST підтримують однорідний інтерфейс. Це зменшує звʼязність між компонентами і сервісами які вони надають і дозволяє просто змінювати компоненти при потребі. Ресурс в системі повинен мати лише один логічний URI, який надає спосіб отримання пов'язаних або додаткових даних. Краще асоціювати (синонімізувати) ресурс з веб-сторінкою.

Усі ресурси доступні за допомогою стандартних методів (GET, POST, PUT, DELETE), що дозволяє стандартизувати взаємодію.

Будь-який ресурс не повинен бути надто великим і містити все у своєму представленні. Коли це доцільно, ресурс повинен містити посилання (HATEOAS: Hypermedia as the Engine of Application State), що вказують на відносні URI для отримання пов'язаної інформації.

Крім того, представлення ресурсів в системі повинні дотримуватися певних рекомендацій, таких як конвенції про імена, формати посилань або формат даних (xml або / і json).

Коли розробник знайомиться з одним ендпоінтом з API, він може дотримуватися аналогічного підходу до інших ендпоінтів API.

**Клієнт-сервер**
Вимагається розділення відповідальності між компонентами, які займаються зберіганням та оновленням даних (сервером), і тими компонентами, які займаються відображенням даних на інтерфейсі користувача та реагування на дії з цим інтерфейсом (клієнтом). По суті, це означає, що клієнтський додаток і серверний додаток повинні мати можливість розвиватись окремо одне від одного без будь-якої залежності. Клієнт повинен знати лише URI ресурсу і нічого більше.

Таке розділення дозволяє компонентам еволюціонувати незалежно. Це зручно тим що можна розділити роботу фронтендерів та бекендерів, та працювати незалежними командами і деплоїти окремо.

**Відсутність стану**
Взаємодії між сервером та клієнтом не мають стану, тобто кожен запит містить всю необхідну інформацію для його обробки, і не покладається на те, що сервер знає щось з попереднього запиту.

Відсутність стану означає, що сервер не знає про стан клієнта і не повинен запамʼятовувати послідовність здійснених до нього запитів, тому що кожен з них є незалежним. Як приклад, у випадку, коли в нас декілька інстансів нас не хвилює, що запити можуть оброблятися різними серверами, все одно запит містить всю необхідну інформацію, так само буде у випадку, якщо сервер впаде.

Клієнтський контекст не повинен зберігатися на сервері між запитами. Клієнт відповідає за управління станом додатку.

**Кешування**
Системи повинні підтримувати кешування. Дані, які передаються сервером, повинні містити інформацію про те, чи можна їх кешувати, і якщо можна, то як довго. Як приклад можна повертати кукі, вказуючи доки вони мають існувати. Для цього можна використовувати заголовки Cache-Control та Set-Cookie.

**Шари абстракції**

REST містить поділ на шари абстракції. Кожен компонент потрапляє в якийсь шар, і спілкується лише з компонентами в шарі під ним або в шарі над ним. Обмеження знання системи одним шаром зменшує складність компонентів. Приклад: фронтенд спілкується тільки з бекендом, а бекенд як з фронтендом так і з бд, а база в свою чергу взаємодіє тільки з бекендом.

**Код на запит**
Необов'язковий принцип. Клієнти повинні дозволяти розширювати свою функціональність дозволяючи завантаження додаткового коду в формі аплетів чи скриптів. Це спрощує клієнти, дозволяючи не реалізовувати всі необхідні функції попередньо.

*Links*

- [Повний огляд REST: нюанси, поради, приклади](https://dou.ua/forums/topic/50364/)


### Що таке SOAP

**SOAP (Simple Object Access Protocol - простий протокол доступу до об'єктів)** - це протокол обміну структурованими повідомленнями у розподіленому обчислювальному середовищі. Початково SOAP використовувався переважно для реалізації віддалених викликів процедур (RPC). Зараз протокол використовується для обміну довільними повідомленнями у форматі XML, а не лише для виклику процедур. Офіційна специфікація останньої версії 1.2 протоколу не розшифровує назву SOAP. SOAP є розширенням протоколу XML-RPC.

SOAP може використовуватися з будь-яким протоколом прикладного рівня: SMTP, FTP, HTTP, HTTPS і т. д. Однак його взаємодія з кожним з цих протоколів має свої особливості, які повинні бути визначені окремо. Найчастіше SOAP використовується поверх HTTP.


### В чому різниця між REST та SOAP веб-сервісами

Деякі відмінності

- REST підтримує різні формати: текст, JSON, XML; SOAP - лише XML
- REST працює лише через HTTP(S), тоді як SOAP може працювати з різними протоколами
- REST може працювати з ресурсами. Кожен URL є представленням деякого ресурсу. SOAP працює з операціями, які реалізують деяку бізнес-логіку за допомогою декількох інтерфейсів
- SOAP, заснований на зчитуванні, не може бути поміщений у кеш, тоді як REST в такому випадку може бути закешовано
- SOAP підтримує SSL та WS-security, тоді як REST - лише SSL, SOAP підтримує ACID (Атомарність, Співставленість, Ізоляція, Довіреність). REST підтримує транзакції, але жодне з ACID не сумісне з двофазним комітом.


### Чи можна посилати SOAP повідомлення з вкладенням

Так, це можливо. Можна посилати вкладенням різні формати: PDF, зображення або інші двійкові дані. Повідомлення SOAP працюють разом із розширенням MIME, в якому передбачено multipart/related.


###  Що використовувати - REST або SOAP - для веб-сервісів?

Протиставлення REST та SOAP можна перефразувати як "Простота проти Стандарту". У випадку REST (простота) буде вища швидкість, розширюваність та підтримка багатьох форматів. У випадку з SOAP у буде більше можливостей щодо безпеки (WS-security) та транзакційної безпеки (ACID).
