import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):
    """
    When saving an image file, allows it to be overwritten,
    instead of creating a new file with a new filename
    """
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name