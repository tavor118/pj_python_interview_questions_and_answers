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



### Рекурсивна функція для чисел Фібоначчі з кешем [❄️1/100]

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



### Декоратор для заміру часу виконання функції [❄️1/100]

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

У файлі містяться слова, розділені пробілом. 
Наприклад: "abba com mother bill mother com abba dog abba mother com". 
Потрібно знайти і вивести трійку слів, які частіше всього зустрічаються разом 
(порядок не має значення). 
Тобто у моєму прикладі трійки слів це "abba com mother", "com mother bill", 
"mother bill mother" і так далі. 
Тут правильною відповіддю має бути "abba com mother" (частота — 3 рази).

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

Функція `hash` буде повертати однакове значення в усіх випадках. 
Але виклик `KeyHolder(2)` не перезапише ключ, оскільки словник вміє працювати з колізіями.
Коли ми отримуємо однакове значення хеша, далі проводиться порівняння за значенням. 
Оскільки в `eq` ми порівнюємо `key`, Python зрозуміє що це інший об'єкт, 
та помістить нову пару в хеш-таблицю. Проблемою цієї реалізації є те, 
що всі виклики `hash` будуть повертати однакове значення. 
Відповідно для того, щоб знайти по ключу відповідно значення, в негативному сценарії 
потрібно буде перебрати усі ключі. Тобто доступ буде O(n), а не O(1).



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

Дескриптор з метою запобігання видаленню атрибутів з об’єкта без необхідних 
адміністративних привілеїв. 

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

Клас `User` вимагає, щоб ім'я користувача та електронна пошта були обов'язковими 
параметрами. 
Згідно з його методом `__init__`, об'єкт не може бути користувачем, якщо у нього немає 
атрибута `email`. 
Якщо видалити цей атрибут і повністю вилучити його з об'єкта, буде некоректний об'єкт, 
який не відповідає інтерфейсу, визначеному класом `User`. 
Інший об'єкт, який буде взаємодіяти з цим користувачем, буде очікувати, що у нього буде атрибут `email`.

Тому "видалення" електронної пошти просто встановлює її значення на `None`. 
З тієї ж причини потрібно заборонити присвоєння значення `None` для цього атрибута, 
оскільки це обійде механізм, який встановлений в методі `__delete__`.



### Максимальна кількість пересічних інтервалів [❄️1/100]

*Summary*
> Класична задача про кімнати/ресурси: знайти момент, де перетинається найбільше інтервалів. 
> Оптимальне рішення - sweep line: `+1` на початок інтервалу, `-1` на кінець, сортування 
> за часом, префіксна сума з відстеженням максимуму. Складність O(N log N).

Дано список інтервалів `[start, end]` (бронювання, зустрічі, заселення). Потрібно визначити 
максимальну кількість інтервалів, що перетинаються в один момент часу - тобто скільки кімнат 
(ресурсів) потрібно одночасно. Та сама задача зустрічається у формулюваннях "meeting rooms", 
"планування слотів", "виділення ресурсів".

**Sweep line (події заселення/виселення)**

Кожен інтервал розкладають на дві події: `+1` у момент `start` (заселення) і `-1` у момент 
`end` (виселення). Події сортують за часом і проходять префіксною сумою, відстежуючи максимум. 
За рівного часу виселення має передувати заселенню - інтервал, що закінчується в момент `t`, 
не перетинається з тим, що починається в `t`. Кортеж `(time, delta)` дає це автоматично, бо 
`-1 < 1`.

```python
def max_overlap(intervals: list[tuple[int, int]]) -> int:
    events: list[tuple[int, int]] = []
    for start, end in intervals:
        events.append((start, 1))    # check-in
        events.append((end, -1))     # check-out
    events.sort()                    # by time; -1 before +1 on ties

    current = best = 0
    for _, delta in events:
        current += delta
        best = max(best, current)
    return best

max_overlap([(1, 5), (2, 6), (3, 7), (8, 10)])  # 3
```

Складність - O(N log N) за рахунок сортування подій; це нижня межа для задачі. Додаткова 
пам'ять - O(N) на масив подій.

**Перебір по шкалі часу.** Альтернатива - пройти кожну цілу точку від мінімального до 
максимального часу й порахувати інтервали, що її покривають. Це O(N * D), де `D` - діапазон 
значень. Рішення прийнятне, лише коли значення обмежені (наприклад, години доби); при 
розріджених великих координатах (`D` у мільярди при кількох інтервалах) воно деградує, тоді 
як sweep line залежить лише від кількості інтервалів `N`.



### Пошук слова в матриці (DFS + backtracking) [❄️1/100]

*Summary*
> Перевірити, чи можна скласти слово, рухаючись сусідніми клітинками сітки літер (вгору, 
> вниз, ліворуч, праворуч), використовуючи кожну клітинку щонайбільше раз. Розв'язок - 
> пошук у глибину з backtracking: клітинку позначають відвіданою на час рекурсії й 
> відновлюють після виходу.

Дано матрицю літер і слово; знайти, чи існує шлях суміжними клітинками, що утворює це слово. 
Кожну клітинку можна використати лише раз у межах одного шляху. Класична задача 
(LeetCode "Word Search").

Запускають DFS з кожної клітинки, що збігається з першою літерою. На кожному кроці клітинку 
тимчасово замінюють маркером (або тримають множину відвіданих), щоб той самий шлях не 
повертався в неї, а після рекурсії - відновлюють (це і є backtracking).

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False

        board[r][c] = "#"            # mark visited (avoid revisiting in this path)
        found = (
            dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
            or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1)
        )
        board[r][c] = word[i]        # restore for other paths (backtracking)
        return found

    return any(dfs(r, c, 0) for r in range(rows) for c in range(cols))

board = [["A", "B", "C", "E"],
         ["S", "F", "C", "S"],
         ["A", "D", "E", "E"]]
exist(board, "ABCCED")  # True
exist(board, "ABCB")    # False  (B can't be reused)
```

Складність - O(M * N * 4^L) у гіршому випадку, де `M*N` - стартові клітинки, а `4^L` - 
розгалуження пошуку на довжину слова `L` (фактично менше через відсікання за літерою й 
межами). Додаткова пам'ять - O(L) на глибину рекурсії. Ключовий момент, який часто 
пропускають, - **відновлення клітинки після рекурсії**; без нього одна гілка пошуку 
"з'їдає" клітинки в інших.



### Максимум у кожному вікні (монотонний дек)

*Summary*
> Для кожного вікна розміру `k` знайти максимум. Наївно - O(n·k). Оптимально - O(n) через 
> монотонний (спадний) дек, що зберігає **індекси** кандидатів: на початку дека завжди індекс 
> поточного максимуму, а застарілі й менші кандидати відкидаються.

Дано масив `nums` і розмір вікна `k`; повернути максимум кожного вікна, що рухається зліва 
направо (LeetCode "Sliding Window Maximum"). Наївний перебір кожного вікна - O(n·k).

**Монотонний дек**

Тримають дек індексів, значення в яких спадають. Перед додаванням нового елемента з хвоста дека 
прибирають усі індекси з меншими або рівними значеннями - вони вже не зможуть стати максимумом, 
бо новий елемент і свіжіший, і більший. На початку дека лишається індекс максимуму поточного 
вікна. Коли індекс на початку виходить за ліву межу вікна, його прибирають. Зберігають саме 
індекси, а не значення, щоб визначати момент виходу елемента з вікна.

```python
from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()   # indices; their values stay decreasing
    result: list[int] = []
    for i, n in enumerate(nums):
        while dq and nums[dq[-1]] <= n:   # drop smaller/equal tail candidates
            dq.pop()
        dq.append(i)
        if dq[0] == i - k:                # front index slid out of the window
            dq.popleft()
        if i >= k - 1:                    # window full -> record its max
            result.append(nums[dq[0]])
    return result

max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3)  # [3, 3, 5, 5, 6, 7]
```

Складність - O(n): кожен індекс додається в дек і прибирається з нього щонайбільше раз, тому 
сумарна робота лінійна, попри вкладений `while`. Додаткова пам'ять - O(k) на дек.



### Перемістити нулі в кінець (два вказівники, in-place)

*Summary*
> Перенести всі нулі масиву в кінець, зберігши порядок ненульових елементів, за O(n) часу і 
> O(1) додаткової пам'яті: вказівник `pos` тримає позицію наступного ненульового елемента, кожен 
> ненульовий елемент переставляють на `pos` і зсувають `pos`.

Дано масив; перенести всі `0` у кінець, не змінюючи відносний порядок інших елементів, на місці 
(LeetCode "Move Zeroes"). Наївне рішення з окремим списком коштує O(n) додаткової пам'яті; 
оптимальне обходиться O(1).

**Два вказівники**

Індекс `pos` указує, куди покласти наступний ненульовий елемент. Масив проходять одним циклом; 
щойно трапляється ненульове значення, його міняють місцями з елементом на `pos` і збільшують 
`pos`. Нулі внаслідок цього "спливають" у кінець.

```python
def move_zeroes(nums: list[int]) -> None:
    pos = 0                       # next slot for a non-zero element
    for i, n in enumerate(nums):
        if n != 0:
            nums[pos], nums[i] = nums[i], nums[pos]
            pos += 1

a = [0, 1, 0, 3, 12]
move_zeroes(a)
a  # [1, 3, 12, 0, 0]
```

Складність - O(n) часу (один прохід) і O(1) додаткової пам'яті. Інваріант: усе ліворуч від `pos` 
- ненульові елементи у вихідному порядку, між `pos` та `i` - лише нулі.



### Декоратор обмеження частоти викликів (rate limit)

*Summary*
> Декоратор, що дозволяє не більше N викликів за ковзне вікно в 1 секунду, а зайві виклики тихо 
> пропускає. Зберігають часові мітки викликів і відкидають ті, що старші за вікно.

Функцію викликають з багатьох місць, а зовнішній сервіс банить за надто часті звернення. Потрібен 
декоратор, що пропускає максимум N викликів за останню секунду (ковзне вікно), а решту ігнорує.

```python
import time
from collections import deque
from functools import wraps

def rate_limit(max_calls: int, period: float = 1.0):
    def decorator(func):
        calls: deque[float] = deque()
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()             # monotonic clock: never jumps backward (NTP-safe)
            while calls and now - calls[0] >= period:
                calls.popleft()                # drop timestamps outside the window
            if len(calls) >= max_calls:
                return None                    # limit reached -> skip this call
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(3)                                 # at most 3 calls per second
def hit_api(): ...
```

Ключові моменти: `time.monotonic()` (а не `time.time()`, який може стрибнути назад при 
NTP-корекції); одне зчитування часу на виклик; ковзне вікно (старі мітки прибирають), а не 
скидання лічильника на межі секунди.



### Кодування довжин серій (run-length encoding)

*Summary*
> Стиснути рядок, замінивши серії однакових символів на символ + кількість: `"aaabb"` → `"a3b2"`. 
> Один прохід зі станом (поточний символ + лічильник); серію дописують на межі та після циклу.

```python
def rle(s: str) -> str:
    if not s:
        return ""
    out, prev, count = [], s[0], 1
    for ch in s[1:]:
        if ch == prev:
            count += 1
        else:
            out.append(prev + (str(count) if count > 1 else ""))
            prev, count = ch, 1
    out.append(prev + (str(count) if count > 1 else ""))   # flush the final run
    return "".join(out)

rle("aaabbc")  # 'a3b2c'
```

Складність - O(n) часу. Ітерують по символах напряму (не за індексом) і тримають попередній 
символ; критично не забути дописати останню серію після циклу.



### Перевірка анаграми

*Summary*
> Два рядки - анаграми, якщо складаються з тих самих символів у тій самій кількості (різниться 
> лише порядок). Найпростіше - порівняти лічильники символів: `Counter(a) == Counter(b)`.

```python
from collections import Counter

def is_anagram(a: str, b: str) -> bool:
    return len(a) == len(b) and Counter(a) == Counter(b)

is_anagram("listen", "silent")  # True
is_anagram("aab", "abb")        # False - different counts of 'a'/'b'
```

`Counter` враховує і набір символів, і їхню кількість, тому випадок з однаковим набором, але 
різними частотами (`"aab"` vs `"abb"`) коректно дає `False`. Складність - O(n); перевірка довжини 
на початку дає швидкий вихід для рядків різної довжини.



### Two Sum (пара з заданою сумою)

*Summary*
> Знайти два елементи масиву, що дають у сумі `target`. Наївно - O(n²) перебір усіх пар. 
> Оптимально - O(n) через хеш-таблицю: для кожного числа перевіряють, чи трапилося раніше 
> доповнення `target - x`.

Дано масив і число `target`; повернути індекси двох елементів, що дають у сумі `target` 
(LeetCode "Two Sum").

**Хеш-таблиця за один прохід**

Ідуть масивом, тримаючи словник `значення -> індекс` уже побачених. Для кожного `x` шукають 
доповнення `target - x` у словнику: якщо воно там, відповідь знайдено - O(n) часу, O(n) пам'яті.

```python
def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}            # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:           # complement already seen?
            return seen[target - x], i
        seen[x] = i
    return None

two_sum([2, 7, 11, 15], 9)  # (0, 1)
```

Альтернатива для **відсортованого** масиву - два вказівники з обох кінців назустріч (звужують 
діапазон, порівнюючи суму з `target`): O(n) і без додаткової пам'яті, але потребує сортування 
O(n log n), якщо вхід не відсортований. Тому для довільного масиву хеш-таблиця краща; перед 
розв'язанням варто уточнити, чи відсортований вхід.
