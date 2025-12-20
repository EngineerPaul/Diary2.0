class ChildrenMixin:
    """Миксин для формирования children из nested_folders и nested_objects"""

    def get_children(self, obj):
        nested_folders = []
        nested_objects = []
        if obj.nested_folders:
            nested_folders = [f'f{f_id}' for f_id in obj.nested_folders.split(',')]
        if obj.nested_objects:
            nested_objects = [f'n{r_id}' for r_id in obj.nested_objects.split(',')]
        return ','.join(nested_folders + nested_objects)
