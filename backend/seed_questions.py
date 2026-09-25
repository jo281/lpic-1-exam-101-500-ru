"""
Полный банк вопросов для экзамена LPI 101-500 (LPIC-1).
Составлен на основе официальных целей LPI:
https://learning.lpi.org/en/learning-materials/101-500/

Всего ~180 вопросов, распределённых по темам пропорционально их весу (weight).
"""
import os
import sys

from database import engine, SessionLocal
from models import Base, Question

# Создаём таблицы
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Проверяем, есть ли уже вопросы
existing = db.query(Question).count()
if existing > 0:
    print(f"⚠️  В базе уже есть {existing} вопросов. Пропускаю сидирование.")
    db.close()
    sys.exit(0)

questions_data = [
    # ═══════════════════════════════════════════════════════════════
    # 101.1 Determine and configure hardware settings (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "101.1",
        "question_type": "text",
        "text": "Какая команда (только имя, без флагов) выводит список всех подключённых устройств PCI?",
        "options": None,
        "correct_answer": "lspci",
        "explanation": "lspci показывает все PCI-шины и подключённые устройства.",
    },
    {
        "topic": "101.1",
        "question_type": "single",
        "text": "Какой файл содержит информацию о загруженных модулях ядра?",
        "options": [
            {"id": "A", "text": "/proc/modules"},
            {"id": "B", "text": "/etc/modules.conf"},
            {"id": "C", "text": "/var/log/modules"},
            {"id": "D", "text": "/sys/modules"},
        ],
        "correct_answer": "A",
        "explanation": "/proc/modules содержит список всех загруженных модулей ядра.",
    },
    {
        "topic": "101.1",
        "question_type": "multiple",
        "text": "Какие ДВЕ команды дают информацию о процессоре? (Выберите 2)",
        "options": [
            {"id": "A", "text": "lscpu"},
            {"id": "B", "text": "cpuinfo"},
            {"id": "C", "text": "cat /proc/cpuinfo"},
            {"id": "D", "text": "ls /cpu"},
            {"id": "E", "text": "procinfo"},
        ],
        "correct_answer": "A,C",
        "explanation": "lscpu и cat /proc/cpuinfo обе предоставляют информацию о CPU.",
    },
    {
        "topic": "101.1",
        "question_type": "text",
        "text": "Какая команда (только имя) загружает модуль ядра вместе с его зависимостями?",
        "options": None,
        "correct_answer": "modprobe",
        "explanation": "modprobe загружает модуль и разрешает зависимости. insmod — без разрешения зависимостей.",
    },
    {
        "topic": "101.1",
        "question_type": "single",
        "text": "Где обычно хранится информация о подключённых USB-устройствах в procfs?",
        "options": [
            {"id": "A", "text": "/proc/usb"},
            {"id": "B", "text": "/proc/bus/usb/devices"},
            {"id": "C", "text": "/proc/devices/usb"},
            {"id": "D", "text": "/sys/usb/info"},
        ],
        "correct_answer": "B",
        "explanation": "В старых ядрах — /proc/bus/usb/devices, в новых — /sys/bus/usb/devices/.",
    },
    {
        "topic": "101.1",
        "question_type": "text",
        "text": "Какая команда выгружает модуль ядра из памяти?",
        "options": None,
        "correct_answer": "rmmod",
        "explanation": "rmmod удаляет модуль из ядра. Модуль не должен использоваться.",
    },
    {
        "topic": "101.1",
        "question_type": "single",
        "text": "Какой файл содержит конфигурацию модулей ядра (алиасы, опции)?",
        "options": [
            {"id": "A", "text": "/etc/modprobe.conf или /etc/modprobe.d/*.conf"},
            {"id": "B", "text": "/etc/modules.conf"},
            {"id": "C", "text": "/proc/modules.conf"},
            {"id": "D", "text": "/etc/kernel/modules"},
        ],
        "correct_answer": "A",
        "explanation": "Современные системы используют /etc/modprobe.d/*.conf. Старый /etc/modules.conf устарел.",
    },
    {
        "topic": "101.1",
        "question_type": "multiple",
        "text": "Какие ДВЕ команды показывают информацию о блочных устройствах? (Выберите 2)",
        "options": [
            {"id": "A", "text": "lsblk"},
            {"id": "B", "text": "blkid"},
            {"id": "C", "text": "fdisk -l"},
            {"id": "D", "text": "cat /proc/cpuinfo"},
            {"id": "E", "text": "lspci"},
        ],
        "correct_answer": "A,B",
        "explanation": "lsblk показывает блочные устройства в виде дерева. blkid показывает UUID и тип ФС.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 101.2 Boot the system (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "101.2",
        "question_type": "single",
        "text": "Где хранится основной конфигурационный файл GRUB2?",
        "options": [
            {"id": "A", "text": "/boot/grub/grub.conf"},
            {"id": "B", "text": "/boot/grub2/grub.cfg"},
            {"id": "C", "text": "/etc/grub.conf"},
            {"id": "D", "text": "/boot/grub/menu.lst"},
        ],
        "correct_answer": "B",
        "explanation": "GRUB2 использует /boot/grub2/grub.cfg (или /boot/grub/grub.cfg в Debian).",
    },
    {
        "topic": "101.2",
        "question_type": "text",
        "text": "Какая команда пересоздаёт конфигурационный файл GRUB2 в Debian/Ubuntu?",
        "options": None,
        "correct_answer": "update-grub",
        "explanation": "update-grub — обёртка над grub-mkconfig, генерирует grub.cfg.",
    },
    {
        "topic": "101.2",
        "question_type": "single",
        "text": "Какая команда показывает сообщения кольцевого буфера ядра?",
        "options": [
            {"id": "A", "text": "syslog"},
            {"id": "B", "text": "dmesg"},
            {"id": "C", "text": "journalctl"},
            {"id": "D", "text": "bootlog"},
        ],
        "correct_answer": "B",
        "explanation": "dmesg выводит сообщения из kernel ring buffer.",
    },
    {
        "topic": "101.2",
        "question_type": "text",
        "text": "Какая команда обновляет initramfs в Debian/Ubuntu?",
        "options": None,
        "correct_answer": "update-initramfs",
        "explanation": "update-initramfs обновляет образ initramfs с драйверами для загрузки.",
    },
    {
        "topic": "101.2",
        "question_type": "single",
        "text": "Какой параметр ядра используется для указания корневого раздела?",
        "options": [
            {"id": "A", "text": "root="},
            {"id": "B", "text": "rootfs="},
            {"id": "C", "text": "boot="},
            {"id": "D", "text": "init="},
        ],
        "correct_answer": "A",
        "explanation": "root= указывает ядру, какой раздел монтировать как корневой.",
    },
    {
        "topic": "101.2",
        "question_type": "text",
        "text": "Какая команда в GRUB2 пересоздаёт конфигурацию в RHEL/CentOS?",
        "options": None,
        "correct_answer": "grub2-mkconfig",
        "explanation": "grub2-mkconfig генерирует grub.cfg. В Debian используется update-grub.",
    },
    {
        "topic": "101.2",
        "question_type": "single",
        "text": "Какой файл содержит параметры ядра по умолчанию в systemd-системах?",
        "options": [
            {"id": "A", "text": "/etc/default/grub"},
            {"id": "B", "text": "/boot/grub/grub.cfg"},
            {"id": "C", "text": "/etc/kernel/cmdline"},
            {"id": "D", "text": "/proc/cmdline"},
        ],
        "correct_answer": "A",
        "explanation": "/etc/default/grub содержит GRUB_CMDLINE_LINUX и другие параметры.",
    },
    {
        "topic": "101.2",
        "question_type": "multiple",
        "text": "Какие ДВА файла используются для настройки загрузчика LILO? (Выберите 2)",
        "options": [
            {"id": "A", "text": "/etc/lilo.conf"},
            {"id": "B", "text": "/boot/lilo.conf"},
            {"id": "C", "text": "/etc/lilo/lilo.conf"},
            {"id": "D", "text": "/boot/grub/grub.cfg"},
            {"id": "E", "text": "/etc/default/lilo"},
        ],
        "correct_answer": "A,B",
        "explanation": "LILO использует /etc/lilo.conf или /boot/lilo.conf. После изменений нужно запустить lilo.",
    },
    {
        "topic": "101.2",
        "question_type": "text",
        "text": "Какая команда устанавливает загрузчик LILO после изменения конфигурации?",
        "options": None,
        "correct_answer": "lilo",
        "explanation": "Команда lilo без параметров перечитывает конфигурацию и записывает загрузчик в MBR.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 101.3 Change runlevels / boot targets and shutdown (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "101.3",
        "question_type": "single",
        "text": "Какой systemd target эквивалентен классическому runlevel 3 (multi-user, без GUI)?",
        "options": [
            {"id": "A", "text": "poweroff.target"},
            {"id": "B", "text": "rescue.target"},
            {"id": "C", "text": "multi-user.target"},
            {"id": "D", "text": "graphical.target"},
        ],
        "correct_answer": "C",
        "explanation": "multi-user.target — многопользовательский режим без GUI. graphical.target — с GUI.",
    },
    {
        "topic": "101.3",
        "question_type": "text",
        "text": "Какой командой systemd можно переключиться в single-user (rescue) режим?",
        "options": None,
        "correct_answer": "systemctl isolate rescue.target",
        "explanation": "systemctl isolate <target> останавливает все юниты, не входящие в указанный target.",
    },
    {
        "topic": "101.3",
        "question_type": "single",
        "text": "Какая команда корректно выключает систему через 10 минут?",
        "options": [
            {"id": "A", "text": "shutdown -h 10"},
            {"id": "B", "text": "poweroff -t 10"},
            {"id": "C", "text": "halt -d 10"},
            {"id": "D", "text": "init 0 +10"},
        ],
        "correct_answer": "A",
        "explanation": "shutdown -h 10 — выключение через 10 минут. -h означает halt/poweroff.",
    },
    {
        "topic": "101.3",
        "question_type": "text",
        "text": "Какая команда перезагружает систему немедленно?",
        "options": None,
        "correct_answer": "reboot",
        "explanation": "reboot немедленно перезагружает систему. shutdown -r now — альтернатива.",
    },
    {
        "topic": "101.3",
        "question_type": "single",
        "text": "Какой runlevel в SysVinit соответствует перезагрузке?",
        "options": [
            {"id": "A", "text": "0"},
            {"id": "B", "text": "1"},
            {"id": "C", "text": "6"},
            {"id": "D", "text": "10"},
        ],
        "correct_answer": "C",
        "explanation": "Runlevel 6 — перезагрузка. 0 — выключение. 1 — single-user.",
    },
    {
        "topic": "101.3",
        "question_type": "text",
        "text": "Какая команда показывает текущий runlevel в SysVinit?",
        "options": None,
        "correct_answer": "runlevel",
        "explanation": "runlevel показывает предыдущий и текущий runlevel.",
    },
    {
        "topic": "101.3",
        "question_type": "single",
        "text": "Какой systemd target эквивалентен runlevel 0 (выключение)?",
        "options": [
            {"id": "A", "text": "poweroff.target"},
            {"id": "B", "text": "halt.target"},
            {"id": "C", "text": "shutdown.target"},
            {"id": "D", "text": "reboot.target"},
        ],
        "correct_answer": "A",
        "explanation": "poweroff.target — выключение. halt.target — остановка без выключения питания.",
    },
    {
        "topic": "101.3",
        "question_type": "multiple",
        "text": "Какие ДВЕ команды корректно выключают систему? (Выберите 2)",
        "options": [
            {"id": "A", "text": "shutdown -h now"},
            {"id": "B", "text": "poweroff"},
            {"id": "C", "text": "halt -p"},
            {"id": "D", "text": "init 0"},
            {"id": "E", "text": "reboot -h"},
        ],
        "correct_answer": "A,B",
        "explanation": "shutdown -h now, poweroff, init 0 — все корректно выключают систему.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 102.1 Customize and use the shell environment (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "102.1",
        "question_type": "single",
        "text": "Какой файл выполняется при логине пользователя в bash?",
        "options": [
            {"id": "A", "text": "~/.bashrc"},
            {"id": "B", "text": "~/.profile или ~/.bash_profile"},
            {"id": "C", "text": "/etc/bashrc"},
            {"id": "D", "text": "~/.bash_logout"},
        ],
        "correct_answer": "B",
        "explanation": "При login shell читается ~/.bash_profile, ~/.bash_login или ~/.profile (первый найденный).",
    },
    {
        "topic": "102.1",
        "question_type": "text",
        "text": "Какая переменная окружения содержит список каталогов, в которых shell ищет исполняемые файлы?",
        "options": None,
        "correct_answer": "PATH",
        "explanation": "PATH — список каталогов через ':', в которых ищутся команды.",
    },
    {
        "topic": "102.1",
        "question_type": "single",
        "text": "Какая команда показывает все установленные переменные окружения?",
        "options": [
            {"id": "A", "text": "env или printenv"},
            {"id": "B", "text": "set"},
            {"id": "C", "text": "export"},
            {"id": "D", "text": "echo $*"},
        ],
        "correct_answer": "A",
        "explanation": "env и printenv показывают переменные окружения. set — ещё и shell-переменные и функции.",
    },
    {
        "topic": "102.1",
        "question_type": "text",
        "text": "Какая команда делает переменную доступной для дочерних процессов?",
        "options": None,
        "correct_answer": "export",
        "explanation": "export VAR=value делает переменную переменной окружения.",
    },
    {
        "topic": "102.1",
        "question_type": "single",
        "text": "Какой файл выполняется при запуске интерактивного non-login bash?",
        "options": [
            {"id": "A", "text": "~/.bash_profile"},
            {"id": "B", "text": "~/.bashrc"},
            {"id": "C", "text": "~/.profile"},
            {"id": "D", "text": "/etc/profile"},
        ],
        "correct_answer": "B",
        "explanation": "Интерактивный non-login shell читает ~/.bashrc.",
    },
    {
        "topic": "102.1",
        "question_type": "text",
        "text": "Какая переменная окружения содержит домашний каталог текущего пользователя?",
        "options": None,
        "correct_answer": "HOME",
        "explanation": "HOME содержит полный путь к домашнему каталогу пользователя.",
    },
    {
        "topic": "102.1",
        "question_type": "single",
        "text": "Какой символ используется для обращения к значению переменной в bash?",
        "options": [
            {"id": "A", "text": "$"},
            {"id": "B", "text": "&"},
            {"id": "C", "text": "#"},
            {"id": "D", "text": "@"},
        ],
        "correct_answer": "A",
        "explanation": "$VAR или ${VAR} обращается к значению переменной.",
    },
    {
        "topic": "102.1",
        "question_type": "multiple",
        "text": "Какие ДВА файла выполняются при логине в bash? (Выберите 2)",
        "options": [
            {"id": "A", "text": "/etc/profile"},
            {"id": "B", "text": "~/.bashrc"},
            {"id": "C", "text": "~/.bash_profile"},
            {"id": "D", "text": "~/.bash_logout"},
            {"id": "E", "text": "/etc/bashrc"},
        ],
        "correct_answer": "A,C",
        "explanation": "При login shell выполняются /etc/profile, затем ~/.bash_profile (или ~/.profile).",
    },
    {
        "topic": "102.1",
        "question_type": "text",
        "text": "Какая команда удаляет переменную окружения?",
        "options": None,
        "correct_answer": "unset",
        "explanation": "unset VAR удаляет переменную из окружения.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 102.2 Customize or write simple scripts (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "102.2",
        "question_type": "single",
        "text": "Что означает $1 в bash-скрипте?",
        "options": [
            {"id": "A", "text": "Первый аргумент скрипта"},
            {"id": "B", "text": "PID скрипта"},
            {"id": "C", "text": "Имя скрипта"},
            {"id": "D", "text": "Количество аргументов"},
        ],
        "correct_answer": "A",
        "explanation": "$1 — первый позиционный аргумент. $0 — имя скрипта. $# — количество аргументов. $$ — PID.",
    },
    {
        "topic": "102.2",
        "question_type": "text",
        "text": "Какой shebang (первая строка) должен быть у bash-скрипта?",
        "options": None,
        "correct_answer": "#!/bin/bash",
        "explanation": "#!/bin/bash указывает, что скрипт должен выполняться интерпретатором bash.",
    },
    {
        "topic": "102.2",
        "question_type": "single",
        "text": "Какой оператор используется для проверки равенства строк в bash?",
        "options": [
            {"id": "A", "text": "="},
            {"id": "B", "text": "=="},
            {"id": "C", "text": "-eq"},
            {"id": "D", "text": "equals"},
        ],
        "correct_answer": "A",
        "explanation": "В [ ] для строк используется =. -eq — для чисел.",
    },
    {
        "topic": "102.2",
        "question_type": "text",
        "text": "Какой оператор используется для проверки равенства чисел в bash?",
        "options": None,
        "correct_answer": "-eq",
        "explanation": "-eq — равно. -ne — не равно. -lt — меньше. -gt — больше.",
    },
    {
        "topic": "102.2",
        "question_type": "single",
        "text": "Какая конструкция используется для цикла по списку в bash?",
        "options": [
            {"id": "A", "text": "for ... in ... do ... done"},
            {"id": "B", "text": "loop ... end"},
            {"id": "C", "text": "foreach ... end"},
            {"id": "D", "text": "while ... do ... done"},
        ],
        "correct_answer": "A",
        "explanation": "for var in list; do ... done — цикл по элементам списка.",
    },
    {
        "topic": "102.2",
        "question_type": "text",
        "text": "Какой специальный символ используется для подстановки результата команды в bash?",
        "options": None,
        "correct_answer": "$() или ``",
        "explanation": "$(command) или `command` подставляет вывод команды. Предпочтительнее $().",
    },
    {
        "topic": "102.2",
        "question_type": "single",
        "text": "Какой код возврата означает успешное выполнение команды?",
        "options": [
            {"id": "A", "text": "0"},
            {"id": "B", "text": "1"},
            {"id": "C", "text": "true"},
            {"id": "D", "text": "success"},
        ],
        "correct_answer": "A",
        "explanation": "0 — успех. Любое ненулевое значение — ошибка.",
    },
    {
        "topic": "102.2",
        "question_type": "text",
        "text": "Какая переменная содержит код возврата последней выполненной команды?",
        "options": None,
        "correct_answer": "$?",
        "explanation": "$? содержит exit status последней команды.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 102.3 SQL data management (weight: 2)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "102.3",
        "question_type": "single",
        "text": "Какой SQL-запрос выбирает все записи из таблицы users?",
        "options": [
            {"id": "A", "text": "SELECT * FROM users;"},
            {"id": "B", "text": "GET ALL FROM users;"},
            {"id": "C", "text": "SELECT users;"},
            {"id": "D", "text": "FETCH * FROM users;"},
        ],
        "correct_answer": "A",
        "explanation": "SELECT * FROM table — стандартный SQL-запрос для выбора всех записей.",
    },
    {
        "topic": "102.3",
        "question_type": "text",
        "text": "Какой SQL-оператор используется для вставки данных в таблицу?",
        "options": None,
        "correct_answer": "INSERT",
        "explanation": "INSERT INTO table (columns) VALUES (values) — вставка записей.",
    },
    {
        "topic": "102.3",
        "question_type": "single",
        "text": "Какой SQL-оператор используется для обновления существующих записей?",
        "options": [
            {"id": "A", "text": "UPDATE"},
            {"id": "B", "text": "MODIFY"},
            {"id": "C", "text": "CHANGE"},
            {"id": "D", "text": "ALTER"},
        ],
        "correct_answer": "A",
        "explanation": "UPDATE table SET column=value WHERE condition — обновление записей.",
    },
    {
        "topic": "102.3",
        "question_type": "text",
        "text": "Какой SQL-оператор удаляет записи из таблицы?",
        "options": None,
        "correct_answer": "DELETE",
        "explanation": "DELETE FROM table WHERE condition — удаление записей.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.1 Work on the command line (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.1",
        "question_type": "text",
        "text": "Какая команда показывает текущий рабочий каталог?",
        "options": None,
        "correct_answer": "pwd",
        "explanation": "pwd (print working directory) выводит полный путь к текущему каталогу.",
    },
    {
        "topic": "103.1",
        "question_type": "single",
        "text": "Какая команда используется для перехода в предыдущий каталог?",
        "options": [
            {"id": "A", "text": "cd -"},
            {"id": "B", "text": "cd .."},
            {"id": "C", "text": "cd ~"},
            {"id": "D", "text": "cd !"},
        ],
        "correct_answer": "A",
        "explanation": "cd - переключает в предыдущий каталог. cd .. — в родительский. cd ~ — в домашний.",
    },
    {
        "topic": "103.1",
        "question_type": "text",
        "text": "Какая команда показывает содержимое каталога?",
        "options": None,
        "correct_answer": "ls",
        "explanation": "ls (list) показывает файлы и каталоги.",
    },
    {
        "topic": "103.1",
        "question_type": "single",
        "text": "Какой флаг ls показывает скрытые файлы?",
        "options": [
            {"id": "A", "text": "-a"},
            {"id": "B", "text": "-h"},
            {"id": "C", "text": "-l"},
            {"id": "D", "text": "-s"},
        ],
        "correct_answer": "A",
        "explanation": "-a (all) показывает все файлы, включая скрытые (начинающиеся с .).",
    },
    {
        "topic": "103.1",
        "question_type": "text",
        "text": "Какая команда создаёт пустой файл или обновляет его timestamp?",
        "options": None,
        "correct_answer": "touch",
        "explanation": "touch создаёт файл, если его нет, или обновляет время модификации.",
    },
    {
        "topic": "103.1",
        "question_type": "single",
        "text": "Какой символ используется для обращения к домашнему каталогу?",
        "options": [
            {"id": "A", "text": "~"},
            {"id": "B", "text": "$"},
            {"id": "C", "text": "@"},
            {"id": "D", "text": "#"},
        ],
        "correct_answer": "A",
        "explanation": "~ раскрывается в путь к домашнему каталогу текущего пользователя.",
    },
    {
        "topic": "103.1",
        "question_type": "multiple",
        "text": "Какие ДВА символа используются для обращения к родительскому и текущему каталогам? (Выберите 2)",
        "options": [
            {"id": "A", "text": "."},
            {"id": "B", "text": ".."},
            {"id": "C", "text": "..."},
            {"id": "D", "text": "/"},
            {"id": "E", "text": "~"},
        ],
        "correct_answer": "A,B",
        "explanation": ". — текущий каталог. .. — родительский.",
    },
    {
        "topic": "103.1",
        "question_type": "text",
        "text": "Какая команда показывает тип файла (исполняемый, текстовый и т.д.)?",
        "options": None,
        "correct_answer": "file",
        "explanation": "file определяет тип файла по его содержимому.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.2 Process text streams using filters (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.2",
        "question_type": "text",
        "text": "Какая команда сортирует строки файла?",
        "options": None,
        "correct_answer": "sort",
        "explanation": "sort сортирует строки. uniq удаляет соседние дубликаты.",
    },
    {
        "topic": "103.2",
        "question_type": "single",
        "text": "Какая команда удаляет повторяющиеся строки (после сортировки)?",
        "options": [
            {"id": "A", "text": "uniq"},
            {"id": "B", "text": "sort -u"},
            {"id": "C", "text": "cut"},
            {"id": "D", "text": "tr"},
        ],
        "correct_answer": "A",
        "explanation": "uniq удаляет соседние дубликаты. sort -u тоже работает, но uniq — канонический ответ.",
    },
    {
        "topic": "103.2",
        "question_type": "text",
        "text": "Какая команда заменяет символы в потоке (например, переводит в верхний регистр)?",
        "options": None,
        "correct_answer": "tr",
        "explanation": "tr (translate) заменяет или удаляет символы. Пример: tr 'a-z' 'A-Z'.",
    },
    {
        "topic": "103.2",
        "question_type": "single",
        "text": "Какая команда извлекает поля из строк (например, колонки из CSV)?",
        "options": [
            {"id": "A", "text": "cut"},
            {"id": "B", "text": "awk"},
            {"id": "C", "text": "sed"},
            {"id": "D", "text": "split"},
        ],
        "correct_answer": "A",
        "explanation": "cut извлекает поля по разделителю. awk мощнее, но cut проще для базовых задач.",
    },
    {
        "topic": "103.2",
        "question_type": "text",
        "text": "Какая команда показывает последние 10 строк файла?",
        "options": None,
        "correct_answer": "tail",
        "explanation": "tail по умолчанию показывает последние 10 строк.",
    },
    {
        "topic": "103.2",
        "question_type": "single",
        "text": "Какой флаг tail позволяет отслеживать изменения файла в реальном времени?",
        "options": [
            {"id": "A", "text": "-f"},
            {"id": "B", "text": "-r"},
            {"id": "C", "text": "-l"},
            {"id": "D", "text": "-t"},
        ],
        "correct_answer": "A",
        "explanation": "tail -f (follow) показывает новые строки по мере их добавления в файл.",
    },
    {
        "topic": "103.2",
        "question_type": "text",
        "text": "Какая команда подсчитывает количество строк, слов и байтов в файле?",
        "options": None,
        "correct_answer": "wc",
        "explanation": "wc (word count) считает строки (-l), слова (-w), байты (-c).",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.3 Perform basic file management (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.3",
        "question_type": "text",
        "text": "Какая команда копирует файлы и каталоги рекурсивно?",
        "options": None,
        "correct_answer": "cp -r",
        "explanation": "cp -r (recursive) копирует каталоги со всем содержимым.",
    },
    {
        "topic": "103.3",
        "question_type": "single",
        "text": "Какая команда удаляет непустой каталог со всем содержимым?",
        "options": [
            {"id": "A", "text": "rm -rf"},
            {"id": "B", "text": "rmdir"},
            {"id": "C", "text": "rm -d"},
            {"id": "D", "text": "del -r"},
        ],
        "correct_answer": "A",
        "explanation": "rm -rf удаляет рекурсивно и без вопросов. rmdir удаляет только пустые каталоги.",
    },
    {
        "topic": "103.3",
        "question_type": "text",
        "text": "Какая команда перемещает или переименовывает файлы?",
        "options": None,
        "correct_answer": "mv",
        "explanation": "mv (move) перемещает файлы или переименовывает их.",
    },
    {
        "topic": "103.3",
        "question_type": "single",
        "text": "Какой флаг cp сохраняет атрибуты файла (время, права)?",
        "options": [
            {"id": "A", "text": "-p"},
            {"id": "B", "text": "-a"},
            {"id": "C", "text": "-r"},
            {"id": "D", "text": "-s"},
        ],
        "correct_answer": "A",
        "explanation": "-p (preserve) сохраняет mode, ownership, timestamps. -a — архивный режим (включает -p и -r).",
    },
    {
        "topic": "103.3",
        "question_type": "text",
        "text": "Какая команда создаёт каталог?",
        "options": None,
        "correct_answer": "mkdir",
        "explanation": "mkdir (make directory) создаёт каталог.",
    },
    {
        "topic": "103.3",
        "question_type": "single",
        "text": "Какой флаг mkdir создаёт родительские каталоги, если их нет?",
        "options": [
            {"id": "A", "text": "-p"},
            {"id": "B", "text": "-r"},
            {"id": "C", "text": "-m"},
            {"id": "D", "text": "-v"},
        ],
        "correct_answer": "A",
        "explanation": "-p (parents) создаёт промежуточные каталоги и не выдаёт ошибку, если каталог уже существует.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.4 Use streams, pipes and redirects (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.4",
        "question_type": "single",
        "text": "Какой оператор перенаправляет stderr в файл?",
        "options": [
            {"id": "A", "text": "2>"},
            {"id": "B", "text": "1>"},
            {"id": "C", "text": "&>"},
            {"id": "D", "text": ">>"},
        ],
        "correct_answer": "A",
        "explanation": "2> — stderr в файл. 1> — stdout. &> — оба. >> — дописывание в stdout.",
    },
    {
        "topic": "103.4",
        "question_type": "text",
        "text": "Какой символ передаёт stdout одной команды на stdin другой?",
        "options": None,
        "correct_answer": "|",
        "explanation": "Символ | (pipe) соединяет stdout одной команды с stdin другой.",
    },
    {
        "topic": "103.4",
        "question_type": "single",
        "text": "Какой оператор перенаправляет и stdout, и stderr в файл?",
        "options": [
            {"id": "A", "text": "&> или >file 2>&1"},
            {"id": "B", "text": ">>"},
            {"id": "C", "text": "|&"},
            {"id": "D", "text": "2>&1"},
        ],
        "correct_answer": "A",
        "explanation": "&> — bash-расширение. >file 2>&1 — POSIX-совместимый способ.",
    },
    {
        "topic": "103.4",
        "question_type": "text",
        "text": "Какой оператор дописывает stdout в файл (не перезаписывает)?",
        "options": None,
        "correct_answer": ">>",
        "explanation": ">> дописывает в конец файла. > перезаписывает.",
    },
    {
        "topic": "103.4",
        "question_type": "single",
        "text": "Какой файловый дескриптор соответствует stdin?",
        "options": [
            {"id": "A", "text": "0"},
            {"id": "B", "text": "1"},
            {"id": "C", "text": "2"},
            {"id": "D", "text": "3"},
        ],
        "correct_answer": "A",
        "explanation": "0 — stdin, 1 — stdout, 2 — stderr.",
    },
    {
        "topic": "103.4",
        "question_type": "text",
        "text": "Какой оператор передаёт и stdout, и stderr через pipe?",
        "options": None,
        "correct_answer": "|&",
        "explanation": "|& — bash-расширение, передаёт оба потока. В POSIX: 2>&1 |.",
    },
    {
        "topic": "103.4",
        "question_type": "single",
        "text": "Какая команда читает stdin и записывает в файл (используется в скриптах)?",
        "options": [
            {"id": "A", "text": "tee"},
            {"id": "B", "text": "cat"},
            {"id": "C", "text": "read"},
            {"id": "D", "text": "echo"},
        ],
        "correct_answer": "A",
        "explanation": "tee читает stdin и записывает в файл и stdout одновременно.",
    },
    {
        "topic": "103.4",
        "question_type": "text",
        "text": "Какой символ используется для here-document в bash?",
        "options": None,
        "correct_answer": "<<",
        "explanation": "<<EOF ... EOF — here-document, передаёт многострочный текст на stdin.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.5 Create, monitor and kill processes (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.5",
        "question_type": "single",
        "text": "Какая команда показывает интерактивный список процессов?",
        "options": [
            {"id": "A", "text": "top или htop"},
            {"id": "B", "text": "ps"},
            {"id": "C", "text": "pgrep"},
            {"id": "D", "text": "proc"},
        ],
        "correct_answer": "A",
        "explanation": "top и htop — интерактивные мониторы процессов. ps — снимок.",
    },
    {
        "topic": "103.5",
        "question_type": "text",
        "text": "Какой сигнал по умолчанию отправляет команда kill?",
        "options": None,
        "correct_answer": "SIGTERM",
        "explanation": "kill по умолчанию отправляет SIGTERM (15). Для SIGKILL нужен флаг -9.",
    },
    {
        "topic": "103.5",
        "question_type": "single",
        "text": "Как запустить процесс в фоновом режиме?",
        "options": [
            {"id": "A", "text": "Добавить & в конце команды"},
            {"id": "B", "text": "Добавить # в конце команды"},
            {"id": "C", "text": "Использовать флаг -b"},
            {"id": "D", "text": "Нажать Ctrl+Z"},
        ],
        "correct_answer": "A",
        "explanation": "Символ & в конце запускает процесс в фоне. Ctrl+Z — приостанавливает.",
    },
    {
        "topic": "103.5",
        "question_type": "text",
        "text": "Какая команда показывает список запущенных процессов?",
        "options": None,
        "correct_answer": "ps",
        "explanation": "ps (process status) показывает снимок процессов.",
    },
    {
        "topic": "103.5",
        "question_type": "single",
        "text": "Какой флаг ps показывает все процессы в системе?",
        "options": [
            {"id": "A", "text": "-e или -A"},
            {"id": "B", "text": "-a"},
            {"id": "C", "text": "-p"},
            {"id": "D", "text": "-l"},
        ],
        "correct_answer": "A",
        "explanation": "ps -e или ps -A показывает все процессы.",
    },
    {
        "topic": "103.5",
        "question_type": "text",
        "text": "Какая команда находит PID процесса по имени?",
        "options": None,
        "correct_answer": "pgrep",
        "explanation": "pgrep ищет процессы по имени и возвращает их PID.",
    },
    {
        "topic": "103.5",
        "question_type": "single",
        "text": "Какой сигнал принудительно завершает процесс (не может быть перехвачен)?",
        "options": [
            {"id": "A", "text": "SIGKILL (9)"},
            {"id": "B", "text": "SIGTERM (15)"},
            {"id": "C", "text": "SIGHUP (1)"},
            {"id": "D", "text": "SIGINT (2)"},
        ],
        "correct_answer": "A",
        "explanation": "SIGKILL (9) — принудительное завершение. SIGTERM (15) — корректное завершение.",
    },
    {
        "topic": "103.5",
        "question_type": "text",
        "text": "Какая команда запускает процесс, который продолжит работу после выхода из shell?",
        "options": None,
        "correct_answer": "nohup",
        "explanation": "nohup игнорирует SIGHUP, процесс не завершится при выходе из shell.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.6 Modify process execution priority (weight: 2)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.6",
        "question_type": "single",
        "text": "Какая команда запускает процесс с пониженным приоритетом?",
        "options": [
            {"id": "A", "text": "nice"},
            {"id": "B", "text": "priority"},
            {"id": "C", "text": "renice"},
            {"id": "D", "text": "low"},
        ],
        "correct_answer": "A",
        "explanation": "nice запускает процесс с изменённым приоритетом. renice меняет приоритет уже запущенного.",
    },
    {
        "topic": "103.6",
        "question_type": "text",
        "text": "Какой диапазон значений nice в Linux?",
        "options": None,
        "correct_answer": "от -20 до 19",
        "explanation": "Nice-значение от -20 (наивысший приоритет) до 19 (низший). По умолчанию 0.",
    },
    {
        "topic": "103.6",
        "question_type": "single",
        "text": "Какая команда изменяет приоритет уже запущенного процесса?",
        "options": [
            {"id": "A", "text": "renice"},
            {"id": "B", "text": "nice"},
            {"id": "C", "text": "priority"},
            {"id": "D", "text": "chpri"},
        ],
        "correct_answer": "A",
        "explanation": "renice изменяет nice-значение запущенного процесса.",
    },
    {
        "topic": "103.6",
        "question_type": "text",
        "text": "Какой флаг nice устанавливает приоритет 10?",
        "options": None,
        "correct_answer": "-n 10",
        "explanation": "nice -n 10 command — запускает команду с nice-значением 10.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.7 Search text files using regular expressions (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.7",
        "question_type": "single",
        "text": "Какой символ в регулярных выражениях обозначает начало строки?",
        "options": [
            {"id": "A", "text": "^"},
            {"id": "B", "text": "$"},
            {"id": "C", "text": "*"},
            {"id": "D", "text": "."},
        ],
        "correct_answer": "A",
        "explanation": "^ — начало строки. $ — конец строки. . — любой символ. * — 0 или более повторений.",
    },
    {
        "topic": "103.7",
        "question_type": "text",
        "text": "Какая команда ищет строки в файлах по регулярному выражению?",
        "options": None,
        "correct_answer": "grep",
        "explanation": "grep ищет строки, соответствующие регулярному выражению.",
    },
    {
        "topic": "103.7",
        "question_type": "single",
        "text": "Какой флаг grep включает расширенные регулярные выражения?",
        "options": [
            {"id": "A", "text": "-E"},
            {"id": "B", "text": "-e"},
            {"id": "C", "text": "-r"},
            {"id": "D", "text": "-x"},
        ],
        "correct_answer": "A",
        "explanation": "-E (extended) включает ERE. Альтернатива — egrep.",
    },
    {
        "topic": "103.7",
        "question_type": "text",
        "text": "Какой символ в регулярных выражениях обозначает любой одиночный символ?",
        "options": None,
        "correct_answer": ".",
        "explanation": ". (точка) соответствует любому символу, кроме новой строки.",
    },
    {
        "topic": "103.7",
        "question_type": "single",
        "text": "Какой символ обозначает '0 или более повторений' в регулярных выражениях?",
        "options": [
            {"id": "A", "text": "*"},
            {"id": "B", "text": "+"},
            {"id": "C", "text": "?"},
            {"id": "D", "text": "#"},
        ],
        "correct_answer": "A",
        "explanation": "* — 0 или более. + — 1 или более. ? — 0 или 1.",
    },
    {
        "topic": "103.7",
        "question_type": "text",
        "text": "Какая команда ищет строки, НЕ соответствующие шаблону?",
        "options": None,
        "correct_answer": "grep -v",
        "explanation": "-v (invert) показывает строки, не соответствующие шаблону.",
    },
    {
        "topic": "103.7",
        "question_type": "multiple",
        "text": "Какие ДВЕ команды поддерживают регулярные выражения? (Выберите 2)",
        "options": [
            {"id": "A", "text": "grep"},
            {"id": "B", "text": "sed"},
            {"id": "C", "text": "awk"},
            {"id": "D", "text": "cut"},
            {"id": "E", "text": "sort"},
        ],
        "correct_answer": "A,B",
        "explanation": "grep и sed работают с регулярными выражениями. awk тоже, но grep/sed — канонический ответ.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 103.8 Basic file editing (weight: 2)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "103.8",
        "question_type": "single",
        "text": "Какой редактор является стандартным для POSIX и присутствует практически в любом Unix?",
        "options": [
            {"id": "A", "text": "vi"},
            {"id": "B", "text": "emacs"},
            {"id": "C", "text": "nano"},
            {"id": "D", "text": "gedit"},
        ],
        "correct_answer": "A",
        "explanation": "vi — стандарт POSIX, присутствует везде. nano и emacs — опциональны.",
    },
    {
        "topic": "103.8",
        "question_type": "text",
        "text": "Какая команда в vi сохраняет файл и выходит?",
        "options": None,
        "correct_answer": ":wq",
        "explanation": ":wq (write and quit) сохраняет и выходит. :q! — выход без сохранения.",
    },
    {
        "topic": "103.8",
        "question_type": "single",
        "text": "Какая команда в vi переходит в режим вставки?",
        "options": [
            {"id": "A", "text": "i"},
            {"id": "B", "text": "a"},
            {"id": "C", "text": "o"},
            {"id": "D", "text": "Все вышеперечисленные"},
        ],
        "correct_answer": "D",
        "explanation": "i — перед курсором, a — после курсора, o — новая строка ниже. Все входят в режим вставки.",
    },
    {
        "topic": "103.8",
        "question_type": "text",
        "text": "Какая команда в vi отменяет последнее действие?",
        "options": None,
        "correct_answer": "u",
        "explanation": "u (undo) отменяет последнее изменение в нормальном режиме.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.1 Create partitions and filesystems (weight: 4)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.1",
        "question_type": "multiple",
        "text": "Какие ДВЕ команды создают файловую систему? (Выберите 2)",
        "options": [
            {"id": "A", "text": "mkfs.ext4"},
            {"id": "B", "text": "fdisk"},
            {"id": "C", "text": "mkfs"},
            {"id": "D", "text": "mount"},
            {"id": "E", "text": "parted"},
        ],
        "correct_answer": "A,C",
        "explanation": "mkfs и mkfs.ext4 создают ФС. fdisk/parted — разметка, mount — монтирование.",
    },
    {
        "topic": "104.1",
        "question_type": "single",
        "text": "Какая утилита позволяет управлять разделами в интерактивном режиме и поддерживает GPT?",
        "options": [
            {"id": "A", "text": "parted"},
            {"id": "B", "text": "fdisk"},
            {"id": "C", "text": "mkfs"},
            {"id": "D", "text": "fsck"},
        ],
        "correct_answer": "A",
        "explanation": "parted поддерживает и MBR, и GPT. fdisk (старый) — только MBR, fdisk (новый) — и то и другое.",
    },
    {
        "topic": "104.1",
        "question_type": "text",
        "text": "Какая команда создаёт файловую систему ext4 на разделе /dev/sda1?",
        "options": None,
        "correct_answer": "mkfs.ext4 /dev/sda1",
        "explanation": "mkfs.ext4 создаёт ФС ext4. mkfs -t ext4 — альтернатива.",
    },
    {
        "topic": "104.1",
        "question_type": "single",
        "text": "Какая таблица разделов поддерживает диски размером более 2 ТБ?",
        "options": [
            {"id": "A", "text": "GPT"},
            {"id": "B", "text": "MBR"},
            {"id": "C", "text": "BSD"},
            {"id": "D", "text": "DOS"},
        ],
        "correct_answer": "A",
        "explanation": "GPT (GUID Partition Table) поддерживает диски >2 ТБ. MBR ограничен 2 ТБ.",
    },
    {
        "topic": "104.1",
        "question_type": "text",
        "text": "Какая команда показывает таблицу разделов диска?",
        "options": None,
        "correct_answer": "fdisk -l",
        "explanation": "fdisk -l показывает все разделы на всех дисках.",
    },
    {
        "topic": "104.1",
        "question_type": "single",
        "text": "Какой тип раздела в MBR является основным загрузочным?",
        "options": [
            {"id": "A", "text": "Primary"},
            {"id": "B", "text": "Extended"},
            {"id": "C", "text": "Logical"},
            {"id": "D", "text": "Swap"},
        ],
        "correct_answer": "A",
        "explanation": "Primary — основной раздел. Extended содержит logical. Максимум 4 primary.",
    },
    {
        "topic": "104.1",
        "question_type": "multiple",
        "text": "Какие ДВЕ файловые системы являются журналируемыми? (Выберите 2)",
        "options": [
            {"id": "A", "text": "ext4"},
            {"id": "B", "text": "ext2"},
            {"id": "C", "text": "xfs"},
            {"id": "D", "text": "vfat"},
            {"id": "E", "text": "swap"},
        ],
        "correct_answer": "A,C",
        "explanation": "ext4 и xfs — журналируемые ФС. ext2 — не журналируемая. vfat — для Windows.",
    },
    {
        "topic": "104.1",
        "question_type": "text",
        "text": "Какая команда создаёт swap-раздел?",
        "options": None,
        "correct_answer": "mkswap",
        "explanation": "mkswap инициализирует раздел как swap-пространство.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.2 Maintain the integrity of filesystems (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.2",
        "question_type": "single",
        "text": "Какая команда проверяет целостность файловой системы ext4?",
        "options": [
            {"id": "A", "text": "fsck"},
            {"id": "B", "text": "mkfs"},
            {"id": "C", "text": "mount"},
            {"id": "D", "text": "tune2fs"},
        ],
        "correct_answer": "A",
        "explanation": "fsck (file system check) проверяет и восстанавливает ФС. Должна запускаться на размонтированной ФС.",
    },
    {
        "topic": "104.2",
        "question_type": "text",
        "text": "Какая команда показывает статистику файловой системы ext2/ext3/ext4?",
        "options": None,
        "correct_answer": "dumpe2fs",
        "explanation": "dumpe2fs показывает информацию о ФС: размер, inode, суперблоки.",
    },
    {
        "topic": "104.2",
        "question_type": "single",
        "text": "Какая команда изменяет параметры файловой системы ext2/ext3/ext4?",
        "options": [
            {"id": "A", "text": "tune2fs"},
            {"id": "B", "text": "fsck"},
            {"id": "C", "text": "mkfs"},
            {"id": "D", "text": "debugfs"},
        ],
        "correct_answer": "A",
        "explanation": "tune2fs изменяет параметры ФС: интервал проверок, количество монтирований и т.д.",
    },
    {
        "topic": "104.2",
        "question_type": "text",
        "text": "Какая команда показывает состояние файловой системы (использованное/свободное пространство)?",
        "options": None,
        "correct_answer": "df",
        "explanation": "df (disk free) показывает использование дискового пространства.",
    },
    {
        "topic": "104.2",
        "question_type": "single",
        "text": "Какой флаг fsck принудительно проверяет файловую систему даже если она чистая?",
        "options": [
            {"id": "A", "text": "-f"},
            {"id": "B", "text": "-y"},
            {"id": "C", "text": "-n"},
            {"id": "D", "text": "-r"},
        ],
        "correct_answer": "A",
        "explanation": "-f (force) принудительная проверка. -y — автоматически отвечать 'да' на все вопросы.",
    },
    {
        "topic": "104.2",
        "question_type": "text",
        "text": "Какая команда показывает использование дискового пространства каталогами?",
        "options": None,
        "correct_answer": "du",
        "explanation": "du (disk usage) показывает размер каталогов и файлов.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.3 Control mounting and unmounting of filesystems (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.3",
        "question_type": "text",
        "text": "Укажите полный путь к файлу, в котором настраиваются ФС для автомонтирования при загрузке.",
        "options": None,
        "correct_answer": "/etc/fstab",
        "explanation": "/etc/fstab содержит таблицу файловых систем и точек монтирования.",
    },
    {
        "topic": "104.3",
        "question_type": "single",
        "text": "Какая команда монтирует все ФС из /etc/fstab?",
        "options": [
            {"id": "A", "text": "mount -a"},
            {"id": "B", "text": "mount --all"},
            {"id": "C", "text": "fstab-mount"},
            {"id": "D", "text": "mount -f"},
        ],
        "correct_answer": "A",
        "explanation": "mount -a монтирует все ФС, указанные в fstab (кроме тех, что с опцией noauto).",
    },
    {
        "topic": "104.3",
        "question_type": "text",
        "text": "Какая команда размонтирует файловую систему?",
        "options": None,
        "correct_answer": "umount",
        "explanation": "umount размонтирует ФС. Должна вызываться из каталога, не находящегося внутри ФС.",
    },
    {
        "topic": "104.3",
        "question_type": "single",
        "text": "Какая опция mount делает файловую систему доступной только для чтения?",
        "options": [
            {"id": "A", "text": "ro"},
            {"id": "B", "text": "readonly"},
            {"id": "C", "text": "r"},
            {"id": "D", "text": "read"},
        ],
        "correct_answer": "A",
        "explanation": "ro (read-only) монтирует ФС только для чтения. rw — для чтения и записи.",
    },
    {
        "topic": "104.3",
        "question_type": "text",
        "text": "Какая команда показывает все смонтированные файловые системы?",
        "options": None,
        "correct_answer": "mount",
        "explanation": "mount без параметров показывает все текущие монтирования.",
    },
    {
        "topic": "104.3",
        "question_type": "single",
        "text": "Какая опция в /etc/fstab предотвращает автоматическое монтирование при загрузке?",
        "options": [
            {"id": "A", "text": "noauto"},
            {"id": "B", "text": "manual"},
            {"id": "C", "text": "nomount"},
            {"id": "D", "text": "skip"},
        ],
        "correct_answer": "A",
        "explanation": "noauto — ФС не монтируется при boot. user — позволяет монтировать обычному пользователю.",
    },
    {
        "topic": "104.3",
        "question_type": "multiple",
        "text": "Какие ДВЕ опции mount позволяют обычному пользователю монтировать ФС? (Выберите 2)",
        "options": [
            {"id": "A", "text": "user"},
            {"id": "B", "text": "users"},
            {"id": "C", "text": "owner"},
            {"id": "D", "text": "sudo"},
            {"id": "E", "text": "allow"},
        ],
        "correct_answer": "A,B",
        "explanation": "user — любой пользователь может монтировать. users — любой может монтировать и размонтировать.",
    },
    {
        "topic": "104.3",
        "question_type": "text",
        "text": "Какой идентификатор используется в /etc/fstab для указания устройства по UUID?",
        "options": None,
        "correct_answer": "UUID=",
        "explanation": "UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx — предпочтительный способ указания устройств.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.4 Manage disk quotas (weight: 2)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.4",
        "question_type": "single",
        "text": "Какая команда устанавливает дисковые квоты для пользователя?",
        "options": [
            {"id": "A", "text": "edquota"},
            {"id": "B", "text": "quota"},
            {"id": "C", "text": "setquota"},
            {"id": "D", "text": "quotactl"},
        ],
        "correct_answer": "A",
        "explanation": "edquota (edit quota) открывает редактор для установки квот. repquota показывает отчёт.",
    },
    {
        "topic": "104.4",
        "question_type": "text",
        "text": "Какая команда показывает использование дисковых квот пользователем?",
        "options": None,
        "correct_answer": "quota",
        "explanation": "quota показывает текущее использование и лимиты для пользователя.",
    },
    {
        "topic": "104.4",
        "question_type": "single",
        "text": "Какая опция mount включает поддержку квот для пользователей?",
        "options": [
            {"id": "A", "text": "usrquota"},
            {"id": "B", "text": "userquota"},
            {"id": "C", "text": "quota"},
            {"id": "D", "text": "uquota"},
        ],
        "correct_answer": "A",
        "explanation": "usrquota — квоты пользователей. grpquota — квоты групп.",
    },
    {
        "topic": "104.4",
        "question_type": "text",
        "text": "Какая команда создаёт файлы квот (aquota.user, aquota.group)?",
        "options": None,
        "correct_answer": "quotacheck",
        "explanation": "quotacheck сканирует ФС и создаёт файлы квот. -c — создать, -u — пользователи, -g — группы.",
    },
    {
        "topic": "104.4",
        "question_type": "single",
        "text": "Какая команда включает дисковые квоты?",
        "options": [
            {"id": "A", "text": "quotaon"},
            {"id": "B", "text": "quotaenable"},
            {"id": "C", "text": "quotactl"},
            {"id": "D", "text": "quota -on"},
        ],
        "correct_answer": "A",
        "explanation": "quotaon включает квоты. quotaoff — выключает.",
    },
    {
        "topic": "104.4",
        "question_type": "text",
        "text": "Какая команда показывает отчёт по квотам для всех пользователей?",
        "options": None,
        "correct_answer": "repquota",
        "explanation": "repquota (report quota) показывает сводку по квотам для всех пользователей или групп.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.5 Manage file permissions and ownership (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.5",
        "question_type": "text",
        "text": "Какая команда изменяет права доступа к файлу?",
        "options": None,
        "correct_answer": "chmod",
        "explanation": "chmod (change mode) изменяет права доступа.",
    },
    {
        "topic": "104.5",
        "question_type": "single",
        "text": "Какой символ в правах доступа обозначает setuid-бит?",
        "options": [
            {"id": "A", "text": "s"},
            {"id": "B", "text": "t"},
            {"id": "C", "text": "x"},
            {"id": "D", "text": "S"},
        ],
        "correct_answer": "A",
        "explanation": "Маленькая 's' — setuid с правом выполнения. 'S' — setuid без выполнения.",
    },
    {
        "topic": "104.5",
        "question_type": "text",
        "text": "Какая команда изменяет владельца файла?",
        "options": None,
        "correct_answer": "chown",
        "explanation": "chown (change owner) изменяет владельца и/или группу файла.",
    },
    {
        "topic": "104.5",
        "question_type": "single",
        "text": "Какие права доступа устанавливает команда chmod 755?",
        "options": [
            {"id": "A", "text": "rwxr-xr-x"},
            {"id": "B", "text": "rwxrwxr-x"},
            {"id": "C", "text": "rw-r--r--"},
            {"id": "D", "text": "rwx------"},
        ],
        "correct_answer": "A",
        "explanation": "7=rwx, 5=r-x, 5=r-x. Владелец: rwx, группа: r-x, остальные: r-x.",
    },
    {
        "topic": "104.5",
        "question_type": "text",
        "text": "Какая команда изменяет группу файла?",
        "options": None,
        "correct_answer": "chgrp",
        "explanation": "chgrp (change group) изменяет группу файла. chown тоже может: chown :group file.",
    },
    {
        "topic": "104.5",
        "question_type": "single",
        "text": "Какой символ в правах доступа обозначает sticky bit?",
        "options": [
            {"id": "A", "text": "t"},
            {"id": "B", "text": "s"},
            {"id": "C", "text": "T"},
            {"id": "D", "text": "x"},
        ],
        "correct_answer": "A",
        "explanation": "Маленькая 't' — sticky bit с правом выполнения. 'T' — sticky без выполнения.",
    },
    {
        "topic": "104.5",
        "question_type": "multiple",
        "text": "Какие ДВА специальных бита влияют на выполнение файлов? (Выберите 2)",
        "options": [
            {"id": "A", "text": "setuid (s)"},
            {"id": "B", "text": "setgid (s)"},
            {"id": "C", "text": "sticky bit (t)"},
            {"id": "D", "text": "hidden bit (h)"},
            {"id": "E", "text": "readonly bit (r)"},
        ],
        "correct_answer": "A,B",
        "explanation": "setuid — выполнение от имени владельца. setgid — выполнение от имени группы. Sticky bit — для каталогов.",
    },
    {
        "topic": "104.5",
        "question_type": "text",
        "text": "Какой флаг chmod применяет изменения рекурсивно?",
        "options": None,
        "correct_answer": "-R",
        "explanation": "chmod -R рекурсивно изменяет права для всех файлов в каталоге.",
    },
    {
        "topic": "104.5",
        "question_type": "single",
        "text": "Какие числовые права соответствуют rw-r--r--?",
        "options": [
            {"id": "A", "text": "644"},
            {"id": "B", "text": "755"},
            {"id": "C", "text": "600"},
            {"id": "D", "text": "744"},
        ],
        "correct_answer": "A",
        "explanation": "rw-=6, r--=4, r--=4. Итого: 644.",
    },
    {
        "topic": "104.5",
        "question_type": "text",
        "text": "Какой символ используется в chmod для добавления прав?",
        "options": None,
        "correct_answer": "+",
        "explanation": "+ добавляет права. - убирает. = устанавливает точно.",
    },
    {
        "topic": "104.5",
        "question_type": "single",
        "text": "Что означает umask 022?",
        "options": [
            {"id": "A", "text": "Новые файлы: 644, каталоги: 755"},
            {"id": "B", "text": "Новые файлы: 600, каталоги: 700"},
            {"id": "C", "text": "Новые файлы: 755, каталоги: 644"},
            {"id": "D", "text": "Новые файлы: 777, каталоги: 777"},
        ],
        "correct_answer": "A",
        "explanation": "umask 022 вычитается из 666 (файлы) и 777 (каталоги). 666-022=644, 777-022=755.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.6 Create and change hard and symbolic links (weight: 2)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.6",
        "question_type": "single",
        "text": "Какой флаг команды ln создаёт символическую (мягкую) ссылку?",
        "options": [
            {"id": "A", "text": "-s"},
            {"id": "B", "text": "-l"},
            {"id": "C", "text": "-L"},
            {"id": "D", "text": "-S"},
        ],
        "correct_answer": "A",
        "explanation": "ln -s создаёт символическую ссылку. Без флагов — жёсткую.",
    },
    {
        "topic": "104.6",
        "question_type": "text",
        "text": "Какая команда создаёт жёсткую ссылку?",
        "options": None,
        "correct_answer": "ln",
        "explanation": "ln source target создаёт жёсткую ссылку. ln -s — символическую.",
    },
    {
        "topic": "104.6",
        "question_type": "single",
        "text": "Какое ограничение жёстких ссылок в Linux?",
        "options": [
            {"id": "A", "text": "Не могут ссылаться на каталоги"},
            {"id": "B", "text": "Не могут ссылаться на файлы"},
            {"id": "C", "text": "Могут быть только на одном разделе"},
            {"id": "D", "text": "Только A и C"},
        ],
        "correct_answer": "D",
        "explanation": "Жёсткие ссылки не работают с каталогами и ограничены одним разделом (одной ФС).",
    },
    {
        "topic": "104.6",
        "question_type": "text",
        "text": "Какая команда показывает, сколько жёстких ссылок имеет файл?",
        "options": None,
        "correct_answer": "ls -l",
        "explanation": "ls -l показывает количество жёстких ссылок во втором поле (после прав).",
    },
    {
        "topic": "104.6",
        "question_type": "single",
        "text": "Что происходит с файлом при удалении жёсткой ссылки?",
        "options": [
            {"id": "A", "text": "Файл удаляется только если это последняя ссылка"},
            {"id": "B", "text": "Файл удаляется немедленно"},
            {"id": "C", "text": "Файл остаётся, но становится недоступным"},
            {"id": "D", "text": "Ошибка, нельзя удалить жёсткую ссылку"},
        ],
        "correct_answer": "A",
        "explanation": "Данные удаляются только когда удаляется последняя жёсткая ссылка (счётчик ссылок = 0).",
    },
    {
        "topic": "104.6",
        "question_type": "text",
        "text": "Какая команда показывает, на какой файл указывает символическая ссылка?",
        "options": None,
        "correct_answer": "ls -l",
        "explanation": "ls -l показывает цель символической ссылки после '->'.",
    },
    {
        "topic": "104.6",
        "question_type": "single",
        "text": "Что происходит с символической ссылкой при удалении целевого файла?",
        "options": [
            {"id": "A", "text": "Ссылка остаётся, но становится 'битой' (dangling)"},
            {"id": "B", "text": "Ссылка автоматически удаляется"},
            {"id": "C", "text": "Ссылка указывает на себя"},
            {"id": "D", "text": "Ошибка при следующем обращении"},
        ],
        "correct_answer": "A",
        "explanation": "Символическая ссылка остаётся, но указывает на несуществующий файл (broken link).",
    },
    {
        "topic": "104.6",
        "question_type": "multiple",
        "text": "Какие ДВА утверждения о символических ссылках верны? (Выберите 2)",
        "options": [
            {"id": "A", "text": "Могут ссылаться на каталоги"},
            {"id": "B", "text": "Могут указывать на файлы на других разделах"},
            {"id": "C", "text": "Имеют тот же inode, что и целевой файл"},
            {"id": "D", "text": "Не могут быть удалены"},
            {"id": "E", "text": "Требуют прав на целевой файл"},
        ],
        "correct_answer": "A,B",
        "explanation": "Символические ссылки могут указывать на каталоги и работать между разделами. Имеют свой inode.",
    },

    # ═══════════════════════════════════════════════════════════════
    # 104.7 Find system files and place files in correct location (weight: 3)
    # ═══════════════════════════════════════════════════════════════
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Какая команда ищет файлы в файловой системе по имени?",
        "options": None,
        "correct_answer": "find",
        "explanation": "find рекурсивно ищет файлы по различным критериям.",
    },
    {
        "topic": "104.7",
        "question_type": "single",
        "text": "Какая команда ищет исполняемые файлы в каталогах из PATH?",
        "options": [
            {"id": "A", "text": "which"},
            {"id": "B", "text": "find"},
            {"id": "C", "text": "locate"},
            {"id": "D", "text": "whereis"},
        ],
        "correct_answer": "A",
        "explanation": "which ищет команду в PATH. whereis ищет бинарник, исходник и man. locate — по базе.",
    },
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Какая команда ищет файлы по предварительно созданной базе данных?",
        "options": None,
        "correct_answer": "locate",
        "explanation": "locate ищет по базе, обновляемой командой updatedb. Быстрее find, но может быть неактуальной.",
    },
    {
        "topic": "104.7",
        "question_type": "single",
        "text": "Какой флаг find ищет файлы по имени?",
        "options": [
            {"id": "A", "text": "-name"},
            {"id": "B", "text": "-iname"},
            {"id": "C", "text": "-type"},
            {"id": "D", "text": "A и B"},
        ],
        "correct_answer": "D",
        "explanation": "-name — по имени (чувствительно к регистру). -iname — без учёта регистра.",
    },
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Какой флаг find ищет только каталоги?",
        "options": None,
        "correct_answer": "-type d",
        "explanation": "-type d — каталоги. -type f — файлы. -type l — ссылки.",
    },
    {
        "topic": "104.7",
        "question_type": "single",
        "text": "Где обычно хранятся конфигурационные файлы системы?",
        "options": [
            {"id": "A", "text": "/etc"},
            {"id": "B", "text": "/var"},
            {"id": "C", "text": "/usr"},
            {"id": "D", "text": "/opt"},
        ],
        "correct_answer": "A",
        "explanation": "/etc — конфигурационные файлы. /var — переменные данные. /usr — программы. /opt — дополнительные пакеты.",
    },
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Где обычно хранятся логи системы?",
        "options": None,
        "correct_answer": "/var/log",
        "explanation": "/var/log содержит логи: syslog, auth.log, messages и т.д.",
    },
    {
        "topic": "104.7",
        "question_type": "single",
        "text": "Где находятся исполняемые файлы, доступные всем пользователям?",
        "options": [
            {"id": "A", "text": "/usr/bin"},
            {"id": "B", "text": "/bin"},
            {"id": "C", "text": "A и B"},
            {"id": "D", "text": "/usr/local/bin"},
        ],
        "correct_answer": "C",
        "explanation": "/bin и /usr/bin содержат системные команды. /usr/local/bin — для локально установленных.",
    },
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Какая команда обновляет базу данных для locate?",
        "options": None,
        "correct_answer": "updatedb",
        "explanation": "updatedb сканирует ФС и обновляет базу для locate. Обычно запускается cron'ом.",
    },
    {
        "topic": "104.7",
        "question_type": "multiple",
        "text": "Какие ДВА утверждения о FHS (Filesystem Hierarchy Standard) верны? (Выберите 2)",
        "options": [
            {"id": "A", "text": "/home содержит домашние каталоги пользователей"},
            {"id": "B", "text": "/tmp содержит временные файлы"},
            {"id": "C", "text": "/root — домашний каталог обычного пользователя"},
            {"id": "D", "text": "/dev содержит конфигурационные файлы"},
            {"id": "E", "text": "/proc содержит виртуальную файловую систему ядра"},
        ],
        "correct_answer": "A,B",
        "explanation": "/home — домашние каталоги. /tmp — временные файлы. /root — домашний каталог root. /dev — устройства. /proc — виртуальная ФС.",
    },
    {
        "topic": "104.7",
        "question_type": "single",
        "text": "Какой флаг find выполняет команду над найденными файлами?",
        "options": [
            {"id": "A", "text": "-exec"},
            {"id": "B", "text": "-run"},
            {"id": "C", "text": "-command"},
            {"id": "D", "text": "-do"},
        ],
        "correct_answer": "A",
        "explanation": "-exec command {} \\; выполняет команду для каждого найденного файла.",
    },
    {
        "topic": "104.7",
        "question_type": "text",
        "text": "Какая команда показывает информацию о файле и его расположение в системе?",
        "options": None,
        "correct_answer": "whereis",
        "explanation": "whereis ищет бинарник, исходный код и man-страницу для команды.",
    },
]

# Добавление вопросов в базу
for q_data in questions_data:
    question = Question(**q_data)
    db.add(question)

db.commit()
print(f"✅ Добавлено {len(questions_data)} вопросов в базу данных")

# Статистика по темам
from collections import Counter
topic_counts = Counter(q["topic"] for q in questions_data)
print("\n📊 Распределение вопросов по темам:")
for topic in sorted(topic_counts.keys()):
    print(f"  {topic}: {topic_counts[topic]} вопросов")

print(f"\n📈 Всего вопросов: {len(questions_data)}")

db.close()
