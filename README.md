# e-diary

Программа правки плохих оценок в учебном электронном дневнике.  
Исходник сайта, инструкция запуска, описание данных электронного дневника размещены [тут](https://github.com/devmanorg/e-diary).

## Запуск
Поместите файл `scripts.py` в корневой каталог проекта сайта, рядом с `manage.py`.
Запустите из командной строки:
```bash
python scripts.py Фамилия Предмет
```
Регистр букв важен!

## Как работает
Программа, удаляет замечания учителей, исправляет оценки ниже 4, лайкает ученика по предметам.  
По умолчанию исправления работают по ученикам 6А класса.
Пример работы программы:
```shell
python scripts.py 'Фролов Иван' 'Технология'
Исправлено оценок - 263
Удалено замечаний - 8
Похвала: Это как раз то, что нужно! от Одинцов Арефий Трофимович по Технология 6 класса
```

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).