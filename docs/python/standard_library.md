## Standard Library

### Які є широко використовувані модулі?

- **os** - надає функції для взаємодії з операційною системою, такі як створення/видалення файлів та робота з директоріями.
- **sys** - надає доступ до функціональності та змінних, пов'язаних з інтерпретатором Python, такі як шляхи пошуку модулів, аргументи командного рядка.
- **math** - містить математичні функції та константи для виконання різних обчислень, таких як тригонометрія, логарифми, степені.
- **random** - допомагає генерувати випадкові числа та випадкові вибірки, такі як вибір випадкового елемента зі списку, генерація випадкових чисел з різними розподілами.
- **datetime** - надає засоби для роботи з датами та часом, такі як створення, форматування, парсинг і арифметика з датами і часом.
- **re** - надає регулярні вирази для виконання операцій з текстом, такі як пошук, заміна, поділ.
- **json** - дозволяє робити роботу з форматом даних JSON (JavaScript Object Notation) для обміну даними між програмами.
- **urllib** - надає функції для виконання операцій з URL-адресами, такі як читання, запис і надсилання HTTP-запитів.
- **csv** - надає функції для роботи з CSV-файлами, такі як читання, запис і маніпуляції даними у форматі CSV.
- **pickle** - для збереження та відновлення об'єктів, забезпечуючи серіалізацію та десеріалізацію даних. 
- **itertools** - містить функції для роботи з ітераторами і створення ітераторів
- **collections** - надає різні корисні класи та типи даних, які допомагають працювати зі спеціалізованими структурами даних.


### Які ви функції знаєте з модуля `itertools`

Модуль itertools містить функції для роботи з ітераторами та створення ітераторів.

- `product` - декартовий добуток ітераторів (для уникнення вкладених циклів for)
- `permutations` - генерація перестановок
- `combinations` - генерація комбінацій
- `combinations_with_replacement` - генерація комбінацій з повторенням
- `chain` - з'єднання кількох ітераторів в один
- `takewhile` - отримання значень послідовності, поки значення функції-предикату для її елементів є істинним
- `dropwhile` - отримання значень послідовності починаючи з елемента, для якого значення функції-предикату перестане бути істинним
- `groupby` - дозволяє групувати елементи об'єкта, що ітерується, за заданим ключем (iterable вже має бути відсортований за тією самою ключовою функцією)
- `tee` - дозволяє створити кілька незалежних ітераторів із одного базового ітератора. Вона використовується, коли потрібно ітерувати по одному джерелу даних кілька разів одночасно. При використанні `itertools.tee` базовий ітератор ітерується лише один раз. Це можливо завдяки механізму буферизації, який зберігає результати для кожного створеного ітератора.

- `product`

```python
for item in itertools.product('AB', '12'):
    print(item)  # Output: ('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')
```

- `permutations`

```python
for item in itertools.permutations('ABC', 2):
    print(item)  # Output: ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')
```

-  `combinations` 

```python
for item in itertools.combinations('ABC', 2):
    print(item)  # Output: ('A', 'B'), ('A', 'C'), ('B', 'C')
```

- `combinations_with_replacement` 

```python
for item in itertools.combinations_with_replacement('ABC', 2):
    print(item)  # Output: ('A', 'A'), ('A', 'B'), ('A', 'C'), ('B', 'B'), ('B', 'C'), ('C', 'C')
```

-  `chain`

```python
for item in itertools.chain('ABC', '123'):
    print(item)  # Output: 'A', 'B', 'C', '1', '2', '3'
```

- `takewhile` 

```python
for item in itertools.takewhile(lambda x: x < 5, [1, 3, 7, 4, 1, 2, 5]):
    print(item)  # Output: 1, 3
```

- `dropwhile`

```python
for item in itertools.dropwhile(lambda x: x < 5, [1, 3, 7, 4, 1, 2, 5]):
    print(item)  # Output: 7, 4, 1, 2, 5
```

- `groupby` 

```python
data = [('A', 1), ('A', 3), ('B', 2), ('B', 4)] # Sorted by the key 
for key, groups in itertools.groupby(data, lambda x: x[0]): 
    print(key, list(groups))  # Output: A [('A', 1), ('A', 3)], B [('B', 2), ('B', 4)]
```

- `tee` 

```python
def process_purchases(purchases):
    min_, max_, avg = itertools.tee(purchases, 3)  
    return min(min_), max(max_), median(avg)
```


### Модуль `collections`

Модуль `collections` у Python надає різні корисні класи та типи даних, які допомагають працювати зі спеціалізованими структурами даних.

- **`Counter`** - Цей клас допомагає підраховувати кількість входжень елементів у послідовності. Особливо корисний для аналізу даних та обробки тексту.

```python
from collections import Counter  
text = "Tururu"  
Counter(text)  # Counter({'u': 3, 'r': 2, 'T': 1})

words = "if there was there was but if there was not there was not".split()
Counter(words)  # Counter({'if': 2, 'there': 4, 'was': 4, 'not': 2, 'but': 1})

counts.most_common(2)  # [('there', 4), ('was', 4)]
```

- **`defaultdict`** - Цей клас створює словники, де значенням за замовчуванням є певний тип даних.

```python
from collections import defaultdict

food_dict = defaultdict(list)

food_dict['fruits'].append('apple')
food_dict['fruits'].append('banana')
food_dict['vegetables'].append('carrot')

print(food_dict)
```

- **`deque`** - Цей клас реалізує двонапрямлений список, що дозволяє швидкі вставки та видалення з обох кінців. Це особливо корисно для операцій, де важлива ефективна робота зі стеками та чергами.

```python
from collections import deque

my_queue = deque()

my_queue.append('first')
my_queue.append('second')
my_queue.append('third')

print(my_queue.popleft())  # Output: 'first'
```

- **`namedtuple`** - Цей клас допомагає створювати іменовані кортежі, які схожі на звичайні кортежі, але мають іменовані поля, що полегшує доступ до даних.

```python
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

p = Point(x=1, y=2)
print(p.x, p.y)  # Output: 1 2
```



### Модуль `random` 

Модуль `random` використовується для роботи зі випадковими числами та іншими об'єктами. Він надає функціонал для генерації випадкових чисел, вибору випадкових елементів із послідовностей та створення випадкових перестановок. 

Основні аспекти модуля `random`
- Використовується для генерації псевдовипадкових чисел, які обчислюються за допомогою алгоритму, заснованого на початковому значенні (seed).
- Дозволяє отримувати випадкові числа з різних діапазонів і розподілів, наприклад, рівномірного, нормального або трикутного.
- Забезпечує функцію для вибору випадкового елемента з послідовності (`random.choice`) та створення випадкової перестановки (`random.shuffle`).
- Для криптографічно стійких випадкових чисел використовується модуль `secrets`, а не `random`.

```python
import random

random_float = random.random()  # Generate a random float number between 0 and 1
print("Random float between 0 and 1:", random_float)

random_int = random.randint(1, 10)  # Generate a random integer between 1 and 10
print("Random integer between 1 and 10:", random_int)

items = ['apple', 'banana', 'cherry']
random_item = random.choice(items)  # Choose a random element from a list
print("Random item from the list:", random_item)

random.shuffle(items)  # Shuffle a list randomly
print("Shuffled list:", items)

random_range = random.randrange(0, 20, 2)  # Generate a random number within a range with a step
print("Random number in range [0, 20) with step 2:", random_range)
```


### Модуль `datetime`

`datetime` — це модуль у Python, який надає класи для роботи з датами та часом.

Він дозволяє
- отримувати поточні системні дату і час
- обчислювати різницю між датами та інші схожі операції
- порівнювати дати/час
- форматувати інформацю про дату/час

`datetime`
- Надає класи `date`, `time`, `datetime` та `timedelta` для роботи з датами, часом і їх обчисленнями.
- Дозволяє отримати поточну дату й час за допомогою методу `datetime.now()`.
- Підтримує роботу з часовими зонами через модуль `pytz` або вбудований модуль `zoneinfo` (починаючи з Python 3.9).
- Забезпечує зручне форматування дат і часу за допомогою методів `strftime` та парсинг за допомогою `strptime`.
- Дозволяє виконувати арифметичні операції, наприклад, додавання або віднімання днів, годин, хвилин.

```python
from datetime import datetime, timedelta

now = datetime.now()  # Get current date and time
print("Current date and time:", now)

future_date = now + timedelta(days=7)  # Add 7 days to the current date
print("Future date:", future_date)

formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")  # Format datetime object as string
print("Formatted date:", formatted_date)

parsed_date = datetime.strptime("2024-11-24", "%Y-%m-%d")  # Parse string to datetime
print("Parsed date:", parsed_date)
```




### Модуль `math`

Модуль `math` використовується для виконання математичних операцій. Він надає функції для роботи з числами, тригонометрії, логарифмами, константами та іншими математичними обчисленнями. 

Основні аспекти модуля `math`
- Надає широкий набір математичних функцій, таких як `sqrt` (квадратний корінь), `ceil` (округлення вгору), `floor` (округлення вниз).
- Включає тригонометричні функції, такі як `sin`, `cos`, `tan`, і їх обернені функції, наприклад, `asin`, `acos`.
- Містить логарифмічні та експоненціальні функції, такі як `log`, `log10`, `exp`.
- Забезпечує доступ до математичних констант, таких як `pi` (π) та `e` (основа натурального логарифму).
- Пропонує функції для роботи з факторіалами (`factorial`), степенями (`pow`) та модулями (`fabs`).

```python
import math

square_root = math.sqrt(16)  # Calculate the square root of 16
print("Square root of 16:", square_root)

ceil_value = math.ceil(4.2)  # Round up and round down a number
floor_value = math.floor(4.8)
print("Ceil value:", ceil_value)
print("Floor value:", floor_value)

sine_value = math.sin(math.pi / 2)  # Calculate the sine of π/2
print("Sine of π/2:", sine_value)

log_value = math.log(math.e)  # Calculate the natural logarithm of e
print("Natural logarithm of e:", log_value)

factorial_value = math.factorial(5)  # Calculate factorial of 5
print("Factorial of 5:", factorial_value)
```


### Модуль `os`

`os` — надає функції для роботи з операційною системою, включаючи операції з файлами, такі як створення, видалення та переміщення файлів.

```python
import os
os.getcwd() # show current directory
os.path.exists('sample_data') # check if directory 'sample_data' exists
os.mkdir('test_dir') # create directory 'test_dir'
os.listdir('sample_data') # view contents of directory 'sample_data'
```


### Модуль `sys`

Модуль `sys`  використовується для взаємодії з інтерпретатором Python та отримання інформації про середовище виконання. Він дозволяє керувати поведінкою програми на рівні системи та надає важливі об'єкти і функції для цієї взаємодії. 

Основні аспекти модуля `sys`
- Надає доступ до аргументів командного рядка через список `sys.argv`.
- Забезпечує вихід із програми за допомогою функції `sys.exit()`.
- Містить інформацію про платформу та версію Python через об'єкти `sys.platform` і `sys.version`.
- Дозволяє перенаправляти стандартні потоки введення, виведення та помилок через `sys.stdin`, `sys.stdout` і `sys.stderr`.
- Включає об'єкти для управління модульною системою, наприклад, `sys.modules` і `sys.path` для роботи з шляхами пошуку модулів.
- Підтримує обробку рекурсії через `sys.setrecursionlimit()` та інші інструменти.

```python
import sys

print("Command-line arguments:", sys.argv)  # Print command-line arguments
print("Python version:", sys.version)  # Get Python version
print("Platform:", sys.platform)  # Get platform information

sys.stdout = open("output.txt", "w")  # Redirect stdout temporarily
print("This will be written to a file instead of the console.")
sys.stdout.close()
sys.stdout = sys.__stdout__  # Restore default stdout

print("Exiting the program...")  # Exit the program with a specific exit code
sys.exit(0)
```


### Модуль `pathlib`

Модуль `pathlib` використовується для роботи з файловими шляхами. Він забезпечує зручний та об'єктно-орієнтований спосіб роботи з файловою системою, пропонуючи функціонал для створення, аналізу та маніпуляції шляхами. 

Основні аспекти модуля `pathlib`
- Надає класи для роботи з шляхами: `Path` для кросплатформних операцій, `PosixPath` для Unix-подібних систем та `WindowsPath` для Windows.
- Підтримує як абсолютні, так і відносні шляхи.
- Дозволяє легко виконувати перевірки, наприклад, чи існує файл або директорія (`exists`, `is_file`, `is_dir`).
- Забезпечує простий доступ до компонентів шляху, таких як ім'я файлу (`name`), розширення (`suffix`), батьківський каталог (`parent`).
- Підтримує створення, видалення, перейменування файлів і директорій.
- Надає зручний синтаксис для читання та запису даних у файли через методи `read_text`, `write_text`, `read_bytes`, `write_bytes`.

```python
from pathlib import Path

path = Path("/home/user/example.txt")  # Create a Path object

if path.exists() and path.is_file():  # Check if the path exists and is a file
    print(f"File exists: {path}")

print("File name:", path.name)  # example.txt
print("File extension:", path.suffix)  # .txt
print("Parent directory:", path.parent)  # /home/user


new_dir = Path("/home/user/new_folder")
new_dir.mkdir(parents=True, exist_ok=True)  # Create a new directory

file_path = new_dir / "test.txt"
file_path.write_text("Hello, pathlib!")  # Write text to file
print(file_path.read_text())  # Read and print text from file


for file in new_dir.iterdir():  # Iterate through all files in a directory
    print("File in directory:", file)
```


### Модуль `re`

Python підтримує використання регулярних виразів (regex). У стандартній бібліотеці Python є модуль `re`, який функції для роботи з регулярними виразами. Цей модуль дозволяє виконувати різні операції, такі як пошук, заміна, розбиття тексту на підрядки та перевірку збігів із шаблоном регулярного виразу.

Основні компоненти регулярних виразів

- `w` – відповідає всім символам слів. Символи слів є букво-цифровими (a-z, A-Z символи та підкреслення).
- `W` - відповідає символам "не слів". Все, крім букво-цифрових символів та підкреслення.
- `d` – відповідає символам "цифр". Будь-яка цифра від 0 до 9.
- `D` – символи "не цифр". Усі, крім від 0 до 9.
- `s` – символи пропуску, у т.ч. символи табуляції та розриви рядків.
- `S` – все, окрім пропусків.
- `.` – будь-який символ, окрім розриву рядка.
- `[A-Z]` – символи у діапазоні; наприклад, `[A-E]` буде відповідати A, B, C, D та E.
- `[ABC]` – символи у заданому наборі; наприклад, `[AMT]` буде відповідати лише A, M та T.
- `[^ABC]` – символи, які відсутні у заданому наборі. Наприклад, `[^A-E]` буде відповідати всім символам, крім A, B, C, D та E.
- `+` – одне або кілька входжень попереднього символу. Наприклад, `w+` поверне ABD12D у вигляді єдиної відповідності замість шести різних збігів.
- `*` – нуль чи більше входження попереднього символу. Наприклад, `bw*` відповідає частинам у фразі b, bat, bajhdsfbfjhbe. В цілому він відповідає нулю або більше символам слова після b.
- `{m, n}` – не менше m і не більше n входжень попереднього символу. `{m,}` відповідатиме не менше m входжень, і верхньої межі для збігу не буде. `{k}` відповідатиме точно k входженням попереднього символу.
- `?` - нуль або одне входження попереднього символу. Наприклад, це може бути корисно при пошуку двох варіантів написання для однієї і тієї ж роботи. Наприклад, `/behaviou?r/` буде відповідати як behavior, і behaviour.
- `|` – відповідає виразу до або після “pipe” символу. Наприклад, `/se(a|e)/` відповідає як see, і sea.
- `^` – шукає регулярне вираження на початку тексту або на початку кожного рядка, якщо увімкнено багаторядковий режим.
- `$` – шукає регулярний вираз наприкінці тексту чи кінці кожного рядка, якщо включений багаторядковий режим.
- `b` – попередній символ відповідає лише якщо це межа слова.
- `B` – попередній символ відповідає лише тому випадку, якщо межа слова відсутня.
- `(ABC)` – це згрупує кілька символів разом і запам'ятає підрядок, що відповідає їм, для подальшого використання. Це називається скобковою групою.
- `(?:ABC)` – це також об'єднує кілька символів разом, але не запам'ятовує збігу.
- `d+(?=ABC)` – це буде відповідати символу(ам), що передує `(?=ABC)`, тільки якщо за ним слідує ABC. Частина ABC не буде включена до масиву збігів. Частина d – це лише приклад. Це може бути будь-який рядок регулярного вираження.
- `d+(?!ABC)` – це буде відповідати символу(ам), що передує `(?!ABC)`, тільки якщо за ним не слідує ABC. Частина ABC не буде включена до масиву збігів. Частина d – це лише приклад. Це може бути будь-який рядок регулярного вираження.

Для роботи з регулярними виразами Python зазвичай використовуються рядкові літерали з префіксом r (raw string), які дозволяють використовувати спеціальні символи без екранування. Наприклад, регулярний вираз для пошуку слів, що починаються на "a" і закінчуються на "b", може бути записано так:

```python
import re
text = "apple and banana are fruits, but apricot is not"
pattern = r"\ba\w{3,}\b"
matches = re.findall(pattern, text)
print(matches)  # Output: ['apple', 'apricot']
```


### Модуль `logging`

Модуль `logging` використовується для створення і управління журналами (логами) додатків. Він надає потужний і гнучкий механізм для запису повідомлень про помилки, події або іншу важливу інформацію під час виконання програми. 

Основні аспекти модуля `logging`
- Підтримує кілька рівнів журналювання: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- Дозволяє налаштовувати формат повідомлень за допомогою форматерів (`Formatter`).
- Підтримує використання хендлерів (`Handler`) для виведення логів у різні місця, такі як консоль, файли, мережеві сервіси тощо.
- Може працювати з конфігураціями через програмний інтерфейс або файл конфігурації (наприклад, `logging.config`).
- Дозволяє створювати ієрархічні логери, які спрощують структурування і обробку повідомлень.
- Забезпечує можливість фільтрації повідомлень за рівнем або іншими критеріями.

```python
import logging

logging.basicConfig(  # Configure basic logging
    level=logging.DEBUG,  # Set minimum logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("example_logger")  # Create a logger

logger.debug("This is a debug message")  # Log messages of different levels
logger.info("This is an info message")
logger.warning("This is a warning message")
logger.error("This is an error message")
logger.critical("This is a critical message")

file_handler = logging.FileHandler("app.log")  # Write logs to a file with a custom handler
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
logger.addHandler(file_handler)

logger.error("This error will also be written to app.log")
```


### Модуль `pdb`

Модуль `pdb` використовується для інтерактивного налагодження коду. Він дозволяє зупиняти виконання програми, аналізувати значення змінних, виконувати покрокове виконання коду та знаходити помилки. 

Основні аспекти модуля `pdb`
- Дозволяє встановлювати точки зупинки (breakpoints) у коді, щоб зупинити виконання програми в потрібному місці.
- Підтримує покрокове виконання коду, як по одному рядку (`step`), так і переходячи до наступного рядка без занурення в функцію (`next`).
- Забезпечує можливість перегляду та зміни значень змінних у процесі виконання.
- Надає доступ до стеку викликів і дозволяє перемикатися між рівнями стека для аналізу стану програми.
- Містить інтерактивну консоль, у якій можна виконувати Python-код у контексті програми.

Основні команди модуля `pdb`

- `l` (list): Показати частину коду навколо поточної точки.
- `n` (next): Виконати наступний рядок коду.
- `s` (step): Зайти в функцію, яка викликається на поточному рядку.
- `c` (continue): Продовжити виконання програми до наступного breakpoint або завершення.
- `p` (print): Вивести значення змінної або виразу (`p variable`).
- `q` (quit): Вийти з налагоджувача та завершити програму.

```python

def buggy_function(a, b):  # Example script with a bug
    result = a / b  # Possible division by zero
    return result

import pdb

pdb.set_trace()  # Set a breakpoint

x = 10
y = 0
print(buggy_function(x, y))
```


### Модуль `operator`

Модуль `operator` містить функції, які відповідають стандартним операторам. Таким чином, замість `lambda x, y: x + y` можна використовувати вже готову функцію `operator.add` і т.д.


### Модуль `functools`

Модуль `functools` — це бібліотека для роботи з функціями в функціональному стилі. Він надає інструменти для створення і модифікації функцій, спрощення коду, покращення продуктивності та управління функціональними об'єктами. 

Основні функції модуля `functools`

- Декоратор `lru_cache` для кешування результатів викликів функцій, що покращує продуктивність при повторних обчисленнях.
- Декоратор `partial`, який дозволяє створювати нові функції з попередньо заданими аргументами. Виклик функції з меншою кількістю аргументів, ніж вона очікує, і отримання функції, яка приймає решту параметрів
- Декоратор `wraps`, що полегшує створення власних декораторів, зберігаючи метадані оригінальної функції (документація, ім'я).
-  Функція `cmp_to_key`, яка дозволяє порівнювати об'єкти, перетворює функцію порівняння у ключову функцію для сортування.
- Функція `reduce`, яка застосовує функцію до всіх елементів ітерації для обчислення єдиного результату.

```python
from functools import lru_cache, partial, wraps


@lru_cache(maxsize=32)  # Using lru_cache to cache results of a function, cache up to 32 results
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print("Fibonacci(10):", fibonacci(10))

def power(base, exponent):  # Using partial to predefine arguments
    return base ** exponent

square = partial(power, exponent=2)  # Create a new function for squaring numbers
print("Square of 5:", square(5))

def log_decorator(func):
    @wraps(func)  # Using wraps to create a custom decorator
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_decorator
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```


### Модуль `inspect`

Модуль `inspect` використовується для отримання інформації про живі об'єкти під час виконання програми. Він дозволяє аналізувати функції, класи, методи, змінні, модулі та їхні атрибути. Завдяки цьому модуль є незамінним інструментом для розробників, які працюють з динамічним аналізом коду, налагодженням або створенням документації.

Основні можливості модуля `inspect`

- Отримання метаінформації про функції та методи, включно з їхніми аргументами, сигнатурами, докстрінгами та вихідним кодом.
- Аналіз класів, їхніх методів і атрибутів.
- Робота з поточним стеком викликів, включно з переглядом трасування.
- Визначення джерела об'єкта, його місцезнаходження у файлі та рядку.
- Аналіз модулів і пакетів для виявлення їхньої структури та вмісту.

Отримання інформації про функцію

```python
import inspect

def example_function(x: int, y: int) -> int:
    """Adds two integers and returns the result."""
    return x + y

signature = inspect.signature(example_function)  # Get the function's signature
print(signature)  # Output: (x: int, y: int) -> int

docstring = inspect.getdoc(example_function)  # Get the docstring
print(docstring)  # Output: Adds two integers and returns the result.
```

Перегляд вихідного коду функції

```python
source_code = inspect.getsource(example_function)
print(source_code)
```

Аналіз класів і методів

```python
class MyClass:
    def method(self):
        pass

methods = inspect.getmembers(MyClass, predicate=inspect.isfunction)
print(methods)  # Output: [('method', <function MyClass.method at ...>)]
```

Робота з поточним стеком викликів:

```python
def trace():
    frame = inspect.currentframe()
    print(inspect.getframeinfo(frame))

trace()  # Output: FrameInfo(filename='your_script.py', lineno=..., function='trace', ...)
```


### `@lru_cache`

**LRU (least recently used)** — це алгоритм, при якому виштовхуються значення, які найдовше не запитувалися. Відповідно, потрібно зберігати час останнього запиту до значення. І як тільки число закешованих значень перевищує N, потрібно виштовхнути з кешу значення, яке найдовше не запитувалося.

`lru_cache` - декоратор, який кешує значення функцій, які не змінюють свій результат при не змінних аргументах; корисний для кешування даних, мемоїзації (збереження результатів для повернення без обчислення функції) значень рекурсивних функцій (наприклад, такого типу, як функція обчислення n-го числа Фібоначчі) і т.д.;

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n-2) + fib(n-1)
```

Розмір кешу за замовчуванням становить 128 значень. Параметр `maxsize=None` робить його необмеженим.

*Links*

- [LRU, метод вытеснения из кэша](https://habr.com/ru/post/136758/)


### Unittests

Бібліотека `unittests` в Python використовується для написання юніт-тестів - автоматизованих тестів, що перевіряють правильність роботи окремих частин програмного коду. 

Основні класи, методи і поняття бібліотеки unittest

- `unittest.TestCase` - Це базовий клас для створення тестових випадків. Він містить методи для підготовки до виконання тесту (`setUp`) і очищення після тесту (`tearDown`), а також різні методи `assert*`, наприклад, `assertEqual`, `assertTrue`, `assertFalse`, щоб перевіряти очікувані результати.
- Тестові методи: Це методи класу `unittest.TestCase`, які мають ім'я, що починається з "test". Вони містять код для перевірки конкретної частини програмного коду.
- `Mock` - це об'єкт бібліотеки `unittest.mock`, який використовується для створення фіктивних (замінених) об'єктів та функцій. Він дозволяє визначити, як функція чи об'єкт повинні поводитися під час тестування і які значення вони повертають.
- `patch` - декоратор `@unittest.mock.patch` використовується для заміни функцій чи об'єктів у  коді фіктивними Mock об'єктами під час виконання тестів. Це допомагає ізолювати код, який тестується, від його залежностей, таких як бази даних або зовнішні сервіси, та забезпечити більший контроль над тестами.


### Для чого використовують pickle?

Модуль `pickle` у Python використовується для серіалізації та десеріалізації об'єктів. Серіалізація - це процес перетворення об'єктів Python у байтовий потік, що дозволяє їх зберегти або передати через мережу. Десеріалізація - це зворотний процес, коли байтовий потік перетворюється назад у об'єкти Python.

Перевагами модуля `pickle` порівняно з JSON є підтримка серіалізації різноманітних об'єктів Python, включаючи функції та класи, а також збереження внутрішнього стану об'єктів, але недоліками є відсутність зовнішнього стандарту даних, який робить дані `pickle` менш читабельними для інших мов програмування та може мати питання безпеки, порівняно з JSON, який є більш платформонезалежним, має простіший формат та може бути безпечнішим для обробки даних з невідомих джерел.

