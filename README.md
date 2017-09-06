### Some common words

Essential time in my work I was engaged in infrastructural tasks in IT companies.
More precisely, the launch of certain tasks and monitoring their execution.

This project demonstrates a few simple ideas that can make your work more visible
and as a result to allow to complete it with fewer bugs and more fun from work.

Ideas are:
 - write down why you need this piece of code, because with the accumulation of the number of functional blocks, you will forget the very existence of some of them;
 - for related tasks, in an explicit form, record their relations, since this simplifies support and allows you to build more complex schemes.

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

TODO

Try:
```bash
 $ ./skeleton.sh
 $ ./skeleton.sh --help
 $ ./skeleton.sh usage
 $ ./skeleton.sh svg
```

It might need to install additional packages like:
```
$ sudo apt install graphviz feh
```

### skeleton.py

TODO

