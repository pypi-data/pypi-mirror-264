def get(file_path):
    file = open(file_path).read()
    try:
        file = int(file)
    except ValueError:
        pass
    return file


def get_list(file_path, raw=False):
    file = open(file_path)
    data_list = file.read().split('\n')
    if not raw:
        for x in range(len(data_list)):
            try:
                # noinspection PyTypeChecker
                data_list[x] = int(data_list[x])
            except ValueError:
                pass
        if data_list == ['']:
            data_list = []
    file.close()
    return data_list


def update(file_path, data: [str, int]):  # type: ignore
    open(file_path, 'w').write(str(data))


def update_list(file_path, data: list):
    file = open(file_path, 'w')
    try:
        file.write('\n'.join(x for x in data))
    except TypeError:
        for x in range(len(data)):
            data[x] = str(data[x])
        file.write('\n'.join(x for x in data))
    file.close()


def reset(*file_paths):
    for file_path in file_paths:
        update(file_path, '')
