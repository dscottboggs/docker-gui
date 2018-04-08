runcmd = lambda cmd: run(cmd, check=True, shell=True, stdout=PIPE, stdin=PIPE)

def check_isdir(filepath:str):
    if not isdir(filepath):
        if access(filepath, mode=file_exists):
            raise FileExistsError("Goal directory {filepath} exists as a file.")
        else:
            mkdir(filepath, mode=0o755)
            return True
    return False
