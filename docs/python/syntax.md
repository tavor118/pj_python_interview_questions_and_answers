## Syntax - Синтаксис

### Що таке PEP 8? [❄️6/100]

PEP означає Python Enhancement Proposal (Пропозиція щодо покращення Python). 
Це набір правил, які визначають, як писати та форматувати код Python для досягнення 
максимальної читабельності.

Наприклад, класи називають CamelCase, функції, змінні - snake_case.



### Що таке ключові слова в Python? [❄️3/100]

Ключові слова в Python є зарезервованими словами, які мають особливий зміст. 
Зазвичай вони використовуються для визначення типу змінних. 
Ключові слова не можна використовувати як імена змінних або функцій. 

У Python існує 33 ключових слова:

- None, True, False
- is
- in
- and, or, not
- if, elif, else
- for, while, break, continue
- class
- def, lambda, return, yield
- pass
- try, except, finally, raise
- with, as
- global, nonlocal
- del
- import, from
- assert



### Що таке list/dict comprehension? [💡15/100]

List comprehension та dict comprehension - це спосіб створення списків та словників. 
Являють собою вираз, загорнений у квадратні/фігурні дужки, у якому використовуються 
ключові слова `for` і `in` для побудови списку/словника шляхом обробки і фільтрації 
елементів з одного або декількох ітерабельних об'єктів.

List comprehension дозволяє створювати списки на основі наявних списків або інших 
ітераційних об'єктів за допомогою одного рядка коду.

```python
squares = [x**2 for x in range(10)]
print(squares)  # Output: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

Dict comprehension дозволяє створювати словники на основі наявних ітераційних об'єктів.

```python
squares_dict = {x: x**2 for x in range(10)}
print(squares_dict)  # Output: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}
```

Можна додати умови для фільтрації елементів.

```python
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)  # Output: [0, 4, 16, 36, 64]

even_squares_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares_dict)  # Output: {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}
```

Можна використовувати вкладені вирази для створення багатовимірних структур.

```python
matrix = [[j for j in range(3)] for i in range(3)]
print(matrix)  # Output: [[0, 1, 2], [0, 1, 2], [0, 1, 2]]
```

Переваги comprehension

- Лаконічність: Менше коду для написання.
- Читабельність: Часто легше зрозуміти наміри коду.
- Ефективність: Часто працює швидше завдяки оптимізації внутрішніх операцій Python.



### Для чого оператори % та // ? [❄️4/100]

Оператори `%` та `//` у Python використовуються 

- **`%`** використовується для отримання залишку.
- **`//`** використовується для отримання цілої частини від ділення.

**Оператор `%` (Модуль)** обчислює залишок від ділення одного числа на інше. 
Це корисно для перевірки парності числа, циклічних завдань та інших обчислень, 
які потребують залишку.

```python
result = 10 % 3
print(result)  # 1

number = 8
if number % 2 == 0:
    print(f"{number} is an even number")
else:
    print(f"{number} is an odd number")
```

**Оператор `//` (Цілочисельне ділення)** обчислює результат ділення двох чисел, 
округлюючи результат до найближчого цілого числа в менший бік. 
Це корисно, коли потрібно отримати цілу частину від ділення без десяткової частини.

```python
result = 10 // 3
print(result)  # 3

days = 23
weeks = days // 7
print(f"Number of full weeks in {days} days: {weeks}") # Output: Number of full weeks in 23 days: 3
```

**Поведінка з від'ємними операндами**

`//` округлює *вниз* (floor), а не до нуля, тому залишок `%` завжди має знак
дільника. Це відрізняється від C/C++, Java та JavaScript, де ділення відсікається
до нуля, а залишок успадковує знак діленого, тож там `-11 % 10 == -1`.

```python
print(-11 // 10)  # -2  (floor division, not toward zero)
print(-11 % 10)   #  9  (sign of the divisor, not the dividend)
print(11 % -10)   # -9
# invariant Python always preserves: a == (a // b) * b + a % b
```

Якщо потрібен залишок зі знаком діленого (як у C), використовують `math.fmod`:

```python
import math
print(math.fmod(-11, 10))  # -1.0
```



### Тернарний оператор в Python [❄️8/100]

Тернарний оператор - це спосіб короткого запису умовного виразу, який дозволяє визначити 
значення залежно від умови. 

```python
x = 10
y = 20

max_value = x if x > y else y

print(max_value)  # 20
```



### Оператор match (switch) [❄️4/100]

*Summary*
> Оператор `match` у Python був представлений у версії 3.10 і дозволяє здійснювати 
> патерн-матчинг (pattern matching). 
> Це робить його подібним до оператора `switch` з інших мов програмування, 
> проте `match` є гнучкішим і кращим. Допомагає замінити блок `if...elif..else`.

`match` використовується для порівняння значення зі специфічними патернами (шаблонами). 
Це дозволяє писати чистий та ефективний код, особливо коли потрібно перевіряти складні 
структури даних. 
Блок `case` визначає шаблон, який перевіряється. 
Якщо значення відповідає шаблону, виконується відповідний блок коду. 
Символ `_` використовується для позначення "всього іншого" і є аналогом `default` 
в інших мовах.

`match` підтримує роботу не тільки зі звичайними значеннями, але й з кортежами, 
списками, словниками і класами.

```python
value = 10
match value:
    case 1:
        print("Value is 1")
    case 10:
        print("Value is 10")
    case _:
        print("Unknown value")
```

Також можна робити патерн-матчинг для складніших структур, як кортежі чи списки

```python
point = (0, 5)
match point:
    case (0, y):
        print(f"Point is on Y axis with y={y}")
    case (x, 0):
        print(f"Point is on X axis with x={x}")
    case (x, y):
        print(f"Point is on coordinates: x={x}, y={y}")
```


Приклад із використанням класів

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)

match p:
    case Point(x=1, y=y):
        print(f"x=1, y={y}")
    case Point(x=0, y=0):
        print("This is the origin point")
    case _:
        print("Unknown point")
```



### Оператор-морж (walrus `:=`)

*Summary*
> Оператор присвоєння-у-виразі `:=` (PEP 572, Python 3.8) присвоює значення змінній і
> одночасно повертає його, дозволяючи поєднати обчислення та присвоєння в одному виразі.

Оператор прибирає дублювання, коли значення потрібне і в умові, і в тілі: обчислення
виконується один раз, а результат одразу зв'язується з іменем.

```python
# read in chunks until empty - assign and test in one expression
while (chunk := f.read(8192)):
    process(chunk)

# reuse a computed value inside a comprehension without calling f() twice
data = [y for x in values if (y := f(x)) is not None]
```

Дужки навколо `:=` часто обов'язкові через низький пріоритет оператора. Зловживання знижує
читабельність, тому його застосовують лише там, де він усуває явне повторення обчислення.



### Що означають вирази `*tuple` i `**dict`? [❄️8/100]

*Summary*
> Вирази `*tuple` і `**dict` використовуються для "розпаковування" елементів 
> з кортежів або словників.

`*tuple` - використовується для розпаковування елементів з кортежу 
(або будь-якої послідовності).

```python
def my_function(a, b, c):
    print(a, b, c)

my_tuple = (1, 2, 3)
my_function(*my_tuple)  # unpacks (1, 2, 3) into positional arguments

a, b, c = my_tuple 
print(a, b, c)  # 1 2 3

list1 = [1, 2, 3]
list2 = [4, 5, 6]
merged_list = [*list1, *list2]
print(merged_list)  # [1, 2, 3, 4, 5, 6]
```

Також може використовуватись для запаковування частини значень в список.

```python
numbers = (1, 2, 3, 4, 5)
a, b, *rest = my_tuple
print(a, b, rest)  # 1 2 [3, 4, 5]

first, *middle, last = numbers 
print(first, middle, last) # 1 [2, 3, 4] 5

```

`**dict` - використовується для розпаковування елементів зі словника в іменовані пари 
ключ-значення.

```python
def my_function(name, age):
    print(f"{name} is {age} years old")

my_dict = {"name": "John", "age": 30}
my_function(**my_dict)  # unpacks a dictionary into key-value arguments

dict1 = {'a': 1, 'b': 2} 
dict2 = {'c': 3, 'd': 4} 
merged_dict = {**dict1, **dict2}
print(merged_dict)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

Щоб клас підтримував розпаковку, потрібно визначити спеціальні методи `__iter__`, 
який буде повертати ітератор, об'єкта для `*` (позиційна розпаковка) і `__getitem__` 
або `__iter__` з `items()` для `**` (іменована розпаковка), щоб клас поводився як словник.

Позиційна розпаковка

```python
class MyClass:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __iter__(self):
        return iter([self.a, self.b, self.c])

obj = MyClass(1, 2, 3)
a, b, c = obj
```

Іменована розпаковка

```python
class MyClass:  
    def __init__(self, a, b, c):  
        self.a = a  
        self.b = b  
        self.c = c  
  
    def __iter__(self):  
        yield from self.__dict__.items()  
  
    def __getitem__(self, key):  
        return getattr(self, key)  
  
obj = MyClass(1, 2, 3)  
d = dict(**dict(obj))  
  
print(d)  # {'a': 1, 'b': 2, 'c': 3}  

a, b, c = d['a'], d['b'], d['c']  
print(a)  # 1  
print(b)  # 2  
print(c)  # 3
```



### Що означає конструкція `if __name__ == "__main__":`? [❄️3/100]

*Summary*
> Конструкція `if __name__ == "__main__":` у Python використовується для того, 
> щоб визначити, чи був скрипт запущений безпосередньо, чи імпортований як модуль 
> в інший скрипт. 
> Це дозволяє розмежувати код, який повинен виконуватися при прямому запуску скрипта, 
> від коду, який не повинен виконуватися при імпорті цього скрипта в інший модуль. 
> Якщо умова істинна, виконується код всередині блоку.

**`__name__`** - це спеціальна змінна, яка автоматично встановлюється Python. 
Якщо скрипт запущено безпосередньо, `__name__` буде рівне `"__main__"`. 
Якщо скрипт імпортований як модуль, `__name__` міститиме ім'я модуля.

```python
def main():
    print("This script is running directly.")

if __name__ == "__main__":
    main()
```

При запуску скрипта  `__name__` дорівнюватиме `"__main__"` і виконається функція `main()`,
виводячи `"This script is running directly."`.

```bash
$ python script.py
```

Проте у випадку імпорту `__name__` буде містити ім'я модуля (`"script"`),
і функція `main()` не буде виконана автоматично, що дозволяє використовувати функції 
та класи цього модуля без виконання коду, який призначений лише для запуску.

```python
import script
```
  


### Функції `dir()`, `vars()`, `globals()`, `locals()` [❄️5/100]

Функції `dir`, `vars`, `globals` та `locals` в Python використовуються для отримання інформації про об'єкти та поточний стан програми.

- `dir()` - повертає список атрибутів і методів об'єкта. Якщо об'єкт не переданий, вона повертає список імен у поточній області видимості.
- `locals()` - повертає словник локальних змінних у поточній області видимості. У глобальній області видимості вона працює аналогічно функції `globals()`.
- `vars()` - повертає `__dict__` об'єкта, тобто словник атрибутів об'єкта. Якщо об'єкт не переданий, повертається словник поточної області видимості.
- `globals()`-  використовується для отримання словника, який містить всі глобальні змінні та їхні значення в поточному модулі

```python
class MyClass:
    def __init__(self, value):
        self.value = value

obj = MyClass(10)
print(vars(obj))  # Output: {'value': 10}

print(vars())  # Without arguments, returns the dictionary of the current local scope
```



### Що повертає `id()`? [❄️5/100]

`id()` повертає унікальний ідентифікатор об'єкта. 
Цей ідентифікатор можна використовувати для порівняння об'єктів. 
Якщо об'єкти мають однаковий `id()`, то вони вказують на один і той самий об'єкт 
у пам'яті комп'ютера.



### Для чого використовується одинарне підкреслення? [❄️4/100]

Існує 5 випадків використання підкреслення в Python:

1. Для зберігання значення останнього виразу в REPL.
2. Ігнорування значення.
3. Для визначення спеціального значення функції або змінної.
   - одинарне на початку або в кінці назви
   - подвійне на початку
   - подвійне на початку і в кінці
4. Для використання як функції локалізації.
5. Для розділення символів числа (`1_000 == 1000`).

*Links*

- [Understanding the underscore of Python](https://hackernoon.com/understanding-the-underscore-of-python-309d1a029edc)



### Три типи копіювання: assignment, shallow copy, deep copy [💡11/100]

*Summary*
> Python розрізняє три рівні "копіювання": **присвоєння** (`b = a`) - новий
> ідентифікатор на той самий об'єкт без копіювання; **поверхнева копія**
> (`copy.copy(a)` або `a.copy()`) - новий контейнер з тими ж посиланнями на
> вкладені елементи; **глибока копія** (`copy.deepcopy(a)`) - рекурсивне
> копіювання всього дерева. Вибір залежить від вкладеності об'єкта і
> очікуваної ізоляції.

**1. Присвоєння (`b = a`) - той самий об'єкт**

Жодного копіювання не відбувається. Створюється нове ім'я, яке посилається на
вже існуючий об'єкт. `id(a) == id(b)`, `a is b` повертає `True`. Зміна через
одне ім'я видима через інше:

```python
import copy

a = [1, 2, [3, 4]]
b = a                # No copy - same object
b.append(5)
print(a)             # [1, 2, [3, 4], 5] - a is mutated too
print(a is b)        # True
```

**2. Поверхнева копія (`copy.copy`, `list.copy`, `dict.copy`, `[:]`)**

Створюється новий контейнер. Вкладені об'єкти **не** копіюються - копіюються
посилання на них. Верхній рівень ізольований, вкладені - спільні.

```python
a = [1, 2, [3, 4]]
b = copy.copy(a)     # Shallow copy
# Equivalent: b = list(a), b = a[:], b = a.copy()

b.append(5)
print(a)             # [1, 2, [3, 4]] - top level NOT mutated
print(b)             # [1, 2, [3, 4], 5]

b[2].append(99)
print(a)             # [1, 2, [3, 4, 99]] - nested list IS mutated
print(a[2] is b[2])  # True - same nested object
```

Поширені способи зробити поверхневу копію:

- `copy.copy(x)` - універсальний;
- `list(x)`, `dict(x)`, `set(x)` - через конструктор;
- `x.copy()` - метод (списки, словники, множини, з 3.9+);
- `x[:]` - slice-копія для послідовностей.

**3. Глибока копія (`copy.deepcopy`)**

Рекурсивно копіює об'єкт і всі вкладені. Жодних спільних посилань між оригіналом
і копією не лишається:

```python
a = [1, 2, [3, 4]]
b = copy.deepcopy(a)
b[2].append(99)
print(a)             # [1, 2, [3, 4]] - original unchanged
print(b)             # [1, 2, [3, 4, 99]]
print(a[2] is b[2])  # False - distinct nested objects
```

**Як обробляються циклічні посилання**

`deepcopy` тримає словник `memo` зі вже скопійованих об'єктів. Якщо натикається
на цикл - повертає вже скопійований варіант, уникаючи безкінечної рекурсії:

```python
a = [1]
a.append(a)          # Cycle: a contains itself
b = copy.deepcopy(a) # No StackOverflow - memo breaks the cycle
print(b[1] is b)     # True - cycle preserved in copy
```

**Кастомізація: `__copy__` і `__deepcopy__`**

Клас може контролювати поведінку копіювання. `deepcopy` приймає `memo`:

```python
class Node:
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

    def __copy__(self):
        return Node(self.value, self.children)   # Shallow: shares children list

    def __deepcopy__(self, memo):
        return Node(copy.deepcopy(self.value, memo),
                    copy.deepcopy(self.children, memo))
```

**Що вибирати**

| Сценарій | Інструмент |
| --- | --- |
| Передати посилання | `b = a` (нема копії) |
| Контейнер без вкладених mutable | `copy.copy(a)` / `a.copy()` / `a[:]` |
| Дерево, вкладені списки/словники | `copy.deepcopy(a)` |
| Контрольоване копіювання класу | `__copy__` / `__deepcopy__` |

**Підводні камені**

- `dict.copy()` копіює тільки верхній рівень. Якщо значення - вкладений словник
  чи список, його зміна видима в обох.
- `deepcopy` дорогий: O(n) по всіх елементах + alloc на кожен. Для великих
  структур краще зробити immutable-копію (`tuple`, `frozenset`, `MappingProxyType`).
- `deepcopy` не копіює відкриті файлові дескриптори, сокети, threads - спробує
  через pickle-протокол, який може кинути виняток для несеріалізованих об'єктів.

*Links*

- [Python docs: copy - Shallow and deep copy operations](https://docs.python.org/3/library/copy.html)
