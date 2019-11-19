import mmap as mmap


class FileSystem:

    def __init__(self):
        self.fileOrigin = "fileOrigin.dat"
        self.num_size_fat_reserved = 4
        self.fat_size = 2048
        self.bock_size = 1024
        self.p_memory = 2048

    def build_file(self):

        with open(self.fileOrigin, "wb") as new_file_origin:
            for i in range(self.fat_size):
                if i < 5:
                    new_file_origin.write(b"7ffe")
                elif i == 5:
                    new_file_origin.write(b"7fff")
                else:
                    new_file_origin.write(b"0000")

            for i in range(self.p_memory * self.bock_size):
                new_file_origin.write(b"0000")

    def get_empty_block(self):

        with open(self.fileOrigin, "r+b") as new_file_origin:

            target = mmap.mmap(new_file_origin.fileno(), 0).readline()
            for i in range(0, len(target), 4):
                block = new_file_origin.read(4)
                #print(block)
                if block == b"0000":
                    return int((i/4) - 4)

    def write_in_fat(self, block_number):
        block = (block_number + 4) * 4

        print("Block position: " + str(block))
        with open(self.fileOrigin, "r+b") as new_file_origin:
            with mmap.mmap(new_file_origin.fileno(), block) as mm:
                mm[block-4:block] = b"7fff"
                exit()


if __name__ == "__main__":
    f = FileSystem()
    f.build_file()
    print("Bock number: " + str(f.get_empty_block()))
    f.write_in_fat(f.get_empty_block())