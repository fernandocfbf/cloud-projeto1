def initialize_log_file(file):
    with open(r'./' + file, 'a') as f:
        f.truncate(0) #erase file content
        