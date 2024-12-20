## General

### Які основні особливості має Python?

*Summary*

- Python
	- Інтерпретований
	- З динамічною типізацією
	- Об'єктно-орієнтований

- Python - це інтерпретована мова. Це означає, що, на відміну від мов, які потребують компіляції перед запуском, таких як C та його варіанти, Python не потребує компіляції. Інші мови, які також є інтерпретованими, включають PHP та Ruby.
- Python є динамічно типізованою мовою, це означає, що вам не потрібно вказувати типи змінних при їх оголошенні або подібне до цього. Ви можете робити речі, подібні до `x=111`, а потім `x="I'm a string"`, без помилок.
- Python добре підходить для об'єктно-орієнтованого програмування, оскільки воно дозволяє визначати класи разом з композицією та наслідуванням. Python не має специфікаторів доступу (подібних до `public`, `private` у C++).
- У Python, функції є об'єктами першого класу (first-class objects). Це означає, що їх можна присвоювати змінним, повертати з інших функцій і передавати в функції. Класи також є об'єктами першого класу.
- Написання коду Python швидке, але виконання його часто повільніше, ніж у скомпільованих мовах. На щастя, Python дозволяє включати розширення на основі C, так що можна оптимізувати вузькі місця в коді. Пакет [numpy](https://www.edureka.co/blog/python-numpy-tutorial/) є гарним прикладом цього: він дуже швидкий, оскільки багато обчислень здійснюються на С а не власне на Python.


### Що таке компільована мова? Що таке інтерпретована мова?

**Компільована мова програмування** - мова програмування, вихідний код якої перетворюється компілятором в машинний код і записує в файл з особливим заголовком/розширенням, для подальшої ідентифікації цього файлу, як виконуваного операційною системою.

**Компіляція** - збірка програми, яка включає трансляцію всіх модулів програми, написаних на одному чи кількох вихідних мовах програмування в еквівалентні програмні модулі на низькорівневу мову, близьку до машинного коду або на машинному коді.

**Інтерпретована мова** - це мова програмування, код якої перетворюється на виконувані команди безпосередньо під час виконання програми (не перетворюється на машинний код перед виконанням), методом інтерпретації: оператори програми окремо транслюються і відразу виконуються (інтерпретуються) з допомогою інтерпретатора.

**Інтерпретація** - порядковий аналіз, обробка і виконання вихідного коду програми або запиту.

**Машинний код** - система команд, яка інтерпретується безпосередньо процесором.

**Процесор** - електронний блок, який виконує машинні інструкції (код команди).

**Трансляція в байт-код** - проміжний по ефективності між прямою інтерпретацією і компіляцією.

- Компільована vs інтерпретована
	- Швидкість виконання програми, скомпільованої в машинний код, перевищує швидкість інтерпретованої програми
	- При використанні компілятора, при внесенні змін в вихідний код програми, перед тим, як зміни можна побачити, необхідно виконати компіляцію вихідного коду.


### Python декларативний чи імперативний?

*Summary*
> Python є імперативною мовою програмування. В імперативному програмуванні програміст складає послідовність команд, які виконуються комп'ютером. Python також підтримує деякі функціональні та об'єктно-орієнтовані концепції програмування, проте основний підхід у мові є імперативним.

**Імперативна мова** - це мова програмування, яка використовує прямі команди для керування комп'ютером, на відміну від
декларативних мов. У імперативних мовах програміст явно описує дії, які необхідно виконати комп'ютеру, а чи не просто визначає бажаний результат. Приклади імперативних мов програмування це Java, C, C++, Python та JavaScript.

**Декларативна мова** – це мова програмування, яка призначає технічну реалізацію системи або програми для досягнення певної мети, але не вказує на конкретні кроки для її виконання. Натомість ви визначаєте, яка інформація має бути оброблена, а система сама визначає, як вирішити цю проблему. Прикладами декларативних мов є SQL для роботи з базами даних та HTML для створення веб-сторінок. Такі мови зазвичай використовуються у випадках, коли важливіше задати бажаний результат, ніж вказати, як досягти цього результату


### Що таке статична і динамічна типізація і як це виявляється в Python?

Статична типізація - це підхід до типізації, де типи змінних визначаються під час компіляції програми і залишаються незмінними під час виконання. Динамічна типізація, натомість, дозволяє змінювати типи змінних під час виконання програми.

У Python використовується динамічна типізація. Це означає, що можна створювати змінні без явної вказівки типу, і їх тип буде визначатися автоматично під час присвоєння значень. Також можна змінювати тип змінної під час виконання програми. Наприклад, змінна може спочатку містити число, а потім рядок.

Це дає більшу гнучкість, але також може спричинити помилки виконання через неправильне використання типів. Тому важливо бути уважним та дбайливо перевіряти типи даних при розробці програм на Python.

Завдяки модулю `typing` у Python можна вказати типи аргументів функцій, значень, атрибутів тощо. Це необов'язковий, але корисний підхід, який дозволяє зробити код більш зрозумілим і зменшити кількість помилок, пов'язаних з неправильними типами даних.

Крім того, інструменти, такі як `mypy`, можуть бути використані для статичної перевірки типів у коді. `mypy` допомагає виявляти потенційні помилки типів перед виконанням програми, що допомагає уникнути часто помилок, які часто зустрічаються, та поліпшити стабільність і надійність програми.


### Варіанти реалізації шаблону Singleton у Python

**Декоратор**

```python
def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class MyClass(BaseClass):
    pass
```

Переваги
- Декоратори часто є більш інтуїтивно зрозумілими, ніж множинне успадкування.
Недоліки
- Хоча об'єкти, створені за допомогою `MyClass()`, будуть справжніми singleton об'єктами, сам `MyClass` є функцією, а не класом, тому ви не можете викликати методи класу з нього.
- Ускладнює тестування.

**Базовий клас**

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

class MyClass(Singleton, BaseClass):
    pass
```

Переваги
- Це справжній клас.
Недоліки
- Множинне успадкування ускладнює код. `__new__` може бути перезаписаний під час успадкування від другого базового класу

**Метакласи**

```python
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(BaseClass, metaclass=Singleton):
	pass
```

Переваги
- Це справжній клас.
- Автоматично застосовується при наслідуванні.
- Використовує метакласи за їхнім прямим призначенням.
Недоліки
- Немає

*Links*

- [Creating a singleton in Python](https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python)


### Що таке "monkey patching"?

"Monkey patching" означає динамічні зміни класів або модулів під час виконання програми. Це дозволяє розробникам змінювати або доповнювати функціональність об'єктів або модулів без внесення змін у вихідний код. Простіше кажучи, "monkey patching" дозволяє змінювати програмний код вже після того, як він був написаний.

```python
class MyClass:
    def original_method(self):
        print("Original method")

def new_method(self):
    print("Patched method")

obj = MyClass()
obj.original_method()  # Outputs: Original method

obj.original_method = new_method
obj.original_method()  # Patched method

```


### Що таке інтроспекція

*Summary*
> **Інтроспекція** - це здатність програми досліджувати і вивчати структуру, властивості та атрибути об'єктів під час виконання програми. Це дозволяє отримати доступ до типу об'єкта, перевірити його атрибути, методи та інші характеристики.

У Python є кілька вбудованих функцій та методів, які допомагають здійснювати інтроспекцію
- `type()`: Функція `type()` повертає тип об'єкта. Наприклад, `type(obj)` поверне тип `obj`.
- `dir()`: Функція `dir()` повертає список атрибутів та імені, доступних у заданому об'єкті. Наприклад, `dir(obj)` поверне список імен атрибутів obj.
- `getattr()`: Функція `getattr()` дозволяє отримати значення атрибута об'єкта за його ім'ям. Наприклад, `getattr(obj, 'attribute')` поверне значення атрибута з ім'ям `'attribute'` у `obj`.
- `hasattr()`: Функція `hasattr()` перевіряє, чи має об'єкт атрибут з заданим ім'ям. Наприклад, `hasattr(obj, 'attribute')` поверне True, якщо `obj` має атрибут з ім'ям `'attribute'`, і `False` - в іншому випадку.
- `callable()`: Функція `callable()` перевіряє, чи можна викликати (використовувати як функцію) заданий об'єкт. Наприклад, `callable(obj)` поверне `True`, якщо `obj` можна викликати, і `False` - в іншому випадку.

```python
class Foo():
	def __init__(self, val):
		self.x = val
	def bar(self):
		return self.x

dir(foo(5))
=> ['__class__', '__delattr__', '__dict__', '__doc__', '__getattribute__', '__hash__', '__init__', '__module__',
'__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__str__', '__weakref__', 'bar', 'x']
```

Ці функції та методи допомагають отримати інформацію про типи, атрибути та властивості об'єктів під час виконання програми, що дає можливість розробникам аналізувати та взаємодіяти з кодом більш гнучко та динамічно.

Модуль `inspect` надає функції для отримання інформації про об'єкт, включаючи функції. Функція `inspect.signature()` повертає об'єкт `Signature`, який містить інформацію про аргументи функції.

```python
import inspect

def add(x: int, y: int) -> int:
    return x + y

signature = inspect.signature(add)
print(signature)  # (x: int, y: int) -> int
```

За допомогою сигнатури функції можна отримати інформацію про аргументи, їх імена, типи та значення за замовчуванням через властивість `parameters` об'єкта `Signature`:

```python
for parameter in signature.parameters.values():
    print(parameter.name, ':', parameter.annotation)
>>> x : <class 'int'>
>>> y : <class 'int'>
```

*Links*

- [Introspection in Python](http://zetcode.com/lang/python/introspection/)


### Що таке рефлексія

Інтроспекція дозволяє вивчати атрибути об'єкта під час виконання програми, а рефлексія - маніпулювати ними. Рефлексія - це здатність комп'ютерної програми вивчати і модифікувати свою структуру і поведінку (значення, метадані, властивості та функції) під час виконання. Простою мовою: вона дозволяє викликати методи об'єктів, створювати нові об'єкти, модифікувати їх навіть без знання імен інтерфейсів, полів, методів.

```python
Foo().hello()  # without reflection
getattr(globals()['Foo'](), 'hello')()  # with reflection
```
