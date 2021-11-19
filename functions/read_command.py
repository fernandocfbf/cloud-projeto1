def read_command(file_name):
    path = r'./commands/'
    with open(path+file_name, 'r') as file:
        return file.read()