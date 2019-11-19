from pathlib import Path
from SisopShell.fileSystem import FileSystem
def process_command(input_string,f):

    if not input_string:
        return ''
    commands = {
        "ls" : f.get_block_with_name,
    }
    print(commands.get(input_string)(b"TESTE"))


def start():
    f = FileSystem()
    f.build_file()


    while True:

        enter_command = input(str((Path(__file__).parent / 'root').absolute()) + '>')
        process_command(enter_command, f)





if __name__ == "__main__":
    start()
