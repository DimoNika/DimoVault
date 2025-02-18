

def bytes_to_human_readable(size_in_bytes):
    for unit in ['b', 'Kb', 'Mb', 'Gb']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0