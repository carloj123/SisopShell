from pathlib import Path
def process_command(input_string):
    if not input_string:
        return ''

def start():
    while True:
        enter_command = input(str((Path(__file__).parent / 'root').absolute()) + '>')
        process_command(enter_command)


if __name__ == "__main__":
    start()