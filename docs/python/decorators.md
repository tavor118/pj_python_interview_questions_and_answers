## Decorator - Декоратор

### Що таке декоратори. Навіщо вони потрібні

*Summary*
> **Декоратор** - структурний шаблон проєктування, який дозволяє модифікувати функцію або клас без зміни їхнього вихідного коду. У Python декоратор - це функція, яка приймає іншу функцію або клас як аргумент і повертає модифіковану версію цієї функції або класу.

З допомогою декоратора ми можемо додати код до або після виконання функції. Синтаксис декораторів базується на використанні символу `@`, за яким слідує назва декоратора і перед функцією або класом, який потрібно декорувати.

Основна ідея декораторів полягає в тому, що вони додають додаткову функціональність до існуючої функції або класу, не змінюючи їхнього вихідного коду. Це зроблено шляхом обгортання (wrapping) оригінальної функції або класу в нову функцію або клас, яка виконує додаткову логіку.

Основне використання декораторів включає реалізацію логування, мемоізації, перехоплення виключень, аутентифікації та багато іншого. Завдяки декораторам можна використовувати ці функціональні можливості зокрема для багатьох функцій чи класів, спрощуючи процес розробки та підтримки програмного коду.

Декоратор використовує механізм замикання.

Приклад декоратора в Python, який друкує повідомлення перед виконанням функції.

```python
def decorator(func):  
    def wrapper(*args, **kwargs):  
        print("Some logic before original func")  
        return func(*args, **kwargs)  
    return wrapper  

@decorator  
def my_function():  
    print("Original function")

print(my_function.__name__)  # wrapper # NOTE: because we didn't use wraps
print(my_function.__closure__[0])  # <cell at 0x10...: function object at 0x108e25170>
print(my_function.__closure__[0].cell_contents.__name__)  # my_function
```

*Links*

- [Понимаем декораторы в Python'e, шаг за шагом. Шаг 1](https://habr.com/ru/post/141411/)
- [Понимаем декораторы в Python'e, шаг за шагом. Шаг 2](https://habr.com/ru/post/141501/)


### Що може бути декоратором. До чого можна застосовувати декоратор

Декоратором може бути будь-який callable об'єкт: функція, лямбда, клас, екземпляр класу. У випадку з останнім визначається метод `__call__`.

Декоратор можна застосовувати до будь-якого об'єкта, але найчастіше до функцій, методів і класів. Декорування зустрічається настільки часто, що для нього існує окремий оператор `@`.

```python
def auth_only(view):
    ...

@auth_only
def dashboard(request):
    ...
```

Якби не існувало оператора декорування, ми записали би код вище так:

```python
def auth_only(view):
    ...

def dashboard(request):
    ...

dashboard = auth_only(dashboard)
```

### Що станеться, якщо декоратор не повертає нічого

Якщо в тілі функції немає оператора `return`, виклик верне значення `None`. Проте результат декоратора замінює декорований об'єкт. У випадку якщо декоратор поверне `None`, і функція, яку ми декоруємо, також стане `None`. При спробі викликати її після декорування отримаємо помилку "NoneType is not callable".

### Чим відрізняється `@foobar` від `@foobar()`

Перший випадок - це звичайне декорування функцією foobar.

Другий випадок - декорування функцією, яку поверне виклик foobar. Інакше це називається  параметризований декоратор або фабрика декораторів.


### Що таке фабрика декораторів

Це функція, яка повертає декоратор. Наприклад, вам потрібен декоратор для перевірки прав. Логіка перевірки однакова, але прав може бути багато. Щоб не копіювати код, можна використати фабрику декораторів.

```python
from functools import wraps

def has_perm(perm):
    def decorator(view):
        @wraps(view)
        def wrapper(request):
            if perm in request.user.permissions:
                return view(request)
            else:
                return HTTPRedirect('/login')
        return wrapper
    return decorator

@has_perm('view_user')
def users(request):
    ...
```

Інший спосіб написання фабрики декораторів - використати об'єкт в якості декоратора.

```python
_DEFAULT_RETRIES_LIMIT = 3

class WithRetry:
    def __init__(
        self, 
        retries_limit: int = _DEFAULT_RETRIES_LIMIT, 
        allowed_exceptions: Optional[Sequence[Exception]] = None,
    ) -> None:
        self.retries_limit = retries_limit
        self.allowed_exceptions = allowed_exceptions or (ControlledException,)

    def __call__(self, operation):
        @wraps(operation)
        def wrapped(*args, **kwargs):
            last_raised = None
            for _ in range(self.retries_limit):
                try:
                    return operation(*args, **kwargs)
                except self.allowed_exceptions as e:
                    logger.warning(
                        "retrying %s due to %s", operation.__qualname__, e
                    )
                    last_raised = e
            raise last_raised
        return wrapped

@WithRetry(retries_limit=5)
def run_with_custom_retries_limit(task):
    return task.run()
```


### Декоратор з дефолтними значеннями

Щоб забезпечити можливість викликати декоратор з дефолтними параметрами та без, потрібно розділити два виклики та обробляти в залежності від переданих даних.

```python
def decorator(function=None, *, x=DEFAULT_X, y=DEFAULT_Y):
    if function is None:  # called as `@decorator(...)`
        def decorated(function):
            @wraps(function)
            def wrapped():
                return function(x, y)
            return wrapped
        return decorated
    else:  # called as `@decorator`
        @wraps(function)
        def wrapped():
            return function(x, y)
        return wrapped

@decorator() 
def my function(): 
	...

@decorator 
def my function(): 
	...

@decorator(x=3, y=4) 
def my_function(x, y): 
	return x + y 

my_function() # 7
```

Оскільки параметри є keyword-only, це значно спрощує визначення декоратора, оскільки можна припустити, що функція `None`, коли вона викликається без аргументів (інакше, якби ми передавали значення за позицією, перший із переданих параметрів було б сплутано з функцією).

Іншою альтернативою є застосування `functools.partial` та рекурсивного виклику.

```python
def decorator(function=None, *, x=DEFAULT_X, y=DEFAULT_Y):
    if function is None:        
        return partial(decorator, x=x, y=y)  # or `return lambda f: decorator(f, x=x, y=y)`

    @wraps(function)
    def wrapped():
        return function(x, y)
    
    return wrapped
```


### Навіщо потрібний `wraps`

`wraps` - це декоратор зі стандартного модуля `functools`, який призначає функції-обгортці ті ж самі атрибути `__name__`, `__module__`, `__doc__`, що й у початкової функції, яку декорують. Це потрібно для того, щоб після декорування функція-обгортка в стек-трейсах виглядала як декорована функція.

```python
from functools import wraps
>>> def my_decorator(func):
...     @wraps(func)
...     def wrapper(*args, **kwargs):
...         print('Calling decorated function')
...         return f(*args, **kwargs)
...     return wrapper
...
>>> @my_decorator
... def example():
... """Docstring"""
...     print('Called example function')
...
>>> example()
Calling decorated function
Called example function
>>> example.__name__
'example'
>>> example.__doc__
'Docstring'
```


### Декоратор для корутин

Щоб написати декоратор для корутини, потрібно не забувати дочекатися обгорнутої корутини та присвоїти обгорнутий об'єкт як співпрограму, тобто внутрішня функція, повинна буде використовувати `async def` замість просто `def`.

Проте буде проблема, якщо декоратор потрібно застосувати і до функцій, і до корутин. У більшості випадків найпростіший вихід - створення двох декораторів. Але якщо потрібно надати простіший інтерфейс, можна створити тонку обгортку, яка діятиме як диспетчер для двох внутрішніх декораторів. Це як створити фасад, але з декоратором.

```python
import time
import inspect
from functools import wraps

def timing(callable):
    def wrapped(*args, **kwargs):  # Synchronous wrapper
        start = time.time()
        result = callable(*args, **kwargs)
        latency = time.time() - start
        return {"latency": latency, "result": result}

    async def wrapped_coro(*args, **kwargs):  # Asynchronous wrapper
        start = time.time()
        result = await callable(*args, **kwargs)
        latency = time.time() - start
        return {"latency": latency, "result": result}

    if inspect.iscoroutinefunction(callable):
        return wraps(callable)(wrapped_coro)
    return wraps(callable)(wrapped)
```

Другий wrapper необхідний для корутин. Якщо б його не було, то виникли б дві проблеми. По-перше, виклик callable (без використання `await`) фактично не чекав би завершення операції, що призвело б до некоректних результатів. А також, значення для ключа `result` у словнику не було б власне результатом, а корутиною, яка була створена. В результаті відповідь була б словником, і якщо викликати його, то, намагаючись використати `await` для словника, отримає помилку.

Загалом, слід замінювати декорований об’єкт на інший об’єкт того ж типу: функцію на функцію, а корутину на іншу корутину.

