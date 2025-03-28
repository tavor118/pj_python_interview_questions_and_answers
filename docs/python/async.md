## Async

### Асинхронність

**Асинхронність** - один зі способів виконання кількох завдань відразу. Асинхронний код дозволяє програмі виконувати інші операції під час чекання на відповідь від введення/виведення або мережевого запиту. Асинхронність поліпшує продуктивність, оскільки програма не чекає завершення блокуючих операцій перед виконанням інших завдань.

Вона пропонує вирішувати проблему з допомогою функцій зворотнього виклику (callback). Зустрівши в коді блокуючий запит, інтерпретатор вішає на нього сигнальний маячок і йде далі. Коли запит завершується, маячок подасть сигнал. В цей момент обробник повернеться, отримає результат і викличе колбек.


### Coroutines - Корутини - Співпрограми

**Корутина** - це спеціальний вид асинхронних функцій, яка може призупиняти своє виконання, і продовжити виконання з місця зупинки. На відміну від звичайних функцій, які виконуються наново з початку. Поведінка корутин схожа на поведінку генераторів. Для визначення корутини починаючи з Python 3.5+ використовують ключове слово `async`. Вони використовуються для виконання асинхронних операцій, де важливо чекати на відповідь без блокування основного потоку виконання.

Інше визначення - співпрограма — це термін, який позначає завдання, яке планується циклом подій у програмі замість операційної системи.

У корутині можна використовувати ключове слово `await`, що вказує на асинхронне очікування результату виконання іншої корутини чи асинхронної функції.

Корутини мають багато спільного з потоками, але на відміну від потоків, вони віддають керування лише тоді, коли викликають іншу корутину, і вони не використовують так багато пам'яті.

Корутини є основою для асинхронного програмування в Python і дозволяють виконувати багатозадачні операції без необхідності великої кількості потоків чи процесів.

Корутини можна визначати і створювати у звичайному Python-коді, але запускати їх можна лише в циклі подій.


### Асинхронність в Python

- Починаючи з Python 3.5+ асинхронність реалізована за допомогою асинхронних функцій і ключових слів `async` та `await`. Асинхронні функції визначаються з використанням ключового слова `async` перед визначенням функції. Ключове слово `await` вказує на те, що програма повинна зачекати на результат виконання асинхронної функції перед тим, як продовжити виконання наступних інструкцій.
- Для управління асинхронними задачами у Python використовуються `asyncio` бібліотека та `event loop`, яка дозволяє виконувати асинхронний код в кооперативному багатозадачному середовищі.

*Links*

- [David Beazley - Build Your Own Async - PyCon India, 2019](https://www.youtube.com/watch?v=Y4Gt3Xjd7G8)


### Asyncio

`Asyncio` – модуль асинхронного програмування, який був представлений в Python 3.4. Він призначений для використання співпрограм і `future` для спрощення написання асинхронного коду і робить його майже таким самим читаним, як синхронний код, через відсутності callback-ів.

Asyncio надає цикл подій та ще деякі інші функції. Цикл подій реагує на різні I/O-події та перемикається на завдання, що можуть виконуватися і призупиняє ті, що чекають на I/O. Тобто ми не витрачаємо час на завдання, що ще не готові виконуватися.

`Asyncio` використовує різні конструкції: `event loop`, співпрограми та `future`.
- [event loop](https://docs.python.org/dev/library/asyncio-eventloop.html) управляє і контролює виконання різних завдань. Він реєструє їх і обробляє розподіл потоку управління між ними.
- [Співпрограми](https://docs.python.org/3.5/library/asyncio-task.html#coroutines) – це спеціальні функції, робота яких схожа з роботою генераторів в Python, за допомогою `await` вони повертають потік управління назад в `event loop`. Запуск співпрограми повинен бути запланований в `event loop`. Заплановані співпрограми будуть обгорнуті в Завдання, що є типом `Future`.
- [Future](https://docs.python.org/3.5/library/asyncio-task.html#future) показує результат задачі, яка може або не може бути виконана. Результатом може бути exception. Коли огортаємо співпрограму в `Future` - отримуємо об’єкт `Task`.
- Завдання (`asyncio.Tasks`) огортає корутини, аби їх виконання могло незалежно плануватись циклом подій, коли йому передається управління (зазвичай за допомогою `await`). Створити завдання можна за допомогою `asyncio.create_task()`.

Спрощено схема роботи виглядає наступним чином: У нас є цикл подій (event loop) та асинхронні функції, I/O-операції. Ми передаємо свої функції до циклу подій, щоб він запустив їх. Цикл подій повертає нам об'єкт `Future`. Можна сказати, що це обіцянка, що ми отримаємо якісь дані в майбутньому. Ми зберігаємо його і час від часу перевіряємо чи не має наш `Future` результату виконання. І якщо так, то використовуємо ці дані для подальшої обробки.

Щоб зупиняти та відновлювати завдання asyncio використовує генератори та співпрограми (generators and coroutines). У разі, якщо в черзі очікування є завдання, то контекст буде перемикнуто, в іншому випадку – ні.

Визначення корутини починається з `async`, а її виклик - з `await`.
`asyncio.run(coroutine)` є основною точкою входу для асинхронних програм.

Функції `wait()`, `gather()` і `as_completed()` запускають кілька корутин одночасно. 
Модуль asyncio також надає власні класи `Queue`, `Event`, `Lock` і `Semaphore`.

Asyncio на прикладі

```python
import asyncio
import datetime
import random

async def my_sleep_func():
    await asyncio.sleep(random.randint(0, 5))

async def display_date(num, loop):
    end_time = loop.time() + 50.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) >= end_time:
            break
        await my_sleep_func()

loop = asyncio.get_event_loop()

asyncio.ensure_future(display_date(1, loop))
asyncio.ensure_future(display_date(2, loop))

loop.run_forever()
```

- Асинхронна функція `display_date` приймає число-індентифікатор та цикл подій.
- Функція має безкінечний цикл, що переривається через 50 секунд. Але поки 50 секунд не минуло, вона друкує час і засинає на випадкову кількість секунд. Ключове слово `await` вказує, що під час виконання функції, що стоїть після нього, можна перемкнутися на іншу асинхронну функцію (співпрограму).
- Функції додаються до циклу подій за допомогою функції `ensure_future`.
- Запускається цикл подій.

*Links*

- https://habr.com/ru/companies/wunderfund/articles/716740/


### Що таке `async`/`await`, навіщо вони потрібні і як їх використовувати

Ключове слово `async` використовується перед `def`, щоб показати, що функція є асинхронною (корутиною). Тобто, якщо визначити функцію `async def f(): ...` та викликатие її як `f()` — повернеться корутина. Прийшла на зміну декоратору `@asyncio.coroutine` в Python 3.5+.

Ключове слово `await` вказує, що очікується завершення співпрограми. `await` може бути використане лише в співпрограмі. awaitable — все, що підтримує `await`, тобто корутини, `asyncio.Futures`, `asyncio.Tasks`, об'єкти з методом `__await__`. `await` прийшов на зміну `yield from` в Python 3.5+.

```python
import asyncio
import aiohttp

urls = ['https://www.google.com', 'https://www.python.org']

async def call_url(session, url):
    print(f'Run {url}')
    async with session.get(url) as response:
        data = await response.text()
        print(f'{url}: {len(data)} bytes')
        return data

async def main(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [call_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        return results

asyncio.run(main(urls))  # Run the event loop

```

Програма містить асинхронний метод. Під час виконання він повертає співпрограму, яка потім перебуває у стані очікування.

`async/await` необхідні для того, щоб не блокувати виконання потоку під час очікування асинхронної події. Конструкція `async/await` фактично перетворює функцію на корутину (співпрограму): вона призупиняє своє виконання під час `await`, очікує асинхронної події та продовжує роботу.


### Що таке `event loop` (цикл подій) в asyncio і як він працює?

Цикл подій є ядром кожної асинхронної програми. Цикли подій запускають асинхронні завдання та зворотні виклики, виконують мережеві операції вводу-виводу та запускають підпроцеси.

Event Loop - це механізм, який дозволяє координувати виконання асинхронних операцій у Python. Він дозволяє програмі взаємодіяти з багатьма завданнями, такими як ввід-вивід, мережеві запити, без блокування основного потоку виконання.

Event Loop - це як певний безкінечний цикл, який дозволяє розпізнати, чи настала певне подія операційної системи (наприклад, запис даних до сокету).

Event Loop працює на принципі опитування: він постійно перевіряє список подій та завдань, які очікують виконання, і обробляє їх послідовно. Коли подія стає доступною для обробки (наприклад, завершення мережевого запиту), Event Loop викликає відповідну функцію-зворотний виклик, яку визначили, для обробки результату.

Під капотом, Event Loop в `asyncio` працює на подібних принципах, як в традиційних механізмах вводу-виводу як `Select`, `Poll` та `Epoll`. Він встановлює "наглядачі" на різні асинхронні операції та очікує їхнього готовності.

З допомогою `Select` формується список файлових дескрипторів, за якими планується спостерігати. У клієнтському коді доведеться перевіряти всі передані дескриптори на наявність подій (і їх кількість обмежена 1024), що робить його повільним та незручним.

У випадку `Poll` та `Epoll`, Event Loop використовує більш ефективні механізми опитування, дозволяючи ефективно взаємодіяти з більшим числом подій.

*Links*

- [select / poll / epoll: практическая разница](https://habr.com/ru/companies/infopulse/articles/415259/)


### Чому асинхронний код з `await` може виконуватись синхронно?

`await` у коді НЕ запускає його конкурентно.
Все, що робить `await` - віддає управління в event loop, щоб той мав можливість переключитися на сусідню корутину і, якщо там очікування закінчилося, продовжити виконання коду цієї сусідньої корутини.

﻿﻿Для конкурентного («одночасного») запуску корутин (функцій, визначених `async def`) їх треба запускати не просто з `await`, а ﻿﻿потрібно створювати завдання (`asyncio.Task`) — безпосередньо з `asyncio.create_task(coro())` або за допомогою інших АРІ asyncio.

```python
import asyncio  
import time  
  
async def delay(seconds: int) -> None:  
    print (f"delay ({seconds=}) started", flush=True)  
    await asyncio.sleep (seconds)  
    print (f"delay ({seconds=}) finished", flush=True)  
  
async def main():  
    start_time = time.perf_counter()  
    await delay(1)  
    await delay(3)  
    await delay(2)  
    print(f"elapsed time: {time.perf_counter() - start_time:.1f} seconds")  
  
asyncio.run(main())  # elapsed time: 6.0 seconds
```



### Як запустити код конкурентно в asyncio?

Існує 5 основних способів запустити код асинхронно:
- створення завдань з `asyncio.create_task(...)` і потім їх очікування з `await`
- `asyncio.gather (...)`
-  `asyncio.TaskGroup`
-  `asyncio.as_completed(...)`
-  `asyncio.wait(...)`



### Для чого використовується `asyncio.create_task(...)`?

`asyncio.create_task(...)` використовується для запуску корутини як незалежного асинхронного завдання (task) у фоновому режимі. Це дозволяє корутині виконуватися паралельно з іншими частинами програми, не блокуючи поточний потік виконання. 

Завдання не починає виконуватись відразу (тільки планується її виконання), а чекає, поки зустрінеться перший `await`, коли ми віддаємо управління з поточної асинхронної функції в event loop. Тільки тоді він отримає можливість запустити створені завдання. 

Важливий моментом є те, що ми можемо запустити завдання, але не дочекатись його виконання. 
Щоб завдання точно повністю відпрацювало, треба явно чекати закінчення завдання з `await task`  - важливо не забувати про це у такому сценарії запуску конкурентності.

`Exception`, що виникли у завданнях та необроблені в них не скасовують роботу інших завдань після виникнення виключення.
Обробляти винятки потрібно на рядку `await task`.

Недоліки `create_task`
- деяка багатослівність - спочатку створити таски, потім почекати на їх виконання з `await`
- немає можливості обробляти результати завдань у міру їх виконання — у циклі з `await` порядок не за швидкістю виконання, а по порядку додавання завдань до списку

```python
import asyncio  
import time  
  
async def delay(seconds: int) -> None:  
    print (f"delay ({seconds=}) started", flush=True)  
    await asyncio.sleep (seconds)  
    print (f"delay ({seconds=}) finished", flush=True)  
  
async def main():  
    start_time = time.perf_counter()  
    first_task = asyncio.create_task(delay(1))  
    second_task = asyncio.create_task(delay(3))  
    third_task = asyncio.create_task(delay(2))  
    print("before first await", flush=True)  
    await first_task  
    print("after first_task", flush=True)  
    await second_task  
    print("after second_task", flush=True)  
    await third_task  
    print(f"elapsed time: {time.perf_counter() - start_time:.1f} seconds")  
  
asyncio.run(main())  # elapsed time: 3.0 seconds
```

`Task` можна відміняти методом `cancel()`.

```python
import asyncio
import time

async def delay(seconds: int) -> None:
    print(f"delay({seconds=}) started", flush=True)
    await asyncio.sleep(seconds)
    print(f"delay({seconds=}) finished", flush=True)

async def main():
    start_time = time.perf_counter()
    tasks = (
        asyncio.create_task(delay(3), name="delay 3 sec"),
        asyncio.create_task(delay(1), name="delay 1 sec"),
        asyncio.create_task(delay(20000), name="delay 20000 sec")
    )
    
    for task in tasks:
        if task.get_name() == "delay 20000 sec":
            task.cancel()
        else:
            await task
    
    print(f"elapsed time: {time.perf_counter() - start_time:.1f} seconds")

if __name__ == "__main__":
    asyncio.run(main())  # elapsed time: 3.0 seconds, # ! not 20000
```



### Для чого використовується `asyncio.TaskGroup`?

`asyncio.TaskGroup` використовується для управління групою асинхронних задач, що виконуються одночасно. Ця структура дозволяє легко створювати, запускати і відстежувати кілька завдань, підтримуючи їх виконання в межах одного контексту, забезпечуючи автоматичне завершення всіх завдань, навіть якщо одне з них викликає помилку. Це новий механізм, введений у Python 3.11.

Всі задачі, що створені в межах одного `TaskGroup`, виконуються паралельно. Завдяки підтримці синтаксису `async with`, після виходу з контексту групи можна бути впевненим, що всі задачі або завершились, або були скасовані.

Якщо одна з задач у групі викидає необроблений виняток, інші задачі також зупиняють роботу - у них викликається `asyncio.CancelledError`.

`TaskGroup` зручно використовувати, коли треба виконати конкурентно кілька завдань, але якщо хоча б одне завершиться з винятком - зупинити всі інші

Це не повний аналог `gather` — оскільки `gather` вміє виконати всі завдання і повернути всі винятки, які виникли.

```python
import asyncio

async def task(name, delay):
    await asyncio.sleep(delay)
    print(f'Task {name} completed after {delay} seconds')

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(task('A', 1))
        tg.create_task(task('B', 2))
        tg.create_task(task('C', 3))
        print('All tasks created')

    print('All tasks completed')

asyncio.run(main())
```

В цьому прикладі три задачі (A, B і C) запускаються одночасно, і TaskGroup забезпечує, що всі вони завершаться перед тим, як main() завершиться. Прекрасний спосіб організації асинхронного коду, правда ж? Щось ще в цьому напрямку?



### Для чого використовується `gather()`?

**`gather()`** - функція, яка призначена для виконання асинхронних задач паралельно та збору їх результатів. Вона приймає кілька кілька асинхронних функцій, огортає їх в завдання, якщо це потрібно, та очікує завершення їх виконання, збираючи результати від кожної задачі. Ми отримуємо результат всіх awaitables у тому ж порядку, в якому вони були передані.

Якщо виникає виняток, `gather()` миттєво поверне його на рядку `await gather`, однак на інші завдання це не вплине, вони продовжують виконання, але важко дістати результати. Якщо ж скасувати `gather()`, всі його awaitables, які ще не завершили своє виконання, також будуть скасовані.

На практиці краще використовувати `gather(*coros, return_exceptions=True)`. При такому підході винятки повертаються з `gather` у результатах - всі результати в порядку `*coros`.

Недоліки
- немає можливості обробляти результати завдань по мірі їх виконання
- документація позиціонує `TaskGroup` як сучасний спосіб створювати завдання та чекати їх повного виконання - хоча `TaskGroup` інакше працює з винятками

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1 done"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 done"

async def main():
    results = await asyncio.gather(task1(), task2())
    print(results)

asyncio.run(main())  # ['Task 1 done', 'Task 2 done']
```



### Для чого використовується `wait_for()`, `as_completed()`, `wait()` ?

**`wait_for()`** - приймає два аргументи: один awaitable та затримку в секундах. Дозволяє очікувати завершення конкретної асинхронної задачі з обмеженням у часі. Якщо awaitable — це корутина, вона автоматично огортається в завдання. Якщо задача не завершиться протягом вказаного таймауту, генерується виняток `asyncio.TimeoutError`.

```python
import asyncio

async def my_task():
    await asyncio.sleep(2)
    return "Task done"

async def main():
    try:
        result = await asyncio.wait_for(my_task(), timeout=1)
        print(result)
    except asyncio.TimeoutError:
        print("Task did not complete within the specified time.")

asyncio.run(main())  # Task did not complete within the specified time.
```

В поєднанні з `gather()` - щойно закінчується затримка, внутрішнє завдання скасовується. Всі завдання в `gather()` також скасовуються

```python
try:
    result_f, result_g = await asyncio.wait_for(
        asyncio.gather(f(), g()),
        timeout=5.0
    )
except asyncio.TimeoutError:
    print("oops took longer than 5s!")
```

**`as_completed()`** - приймає ітерований об'єкт (наприклад, список, кортеж, сет), та повертає асинхронний ітератор, який генерує `asyncio.Futures` в порядку завершення виконання корутин.

Дає можливість обробляти результати корутин у міру їх виконання, а також дозволяє обробити всі завдання, які можуть бути оброблені, навіть після винятку в одному із завдань.

```python
import asyncio

async def task1():
    await asyncio.sleep(2)
    return "Task 1 done"

async def task2():
    await asyncio.sleep(1)
    return "Task 2 done"

async def main():
    tasks = [task1(), task2()]
    for task in asyncio.as_completed(tasks):
        result = await task
        print(result)

asyncio.run(main())  # Task 2 done, Task 1 done
```

**`wait()`** - функція, яка очікує завершення асинхронних задач та повертає кортеж, який містить два сети: задач, які завершили виконання, і ті, що ще в очікуванні. Тобто вона не повертає результати - відповідальність за обробку результату лежить на розробнику.

Можна передати затримку (timeout), після якої `wait()` припинить виконання. Але на відміну від `gather()`, з awaitables нічого не відбувається, коли затримка спливає. Функція просто завершує виконання та розподіляє завдання на виконані та ті, що ще в очікуванні.

Можна зробити так, аби `wait()` не чекав виконання всіх awaitables, за допомогою аргументу `return_when`. Автоматично цей аргумент приймає значення `asyncio.ALL_COMPLETED`. Можна змінити значення на `asyncio.FIRST_EXCEPTION`, яке очікує завершення всіх awaitables, якщо лише якесь з них не спровокує виняток. А от з `asyncio.FIRST_COMPLETED` функція завершує виконання одразу, коли якийсь awaitables завершив виконання.

```python
import asyncio  

async def task1():  
    await asyncio.sleep(2)  
    return "Task 1 done"  

async def task2():  
    await asyncio.sleep(1)  
    return "Task 2 done"  

async def main():  
    tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]  
    completed_tasks, pending_tasks = await asyncio.wait(tasks, timeout=1.5)  
    for task in completed_tasks:  
        print(task.result())  

asyncio.run(main())  # Task 2 done
```

*Links*

- [Очікуємо результат асинхронних операцій в Python - DevZone.ua](https://devzone.org.ua/post/ocikujemo-rezultat-asinxronnix-operacii-v-python)


### Для чого використовується `asyncio.to_thread`

`asyncio.to_thread` використовується в Python для виконання блокуючих IO операцій у фоновому потоці під час асинхронного виконання коду. Це дозволяє уникнути блокування основного асинхронного циклу подій під час виконання операцій, які займають багато часу або можуть заблокувати інші завдання.

Виклик `asyncio.to_thread` виконає передану функцію в іншому потоці з використанням `concurrent.futures.ThreadPoolExecutor`. Це дозволяє не блокувати асинхронний цикл подій під час очікування завершення блокуючої операції. `asyncio.to_thread` поверне корутину, яку можна `await` для отримання результату виконання функції.

```python
import asyncio
import time

def blocking_task():
    time.sleep(2)
    return "Completed"

async def main():
    print("Start blocking task")
    result = await asyncio.to_thread(blocking_task)
    print(result)

asyncio.run(main())
```

Якщо потрібно виконати обчислення у процесі (наприклад, для більш інтенсивних завдань), можна використовувати `concurrent.futures.ProcessPoolExecutor` разом із `run_in_executor`.

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor

def heavy_computation():
    result = sum(i * i for i in range(10**6))
    return result

async def main():
    
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool: # Use a ProcessPoolExecutor to avoid blocking the loop
        result = await loop.run_in_executor(pool, heavy_computation)
        print(result)

asyncio.run(main())
```


### Що таке `aiohttp`

`aiohttp` — це асинхронна бібліотека Python для роботи з HTTP, яка забезпечує клієнтську та серверну функціональність. Підходить для побудови асинхронних додатків, таких як скраперів, REST API серверів та інших мережевих сервісів.

Основні характеристики та можливості `aiohttp`
- Використовує асинхронний ввід/вивід на базі `asyncio`, що дозволяє ефективно обробляти одночасні запити.
- Підтримує створення асинхронних HTTP-клієнтів для виконання запитів, отримання відповідей, роботи з JSON, заголовками та файлами.
- Дозволяє створювати легковажні та швидкі асинхронні веб-сервери з налаштованими маршрутами та обробниками.
- Підтримує WebSocket для побудови двонаправленого зв’язку між клієнтом і сервером.
- Працює з сучасним синтаксисом Python (`async/await`), що робить код більш читабельним і простим.
- Забезпечує гнучке управління сесіями, кукі, редиректами та тайм-аутами.
- Підтримує middlewares для обробки запитів/відповідей на різних етапах.

```python
import aiohttp
import asyncio

async def fetch(url):  # Asynchronous function to fetch data from a URL
    async with aiohttp.ClientSession() as session:  # Create a client session
        async with session.get(url) as response:  # Perform GET request
            return await response.text()  # Await and return response text

async def main():  # Main coroutine to execute the fetch function
    url = "https://example.com"
    html = await fetch(url)  # Fetch the URL content
    print(html)  # Print the response

asyncio.run(main())  # Run the main coroutine
```


### Типові помилки при роботі з `asyncio`

- Спроба виконання корутин шляхом їхнього виклику. При такому виклику корутини її тіло не виконається. Замість цього буде створено об'єкт корутини. Потім можна зачекати завершення роботи цього об'єкта в середовищі виконання asyncio, тобто в циклі подій. Запустити цикл подій для виконання корутини можна, скориставшись функцією asyncio.run().

```python
async def custom_coro():
    print('hi there')
custom_coro()
```

- Корутині не дозволяють виконатися в циклі подій. Якщо виконання не було заплановано в циклі подій, виникне помилка під час виконання.

```python
coro = custom_coro()
coro()  # TypeError: 'coroutine' object is not callable
```

- Використання низькорівневого API модуля Asyncio - низькорівневий API призначений  в першу чергу для творців фреймворків і бібліотек.
- Занадто ранній вихід із головної корутини. Якщо завершиться головна корутина , програма також завершиться, навіть якщо інші корутинали ще не завершили своє виконання. Для уникнення цього, можна застосовувати `asyncio.wait()`, щоб дочекатися завершення усіх задач перед завершенням програми.
- Гонки стану (Race Conditions) - виникають, коли дві або більше корутини намагаються одночасно змінювати спільні дані без належного контролю.
- Взаємне блокування (Deadlocks) - ситуації, коли корутини чекають на ресурси, які утримують одна одну, і ні одна не може продовжити виконання.
- Невірне використання примітивів синхронізації. Неправильне використання `asyncio.Lock`, `asyncio.Event` та інших примітивів може призвести до неправильної синхронізації корутин.
- Неправильна обробка винятків - неуспішна обробка винятків у корутинах може призвести до непередбачуваної поведінки програми.


### Скільки потоків та процесів працює під час асинхронного виконання коду

У асинхронному програмуванні Python використовується один процес, який має один основний потік виконання. Цей основний потік взаємодіє з event loop для управління асинхронними задачами, не створюючи додаткових потоків чи процесів. Такий підхід спрощує управління асинхронним кодом і уникнення проблем, пов'язаних зі синхронізацією ресурсів у багатопроцесових чи багатопотокових програмах.

eventloop дуже швидкий, і він більшу частину часу чекає на syscall (системний виклик), тому немає змісту заводити багато потоків з eventloop в кожному. Ningx та node.js також мають один eventloop. Але в будь-якій асинхронній системі окремо є Thread Pool, в який складаються завдання, які виконуються не миттєво.

