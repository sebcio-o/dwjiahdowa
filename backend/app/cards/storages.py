from django.core.files.storage import FileSystemStorage


class StorageAllowingDirectURLSave(FileSystemStorage):
    def _save(self, name, content):
        if isinstance(content, str):
            return content
        return super()._save(name, content)
