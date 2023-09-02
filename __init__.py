import os
from . import frontmatter
from .frontmatter.default_handlers import JSONHandler

# Files are the basic unit where tasks are stored. Other
# ingredients make use of the methods in this file to 
# load and save them to the filesystem.

def load(path : str) -> frontmatter.Task:
    with open(f'{path}') as file:
            item = frontmatter.load(file)

    return item

def load_dir(dir_path : str, sort_by=None, first=None, last=None) -> list[frontmatter.Task]:
    items = []
    directory = os.listdir(dir_path)

    for item in directory:
        # We skip .swp files, they're yucky
        if item.endswith('.swp'):
            continue

        with open(f'{dir_path}/{item}') as file:
            task = frontmatter.load(file)
            task['filename'] = item
            items.append(task)

    if sort_by is not None:
        try:
            return sorted(items, key=lambda item: item[sort_by])
        except KeyError:
            return items
    else:
        return items

def make_file(file_dict : dict, file_contents: str, file_path : str) -> None:
    new_file = frontmatter.Task(file_contents, **file_dict)

    # Making sure that the file exists before we write to it
    open(f'{file_path}', 'x').close()

    with open(f'{file_path}', 'w') as file:
        file.write(frontmatter.dumps(new_file, JSONHandler()))

def update_file(updates : dict, file_path : str) -> None:
    task = load(file_path)
    for update in updates.keys():
        task[update] = updates[update]

    with open(f'{file_path}', 'w') as file:
        file.write(frontmatter.dumps(task, JSONHandler()))

def delete_file(file_path : str) -> None:
    os.remove(file_path)
