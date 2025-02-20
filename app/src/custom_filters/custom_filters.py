

def bytes_to_human_readable(size_in_bytes):
    for unit in ['b', 'Kb', 'Mb', 'Gb']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0


from datetime import datetime

def time_to_human_readable(datetime: datetime):
    return datetime.strftime("%H:%M %d.%m.%Y")

from .icons_mimes import files_mime_types

def content_type_to_icon(content_type):
    # print(content_type)
    if files_mime_types.get(content_type):
        return files_mime_types.get(content_type)
    else:
        return "document.svg"