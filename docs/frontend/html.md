## HTML

### Що таке HTML?

**HTML (HyperText Markup Language)** — це стандартна мова розмітки, яка використовується для створення веб-сторінок і веб-додатків.  HTML визначає структуру контенту веб-сторінки за допомогою елементів, які представлені у вигляді тегів, наприклад `<html>`, `<head>`, `<body>`, `<div>`, `<p>`, `<a>` тощо.   Теги HTML можуть мати атрибути, які надають додаткову інформацію, наприклад `<a href="https://example.com">`.  HTML дозволяє включати на сторінку інші типи контенту - зображення, відео, форми, посилання та таблиці.  Веб-браузери інтерпретують HTML-код і відображають його як структуровану веб-сторінку.  HTML зазвичай використовується разом із CSS (для стилізації) і JavaScript (для додавання інтерактивності).  

HTML документи мають чітку структуру, яка включає такі частини, як `<head>` для метаданих і `<body>` для видимого контенту. HTML5 ввів семантичні теги, такі як `<header>`, `<footer>`, `<article>`, `<section>`, які допомагають структурувати контент і поліпшують доступність.

Приклад HTML-документа

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple HTML Page</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a paragraph on a simple HTML page.</p>
    <a href="https://example.com">Visit Example</a>
</body>
</html>
```


### Що таке тег?

**Тег**  - це елемент мови розмітки, який використовується для визначення структури і формату контенту на веб-сторінці. Теги можуть бути парними і непарними.

Теги можуть мати атрибути, які надають додаткову інформацію або змінюють поведінку елементів.

```html
<a href="https://www.example.com" target="_blank">Visit Example</a>
```

- Парні теги: складаються з відкриваючого та закриваючого тегів. Контент, що знаходиться між ними, має особливу функцію або стиль.

```html
<p>This is a paragraph.</p>
```

- Непарні теги: не мають закриваючого тегу і використовуються для вставки окремих елементів на сторінку.

```html
<img src="image.jpg" alt="Description of image">
```

Основні теги
- Заголовки: використовуються для створення заголовків різних рівнів, від `<h1>` до `<h6>`.

```html
<h1>Main Title</h1>
<h2>Subheading</h2>
```

- Абзаци: використовуються для створення текстових блоків.

```html
<p>This is a paragraph.</p>
```

- Посилання: дозволяють створювати гіперпосилання на інші сторінки або ресурси.

```html
<a href="https://www.example.com">Visit Example</a>
```

- Зображення: використовуються для вставки зображень на веб-сторінку.

```html
<img src="image.jpg" alt="Description of image">
```


### Що таке атрибут?

**Атрибут** – це додаткове значення, яке має тег. Це значення визначає певний спосіб роботи тега на робочій версії веб-сторінки.

Атрибути надаються тегу в тому ж місці, де відображається ім'я тега.

```html
<!-- Example of using <img> tag with src and alt attributes -->
<img src="path/to/image.jpg" alt="Image description">
```


### Які типи заголовків підтримує HTML-документ?

HTML підтримує шість рівнів заголовків, які позначаються за допомогою тегів `<h1>` до `<h6>`. Кожен із цих тегів є заголовок певного рівня, де `<h1>` позначає найвищий рівень заголовка, а `<h6>` — найнижчий. Список типів заголовків зі своїми рівнями:

```html
<h1>This is a level 1 heading</h1>
<h2>This is a level 2 heading</h2>
<h3>This is a level 3 heading</h3>
<h4>This is a level 4 heading</h4>
<h5>This is a level 5 heading</h5>
<h6>This is a level 6 heading</h6>
<p>This is plain text<p>
```

















