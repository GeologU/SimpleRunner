 - [Some common words](#some-common-words)
 - [bashrc](#bashrc)
 - [skeleton.sh](#skeletonsh)
    - [Run](#run)
    - [Help](#help)
    - [Dependency graph](#dependency-graph)
    - [Helper functions](#helper-functions)
 - [skeleton.py](#skeletonpy)
    - [Running](#running)
    - [Adding new utilities](#adding-new-utilities)
    - [Very useful moment](#very-useful-moment)
    - [with_html.py and its unit tests with_html_ut.py](#with_htmlpy-and-its-unit-tests-with_html_utpy)
    - [skeleton_json.py](#skeleton_jsonpy)

### Some common words

Essential time in my work I was engaged in infrastructural tasks in IT companies.
More precisely, the launch of certain tasks and monitoring their execution.

This project demonstrates a few simple ideas that can make your work more visible
and as a result to allow to complete it with fewer bugs and more fun from work.

Ideas are:
 - write down why you need this piece of code, because with the accumulation of the number of functional blocks, you will forget the very existence of some of them;
 - for related tasks, in an explicit form, record their relations, since this simplifies support and allows you to build more complex schemes.

The project can be especially useful for debugging and prototyping.

The code is written in this form to avoid unnecessary dependencies and complex environments.
I am aware of the existence of [GNU Make](http://www.gnu.org/software/make/), [Celery](http://www.celeryproject.org/) and other similar products (a separate hi to [REM](https://github.com/heni/rem) :wink:).

### bashrc

Part of my `~/.bashrc`, maybe will be useful to someone else.
Complement PS1 (prompt line [Bash](http://www.gnu.org/software/bash/manual/bashref.html)):
 - shows username: root displays in red, the rest are green (by analogy other service users can be marked with color, if necessary);
 - shows the working directory;
 - shows the name of the machine, which is convenient when working with multiple servers;
 - shows the line `user@host:/path`, so that it can be immediately copied in arguments of commands like `scp`;
 - shows the time for displaying the prompt line so that you can judge the start and end time of the commands;
 - shows the result of the previous command with the name of the signal that interrupted it;
 - highlights the result of a successful command in a green, unsuccessful in a red color.

```bash
* $?=0 | 2017-09-06 17:43:53 | alex@r5h:/home/alex *
$ true

* $?=0 | 2017-09-06 17:43:57 | alex@r5h:/home/alex *
$ false

* $?=1 | 2017-09-06 17:44:00 | alex@r5h:/home/alex *
$

* $?=0 | 2017-09-06 17:46:02 | alex@r5h:/home/alex *
$ sleep 20
Completed 

* $?=SIGTERM | 2017-09-06 17:46:38 | alex@r5h:/home/alex *
$
```

### skeleton.sh

#### Run

With the help of the line at the beginning of the file `set -e -o pipefail` we save very, very much time and mental health.
`set -e` causes the execution to fail when an error occurs in any simple command e.g. `ls` on a missing file somewhere in the middle of the script.
`set -o pipefail` leads to an error in the command line if at least one command from the pipeline failed.
In other words, these settings allow you to see the error.

By inserting at the end of the script
```bash
if [ -z "$1" ] || [ "$1" == "--help" ]; then
    usage
else
    "$@"
fi
```
we can call any function by name, command line arguments will be passed to function arguments
```bash
$ ./skeleton.sh greetings Mark "ta, 6ta" Ann
Hello, Mark!
Hello, ta, 6ta!
Hello, Ann!
```
Accordingly, a lot of commands (large and small) we can put together in one file to not look for the right on many files.

#### Help

It is convenient to have commands descriptions.
```bash
$ ./skeleton.sh usage
greetings            say Hello to arguments
make                 echo Make
my                   echo my
day                  echo day
make_my_day          run in parallel: make, my, day
```

To do this, each function must be able to handle the argument `--help`.

An example of the lack of the description:
```bash
$ cat skeleton.sh
...
no_help_example() {
    [ "$1" == "--help" ] && return 0 || true
...
```
Please note that this function will not be displayed in the output of `$ skeleton.sh usage` at all.

An example of the recommended (one simple line) description:
```bash
$ cat skeleton.sh
...
greetings() {
    [ "$1" == "--help" ] && _help_and_exit "say Hello to arguments" || true
...
```

But there are no restrictions on the output of the function for the argument `--help` and you can do more complicated things:
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

The description of the command is generated as a string to substitute in it the value of variables:
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

#### Dependency graph

It is convenient to look at these links explicitly when commands are depend on each other.
To do this, use [Graphviz](http://www.graphviz.org/) for the graph and [Feh](https://wiki.archlinux.org/index.php/feh) for viewing.
On Ubuntu you can install these packages via `$ sudo apt install graphviz feh`.

```bash
$ ./skeleton.sh svg
```

Dependencies are specified explicitly and each function must be able to handle the argument `--deps`.

Without dependencies:
```bash
$ cat skeleton.sh
...
greetings() {
    [ "$1" == "--deps" ] && return 0 || true
...
```

With dependencies:
```bash
$ cat skeleton.sh
...
make_my_day() {
    [ "$1" == "--deps" ] && _deps_and_exit "make" "my" "day" || true
...
```

#### Helper functions

File `skeleton.sh` contains a few helper functions, which add the desired functionality.
It is assumed that working with your commands these you leave as it is:
 - `_help_and_exit` - described above;
 - `_deps_and_exit` - described above;
 - `print_functions` - shows all available functions, because `usage` is not showing the function without description lines and functions whose name starts with an underscore;
 - `print_hidden` - shows only those functions that are not shown by `usage`;
 - `usage` - described above;
 - `_make_dot_file` - is in use by `svg`;
 - `svg` - described above.

Like `usage`, `svg` ignores functions whose name begins with an underscore.

### skeleton.py

The GUI can provide the user with a lot of heterogeneous information and many controls at the same time.
Relatively simple, portable and understandable by a different user method is to use HTML and a browser.
Dynamically generated pages allow you to build complex work scenarios.

The standard Python library contains an HTTP server implementation that with minimal
additions can be used for real work.

#### Running

By default, a multi-threaded server is started on port 8000:
```bash
$ ./skeleton.py
127.0.0.1 - - [09 / Nov / 2017 05:16:21] "GET / HTTP / 1.1" 200 -
...
```
Exit by Ctrl+c.

If you are running from another node, for example `http: //example.com: 8000 /`, make sure that your network settings have the necessary permissions.

`skeleton.py` contains three pages:
 - `/` - contains references to the other two;
 - `/schema/` - shows a picture with dependencies from `./skeleton.sh svg`;
 - `/command/` - shows the table with commands from `./skeleton.sh usage` and their brief description.

#### Adding new utilities

To add new utilities, add a new path to the `do_POST` method (similar to the ones available) and add the code by analogy with the existing `show_*` methods.

Do not forget about the convenience of moving from page to page:
 - on the main page add a reference to the new path;
 - on the new utility page add references to the main page and other potentially useful references.

#### Very useful moment

Graphviz, used by us to visualize dependencies, allows us to create images in svg format with URLs.
That is, the node name can be a link that can be opened in the browser.
In particular, this way you can run different commands by examining the schema in the browser.
[Documentation](http://www.graphviz.org/content/attrs#dURL), [stackoverflow](https://stackoverflow.com/questions/15837283/graphviz-embedded-url).

#### with_html.py and its unit tests with_html_ut.py

I use it to generate HTML.
There are a lot of libraries of this kind, I was interested to write myself.
As an example of use see the end of the `with_html_ut.py` and a few comments in the `with_html.py`.
The HTML is generated, because it's easier for me to write nested tags.
But most importantly, it is much easier to make changes.
For example, replace the table containing lists with the list containing tables via sliding a few lines of code instead of rewriting the entire HTML.

#### with_html_stack.py and its unit tests with_html_stack_ut.py

Further development of `with_html.py` with a simplified interface.
For an example of usage, see the tests in `with_html_stack_ut.py`.

#### skeleton_json.py

Refactoring of skeleton.py (even easier) to work with text and JSON API only. See also `skeleton_json_example.py`.
