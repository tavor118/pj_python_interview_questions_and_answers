## Coding

### Як працюють `and` та `or`

Що виведе код?

```python
def func1():  
    print(1)  

def func2():  
    print(2)  
  
result1 = func1() and func2()  # 1
result2 = 0 or '5'
print(result1)  # None
print(result2)  # 5
```


### FizzBuzz

You are given a list of integers. Your task is to do the following:
- Replace all integers that are evenly divisible by `3` with `"fizz"`
- Replace all integers divisible by `5` with `"buzz"`
- Replace all integers divisible by both `3` and `5` with `"fizzbuzz"`

```python
>>> numbers = [45, 22, 14, 65, 97, 72]
>>> for i, num in enumerate(numbers):
...     if num % 3 == 0 and num % 5 == 0:
...         numbers[i] = 'fizzbuzz'
...     elif num % 3 == 0:
...         numbers[i] = 'fizz'
...     elif num % 5 == 0:
...         numbers[i] = 'buzz'
...
>>> numbers
['fizzbuzz', 22, 14, 'buzz', 97, 'fizz']
```


### Вивести найбільші 2 числа для словника

Вивести значення ключів для двох найбільших значень в словнику.

```python
given_dict = {  
    'a': 40,  
    'b': 99,  
    'c': 10,  
    'd': 200,  
}  

def find_max_values(dictionary: dict) -> Tuple[int, int]:  
    if len(dictionary) < 2:  
        raise ValueError("At least 2 values are required")  
    if len(dictionary) == 2:  
        return tuple(dictionary.keys())  
	max_key = None
	second_max_key = None
    max_value_1 = float('-inf')
    max_value_2 = float('-inf')
    for key, value in dictionary.items():  
        if value > max_value_1:
	        second_max_key = max_key
            max_value_2 = max_value_1
            max_key = key
            max_value_1 = value  
        elif value > max_value_2:
	        second_max_key = key
            max_value_2 = value  
    return max_key, second_max_key  

if __name__ == "__main__":  
    print(find_max_values(given_dict))
```


### Функція перевірки простого числа

```python
import math

def is_prime(number):
    if number <= 1:
        return False

    if number <= 3:
        return True

    sqrt_num = int(math.sqrt(number)) + 1
    for divisor in range(2, sqrt_num):
        if number % divisor == 0:
            return False

    return True
```


### Функція перевірки, чи рядок є паліндромом

```python
def is_palindrome(string):
    string = string.lower()   
    return string == string[::-1]
```


### Генератор для чисел Фібоначчі

```python
def fibonacci_generator():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


fib_gen = fibonacci_generator()
for _ in range(10):
    print(next(fib_gen))
```


### Рекурсивна функція для чисел Фібоначчі

```python
def fibonacci(n):
    if n < 2:  # Base case
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)  # Recursive case

n = 10  # Set your desired Fibonacci number here
result = fibonacci(n)
print(f"The Fibonacci number at position {n} is {result}.")
```


### Рекурсивна функція для чисел Фібоначчі з кешем

- Зовнішній словник як кеш

```python
cache = {}  
  
def fibonacci(n: int):  
    if n < 2:  # Base case  
        return n  
  
    if n in cache:  
        return cache[n]  
  
      
    cache[n] = fibonacci(n - 1) + fibonacci(n - 2)  # Compute and cache the Fibonacci number
    return cache[n]  
  
n = 10  # Set your desired Fibonacci number here  
result = fibonacci(n)  
print(f"The Fibonacci number at position {n} is {result}.")
```

- Декоратор для кешу

```python
def memoize(f):
	cache = {}
	def decorated_function(*args):
		if args in cache:
			return cache[args]
		else:  
			cache[args] = f(*args)  
			return cache[args]
	return decorated_function

@memoize
def fibonacci(n):
    if n < 2:  # Base case
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

n = 10  # Set your desired Fibonacci number here
result = fibonacci(n)
print(f"The Fibonacci number at position {n} is {result}.")
```


### Декоратор для заміру часу виконання функції

```python
import functools
import time

def measure_execution_time(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        execution_time = end - start
        print(f"Execution time of function '{function.__name__}': {execution_time} seconds")
        return result
    return wrapper

@measure_execution_time
def sample_function():
    pass
```


### Декоратора, який буде перехоплювати помилки, і повторіть функцію максимум N раз

```python
from functools import wraps

def retry_on_exception(max_retries):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed with error: {e}. Retrying...")
                    attempts += 1
            raise Exception(f"Function failed after {max_retries} attempts")
        return wrapper
    return decorator

@retry_on_exception(max_retries=3)
def potentially_failing_function():
    print("Executing function")
    raise ValueError("An error occurred")

try:
    potentially_failing_function()
except Exception as e:
    print(f"Function failed with error: {e}")
```


### Функція, яка знаходить найбільше число у вкладеному списку

```python
def find_maximum(lst):  
    maximum = float('-inf')  
    for element in lst:  
        if isinstance(element, (int, float)):  
            maximum = max(maximum, element)  
        elif isinstance(element, list):  
            maximum = max(maximum, find_maximum(element))  
  
    return maximum  

nested_list = [1, [2, 3], [4, [5, 6], 7], 8, 9]  
result = find_maximum(nested_list)  
print(f"The maximum in the nested list is: {result}")
```


### Функція, яка знаходить суму усіх чисел у вкладеному списку

```python
def find_sum(numbers_list):
    total_sum = 0
    for element in numbers_list:
        if isinstance(element, list):
            total_sum += find_sum(element)
        elif isinstance(element, (int, float)):
            total_sum += element
    return total_sum

nested_list = [1, [2, 3], [4, [5, 6], 7], 8, 9]
sum_result = find_sum(nested_list)
print(f"The sum of all numbers in the nested list is: {sum_result}")
```


### Аналог deepcopy для tree

```python
from typing import Any, List

class Tree:
    def __init__(self, data: Any, children: List['Tree'] = None):
        self.data = data
        self.children = children or []

def custom_deepcopy(tree: Tree) -> Tree:
    if not tree:
        return None

    new_root = Tree(tree.data)
    new_root.children = [custom_deepcopy(child) for child in tree.children]
    return new_root

def print_tree(tree: Tree, level: int = 0):  
    if tree:  
        line = ''  
        if level >= 2:  
            line = '│  ' + '   ' * (level - 2)  
        if level:  
            line += '└─ '  
        print(line + str(tree.data))  
        for child in tree.children:  
            print_tree(child, level + 1)

root = Tree(1)  
child1 = Tree(2)  
child2 = Tree(3)  
root.children = [child1, child2]  
child1.children = [Tree(4), Tree(5)]  
child2.children = [Tree(6)]  
  
  
print("Original tree:")  
print_tree(root)  # Checking the original tree

copied_tree = custom_deepcopy(root)  # Copying the tree  

print("\nCopied tree:")  
print_tree(copied_tree)  # Checking the copied tree
```


### Спискові і словникові вирази

```python
A0 = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))  
A1 = range(10)  
A2 = sorted([i for i in A1 if i in A0])  
A3 = sorted([A0[s] for s in A0])  
A4 = [i for i in A1 if i in A3]  
A5 = {i: i * i for i in A1}  
A6 = [[i, i * i] for i in A1]  
A7 = [i if i % 2 else 0 for i in A1 if 2 < i < 8]  
A8 = ','.join(str(j ** 2) for j in range(10))
---
A0 = {'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4}
A1 = range(0, 10)
A2 = []
A3 = [1, 2, 3, 4, 5] 
A4 = [1, 2, 3, 4, 5]
A5 = {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81} 
A6 = [[0, 0], [1, 1], [2, 4], [3, 9], [4, 16], [5, 25], [6, 36], [7, 49], [8, 64], [9, 81]]
A7 = [3, 0, 5, 0, 7]
A8 = '0,1,4,9,16,25,36,49,64,81'
```


### Розташувати функції в порядку зростання часу виконання

```python
def f1(lst):  
    l1 = sorted(lst)  
    l2 = [i for i in l1 if i < 0.5]  
    return [i * i for i in l2]  
  
def f2(lst):  
    l1 = [i for i in lst if i < 0.5]  
    l2 = sorted(l1)  
    return [i * i for i in l2]  
  
def f3(lst):  
    l1 = [i * i for i in lst]  
    l2 = sorted(l1)  
    return [i for i in l1 if i < (0.5 * 0.5)]

>>> f2 >> f1 > f3
```



### Знайти трійку найуживаніших слів у тексті

У файлі містяться слова, розділені пробілом. Наприклад: "abba com mother bill mother com abba dog abba mother com". Потрібно знайти і вивести трійку слів, які частіше всього зустрічаються разом (порядок не має значення). Тобто у моєму прикладі трійки слів це "abba com mother", "com mother bill", "mother bill mother" і так далі. Тут правильною відповіддю має бути "abba com mother" (частота — 3 рази).

```python
from collections import defaultdict  
  
text = "abba com mother bill mother com abba dog abba mother com"  
words = text.split()  
  
triplet_counts = defaultdict(int)  
  
for i in range(len(words) - 2):  
    triplet = [words[i], words[i + 1], words[i + 2]]  
    triplet = tuple(sorted(triplet))  
    triplet_counts[triplet] += 1  

most_common_triplet = max(triplet_counts, key=triplet_counts.get)  

print("The most common triplet of words:", most_common_triplet)  # ('abba', 'com', 'mother')  
print("Frequency of occurrence:", triplet_counts[most_common_triplet])  # 3
```


### Чи можна використати клас як ключ в словнику

Що виведе print та чому?

```python
class KeyHolder:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return 0

d = {KeyHolder(1): 'a', KeyHolder(2): 'b'}

print(d)  # {<__main__.KeyHolder object at 0x10>: 'a', <__main__.KeyHolder object at 0x20>: 'b'}
```

Функція `hash` буде повертати однакове значення в усіх випадках. Але виклик `KeyHolder(2)` не перезапише ключ, оскільки словник вміє працювати з колізіями. Коли ми отримуємо однакове значення хеша, далі проводиться порівняння за значенням. Оскільки в `eq` ми порівнюємо `key`, Python зрозуміє що це інший об'єкт, та помістить нову пару в хеш-таблицю. Проблемою цієї реалізації є те, що всі виклики `hash` будуть повертати однакове значення. Відповідно для того, щоб знайти по ключу відповідно значення, в негативному сценарії потрібно буде перебрати усі ключі. Тобто доступ буде O(n), а не O(1).


### Дескриптор для валідації атрибутів

```python
from typing import Callable, Any

class Validation:
    def __init__(self, validation_function: Callable[[Any], bool], error_msg: str) -> None:
        self.validation_function = validation_function
        self.error_msg = error_msg

    def __call__(self, value):
        if not self.validation_function(value):
            raise ValueError(f"{value!r} {self.error_msg}")


class Field:
    def __init__(self, *validations):
        self._name = None
        self.validations = validations

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def validate(self, value):
        for validation in self.validations:
            validation(value)

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = value


class ClientClass:
    descriptor = Field(
        Validation(lambda x: isinstance(x, (int, float)), "is not a number"),
        Validation(lambda x: x >= 0, "is not >= 0"),
    )

>>> client = ClientClass()
>>> client.descriptor = 42
>>> client.descriptor
42
>>> client.descriptor = -42
Traceback (most recent call last):
...
ValueError: -42 is not >= 0
>>> client.descriptor = "invalid value"
Traceback (most recent call last):
...
ValueError: 'invalid value' is not a number

```


### Дескриптор з метою запобігання видаленню атрибутів

Дескриптор з метою запобігання видаленню атрибутів з об’єкта без необхідних адміністративних привілеїв. 

```python
class ProtectedAttribute:
    def __init__(self, requires_role=None) -> None:
        self.permission_required = requires_role
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __set__(self, user, value):
        if value is None:
            raise ValueError(f"{self._name} can't be set to None")
        user.__dict__[self._name] = value

    def __delete__(self, user):
        if self.permission_required in user.permissions:
            user.__dict__[self._name] = None
        else:
            raise ValueError(
                f"User {user!s} doesn't have {self.permission_required} permission"
            )


class User:
    """Only users with 'admin' privileges can remove their email address."""
    email = ProtectedAttribute(requires_role="admin")

    def __init__(self, username: str, email: str, permission_list: list = None) -> None:
        self.username = username
        self.email = email
        self.permissions = permission_list or []

    def __str__(self):
        return self.username

>>> admin = User("root", "root@d.com", ["admin"])
>>> user = User("user", "user1@d.com", ["email", "helpdesk"])
>>> admin.email
'root@d.com'
>>> del admin.email
>>> admin.email is None
True
>>> user.email
'user1@d.com'
>>> user.email = None
Traceback (most recent call last):
...
ValueError: email can't be set to None
>>> del user.email
Traceback (most recent call last):
...
ValueError: User user doesn't have admin permission
```

Клас `User` вимагає, щоб ім'я користувача та електронна пошта були обов'язковими параметрами. Згідно з його методом `__init__`, об'єкт не може бути користувачем, якщо у нього немає атрибута `email`. Якщо видалити цей атрибут і повністю вилучити його з об'єкта, буде некоректний об'єкт, який не відповідає інтерфейсу, визначеному класом `User`. Інший об'єкт, який буде взаємодіяти з цим користувачем, буде очікувати, що у нього буде атрибут `email`.

Тому "видалення" електронної пошти просто встановлює її значення на `None`. З тієї ж причини потрібно заборонити присвоєння значення `None` для цього атрибута, оскільки це обійде механізм, який встановлений в методі `__delete__`.
