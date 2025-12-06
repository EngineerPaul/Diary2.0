from django.db.models.query import QuerySet


def set_children(folder: QuerySet):
    """ Creating the children field in every folder and deletion nested
    fields """

    nested_folders, nested_records = [], []
    if folder['nested_folders']:
        nested_folders = folder['nested_folders'].split(',')
    if folder['nested_records']:
        nested_records = folder['nested_records'].split(',')
    nested_objects = [f'f{f_id}' for f_id in nested_folders] + \
                     [f'n{r_id}' for r_id in nested_records]
    folder['children'] = ','.join(nested_objects)
    del folder['nested_folders']
    del folder['nested_records']
    return folder
