 - [Несколько общих слов](#toc-1)
 - [bashrc](#bashrc)
 - [skeleton.sh](#skeletonsh)
    - [Запуск](#sh-run)
    - [Help](#help)
    - [Граф зависимостей](#sh-graph)
    - [Вспомогательные функции](#sh-helpers)
 - [skeleton.py (библиотека) и skeleton_example_html.py (пример)]
    - [Запуск](#py-run)
    - [Добавление новых утилит](#py-add)
    - [Очень полезный момент](#py-note)
    - [with_html_stack.py и его блочные тесты with_html_stack_ut.py](#with_html_stackpy-with_html_stack_utpy)
    - [skeleton_example_json.py.py](#skeleton_example_jsonpy)
 - [lint.sh](#lintsh)

### toc-1 Несколько общих слов

Существенное время в моей работе я занимался инфраструктурными задачами в IT компаниях.
Если точнее, запуск неких задач и контроль их выполнения.

Этот проект демонстрирует несколько простых идей, которые могут сделать вашу работу нагляднее
и как следствие позволить завершить её с меньшим числом багов и большим удовольствием от работы.

Идеи таковы:
 - записывать для чего вам этот кусок кода, т.к. с накоплением числа функциональных блоков вы будете забывать о самом существовании некоторых из них;
 - для связанных задач в явном виде записывать их связи, т.к. это упрощает поддержку и позволяет строить более сложные схемы.

Проект может быть особенно полезен при отладке и прототипировании.

Код написан в таком виде чтобы избежать лишних зависимостей и сложного окружения.
Я осведомлён о существовании [GNU Make](http://www.gnu.org/software/make/), [Celery](http://www.celeryproject.org/) и других подобных продуктов (отдельный привет [REM](https://github.com/heni/rem) :wink:).

### bashrc

Часть моего `~/.bashrc`, возможно будет полезной кому-то ещё.
Дополняет PS1 (строку приглашения [Bash](http://www.gnu.org/software/bash/manual/bashref.html)):
 - показывает имя пользователя: root отображает красным, остальные зелёным (по аналогии могут быть отмечены цветом другие служебные пользователи, при необходимости);
 - показывает рабочий каталог;
 - показывает имя машины, что удобно при работе с несколькими серверами;
 - показывает строчку `user@host:/path`, чтобы можно было её сразу скопировать в аргументы команд вроде `scp`;
 - показывает время вывода строки приглашения, чтобы можно было судить о времени запуска и окончания работы команд;
 - показывает результат работы предыдущей команды с указанием имени сигнала, прервавшего программу;
 - подсвечивает результат успешной команды зелёным, неуспешной красным цветом даже для команд из конвейера.

```bash
$ true

* $? = 0 | 2021-07-23 00:08:25 | alex@r9h:/home/alex/git/SimpleRunner *
$ false

* $? = 1 | 2021-07-23 00:08:27 | alex@r9h:/home/alex/git/SimpleRunner *
$

* $? = 1 | 2021-07-23 00:08:31 | alex@r9h:/home/alex/git/SimpleRunner *
$ sleep 20
^C

* $? = SIGINT | 2021-07-23 00:08:38 | alex@r9h:/home/alex/git/SimpleRunner *
$ echo hi | grep by | wc -l
0

* $? = 0 1 0 | 2021-07-23 00:08:43 | alex@r9h:/home/alex/git/SimpleRunner *
$
```

### skeleton.sh

#### Запуск _sh-run_

С помощью строки в начале файла `set -e -o pipefail` мы экономим очень, очень много времени и душевного здоровья.
`set -e` приводит к тому, что выполнение завершается с ошибкой при ошибке в любой простой команде, например `ls` на отсутствующий файл где-то в середине скрипта.
`set -o pipefail` приводит к ошибке в команде с конвейером, если хотя бы одна команда из конвейера дала ошибку.
Другими словами, эти настройки позволяют видеть ошибки.

С помощью вставки в конце скрипта
```bash
if [ -z "$1" ] || [ "$1" == "--help" ]; then
    usage
else
    "$@"
fi
```
мы получаем возможность вызывать любую функцию по имени, аргументы командной строки будут переданы в аргументы функции
```bash
$ ./skeleton.sh greetings Mark "ta, 6ta" Ann
Hello, Mark!
Hello, ta, 6ta!
Hello, Ann!
```
Соответственно много команд (больших и не очень) мы можем сложить в один файл, чтобы не искать нужное по многим файлам.

#### Help

Удобно иметь строчку с описанием команды.
```bash
$ ./skeleton.sh usage
greetings            say Hello to arguments
make                 echo Make
my                   echo my
day                  echo day
make_my_day          run in parallel: make, my, day
```

Для этого каждая функция должна уметь обработать аргумент `--help`.

Пример отсутствия описания:
```bash
$ cat skeleton.sh
...
no_help_example() {
    [ "$1" == "--help" ] && return 0 || true
...
```
Обратите внимание, что такая функция не будет отображена в выводе `$ skeleton.sh usage` совсем.

Пример рекомендуемого (одна простая строчка) описания:
```bash
$ cat skeleton.sh
...
greetings() {
    [ "$1" == "--help" ] && _help_and_exit "say Hello to arguments" || true
...
```

Но никаких ограничений на вывод функции по аргументу `--help` нет, и вы можете делать более сложные вещи:
```bash
$ cat skeleton.sh
...
print_functions() {
    if [ "$1" == "--help" ]; then
        echo
        _help_and_exit "print all functions names"
    fi
...
```

Описание команды формируется как строка чтобы можно было подставлять в неё значение переменных:
```bash
$ cat skeleton.sh
...
usage() {
        [ "$1" == "--help" ] && _help_and_exit "[or $(basename "$SELFNAME") --help] show this help message and exit"  || true
...
$ ./skeleton.sh 
...
usage                [or skeleton.sh --help] show this help message and exit
$
```

#### Граф зависимостей _sh-graph_

Когда команды зависят друг от друга, удобна возможность посмотреть эти связи в явном виде.
Для этого используем [Graphviz](http://www.graphviz.org/) для графа и [Feh](https://wiki.archlinux.org/index.php/feh) для просмотра.
На Ubuntu они добавляются установкой пакетов `$ sudo apt install graphviz feh`

```bash
$ ./skeleton.sh svg
```

Связи указываются в явном виде и для этого каждая функция должна уметь обработать аргумент `--deps`.

Без зависимостей:
```bash
$ cat skeleton.sh
...
greetings() {
    [ "$1" == "--deps" ] && return 0 || true
...
```

С зависимостями:
```bash
$ cat skeleton.sh
...
make_my_day() {
    [ "$1" == "--deps" ] && _deps_and_exit "make" "my" "day" || true
...
```

#### Вспомогательные функции _sh-helpers_

Файл `skeleton.sh` содержит несколько вспомогательных функций, которые и добавляют нужную функциональность.
Предполагается, что работая с вашими командами эти вы оставите как есть:
 - `_help_and_exit` - описана выше;
 - `_deps_and_exit` - описана выше;
 - `print_functions` - показывает все имеющиеся функции, т.к. `usage` не показывает функции без строки описания и функции, чьё имя начинается с подчёркивания;
 - `print_hidden` - показывает только те функции, которые не показывает `usage`;
 - `usage` - описана выше;
 - `_make_dot_file` - используется в работе функции `svg`;
 - `svg` - описана выше.

Как и `usage`, `svg` игнорирует функции, чьё имя начинается с подчёркивания.

### skeleton.py (библиотека) и skeleton_example_html.py (пример)

GUI может предоставить пользователю много разнородной информации и много элементов управления одновременно.
Относительно простой, переносимый и понятный разным пользователем способ - использовать HTML и браузер.
Динамически формируемые страницы позволяют выстраивать сложные сценарии работы.

Стандартная библиотека Python содержит реализацию HTTP сервера, которая с минимальными
дополнениями может быть использована для реальной работы.

#### Запуск

По умолчанию запускается многопочный сервер на порту 8000:
```bash
$ ./skeleton_example_html.py
127.0.0.1 - - [09/Nov/2017 05:16:21] "GET / HTTP/1.1" 200 -
...
```
Выход по Ctrl+c.

Если работаете с другой машины, например `http://example.com:8000/`, убедитесь, что настройки вашей сети имеют необходимые разрешения.

`skeleton_example_html.py` содержит три страницы:
 - `/` - содержит ссылки на две другие;
 - `/schema/` - показывает картинку со связями из `./skeleton.sh svg`;
 - `/command/` - показывает таблицу с командами из `./skeleton.sh usage` и их кратким описанием.

#### Добавление новых утилит

Для добавления новых утилит допишите новый путь в метод `do_POST` (по аналогии с имеющимися) и добавьте код по аналогии с существующими методами `show_*`.

Не забывайте об удобстве перехода со страницы на страницу:
 - на главной странице добавьте ссылку на новый путь;
 - на странице новой утилиты добавьте ссылки на главную страницу и другие потенциально полезные ссылки.

#### Обратите внимание

Используемый нами для визуализации зависимостей Graphviz позволяет создавать картинки в формате svg с урлами.
То есть, имя узла может быть ссылкой, которую можно открыть в браузере.
В частности, таким образом можно запускать разные команды рассматривая в браузере схему.
[Документация](http://www.graphviz.org/content/attrs#dURL), [stackoverflow](https://stackoverflow.com/questions/15837283/graphviz-embedded-url).

#### skeleton_example_json.py

Пример использования `skeleton.py`, когда сервер отдаёт только JSON.
Не тратим усилия даже на минимальный HTML.
Фокус в том, что Firefox (про другие браузеры не скажу) "из коробки" умеет красиво отобразить JSON.
В том числе можно кликать по ссылкам, которые есть в JSON, как на обычной странице HTML.
В отличии от HTML тут не сделать форм для ввода данных, зато легко предварительно создать несколько ссылок, которые могут быть интересны.
Итого разный текст показать можно, легко переходить между "страницами" тоже можно и накладных расходов около ноля.

#### with_html_stack.py и его блочные тесты with_html_stack_ut.py

Подобного рода библиотек много, мне было интересно написать самому.
В качестве примера использования смотрите конец `with_html_stack_ut.py` и комментарии в самом `with_html_stack.py`.
HTML генерируется, т.к. мне так проще писать вложенные теги.

### lint.sh

Запустить `isort`, `black`, `pylint` и `mypy` последовательно на файл `.py`.
`isort` и `black` поправят файл на месте.
При наличии данных от `pylint` (`mypy`) будет открыт `vim` c двумя файлами: `.py` и комментарии `pylint` (`mypy`).
Если на каком-то шаге файл `.py` будет изменён, то скрипт завершит работу с ошибкой, т.к. могут потребоваться другие (ручные) изменения.
Предполагаемый цикл использования: запуск -> правки в процессе -> ошибка -> запуск -> правки в процессе -> ошибка -> запуск -> правок больше нет -> закончили улучшать `.py`.

```bash
$ ./lint.sh skeleton.py
Run isort (utility to sort Python imports) on skeleton.py
Run pylint (python code static checker) on skeleton.py
Файлов для редактирования: 2
Run black (the uncompromising code formatter) on skeleton.py
All done! ✨ 🍰 ✨
1 file left unchanged.
Run mypy (static typing for Python) on skeleton.py
```

#### requirements.in, requirements.txt, requirements.sh

Зависимости для запуска `lint.sh`. Начните с комментариев в `requirements.sh`.
