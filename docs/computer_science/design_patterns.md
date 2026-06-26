## Design Patterns (GoF)

### Design Patterns (GoF) - Overview

*Summary*
> 23 патерни проектування "Банди чотирьох" (Gang of Four) - типові рішення повторюваних
> задач ООП, поділені на три групи за призначенням: **породжувальні** (як створювати об'єкти),
> **структурні** (як компонувати їх у більші структури) та **поведінкові** (як об'єкти
> взаємодіють і розподіляють відповідальність).

**Породжувальні (Creational)** - як створювати об'єкти, відв'язавши код від конкретних класів:

- **Factory Method** - делегує створення об'єкта підкласам через перевизначений метод; клієнт працює з інтерфейсом, не знаючи конкретного класу.
- **Abstract Factory** - створює сімейства пов'язаних об'єктів через єдиний інтерфейс, не прив'язуючись до конкретних класів.
- **Builder** - покроково збирає складний об'єкт, відокремлюючи конструювання від кінцевого представлення.
- **Prototype** - створює нові об'єкти клонуванням наявного зразка замість конструювання з нуля.
- **Singleton** - гарантує єдиний екземпляр класу та глобальну точку доступу до нього.

**Структурні (Structural)** - як компонувати об'єкти у більші структури:

- **Adapter** - перекладає інтерфейс одного класу на той, який очікує клієнт.
- **Bridge** - розділяє абстракцію та реалізацію, щоб змінювати їх незалежно.
- **Composite** - компонує об'єкти в деревоподібну ієрархію, де лист і контейнер мають однаковий інтерфейс.
- **Decorator** - динамічно додає об'єкту нову поведінку, обгортаючи його іншим об'єктом того ж інтерфейсу.
- **Facade** - надає спрощений єдиний інтерфейс до складної підсистеми.
- **Flyweight** - розділяє спільний стан між багатьма об'єктами, щоб економити пам'ять.
- **Proxy** - підставляє замісник, що контролює доступ до реального об'єкта (лінива ініціалізація, кеш, права).

**Поведінкові (Behavioral)** - як об'єкти взаємодіють і розподіляють відповідальність:

- **Chain of Responsibility** - передає запит ланцюгом обробників, доки один не впорається з ним.
- **Command** - інкапсулює запит як об'єкт, даючи змогу ставити дії в чергу, логувати та скасовувати їх.
- **Interpreter** - задає граматику мови й обчислює вирази за деревом її правил.
- **Iterator** - надає послідовний доступ до елементів колекції, не розкриваючи її внутрішню структуру.
- **Mediator** - централізує взаємодію об'єктів у посереднику, прибираючи прямі зв'язки між ними.
- **Memento** - зберігає та відновлює внутрішній стан об'єкта, не порушуючи інкапсуляції.
- **Observer** - сповіщає набір підписників про зміну стану суб'єкта.
- **State** - змінює поведінку об'єкта зі зміною внутрішнього стану, ніби змінюється його клас.
- **Strategy** - інкапсулює взаємозамінні алгоритми й дозволяє підставляти їх під час виконання.
- **Template Method** - задає скелет алгоритму в базовому класі, лишаючи окремі кроки підкласам.
- **Visitor** - виносить операцію над елементами структури в окремий об'єкт, не змінюючи їхніх класів.

**Застереження для Python.** Частину GoF-патернів у Python реалізують помітно простіше, бо функції
та класи - об'єкти першого класу: Strategy - переданою функцією замість ієрархії класів, Factory -
переданим класом-callable, Iterator - протоколом `__iter__`/генераторами, Command - замиканням,
Flyweight - через `functools.lru_cache`, Visitor - через `functools.singledispatch`. Це спрощує
реалізацію, але не скасовує самих патернів - контекст і ролі лишаються тими самими. Структурний
GoF-**Decorator не плутати** із синтаксисом `@decorator`.

**Об'єкт першого класу** (first-class citizen) - сутність, яку мова дозволяє використовувати
без обмежень: присвоїти змінній, передати в функцію як аргумент, повернути з функції та
зберегти в структурі даних (список, словник). У Python функції та класи - повноцінні об'єкти
першого класу нарівні з числами чи рядками, тому їх можна передавати й підставляти напряму.
Саме це усуває потребу в бойлерплейті, яким у мовах без цієї властивості (як-от класична Java)
обгортають поведінку в об'єкт, щоб передати її туди, де приймається лише об'єкт - сам патерн при
цьому нікуди не зникає.

*Links*

- [refactoring.guru: Design Patterns](https://refactoring.guru/design-patterns) - інтенти, структури та відносини між патернами
- [faif/python-patterns](https://github.com/faif/python-patterns) - колекція реалізацій патернів ідіоматичним Python
- [python-patterns.guide (Brandon Rhodes)](https://python-patterns.guide/) - Pythonic-погляд на GoF та патерни, специфічні для Python



### Factory Method (Фабричний метод)

*Summary*
> Породжувальний патерн: визначає інтерфейс створення об'єкта, але дозволяє підкласам
> вирішувати, який саме клас інстанціювати. Делегує створення підкласам через
> перевизначений метод-фабрику.

**Принцип роботи**

Базовий клас містить метод, що повертає об'єкт продукту, не називаючи конкретний клас прямо;
підкласи перевизначають цей метод і повертають свій тип. Клієнтський код працює з абстрактним
продуктом і не залежить від конкретних класів.

```python
from abc import ABC, abstractmethod


class Exporter(ABC):
    @abstractmethod
    def serialize(self, data: dict) -> str: ...


class JsonExporter(Exporter):
    def serialize(self, data):
        return json.dumps(data)


class Report(ABC):
    @abstractmethod
    def make_exporter(self) -> Exporter: ...  # factory method

    def export(self, data):
        return self.make_exporter().serialize(data)


class JsonReport(Report):
    def make_exporter(self):
        return JsonExporter()
```

У Python часто достатньо передати сам клас або функцію як callable, тому повноцінна ієрархія
фабрик потрібна лише за складної логіки вибору продукту.

**Class Attribute Factory і Instance Attribute Factory.** Замість підкласу, що перевизначає
метод-фабрику, продукт-клас зберігають як атрибут. У `http.client.HTTPConnection` це атрибут класу
`response_class = HTTPResponse`: щоб підмінити тип відповіді, успадковують клас і задають свій
`response_class`. Гнучкіший варіант - атрибут екземпляра, переданий у конструктор: `json.JSONDecoder`
приймає `parse_float`, тож кастомний парсер чисел задається без підкласу взагалі.

```python
from decimal import Decimal
from json import JSONDecoder

decoder = JSONDecoder(parse_float=Decimal)  # instance attribute factory - no subclass needed
print(decoder.decode('{"x": 1.5}'))  # {'x': Decimal('1.5')}
```

Атрибут екземпляра перекриває атрибут класу, а приймається будь-який callable - клас, функція,
`functools.partial`, alternative constructor, - бо інстанціювання в Python виглядає як звичайний виклик.

**У Python-екосистемі.** Поля моделей Django: базовий `Field.formfield()` повертає форму за
замовчуванням, а підкласи перевизначають його під свій тип - класичний фабричний метод.

```python
from django.db import models

# formfield() is overridden per field type to build the matching form widget:
print(type(models.DateField().formfield()))  # <class 'django.forms.fields.DateField'>
print(type(models.EmailField().formfield()))  # <class 'django.forms.fields.EmailField'>
```

*Links*

- [refactoring.guru: Factory method](https://refactoring.guru/design-patterns/factory-method)
- [Wikipedia: Factory method pattern](https://en.wikipedia.org/wiki/Factory_method_pattern)
- [SourceMaking: Factory method](https://sourcemaking.com/design_patterns/factory_method)
- [Amir Lavasani: Factory Method (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-factory-method-1882d9a06cb4)
- [python-patterns.guide: The Factory Method Pattern](https://python-patterns.guide/gang-of-four/factory-method/)



### Abstract Factory (Абстрактна фабрика)

*Summary*
> Породжувальний патерн: надає інтерфейс для створення сімейств пов'язаних об'єктів без
> прив'язки до їхніх конкретних класів. Гарантує сумісність продуктів одного сімейства.

**Принцип роботи**

Фабрика оголошує методи для кожного типу продукту; конкретні фабрики реалізують ці методи
узгодженим набором (наприклад, віджети під різні ОС). Клієнт отримує фабрику і створює всі
об'єкти через неї, лишаючись незалежним від конкретного сімейства.

```python
class GuiFactory(ABC):
    @abstractmethod
    def button(self) -> Button: ...
    @abstractmethod
    def checkbox(self) -> Checkbox: ...


class MacFactory(GuiFactory):
    def button(self):
        return MacButton()

    def checkbox(self):
        return MacCheckbox()


def build_form(factory: GuiFactory):  # client depends only on the interface
    return factory.button(), factory.checkbox()
```

Відрізняється від Factory Method масштабом: Factory Method створює **один** продукт,
Abstract Factory - **сімейство** узгоджених продуктів.

**У Python-екосистемі.** Бекенд БД у Django: під вибраний `ENGINE` об'єкт `connection` віддає
узгоджене сімейство пов'язаних об'єктів - курсор, операції, інтроспекцію.

```python
from django.db import connection  # backend chosen by DATABASES["ENGINE"]

cur = connection.cursor()  # one product of the backend family
sql = connection.ops.quote_name("users")  # another product, same backend
# the sqlite / postgres / mysql backends each supply a matching family of objects
```

*Links*

- [refactoring.guru: Abstract factory](https://refactoring.guru/design-patterns/abstract-factory)
- [Wikipedia: Abstract factory pattern](https://en.wikipedia.org/wiki/Abstract_factory_pattern)
- [SourceMaking: Abstract factory](https://sourcemaking.com/design_patterns/abstract_factory)



### Builder (Будівельник)

*Summary*
> Породжувальний патерн: відокремлює конструювання складного об'єкта від його представлення,
> дозволяючи будувати об'єкт покроково й отримувати різні представлення тим самим процесом.

**Принцип роботи**

Будівельник надає методи для поетапного налаштування частин об'єкта і фінальний метод
`build()`, що повертає готовий результат. Корисний, коли конструктор мав би десятки
параметрів або коли потрібні різні конфігурації того самого продукту.

```python
class QueryBuilder:
    def __init__(self):
        self._parts = {"where": [], "limit": None}

    def where(self, cond):
        self._parts["where"].append(cond)
        return self  # fluent

    def limit(self, n):
        self._parts["limit"] = n
        return self

    def build(self) -> str:
        sql = "SELECT * FROM t"
        if self._parts["where"]:
            sql += " WHERE " + " AND ".join(self._parts["where"])
        if self._parts["limit"]:
            sql += f" LIMIT {self._parts['limit']}"
        return sql


QueryBuilder().where("age > 18").limit(10).build()
```

У Python альтернатива простим білдерам - keyword-аргументи з дефолтами або `dataclasses`.
На відміну від Abstract Factory, що одразу повертає готові об'єкти сімейства, Builder
конструює один складний об'єкт покроково і повертає його наприкінці.

**У Python-екосистемі.** SQLAlchemy Core (`select().where().order_by()`) і `QuerySet` Django
(`.filter().exclude().order_by()`) - ланцюжкові білдери: кожен виклик повертає новий незавершений
об'єкт, а матеріалізація в SQL відкладена до кінця.

```python
from sqlalchemy import select, table, column

t = table("users", column("id"), column("name"))
stmt = select(t.c.name).where(t.c.id > 10).order_by(t.c.name)  # step-by-step build
print(stmt)  # SELECT users.name FROM users WHERE users.id > :id_1 ORDER BY users.name
```

*Links*

- [refactoring.guru: Builder](https://refactoring.guru/design-patterns/builder)
- [Wikipedia: Builder pattern](https://en.wikipedia.org/wiki/Builder_pattern)
- [SourceMaking: Builder](https://sourcemaking.com/design_patterns/builder)
- [Amir Lavasani: Builder (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-builder-0732552324b1)



### Prototype (Прототип)

*Summary*
> Породжувальний патерн: створює нові об'єкти копіюванням наявного екземпляра-прототипу,
> а не побудовою з нуля. Корисний, коли інстанціювання дороге або конфігурація складна.

**Принцип роботи**

Об'єкт уміє клонувати себе; новий екземпляр отримують копіюванням готового зразка з потрібним
станом. У Python реалізується через модуль `copy` - `copy.copy` (поверхнева) і `copy.deepcopy`
(глибока копія).

```python
import copy


class Document:
    def __init__(self, styles):
        self.styles = styles

    def clone(self):
        return copy.deepcopy(self)


template = Document(styles={"font": "Inter"})
page = template.clone()  # independent copy with the same setup
```

Різниця поверхневої та глибокої копії - у [`python/syntax.md`](../python/syntax.md).

**У Python-екосистемі.** Модуль `copy` - пряма реалізація Prototype: `copy.copy`/`copy.deepcopy`
клонують готовий зразок, а спеціальні методи `__copy__`/`__deepcopy__` налаштовують цей процес під конкретний клас.

```python
import copy

base_config = {"retries": 3, "hooks": []}
job = copy.deepcopy(base_config)  # clone the prototype - fully independent state
job["hooks"].append("notify")
print(base_config["hooks"], job["hooks"])  # [] ['notify']
# dataclasses.replace(obj, ...) similarly clones with field overrides
```

*Links*

- [refactoring.guru: Prototype](https://refactoring.guru/design-patterns/prototype)
- [Wikipedia: Prototype pattern](https://en.wikipedia.org/wiki/Prototype_pattern)
- [SourceMaking: Prototype](https://sourcemaking.com/design_patterns/prototype)
- [Amir Lavasani: Prototype (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-prototype-6aeeda10f41e)



### Singleton (Одинак)

*Summary*
> Породжувальний патерн: гарантує, що клас має лише один екземпляр, і надає глобальну точку
> доступу до нього. У Python природна заміна - модуль (він кешується в `sys.modules`).

**Принцип роботи**

Клас контролює власне інстанціювання, повертаючи той самий об'єкт при кожному виклику. Типові
реалізації - перевизначення `__new__`, метаклас або декоратор; найпростіша й найідіоматичніша
- модуль-одинак.

```python
class Settings:
    _instance = None

    def __new__(cls, *a, **kw):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

Варіанти реалізації (метаклас, декоратор, модуль) і їхні компроміси -
[`python/general.md`](../python/general.md). Singleton часто критикують як прихований
глобальний стан, що ускладнює тестування.

**"Singleton" у Python - перевантажений термін.** Слово вживають у кількох різних значеннях:
(1) кортеж довжини 1 (термінологія документації); (2) модуль - імпорт кешує єдиний об'єкт у
`sys.modules`; (3) **flyweight** - спільні незмінні значення, яких більше одного на клас: `True`/
`False` (`bool` має рівно два екземпляри), малі цілі `-5..256`, порожні `str`/`tuple`; їх
кешують заради економії, але це не Singleton, бо клас має й інші екземпляри; (4) **well-known
об'єкт** - єдиний екземпляр свого класу з глобальним іменем: `None` (єдиний екземпляр `NoneType`; у
Python 3 навіть `type(None)()` повертає той самий `None`), `Ellipsis` - це найближче до Singleton;
(5) **класичний GoF-Singleton** - звичайний клас, штучно обмежений одним екземпляром через
`__new__` чи метаклас. Тому `None` коректно вважати singleton-подібним well-known об'єктом, а
`True`/`False` - це флайвейти, не Singleton'и.

**У Python-екосистемі.** Імпортований модуль (кешується у `sys.modules`) і `logging.getLogger(name)`
(один `Logger` на ім'я) - готові одинаки, які мова забезпечує без додаткового коду.

```python
import logging, sys

a = logging.getLogger("app")
b = logging.getLogger("app")
print(a is b)  # True - logging keeps one Logger per name
print("logging" in sys.modules)  # True - the imported module is itself a singleton
```

*Links*

- [refactoring.guru: Singleton](https://refactoring.guru/design-patterns/singleton)
- [Wikipedia: Singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern)
- [SourceMaking: Singleton](https://sourcemaking.com/design_patterns/singleton)
- [Amir Lavasani: Singleton (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-singleton-5095a4c14f)
- [python-patterns.guide: The Singleton Pattern](https://python-patterns.guide/gang-of-four/singleton/)



### Adapter (Адаптер)

*Summary*
> Структурний патерн: перетворює інтерфейс одного класу на інтерфейс, який очікує клієнт.
> Дозволяє співпрацювати класам із несумісними інтерфейсами.

**Принцип роботи**

Адаптер обгортає об'єкт і транслює виклики його методів до інтерфейсу, потрібного клієнту.
Застосовується для інтеграції стороннього або legacy-коду без його зміни.

```python
class LegacyPrinter:
    def print_text(self, s):
        print(s)


class PrinterAdapter:  # target interface: write()
    def __init__(self, legacy):
        self._legacy = legacy

    def write(self, s):
        self._legacy.print_text(s)
```

Показаний варіант - **object adapter**: адаптер тримає посилання на адаптований об'єкт і делегує
йому виклики. Альтернатива GoF - **class adapter** через множинне успадкування (адаптер успадковує
і цільовий інтерфейс, і адаптований клас). У Python можливі обидва, але перевагу зазвичай надають
object adapter як гнучкішому: він працює з будь-яким екземпляром і не прив'язаний до конкретного
класу під час визначення.

На відміну від Bridge, який розводить абстракцію та реалізацію **за задумом наперед**,
Adapter узгоджує **вже наявні** несумісні інтерфейси заднім числом. На відміну від Decorator,
що зберігає інтерфейс об'єкта і додає поведінку, Adapter **змінює інтерфейс**, не додаючи
нової функціональності.

**У Python-екосистемі.** `io.TextIOWrapper` адаптує байтовий потік до текстового файлового API;
DB-API-драйвери дають спільний інтерфейс над різними БД.

```python
import io

raw = io.BytesIO(b"line\n")  # byte-level interface
text = io.TextIOWrapper(raw, encoding="utf-8")  # adapts it to a text-file API
print(text.readline())  # 'line\n'
```

*Links*

- [refactoring.guru: Adapter](https://refactoring.guru/design-patterns/adapter)
- [Wikipedia: Adapter pattern](https://en.wikipedia.org/wiki/Adapter_pattern)
- [SourceMaking: Adapter](https://sourcemaking.com/design_patterns/adapter)
- [Amir Lavasani: Adapter (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-adapter-58eb7cc11474)



### Bridge (Міст)

*Summary*
> Структурний патерн: розділяє абстракцію та її реалізацію на дві незалежні ієрархії, щоб
> кожну можна було розвивати окремо. Уникає комбінаторного вибуху підкласів.

**Принцип роботи**

Абстракція містить посилання на об'єкт реалізації та делегує йому роботу (композиція замість
наслідування). Якщо є M абстракцій і N реалізацій, замість M*N підкласів отримують M+N класів.

```python
class Renderer(ABC):  # implementation hierarchy
    @abstractmethod
    def draw_circle(self, r): ...


class SvgRenderer(Renderer):
    def draw_circle(self, r):
        return f"<circle r={r}/>"


class Shape:  # abstraction holds a renderer
    def __init__(self, renderer: Renderer):
        self.renderer = renderer


class Circle(Shape):
    def __init__(self, renderer, r):
        super().__init__(renderer)
        self.r = r

    def draw(self):
        return self.renderer.draw_circle(self.r)
```

**У Python-екосистемі.** SQLAlchemy: незмінне Core/ORM-API (абстракція) працює поверх змінних
діалектів і драйверів (реалізація) - зміна URL у `create_engine` міняє реалізацію, не зачіпаючи
самі запити.

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite://")  # swap impl: "postgresql+psycopg://...", "mysql+pymysql://..."
with engine.connect() as conn:
    print(conn.execute(text("SELECT 1")).scalar())  # 1
# the Core/ORM API is bridged onto whatever dialect+driver the URL names
```

*Links*

- [refactoring.guru: Bridge](https://refactoring.guru/design-patterns/bridge)
- [Wikipedia: Bridge pattern](https://en.wikipedia.org/wiki/Bridge_pattern)
- [SourceMaking: Bridge](https://sourcemaking.com/design_patterns/bridge)
- [Amir Lavasani: Bridge (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-bridge-c34f3fcdd2eb)



### Composite (Компонувальник)

*Summary*
> Структурний патерн: компонує об'єкти у деревоподібні структури та дозволяє працювати з
> окремим об'єктом і з групою об'єктів однаково.

**Принцип роботи**

Спільний інтерфейс мають і "листок" (окремий об'єкт), і "композит" (контейнер дочірніх
елементів); композит делегує операцію всім дітям рекурсивно. Клієнт не розрізняє лист і вузол.

```python
class Node(ABC):
    @abstractmethod
    def size(self) -> int: ...


class File(Node):
    def __init__(self, n):
        self.n = n

    def size(self):
        return self.n


class Folder(Node):
    def __init__(self):
        self.children = []

    def size(self):
        return sum(c.size() for c in self.children)  # recurse
```

Канонічні приклади: файлова система, DOM, дерево UI-компонентів.

**У Python-екосистемі.** `xml.etree.ElementTree.Element` побудований за Composite: той самий вузол
є і листом, і контейнером - його однаково ітерують через `for` і нарощують через `append`/`SubElement`.
Дерева віджетів `tkinter`/Qt влаштовані так само.

```python
import xml.etree.ElementTree as ET

ul = ET.Element("ul")
for item in ("a", "b"):
    ET.SubElement(ul, "li").text = item  # leaf elements added to the container
print(ET.tostring(ul).decode())  # <ul><li>a</li><li>b</li></ul>
```

*Links*

- [refactoring.guru: Composite](https://refactoring.guru/design-patterns/composite)
- [Wikipedia: Composite pattern](https://en.wikipedia.org/wiki/Composite_pattern)
- [SourceMaking: Composite](https://sourcemaking.com/design_patterns/composite)
- [Amir Lavasani: Composite (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-composite-09eba144f65e)



### Decorator (Декоратор - структурний)

*Summary*
> Структурний патерн: динамічно додає об'єкту нову поведінку, обгортаючи його в об'єкт-обгортку
> зі спільним інтерфейсом. Гнучка альтернатива наслідуванню для розширення функціональності.

**Принцип роботи**

Обгортка реалізує той самий інтерфейс, що й об'єкт, який вона огортає, делегує йому виклик і
додає поведінку до або після. Обгортки можна вкладати одна в одну.

```python
class Stream(ABC):
    @abstractmethod
    def write(self, data: bytes): ...


class GzipStream(Stream):  # wrapper adds behavior
    def __init__(self, wrapped: Stream):
        self._w = wrapped

    def write(self, data):
        self._w.write(gzip.compress(data))
```

**Не плутати** із синтаксисом `@decorator` у Python - це різні поняття, хоча ідея обгортання
спільна. Декоратори-функції - у [`python/decorators.md`](../python/decorators.md).

**Динамічна обгортка і її межі.** Коли об'єкт не можна успадкувати (його повертає чужий код),
обгортку часто роблять динамічною: замість делегування кожного методу вручну перевизначають
`__getattr__`/`__setattr__`/`__delattr__` і переадресовують доступ до обгорнутого об'єкта. Дві
застороги. По-перше, дандер-методи шукаються на класі, а не на екземплярі, тож `__iter__`,
`__next__`, `__len__` тощо `__getattr__` не перехопить - їх доводиться оголошувати на обгортці
явно. По-друге, для інтроспекції обгортка не є тим самим об'єктом: `isinstance`, `type()`, `dir()`
і доступ до приватних атрибутів покажуть розбіжність. Тому в Python Decorator надійний для виклику
методів, але не там, де код-споживач інтроспектує сам об'єкт.

**У Python-екосистемі.** Обгортки потоків `io` (`BufferedReader`, `BufferedWriter`,
`gzip.GzipFile`) огортають базовий потік, зберігаючи його байтовий інтерфейс і додаючи
буферизацію чи стиснення. WSGI-middleware огортає застосунок так само.

```python
import io, gzip

buf = io.BytesIO()
gz = gzip.GzipFile(fileobj=buf, mode="wb")  # wraps the stream: same write(), adds compression
gz.write(b"hello")
gz.close()
print(buf.getvalue()[:2])  # b'\x1f\x8b' - gzip magic, behavior added transparently
```

*Links*

- [refactoring.guru: Decorator](https://refactoring.guru/design-patterns/decorator)
- [Wikipedia: Decorator pattern](https://en.wikipedia.org/wiki/Decorator_pattern)
- [SourceMaking: Decorator](https://sourcemaking.com/design_patterns/decorator)
- [Amir Lavasani: Decorator (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-decorator-c882c0db6501)
- [python-patterns.guide: The Decorator Pattern](https://python-patterns.guide/gang-of-four/decorator-pattern/)



### Facade (Фасад)

*Summary*
> Структурний патерн: надає єдиний спрощений інтерфейс до складної підсистеми з багатьох
> класів. Приховує внутрішню складність за однією точкою входу.

**Принцип роботи**

Фасад агрегує виклики до кількох підсистемних об'єктів у прості високорівневі методи. Клієнт
працює з фасадом, не знаючи деталей; за потреби досвідчений код усе одно може звертатися до
підсистем напряму.

```python
class OrderFacade:
    def __init__(self):
        self.pay, self.stock, self.mail = Payment(), Stock(), Mailer()

    def checkout(self, cart, user):  # one call hides three subsystems
        self.stock.reserve(cart)
        self.pay.charge(user, cart.total)
        self.mail.send_receipt(user)
```

**У Python-екосистемі.** `subprocess.run` - фасад над `Popen` (труби, `wait()`, коди повернення);
`requests` - фасад над `urllib3`; `pathlib.Path` спрощує розсип функцій `os`/`os.path`.

```python
import subprocess

r = subprocess.run(["echo", "hi"], capture_output=True, text=True)  # one call = the facade
print(r.stdout.strip())  # hi
# hides Popen construction, pipe wiring, wait() and return-code handling
```

*Links*

- [refactoring.guru: Facade](https://refactoring.guru/design-patterns/facade)
- [Wikipedia: Facade pattern](https://en.wikipedia.org/wiki/Facade_pattern)
- [SourceMaking: Facade](https://sourcemaking.com/design_patterns/facade)
- [Amir Lavasani: Facade (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-facade-0043afc9aa4a)



### Flyweight (Легковаговик)

*Summary*
> Структурний патерн: економить пам'ять, розділяючи спільний незмінний стан між багатьма
> дрібними об'єктами замість зберігання його копії в кожному.

**Принцип роботи**

Внутрішній (незмінний, спільний) стан виносять у розділюваний об'єкт-флайвейт і кешують;
зовнішній (унікальний) стан передають у методи ззовні. Так мільйони об'єктів посилаються на
жменю спільних екземплярів.

```python
import functools


@functools.lru_cache(maxsize=None)  # share one glyph per char
def glyph(char: str) -> "Glyph":
    return Glyph(char)  # intrinsic state, created once
```

Інтернування малих рядків і кеш малих цілих (`-5..256`) у CPython - прояв тієї ж ідеї.

**Три ознаки флайвейта.** Об'єкт безпечно розділяти, якщо він (1) незмінний - інакше зміна
вплине на всіх власників спільної копії; (2) не несе зовнішнього контексту, тобто не пам'ятає, де
його використовують; (3) важливий значенням, а не ідентичністю (його порівнюють через `==`, не
`is`). Рядки й малі цілі задовольняють усі три.

**Фабрика чи конструктор.** GoF роздавали флайвейти лише фабрикою (як `sys.intern`), але в Python
кеш часто переносять у сам конструктор: `bool(0) is False`, `bool(12) is True` (тип `bool` має
рівно два екземпляри), а цілі `-5..256` повертаються вже готовими. `None` сюди **не** належить: він
єдиний екземпляр `NoneType`, тобто well-known об'єкт / Singleton, а флайвейт потребує більш ніж
одного екземпляра класу.

**У Python-екосистемі.** Кеш малих цілих CPython (`-5..256`), інтернування рядків (`sys.intern`,
ідентифікатори) та `True`/`False` з порожніми `str`/`tuple` - розділення спільних незмінних об'єктів.

```python
import sys

a, b = 256, 256
print(a is b)  # True - CPython caches small ints in [-5, 256]
k1, k2 = sys.intern("repeated_key"), sys.intern("repeated_key")
print(k1 is k2)  # True - one shared string instance (flyweight)
```

*Links*

- [refactoring.guru: Flyweight](https://refactoring.guru/design-patterns/flyweight)
- [Wikipedia: Flyweight pattern](https://en.wikipedia.org/wiki/Flyweight_pattern)
- [SourceMaking: Flyweight](https://sourcemaking.com/design_patterns/flyweight)
- [Amir Lavasani: Flyweight (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-flyweight-e7a7334f82b1)
- [python-patterns.guide: The Flyweight Pattern](https://python-patterns.guide/gang-of-four/flyweight/)



### Proxy (Замісник)

*Summary*
> Структурний патерн: підставляє об'єкт-замісник з тим самим інтерфейсом, що контролює доступ
> до реального об'єкта - для лінивого створення, кешування, контролю прав чи логування.

**Принцип роботи**

Проксі реалізує інтерфейс реального об'єкта і делегує йому виклики, додаючи проміжну логіку.
Види: virtual (лінива ініціалізація дорогого об'єкта), protection (перевірка прав), remote
(виклик віддаленого об'єкта), caching.

```python
class ImageProxy:
    def __init__(self, path):
        self.path, self._real = path, None

    def render(self):
        if self._real is None:  # lazy-load on first use (virtual proxy)
            self._real = HeavyImage(self.path)
        return self._real.render()
```

Відрізняється від Decorator метою: Decorator **додає поведінку**, Proxy **керує доступом**;
структурно вони схожі.

**У Python-екосистемі.** `flask.request`/`current_app` - це `LocalProxy` (Werkzeug) до
контекстно-локального об'єкта; Django `SimpleLazyObject` ліниво матеріалізує `request.user`;
`weakref.proxy`; ліниві relationship у SQLAlchemy.

```python
from werkzeug.local import LocalProxy, LocalStack

_stack = LocalStack()
request = LocalProxy(lambda: _stack.top["request"])  # the proxy object


class Req:
    method = "GET"


_stack.push({"request": Req()})
print(request.method)  # GET - attribute access forwarded to the real per-context object
```

*Links*

- [refactoring.guru: Proxy](https://refactoring.guru/design-patterns/proxy)
- [Wikipedia: Proxy pattern](https://en.wikipedia.org/wiki/Proxy_pattern)
- [SourceMaking: Proxy](https://sourcemaking.com/design_patterns/proxy)
- [Amir Lavasani: Proxy (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-proxy-bd04fedbe83d)



### Chain of Responsibility (Ланцюг відповідальності)

*Summary*
> Поведінковий патерн: передає запит уздовж ланцюга обробників, доки один із них його не
> обробить. Відокремлює відправника від конкретного отримувача.

**Принцип роботи**

Кожен обробник має посилання на наступного; отримавши запит, він або обробляє його, або
передає далі. Канонічний приклад - middleware у вебфреймворках і рівні логування.

```python
class Handler:
    def __init__(self, nxt=None):
        self._next = nxt

    def handle(self, req):
        if self._next:
            return self._next.handle(req)
        return None  # end of chain


class AuthHandler(Handler):
    def handle(self, req):
        if not req.user:
            raise PermissionError
        return super().handle(req)  # pass along
```

Детальніше (зокрема як middleware-конвеєр) -
[`architecture/architecture_patterns.md`](../architecture/architecture_patterns.md).

**У Python-екосистемі.** Поширення записів ієрархією логерів (`app.db` -> `app` -> root) і
конвеєр middleware у Django/WSGI - ланцюги обробників: кожен обробляє та/або передає далі.

```python
import logging, sys

logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.getLogger().setLevel("INFO")
logging.getLogger("app.db").info("query ran")  # record climbs app.db -> app -> root
# each logger handles and/or passes the record up the chain while propagate=True
```

*Links*

- [refactoring.guru: Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility)
- [Wikipedia: Chain of Responsibility pattern](https://en.wikipedia.org/wiki/Chain-of-responsibility_pattern)
- [SourceMaking: Chain of Responsibility](https://sourcemaking.com/design_patterns/chain_of_responsibility)
- [Amir Lavasani: Chain of Responsibility (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-chain-of-responsibility-cc22bb241b41)



### Command (Команда)

*Summary*
> Поведінковий патерн: інкапсулює запит як об'єкт, що дозволяє параметризувати дії, ставити їх
> у чергу, логувати та скасовувати (undo).

**Принцип роботи**

Команда зберігає одержувача та аргументи й має метод `execute()` (іноді `undo()`). Виклик
відокремлений від виконання, тож команди можна складати у чергу чи історію. У Python проста
команда без undo часто зводиться до замикання або `functools.partial`.

```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...


class AddText(Command):
    def __init__(self, doc, text):
        self.doc, self.text = doc, text

    def execute(self):
        self.doc.append(self.text)

    def undo(self):
        self.doc.truncate(len(self.text))
```

**У Python-екосистемі.** Задача Celery інкапсулює виклик як об'єкт-команду: її ставлять у чергу,
відкладають, повторюють і логують окремо від виконання. Команди Django (`BaseCommand.handle`) -
схожа ідея.

```python
@app.task  # Celery wraps the call as a Command object (needs a broker)
def send_email(to, body): ...


send_email.delay("a@b.com", "hi")  # enqueue - deferred execution
send_email.apply_async(("a@b.com", "hi"), countdown=10, max_retries=3)  # queue / schedule / retry
```

*Links*

- [refactoring.guru: Command](https://refactoring.guru/design-patterns/command)
- [Wikipedia: Command pattern](https://en.wikipedia.org/wiki/Command_pattern)
- [SourceMaking: Command](https://sourcemaking.com/design_patterns/command)
- [Amir Lavasani: Command (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-command-cc47fec57d54)



### Interpreter (Інтерпретатор)

*Summary*
> Поведінковий патерн: для простої формальної мови визначає представлення граматики та
> інтерпретатор, що обчислює вирази цієї мови.

**Принцип роботи**

Кожному правилу граматики відповідає клас із методом `interpret(context)`; складені вирази
рекурсивно інтерпретують свої частини (по суті - обхід AST). Застосовний для маленьких DSL,
фільтрів, калькуляторів; для складних мов беруть готові парсери.

```python
class Num:
    def __init__(self, v):
        self.v = v

    def interpret(self):
        return self.v


class Add:
    def __init__(self, a, b):
        self.a, self.b = a, b

    def interpret(self):
        return self.a.interpret() + self.b.interpret()


Add(Num(2), Add(Num(3), Num(4))).interpret()  # 9
```

**У Python-екосистемі.** Мова виразів SQLAlchemy і `Q`-об'єкти Django будують дерево виразів і
інтерпретують його в SQL; модуль `ast` + `compile`/`eval` інтерпретує Python; рушій `re` -
граматику регулярних виразів.

```python
from sqlalchemy import column, and_

expr = and_(column("age") > 18, column("active").is_(True))  # build a grammar tree
print(expr)  # age > :age_1 AND active IS true
# SQLAlchemy interprets the same expression tree into dialect-specific SQL
```

*Links*

- [Wikipedia: Interpreter pattern](https://en.wikipedia.org/wiki/Interpreter_pattern)
- [SourceMaking: Interpreter](https://sourcemaking.com/design_patterns/interpreter)



### Iterator (Ітератор)

*Summary*
> Поведінковий патерн: надає спосіб послідовного доступу до елементів колекції без розкриття
> її внутрішнього представлення. У Python вбудований у мову через протокол ітерування.

**Принцип роботи**

Об'єкт-ітератор інкапсулює позицію обходу та віддає наступний елемент. Python формалізує це
протоколом `__iter__`/`__next__`; генератори (`yield`) - найкоротший спосіб створити ітератор.

```python
class Countdown:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        while self.n > 0:  # generator-based iterator
            yield self.n
            self.n -= 1
```

Деталі протоколу, ітератор vs ітерабельний об'єкт, генератори -
[`python/iterator_and_generator.md`](../python/iterator_and_generator.md).

**У Python-екосистемі.** Протокол `__iter__`/`__next__` вбудований у мову: файли, `range`, `dict`,
`csv.reader` та генератори - усе це ітератори, які споживає `for`.

```python
def read_chunks(f, size=1024):
    while chunk := f.read(size):
        yield chunk  # generator is an iterator over file chunks


# for/in, enumerate, zip, dict, csv.reader all consume the same iterator protocol
```

*Links*

- [refactoring.guru: Iterator](https://refactoring.guru/design-patterns/iterator)
- [Wikipedia: Iterator pattern](https://en.wikipedia.org/wiki/Iterator_pattern)
- [SourceMaking: Iterator](https://sourcemaking.com/design_patterns/iterator)
- [Amir Lavasani: Iterator (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-iterator-2d3e9917f930)



### Mediator (Посередник)

*Summary*
> Поведінковий патерн: інкапсулює взаємодію набору об'єктів у окремому посереднику, щоб вони
> не посилалися одне на одного напряму. Знижує зв'язність "усі-з-усіма".

**Принцип роботи**

Замість прямих зв'язків компоненти повідомляють посередника про події, а той координує
відповіді інших компонентів. Канонічний приклад - діалогове вікно, де зміна одного поля
впливає на інші через контролер.

```python
class Mediator:
    def notify(self, sender, event): ...


class Dialog(Mediator):
    def notify(self, sender, event):
        if sender is self.checkbox and event == "toggled":
            self.text_field.enabled = self.checkbox.checked
```

Споріднений з патерном Observer, але координацію централізовано в одному об'єкті.

**У Python-екосистемі.** Готового примітива-посередника стандартна бібліотека не дає - Mediator
реалізують вручну як контролер: у GUI-застосунках (Qt, `tkinter`) клас вікна чи форми зводить
докупи свої віджети й координує їхню взаємодію, а самі віджети один до одного не звертаються.
Диспетчери сигналів (`blinker`, сигнали Django) - це **не** Mediator, а Observer: вони лише
транслюють подію підписникам, тоді як посередник містить саму логіку координації - вирішує, який
компонент і як має зреагувати.

```python
class SignupForm:  # the mediator owns the cross-widget logic
    def __init__(self):
        self.submit_enabled = False

    def changed(self, field, value):  # widgets report TO the mediator, not to each other
        if field == "email":
            self.submit_enabled = "@" in value  # mediator decides the effect on other widgets


form = SignupForm()
form.changed("email", "a@b.com")
print(form.submit_enabled)  # True - coordination logic lives in one place
```

*Links*

- [refactoring.guru: Mediator](https://refactoring.guru/design-patterns/mediator)
- [Wikipedia: Mediator pattern](https://en.wikipedia.org/wiki/Mediator_pattern)
- [SourceMaking: Mediator](https://sourcemaking.com/design_patterns/mediator)
- [Amir Lavasani: Mediator (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-mediator-ca42c2caca52)



### Memento (Хранитель)

*Summary*
> Поведінковий патерн: фіксує та зовні зберігає внутрішній стан об'єкта без порушення
> інкапсуляції, щоб потім відновити його (undo / знімки).

**Принцип роботи**

Об'єкт ("originator") створює memento - непрозорий знімок свого стану - і вміє відновитися з
нього. Зберігач ("caretaker") тримає знімки, але не зазирає всередину. Реалізує undo-стек і
точки відновлення.

```python
class Editor:
    def __init__(self):
        self.text = ""

    def save(self):
        return self.text  # memento (opaque snapshot)

    def restore(self, snapshot):
        self.text = snapshot


history = []
ed = Editor()
ed.text = "v1"
history.append(ed.save())
ed.text = "v2"
ed.restore(history.pop())  # back to "v1"
```

**У Python-екосистемі.** `pickle` (через спеціальні методи `__getstate__`/`__setstate__`) і `copy.deepcopy`
знімають та відновлюють стан як непрозорий memento; `SAVEPOINT` у БД - точки відновлення транзакції.

```python
import pickle

snapshot = pickle.dumps(obj)  # memento: opaque snapshot of internal state
# ... mutate obj ...
obj = pickle.loads(snapshot)  # restore from the memento
# __getstate__/__setstate__ customize exactly what the snapshot captures
```

*Links*

- [refactoring.guru: Memento](https://refactoring.guru/design-patterns/memento)
- [Wikipedia: Memento pattern](https://en.wikipedia.org/wiki/Memento_pattern)
- [SourceMaking: Memento](https://sourcemaking.com/design_patterns/memento)
- [Amir Lavasani: Memento (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-memento-5b8f94d84bc3)



### Observer (Спостерігач)

*Summary*
> Поведінковий патерн: визначає залежність "один-до-багатьох", за якої зміна стану суб'єкта
> автоматично сповіщає та оновлює всіх підписників. Основа подієво-орієнтованих систем.

**Принцип роботи**

Суб'єкт тримає список спостерігачів і викликає їхній метод сповіщення при зміні стану.
Спостерігачі підписуються/відписуються динамічно. Лежить в основі сигналів, pub/sub та
прив'язки даних у UI.

```python
class Subject:
    def __init__(self):
        self._observers = []

    def subscribe(self, fn):
        self._observers.append(fn)

    def notify(self, event):
        for fn in self._observers:
            fn(event)  # push to all subscribers
```

Observer працює в межах одного процесу; pub/sub між процесами через брокер -
[`infrastructure/mq.md`](../infrastructure/mq.md).

**У Python-екосистемі.** Сигнали Django (`post_save`, `pre_delete`, власні `Signal`) і `blinker`
(сигнали Flask) - реалізації Observer: суб'єкт публікує подію, підписані отримувачі реагують.

```python
from django.dispatch import Signal, receiver

order_paid = Signal()  # subject


@receiver(order_paid)  # observer 1
def grant_access(sender, order, **kwargs):
    print("access:", order)


@receiver(order_paid)  # observer 2
def send_receipt(sender, order, **kwargs):
    print("receipt:", order)


order_paid.send(sender=None, order="A-1")  # notify all observers -> access: A-1 / receipt: A-1
```

*Links*

- [refactoring.guru: Observer](https://refactoring.guru/design-patterns/observer)
- [Wikipedia: Observer pattern](https://en.wikipedia.org/wiki/Observer_pattern)
- [SourceMaking: Observer](https://sourcemaking.com/design_patterns/observer)
- [Amir Lavasani: Observer (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-observer-ac50bbf861b5)



### State (Стан)

*Summary*
> Поведінковий патерн: дозволяє об'єкту змінювати поведінку при зміні внутрішнього стану - так,
> ніби він змінює клас. Замінює громіздкі `if/elif` за станами на окремі класи-стани.

**Принцип роботи**

Кожному стану відповідає клас, що реалізує поведінку для цього стану; контекст делегує виклики
поточному об'єкту-стану і перемикає його за переходами. Близький до скінченного автомата.

```python
class Draft:
    def publish(self, doc):
        doc.state = Published()


class Published:
    def publish(self, doc):
        raise RuntimeError("already published")


class Document:
    def __init__(self):
        self.state = Draft()

    def publish(self):
        self.state.publish(self)
```

Скінченний автомат (FSM) як споріднений підхід -
[`architecture/architecture_patterns.md`](../architecture/architecture_patterns.md).

State вважають розширенням Strategy: обидва змінюють поведінку контексту, делегуючи роботу
змінному об'єкту-помічнику. Ключова різниця - у зв'язках між цими об'єктами: стратегії
**незалежні й не знають одна про одну** (їх задає ззовні клієнт), а стани **знають про сусідні
стани** і самі ініціюють переходи між собою.

**У Python-екосистемі.** Бібліотеки скінченних автоматів `transitions` і `django-fsm` реалізують
State: дозволені дії та переходи визначає поточний стан об'єкта. Стани задач `asyncio`
(`PENDING` -> `FINISHED`) - споріднена ідея.

```python
from transitions import Machine


class Order:
    pass


o = Order()
Machine(
    model=o,
    states=["new", "paid", "shipped"],
    initial="new",
    transitions=[
        {"trigger": "pay", "source": "new", "dest": "paid"},
        {"trigger": "ship", "source": "paid", "dest": "shipped"},
    ],
)

o.pay()
print(o.state)  # paid - which actions are allowed now depends on the state
```

*Links*

- [refactoring.guru: State](https://refactoring.guru/design-patterns/state)
- [Wikipedia: State pattern](https://en.wikipedia.org/wiki/State_pattern)
- [SourceMaking: State](https://sourcemaking.com/design_patterns/state)
- [Amir Lavasani: State (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-state-8916b2f65f69)



### Strategy (Стратегія)

*Summary*
> Поведінковий патерн: визначає сімейство взаємозамінних алгоритмів за спільним інтерфейсом і
> дозволяє підставляти їх під час виконання. Контекст зберігає обрану стратегію й делегує їй
> роботу, не знаючи реалізації; у Python стратегією зазвичай є проста функція, а не ієрархія класів.

**Принцип роботи**

Контекст тримає посилання на стратегію за спільним інтерфейсом і делегує їй роботу через єдину
точку виклику; конкретну реалізацію задає клієнт ззовні й може замінити, не чіпаючи контекст. По
суті це структурне оформлення поліморфізму: контекст викликає той самий метод інтерфейсу, а яка
саме реалізація відпрацює - вирішується під час виконання за фактичним типом підставленої стратегії.

```python
from typing import Protocol


class PaymentMethod(Protocol):  # the common strategy interface
    def pay(self, amount: float) -> str: ...


class Card(PaymentMethod):
    def __init__(self, number):
        self.number = number

    def pay(self, amount):
        return f"charged {amount} to card *{self.number[-4:]}"


class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        return f"charged {amount} via PayPal {self.email}"


class Checkout:  # context
    def __init__(self, method: PaymentMethod):
        self.method = method  # strategy injected by the client

    def confirm(self, amount: float) -> str:
        return self.method.pay(amount)  # one call site, polymorphic dispatch


print(Checkout(Card("4111111111111111")).confirm(50))  # charged 50 to card *1111
print(Checkout(PayPal("a@b.com")).confirm(50))  # charged 50 via PayPal a@b.com
```

Виклик `self.method.pay(amount)` - одна точка виклику, але відпрацьовує реалізація фактично
підставленого класу: Strategy і є застосуванням поліморфізму, де взаємозамінні реалізації
підставляють ззовні замість розгалуження `if`/`elif` за типом усередині контексту. Коли стратегія -
один метод без власного стану, у Python замість класу часто передають просту функцію (як `key=` у
`sorted`): першокласні функції прибирають бойлерплейт інтерфейсу й підкласів, але сам патерн
лишається тим самим.

**Вибір стратегії.** Strategy не прибирає сам вибір алгоритму, а зводить його до однієї точки й
виконує один раз. Часто це навіть не розгалуження, а пошук у словнику `{ключ: стратегія}`: вибір
стає даними, тож нова стратегія додається одним записом, без правок наявного коду (принцип
відкритості/закритості). Іноді розгалуження немає зовсім - конкретну стратегію створює клієнтський
код (користувач обрав спосіб оплати в UI; тип прийшов із запиту чи конфігурації). Натомість усі
місця, що виконують поведінку (`confirm`, повернення коштів, аудит), лише поліморфно делегують
`method.pay(...)`; без Strategy той самий `if`/`elif` за типом довелося б повторювати в кожному з них.

```python
PAYMENT_METHODS = {"card": Card, "paypal": PayPal}  # selection becomes data, not if/elif


def make_checkout(method: str, *args) -> Checkout:
    return Checkout(PAYMENT_METHODS[method](*args))  # O(1) lookup; new method = one dict entry


choice = "paypal"  # comes from a request / config / UI
print(make_checkout(choice, "a@b.com").confirm(50))  # charged 50 via PayPal a@b.com
```

**У Python-екосистемі.** `sorted`/`min`/`max` приймають стратегію порівняння через `key`, а
`json.dumps` - стратегію серіалізації через `default`: готова функція-контекст параметризується
переданим callable.

```python
rows = ["bb", "a", "ccc"]
print(sorted(rows, key=len))  # ['a', 'bb', 'ccc'] - key IS the strategy
print(sorted(rows, key=str.upper))  # swap the comparison strategy at the call site
```

*Links*

- [refactoring.guru: Strategy](https://refactoring.guru/design-patterns/strategy)
- [Wikipedia: Strategy pattern](https://en.wikipedia.org/wiki/Strategy_pattern)
- [SourceMaking: Strategy](https://sourcemaking.com/design_patterns/strategy)
- [Amir Lavasani: Strategy (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-strategy-7b14f1c4c162)



### Template Method (Шаблонний метод)

*Summary*
> Поведінковий патерн: визначає кістяк алгоритму в базовому методі, делегуючи окремі кроки
> підкласам. Підкласи перевизначають кроки, не змінюючи структуру алгоритму.

**Принцип роботи**

Базовий клас реалізує незмінний порядок кроків і викликає методи-"заглушки", які підкласи
наповнюють конкретикою. Інверсія керування: базовий клас вирішує, **коли** викликати крок,
підклас - **що** він робить.

Шаблонний метод - не інтерфейс. Інтерфейс (чисто абстрактний клас) лише оголошує сигнатури: ні
логіки, ні заданого порядку викликів, каркаса алгоритму там немає взагалі. Тут навпаки - клас
напівабстрактний: метод-шаблон **конкретний** і містить реальний алгоритм (фіксований порядок
кроків і потік керування), абстрактні - лише окремі кроки, які наповнює підклас. Саме конкретний
шаблон уможливлює інверсію керування (база вирішує **коли**, підклас - **що**); прибрати його,
лишивши самі абстрактні кроки, - і зостанеться звичайний інтерфейс, бо ніщо вже не фіксує порядок
і момент виклику.

```python
class Pipeline(ABC):
    def run(self, src):  # template method - fixed skeleton
        data = self.extract(src)
        return self.load(self.transform(data))

    @abstractmethod
    def extract(self, src): ...
    @abstractmethod
    def transform(self, data): ...
    @abstractmethod
    def load(self, data): ...
```

Strategy досягає схожого через композицію (передачу поведінки), Template Method - через
наслідування.

**У Python-екосистемі.** `unittest.TestCase.run` (фіксований порядок `setUp` -> тест -> `tearDown`),
`View.dispatch` у Django CBV і `BaseHTTPRequestHandler` - шаблонні методи: базовий клас задає
кістяк, підклас наповнює окремі кроки.

```python
import unittest


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.user = "bob"  # overridden step

    def test_name(self):
        self.assertEqual(self.user, "bob")


# TestCase.run() is the template: it always calls setUp() -> test method -> tearDown()
```

*Links*

- [refactoring.guru: Template method](https://refactoring.guru/design-patterns/template-method)
- [Wikipedia: Template method pattern](https://en.wikipedia.org/wiki/Template_method_pattern)
- [SourceMaking: Template method](https://sourcemaking.com/design_patterns/template_method)
- [Amir Lavasani: Template Method (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-template-method-1b76fb561c4a)



### Visitor (Відвідувач)

*Summary*
> Поведінковий патерн: відокремлює алгоритм від структури об'єктів, над якою він працює.
> Дозволяє додавати нові операції над ієрархією, не змінюючи її класи.

**Принцип роботи**

Кожен елемент структури приймає відвідувача (`accept(visitor)`) і викликає відповідний його
метод (double dispatch); відвідувач містить операцію для кожного типу елемента. Нову операцію
додають новим класом-відвідувачем замість правок усіх елементів.

```python
class Visitor(ABC):
    @abstractmethod
    def visit_circle(self, c): ...
    @abstractmethod
    def visit_square(self, s): ...


class Circle:
    def accept(self, v):
        return v.visit_circle(self)  # double dispatch


class AreaVisitor(Visitor):
    def visit_circle(self, c):
        return 3.14 * c.r**2

    def visit_square(self, s):
        return s.side**2
```

Компроміс: легко додавати **операції**, важко додавати **типи елементів** (потрібно правити
кожного відвідувача).

**Pythonic-альтернатива.** Замість ручного double dispatch через `accept`/`visit` у Python
беруть `functools.singledispatch` - диспетчеризацію за типом першого аргументу, що дозволяє
додавати нову операцію без методів у самих елементах:

```python
import functools


@functools.singledispatch
def area(shape):
    raise NotImplementedError


@area.register
def _(s: Circle):
    return 3.14 * s.r**2


@area.register
def _(s: Square):
    return s.side**2
```

**У Python-екосистемі.** `ast.NodeVisitor`/`NodeTransformer` - канонічний Visitor (метод
`visit_<Тип>` на кожен вузол); лінтери та компілятори обходять AST саме так. Pythonic-варіант -
`functools.singledispatch` (вище).

```python
import ast


class NameCollector(ast.NodeVisitor):
    def visit_Name(self, node):  # one operation per node type
        print("name:", node.id)
        self.generic_visit(node)


NameCollector().visit(ast.parse("x + y * z"))  # name: x / name: y / name: z
```

*Links*

- [refactoring.guru: Visitor](https://refactoring.guru/design-patterns/visitor)
- [Wikipedia: Visitor pattern](https://en.wikipedia.org/wiki/Visitor_pattern)
- [SourceMaking: Visitor](https://sourcemaking.com/design_patterns/visitor)
- [Amir Lavasani: Visitor (Medium)](https://medium.com/@amirm.lavasani/design-patterns-in-python-visitor-f20085b35d8b)
