## DRF

### Як працює Serializer в Django REST Framework [❄️8/100]

**Serializer** перетворює інформацію, що зберігається в базі даних і визначається 
за допомогою моделей Django, в формат JSON для передачі через API.

Коли користувач передає інформацію (наприклад, створення нового екземпляра) через API, 
серіалізатор бере дані, перевіряє їх і перетворює їх на об'єкт Python.
Аналогічно, коли користувач отримує доступ до інформації через API, відповідні екземпляри
передаються в серіалізатор, який перетворює їх в формат, який можна легко передати 
користувачеві у вигляді JSON.

```python
class ThingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Thing
    fields = ('name', )
```

Параметр fields дозволяє вказати, які поля доступні для цього серіалізатора.
Замість fields може бути встановлений параметр exclude, який буде включати 
всі поля моделі, крім тих, які вказані в exclude.



### Як відбувається авторизація та автентифікація DRF [❄️1/100]

**Автентифікація (Authentication)**

- DRF використовує middleware для автентифікації користувача під час обробки запитів.
- Для включення автентифікації, потрібно налаштувати `DEFAULT_AUTHENTICATION_CLASSES` у налаштуваннях DRF та вказати один або декілька класів автентифікації.

Приклад коду для використання автентифікації через токени (Token Authentication)

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# view.py
from rest_framework.authentication import TokenAuthentication

class MyAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        ...
```

**Авторизація (Authorization)**

- Авторизація в DRF зазвичай визначається на рівні класів перегляду та використовується для визначення, чи має користувач доступ до певного ресурсу.
- Для включення авторизації, потрібно налаштувати `DEFAULT_PERMISSION_CLASSES` у налаштуваннях DRF та вказати один або декілька класів дозволів.

Приклад коду для обмеження доступу за допомогою `IsAdminUser` (клас авторизації для адміністраторів):

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}

# view.py
from rest_framework.permissions import IsAdminUser

class MyAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        ...
```

Загальною практикою є комбінування різних класів автентифікації та дозволів
для досягнення потрібного рівня безпеки та авторизації у додатку DRF.

Послідовності обробки запиту

- Отримання запиту - запит від користувача надсилається на сервер.
- Автентифікація користувача (User Authentication) - перевіряється наявність автентифікаційних даних у запиті. Якщо у запиті є автентифікаційні дані (такі як токен або інші ідентифікатори), middleware автентифікації використовує ці дані для ідентифікації користувача. Наприклад, для токена JWT виконується перевірка справжності та розшифрування токена для визначення ідентифікації користувача. Іншими прикладами можуть бути `TokenAuthentication`, `SessionAuthentication`, або `BasicAuthentication`.
- Авторизація користувача (User Authorization) - після успішної автентифікації з допомогою класів дозволів (permissions) визначають, чи має користувач доступ до запитуваного ресурсу. Прикладами можуть бути `IsAuthenticated`, `IsAdminUser` або власні класи дозволів.
- View - Якщо користувач успішно автентифікований та авторизований, виконується логіка перегляду. Після обробки ресурсу сервер формує відповідь та надсилає її користувачеві.



### Permissions в DRF [❄️1/100]

**Permissions** у Django Rest Framework (DRF) — це механізм, який забезпечує контроль 
доступу до ресурсів API.
Вони дозволяють визначати, хто може отримати доступ до певного ресурсу, залежно
від різних критеріїв, таких як автентифікація, роль користувача чи інші умови.

Основні концепції та компоненти

- Усі permissions у DRF базуються на класі `BasePermission`. Цей клас надає базовий метод `has_permission`, який перевіряє доступ до представлення (`view`), та `has_object_permission`, який перевіряє доступ до окремого об'єкта.    
- Permissions можуть перевірятися
    - На глобальному рівні (чи дозволений доступ до view загалом).
    - На об'єктному рівні (чи дозволений доступ до конкретного об'єкта).
- Дефолтні permissions у DRF - DRF надає кілька вбудованих permissions, які покривають базові сценарії:    
    - `AllowAny`: дозволяє доступ будь-якому користувачу.
    - `IsAuthenticated`: дозволяє доступ тільки автентифікованим користувачам.
    - `IsAdminUser`: дозволяє доступ лише адміністраторам.
    - `IsAuthenticatedOrReadOnly`: дозволяє доступ для читання (GET-запити) будь-яким користувачам, а зміну (POST, PUT, DELETE) — лише автентифікованим.

```python
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		return Response({"message": "You are authenticated"})
```

- Кастомні permissions - DRF дозволяє створювати власні правила доступу, успадковуючи клас `BasePermission`.

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
	def has_object_permission(self, request, view, obj):
		# Allow access only if the user is the owner of the object
		return obj.owner == request.user

class ExampleView(APIView):
	permission_classes = [IsOwner]

	def get(self, request, pk):
		obj = get_object_or_404(MyModel, pk=pk)
		self.check_object_permissions(request, obj)  # Ensure object-level permission
		return Response({"message": "You are the owner"})
```

- Об'єднання permissions -  можна вказати кілька permissions для одного представлення. У цьому випадку всі вони мають бути виконані.

```python
class ExampleView(APIView):
	permission_classes = [IsAuthenticated, IsAdminUser]
```

- Використання у ViewSet - у `ViewSet` можна застосовувати permissions як до всіх методів, так і окремо до кожного.

```python
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ExampleViewSet(ModelViewSet):
	queryset = MyModel.objects.all()
	permission_classes = [IsAuthenticatedOrReadOnly]
```

- Динамічні permissions - permissions можна задавати динамічно залежно від умов.

```python
class ExampleView(APIView):
	def get_permissions(self):
		if self.request.method == 'POST':
			return [IsAdminUser()]
		return [AllowAny()]
```

*Links*

- [Permissions in Django REST Framework](https://testdriven.io/blog/drf-permissions/)
- [Custom Permission Classes in Django REST Framework](https://testdriven.io/blog/custom-permission-classes-drf/)



### ViewSets в DRF [❄️3/100]

**ViewSets** у Django Rest Framework (DRF) — це компонент, що спрощує побудову REST API, 
об’єднуючи логіку для стандартних CRUD-операцій (створення, читання, оновлення, видалення)
в одному класі.
Вони дозволяють уникнути дублювання коду, що виникає при використанні окремих класів 
для кожного методу (наприклад, `APIView` або `GenericAPIView`).

ViewSets об’єднують CRUD-операцій - всі методи для обробки HTTP-запитів 
(GET, POST, PUT, DELETE) визначаються в одному класі.
Це спрощує структуру коду та робить його більш організованим.

Основні переваги ViewSets

- Зменшення дублювання коду та централізація логіки.
- Інтеграція зі `DefaultRouter` для швидкого налаштування URL-адрес API.

Типи ViewSets у DRF

- `ViewSet` - базовий клас, який вимагає явного визначення всіх методів (наприклад, `list`, `retrieve`, `create`, `update`, `destroy`).
- `GenericViewSet` - поєднується з міксинами для додавання функціональності CRUD.
- `ModelViewSet` -  автоматично додає всі CRUD-операції для моделі.

Для ViewSets маршрутизація налаштовується через `DefaultRouter` або інші подібні класи,
які автоматично генерують URL-адреси для стандартних дій.

```python
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
```

- **ViewSet** - використовується для створення кастомних логік CRUD-операцій.

```python
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class ProductViewSet(ViewSet):
	def list(self, request):
		# Custom logic for listing products
		return Response({"message": "List of products"})

	def retrieve(self, request, pk=None):
		# Custom logic for retrieving a product by ID
		return Response({"message": f"Details of product {pk}"})
```

- **GenericViewSet** - використовується разом із міксинами, такими як `ListModelMixin`, `RetrieveModelMixin`.

```python
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from myapp.models import Product
from myapp.serializers import ProductSerializer

class ProductViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
```

- **ModelViewSet** - найзручніший варіант, що автоматично додає всі CRUD-операції.

```python
from rest_framework.viewsets import ModelViewSet
from myapp.models import Product
from myapp.serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
```

- **Actions** - ViewSet дозволяє визначати додаткові кастомні дії за допомогою декораторів `@action`.

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

	@action(detail=True, methods=['post'])
	def set_price(self, request, pk=None):
		# Custom action to set a price for a product
		return Response({"message": f"Price updated for product {pk}"})
```



### Django vs DRF [❄️1/100]

*Summary*
> Django - повноцінний веб-фреймворк (ORM, шаблони, форми, admin, auth, sessions,
> middleware). DRF (`djangorestframework`) - стороння бібліотека-надбудова поверх
> Django, спеціалізована для побудови REST API: серіалізатори, ViewSets, routers,
> content negotiation, browsable API, throttling, pagination. Django без DRF
> теж дозволяє писати API, але доводиться руками робити те, що DRF дає коробці.

**Що дає Django сам по собі**

- ORM (моделі, міграції, QuerySet'и);
- Routing через `urls.py`;
- View-функції / class-based views (`View`, `TemplateView`, `ListView`, ...);
- Шаблони, форми (для server-rendered UI);
- Admin-панель;
- Auth-система (User model, permissions, groups);
- Middleware-стек;
- Sessions, messages;
- Управління статичними і медіа-файлами.

Для API можна писати без DRF: повертати `JsonResponse`, парсити `request.body`
вручну, серіалізувати dict'и. Працює, але швидко стає boilerplate'ом.

**Що додає DRF**

- **Serializers** - двосторонню валідацію і перетворення між Python-об'єктом
  (модель / dict) і JSON; з підтримкою nested-моделей, кастомних полів і
  валідаторів. Аналог Marshmallow / Pydantic, інтегрований з ORM (`ModelSerializer`).
- **APIView / GenericAPIView / ViewSets / Mixins** - готові шари абстракції
  поверх `View` для CRUD над моделлю.
- **Routers** (`DefaultRouter`, `SimpleRouter`) - генерують URL'и автоматично
  з ViewSet'у.
- **Authentication classes** - `TokenAuthentication`, `SessionAuthentication`,
  `BasicAuthentication`; стороннє - JWT (`djangorestframework-simplejwt`),
  OAuth2.
- **Permissions** - декларативний контроль доступу
  (`IsAuthenticated`, `IsAdminUser`, кастомні).
- **Throttling** - rate limiting per-user / per-anon / per-IP.
- **Pagination** - готові класи (`PageNumberPagination`, `LimitOffsetPagination`,
  `CursorPagination`).
- **Content negotiation** - відповідь у JSON / XML / browsable HTML залежно
  від `Accept`-заголовка.
- **Browsable API** - HTML-сторінка для перегляду/тестування ендпойнтів у браузері.
- **Exception handlers** - DRF-формат помилок (`{"detail": "..."}`).

**Встановлення**

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    ...
    "rest_framework",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.TokenAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```

**Випадки, де DRF не потрібен**

- Дрібний внутрішній сервіс з кількома ендпойнтами без serialization-логіки -
  можна обійтися `JsonResponse`.
- Сервіс, де важлива async-семантика з нуля - FastAPI / Starlette на власній
  основі, без Django-overhead.

Інакше для типового REST-сервісу на Django стек `Django + DRF` - індустріальний
дефолт.

*Links*

- [Django REST Framework: Quickstart](https://www.django-rest-framework.org/tutorial/quickstart/)



### Generic Views у DRF [❄️3/100]

*Summary*
> Generic Views - готові class-based views поверх `GenericAPIView`, кожен
> відповідає за одну HTTP-операцію або їх вузьку комбінацію. Кожен generic view -
> комбінація `GenericAPIView` + один або кілька mixin'ів з `rest_framework.mixins`.
> Альтернатива ViewSet'ам, коли потрібен один-два endpoint'и, а не повний CRUD.

**Базовий клас: `GenericAPIView`**

`GenericAPIView` сам не обробляє HTTP-методи - лише дає атрибути і helper'и:

- `queryset` - джерело даних;
- `serializer_class` - який серіалізатор використати;
- `lookup_field` (default `pk`) - за якою колонкою шукати об'єкт;
- `pagination_class`, `filter_backends`, `permission_classes`,
  `authentication_classes` - стандартний набір;
- `get_queryset()`, `get_serializer()`, `get_object()` - перевизначувані хуки.

**Готові generic views**

| Клас | Метод(и) | Дія |
| --- | --- | --- |
| `ListAPIView` | GET (collection) | список об'єктів |
| `CreateAPIView` | POST | створення |
| `RetrieveAPIView` | GET (single) | один об'єкт |
| `UpdateAPIView` | PUT / PATCH | оновлення |
| `DestroyAPIView` | DELETE | видалення |
| `ListCreateAPIView` | GET / POST | список + створення |
| `RetrieveUpdateAPIView` | GET / PUT / PATCH | один + оновлення |
| `RetrieveDestroyAPIView` | GET / DELETE | один + видалення |
| `RetrieveUpdateDestroyAPIView` | GET / PUT / PATCH / DELETE | один + оновлення + видалення |

```python
from rest_framework import generics
from myapp.models import Product
from myapp.serializers import ProductSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
```

URL'и реєструються вручну:

```python
urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/<int:pk>/", ProductDetail.as_view()),
]
```

**Generics vs ViewSets - як вибирати**

| Сценарій | Інструмент |
| --- | --- |
| Один-два endpoint'и на ресурс, не весь CRUD | Generics |
| Кастомна HTTP-семантика (наприклад, тільки POST для пошуку) | Generics або `APIView` |
| Повний CRUD над моделлю з автогенерацією URL | `ModelViewSet` + `DefaultRouter` |
| Потрібно явно контролювати, які операції доступні | Generics (composition over `ModelViewSet`) |
| Кілька related-actions під одним ресурсом | ViewSet з `@action` |

Принцип: **не давати клієнту операції, яких не передбачено**. `ModelViewSet`
автоматично відкриває POST/PUT/PATCH/DELETE - якщо ресурс read-only, краще
`ListAPIView` + `RetrieveAPIView`, або `ReadOnlyModelViewSet`.

*Links*

- [DRF docs: Generic views](https://www.django-rest-framework.org/api-guide/generic-views/)



### Mixins у DRF [❄️1/100]

*Summary*
> `rest_framework.mixins` - п'ять класів, кожен реалізує одну CRUD-дію поверх
> `GenericAPIView`. Generic views - готові комбінації цих mixin'ів. Власна
> композиція mixin'ів потрібна, коли стандартні generics і ViewSets не дають
> точно потрібного набору операцій.

**П'ять основних mixin'ів**

| Mixin | Метод | HTTP |
| --- | --- | --- |
| `CreateModelMixin` | `.create(request, *args, **kwargs)` | POST |
| `ListModelMixin` | `.list(request, *args, **kwargs)` | GET (collection) |
| `RetrieveModelMixin` | `.retrieve(request, *args, **kwargs)` | GET (single) |
| `UpdateModelMixin` | `.update(...)`, `.partial_update(...)` | PUT, PATCH |
| `DestroyModelMixin` | `.destroy(request, *args, **kwargs)` | DELETE |

Кожен mixin покладається на `GenericAPIView` для `get_queryset()`,
`get_serializer()`, `get_object()` - тому міксується **разом** з `GenericAPIView`
(або `GenericViewSet`).

**Реалізація generic view через mixin'и**

`generics.ListCreateAPIView` під капотом - це:

```python
from rest_framework import mixins, generics

class ListCreateAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,
):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
```

**Власна композиція**

Сценарій: ресурс має `list`, `create`, кастомний action `archive` - але не
`update`/`destroy`:

```python
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        order = self.get_object()
        order.archive()
        return Response({"status": "archived"})
```

Тут немає `UpdateModelMixin` / `DestroyModelMixin` - відповідно PUT/PATCH/DELETE
просто недоступні, без явного блокування на permission-рівні. Це чистіше за
`ModelViewSet` + override методів для `405 Method Not Allowed`.

*Links*

- [DRF docs: Mixins](https://www.django-rest-framework.org/api-guide/generic-views/#mixins)



### Документація OpenAPI: `drf-spectacular`, `drf-yasg` [❄️4/100]

*Summary*
> DRF із коробки генерує мінімальну OpenAPI-схему (`SchemaView`), але для
> production-якісної документації використовують сторонні бібліотеки:
> **`drf-spectacular`** (актуальна, OpenAPI 3.x, активно розробляється) або
> **`drf-yasg`** (історично популярна, OpenAPI 2.0 / Swagger, режим maintenance).
> На відміну від FastAPI, схема не генерується з сигнатур функцій - вона
> будується з серіалізаторів + декораторів-підказок.

**Призначення сторонньої бібліотеки**

DRF знає типи через серіалізатори, але автоматично виведена схема часто
неповна для нетривіальних випадків: динамічні поля, кастомні дії, кілька
response-варіантів, polymorphic-серіалізатори, parameters з query-string.
`drf-spectacular` і `drf-yasg` додають декоратори для уточнення цих місць.

**`drf-spectacular` - рекомендований дефолт**

```bash
pip install drf-spectacular
```

```python
# settings.py
INSTALLED_APPS = [..., "drf_spectacular"]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "My API",
    "VERSION": "1.0.0",
}
```

```python
# urls.py
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    ...
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
]
```

Кастомізація через декоратор `@extend_schema`:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view


@extend_schema(
    parameters=[OpenApiParameter(name="search", type=str, required=False)],
    responses={200: ProductSerializer(many=True)},
    description="Search products by partial name match.",
)
@api_view(["GET"])
def search_products(request):
    ...
```

**`drf-yasg` - історичний варіант**

```python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter("search", openapi.IN_QUERY, type=openapi.TYPE_STRING),
    ],
    responses={200: ProductSerializer(many=True)},
)
@api_view(["GET"])
def search_products(request):
    ...
```

Працює, але обмежений OpenAPI 2.0, не підтримує всі сучасні фічі (oneOf, discriminator,
nullable у деяких контекстах). Для нових проектів - `drf-spectacular`.

**Порівняння з FastAPI**

FastAPI генерує OpenAPI-схему **автоматично** з сигнатур функцій і Pydantic-моделей -
без декораторів. DRF не має такого механізму, бо контракт endpoint'у визначений
не сигнатурою, а серіалізатором + view-класом + permission'ами; інспектувати все
це автоматично без втрат точності складно. Звідси декларативний підхід через
`@extend_schema`.

*Links*

- [drf-spectacular docs](https://drf-spectacular.readthedocs.io/)
- [drf-yasg docs](https://drf-yasg.readthedocs.io/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)

