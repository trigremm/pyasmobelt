import sys

# Импортируем твои существующие main()
from .collect_files_content import main as collect_main
from .add_file_path_comment import main as path_comment_main


COMMANDS = {
    "collect": collect_main,
    "path-comment": path_comment_main,
}


def print_help() -> None:
    cmds = ", ".join(sorted(COMMANDS.keys()))
    print(
        f"""asmobelt – личный CLI-мультитул

Usage:
  asmobelt <command> [options]

Commands:
  collect       Собрать содержимое файлов в один текстовый файл
  path-comment  Добавить в файлы комментарий с относительным путём

Примеры:
  asmobelt collect -p . -o prompt.txt
  asmobelt path-comment -d backend/app --root backend/app

Доступные команды: {cmds}
"""
    )


def main() -> None:
    # Нет аргументов или только -h/--help → показываем помощь
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print_help()
        return

    cmd = sys.argv[1]

    if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}\n")
        print_help()
        sys.exit(1)

    # ВАЖНО: выкидываем команду из argv, чтобы
    # внутренний argparse видел "чистые" аргументы
    sys.argv.pop(1)

    # Дёргаем соответствующий main()
    COMMANDS[cmd]()
