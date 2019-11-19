import mmap as mmap
import pdb

class FileSystem:

    def __init__(self):
        self.fileOrigin = "fileOrigin.dat"
        self.num_size_fat_reserved = 4
        self.blocks = 2048
        self.fat_size = self.blocks * 2
        self.block_size = 1024
        self.dir_entry_size = 32

    def build_file(self):

        with open(self.fileOrigin, "wb") as new_file_origin:
            for i in range(self.fat_size):
                if i < 4:
                    new_file_origin.write(b"7ffe")
                elif i == 4:
                    new_file_origin.write(b"7fff")
                else:
                    new_file_origin.write(b"0000")

            for i in range(self.blocks * self.block_size):
                new_file_origin.write(b"0000")
            new_file_origin.close()

    def get_empty_block(self):

        with open(self.fileOrigin, "r+b") as new_file_origin:

            target = mmap.mmap(new_file_origin.fileno(), 0).readline()
            for i in range(0, len(target), 4):
                block = new_file_origin.read(4)
                print(block)
                if block == b"0000":
                    return int((i / 4) - 4)

    def write_in_fat(self, block_number):
        block = (block_number + 5) * 4

        #print("Block position: " + str(block))
        with open(self.fileOrigin, "r+b") as new_file_origin:
            with mmap.mmap(new_file_origin.fileno(), block) as mm:
                print(mm[block - 4:block])
                mm[block - 4:block] = b"7fff"
                mm.close()

    def get_block_with_name(self, block_name):
        with open(self.fileOrigin, "r+b") as new_file_origin:

            target = mmap.mmap(new_file_origin.fileno(), 0).readline()
            for i in range(0, len(target), 4):
                block = new_file_origin.read(4)
                #print(block)
                if block == block_name:
                    print(int((i / 4) - 4))
                    return int((i / 4) - 4)

    # type 1 arquivo, 2 diretorio e 0 vazio
    def write_dir(self, name, type, parent = 1):

        empty_block = self.get_empty_block()

        if empty_block == -1:
            return False

        self.write_in_fat(empty_block)

        entry = str(
            name.ljust(25, '0') + str(type) + str(empty_block).rjust(4, '0') + '0000').encode('utf-8')

        start = 2048 + (parent * 2048)
        end = start + 2048

        with open(self.fileOrigin, 'r+b') as file:
            with mmap.mmap(file.fileno(), end) as map_file_obj:
                for i in range(0, end, 34):
                    file = map_file_obj[start + i: start + i + 34].decode('utf-8')
                    if len(set(list(file))) == 1:
                        map_file_obj[start + i: start + i + 34] = entry
                        print(map_file_obj[start + i: start + i + 34])
                        return True, empty_block



if __name__ == "__main__":
    f = FileSystem()
    #pdb.set_trace()
    f.build_file()
    print("Bock number: " + str(f.get_empty_block()))
    f.write_in_fat(f.get_empty_block())
    f.write_in_fat(f.get_empty_block())
    print("frase escrita em: " + str(f.write_dir("TESTE",1)[1]))
    print("frase escrita em: " + str(f.write_dir("testeTestado", 1)[1]))
    print("Bock number: " + str(f.get_empty_block()))