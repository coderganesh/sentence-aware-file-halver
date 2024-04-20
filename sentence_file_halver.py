import os, argparse

class FileHalver:
    def __init__(self, file_path, read_chunk_size = 4096):
        self.file_path = file_path
        self.read_chunk_size = read_chunk_size
        self.filename = self.extract_filename_from_path()
        self.file_size = os.path.getsize(file_path)
        self.half_file_size = self.file_size // 2

    def extract_filename_from_path(self):
        if '/' in self.file_path:
            filename_ext = self.file_path.split('/')[-1]
        elif '\\' in self.file_path:
            filename_ext = self.file_path.split('\\')[-1]
        else:
            filename_ext = self.file_path
        if '.' in filename_ext:
            filename = filename_ext.split('.')[0]
        else:
            filename = filename_ext
        return filename
    
    def halve(self):
        with open(self.file_path, 'rb') as f:
            with open(f"{self.filename}_part1.txt", "wb") as f1:
                remaining_size = self.half_file_size
                while remaining_size > 0:
                    chunk_size = min(remaining_size, self.read_chunk_size)
                    data = f.read(chunk_size)
                    f1.write(data)
                    remaining_size -= chunk_size
                cur_pos = f.tell()
                f.seek(cur_pos - 1)
                last_char = f.read(1).decode(errors='replace')
                if last_char != '.':
                    next_char_bytes = f.read(1)
                    next_char = next_char_bytes.decode(errors='replace')
                    while next_char != '.':
                        next_char_bytes = f.read(1)
                        f1.write(next_char_bytes)
                        next_char = next_char_bytes.decode(errors='replace')
                    next_char_bytes = f.read(1)
                    f1.write(next_char_bytes)
            with open(f"{self.filename}_part2.txt", "wb") as f2:
                while True:
                    data = f.read(self.read_chunk_size)
                    if not data:
                        break
                    f2.write(data)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Sentence-aware text file halver")
    arg_parser.add_argument("input_file", type=str, help="Name of the file on which to perform halve operation")
    args = arg_parser.parse_args()
    file_halver = FileHalver(args.input_file)
    file_halver.halve()