import os

def copy_first_n_lines(n: int, filename: str, new_filename: str):
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(dirname, filename)
    path_to_new_file = os.path.join(dirname, new_filename)
    with open(path_to_file, encoding='utf8') as input_file:
        head = [next(input_file) for _ in range(n)]
    with open(path_to_new_file, 'w', encoding='utf8') as output_file:
        for line in head:
            output_file.write(line)

if __name__=='__main__':
    copy_first_n_lines(10000, 'connection_graph.csv', 'con_graph.csv')