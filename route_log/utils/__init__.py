import os
from django.utils.text import slugify


def get_file_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('files', slugify(name, allow_unicode=True) + ext)
