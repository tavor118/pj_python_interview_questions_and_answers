## DRF

### Як працює Serializer в Django REST Framework

**Serializer** перетворює інформацію, що зберігається в базі даних і визначається за допомогою моделей Django, в формат JSON для передачі через API.

Коли користувач передає інформацію (наприклад, створення нового екземпляра) через API, серіалізатор бере дані, перевіряє їх і перетворює їх на об'єкт Python. Аналогічно, коли користувач отримує доступ до інформації через API, відповідні екземпляри передаються в серіалізатор, який перетворює їх в формат, який можна легко передати користувачеві у вигляді JSON.

```python
class ThingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Thing
    fields = (‘name’, )
```

Параметр fields дозволяє вказати, які поля доступні для цього серіалізатора. Замість fields може бути встановлений параметр exclude, який буде включати всі поля моделі, крім тих, які вказані в exclude.


### Як відбувається авторизація та автентифікація DRF

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

Загальною практикою є комбінування різних класів автентифікації та дозволів для досягнення потрібного рівня безпеки та авторизації у додатку DRF.

Послідовності обробки запиту

- Отримання запиту - запит від користувача надсилається на сервер.
- Автентифікація користувача (User Authentication) - перевіряється наявність автентифікаційних даних у запиті. Якщо у запиті є автентифікаційні дані (такі як токен або інші ідентифікатори), middleware автентифікації використовує ці дані для ідентифікації користувача. Наприклад, для токена JWT виконується перевірка справжності та розшифрування токена для визначення ідентифікації користувача. Іншими прикладами можуть бути `TokenAuthentication`, `SessionAuthentication`, або `BasicAuthentication`.
- Авторизація користувача (User Authorization) - після успішної автентифікації з допомогою класів дозволів (permissions) визначають, чи має користувач доступ до запитуваного ресурсу. Прикладами можуть бути `IsAuthenticated`, `IsAdminUser` або власні класи дозволів.
- View - Якщо користувач успішно автентифікований та авторизований, виконується логіка перегляду. Після обробки ресурсу сервер формує відповідь та надсилає її користувачеві.

### Permissions в DRF

**Permissions** у Django Rest Framework (DRF) — це механізм, який забезпечує контроль доступу до ресурсів API. Вони дозволяють визначати, хто може отримати доступ до певного ресурсу, залежно від різних критеріїв, таких як автентифікація, роль користувача чи інші умови.

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


### ViewSets в DRF

**ViewSets** у Django Rest Framework (DRF) — це компонент, що спрощує побудову REST API, об’єднуючи логіку для стандартних CRUD-операцій (створення, читання, оновлення, видалення) в одному класі. Вони дозволяють уникнути дублювання коду, що виникає при використанні окремих класів для кожного методу (наприклад, `APIView` або `GenericAPIView`).

ViewSets об’єднують CRUD-операцій - всі методи для обробки HTTP-запитів (GET, POST, PUT, DELETE) визначаються в одному класі. Це спрощує структуру коду та робить його більш організованим.

Основні переваги ViewSets

- Зменшення дублювання коду та централізація логіки.
- Інтеграція зі `DefaultRouter` для швидкого налаштування URL-адрес API.

Типи ViewSets у DRF

- `ViewSet` - базовий клас, який вимагає явного визначення всіх методів (наприклад, `list`, `retrieve`, `create`, `update`, `destroy`).
- `GenericViewSet` - поєднується з міксинами для додавання функціональності CRUD.
- `ModelViewSet` -  автоматично додає всі CRUD-операції для моделі.

Для ViewSets маршрутизація налаштовується через `DefaultRouter` або інші подібні класи, які автоматично генерують URL-адреси для стандартних дій.

```python
from rest_framework.routers import DefaultRouter
from myapp.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = router.urls
```

- **ViewSet**  - використовується для створення кастомних логік CRUD-операцій.

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

- **GenericViewSet**  - використовується разом із міксинами, такими як `ListModelMixin`, `RetrieveModelMixin`.

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

