# Задание
Разработать инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.

# Формат ввода и вывода
Входной текст на учебном конфигурационном языке принимается из
файла, путь к которому задан ключом командной строки.

Выходной текст наязыке json попадает в файл, путь к которому задан ключом командной строки.

# Конфигурационный язык
Массивы:

( значение, значение, значение, ... )

Словари:

{

 имя => значение,
 
 имя => значение,
 
 имя => значение,
 
 ...
 
}

Имена:

[A-Z]+

Значения:

• Числа.

• Массивы.

• Словари.

Объявление константы на этапе трансляции:

var имя := значение;

Вычисление константного выражения на этапе трансляции (префиксная  форма), пример:

$+ имя 1$

Результатом вычисления константного выражения является значение.

# Операции и функции
Для константных вычислений определены операции и функции:
1. Сложение.
2. mod().

# Требования к тестированию
Все конструкции учебного конфигурационного языка (с учетом их
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2
примера описания конфигураций из разных предметных областей
