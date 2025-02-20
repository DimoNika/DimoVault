

files_mime_types = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "word.svg",  # .docx
    "application/msword": "word.svg",  # .doc, .dot (старый формат)
    "application/vnd.ms-word.template.macroEnabled.12": "word.svg",  # .dotm
    "application/vnd.openxmlformats-officedocument.wordprocessingml.template": "word.svg",  # .dotx
    "application/vnd.ms-word.document.macroEnabled.12": "word.svg",  # .docm
    "application/rtf": "word.svg",  # .rtf (Rich Text Format)
    "application/vnd.oasis.opendocument.text": "word.svg",  # .odt (OpenDocument)
    # "text/plain": "word.svg",  # .txt (если используется в Word)
    # "text/html": "word.svg",  # .html, .htm (если экспортировано из Word)
    "application/xml": "word.svg",  # .xml (если это формат Word XML)
    "application/pdf": "word.svg",  # .pdf (если экспортировано из Word)
    "application/zip": "word.svg",  # .zip (если это архив с документами Word)

    "application/x-zip-compressed": "zip.svg",
    "application/zip": "zip.svg",  # .zip
    "application/x-rar-compressed": "zip.svg",  # .rar
    "application/x-7z-compressed": "zip.svg",  # .7z
    "application/gzip": "zip.svg",  # .gz
    "application/x-tar": "zip.svg",  # .tar
    "application/x-bzip": "zip.svg",  # .bz
    "application/x-bzip2": "zip.svg",  # .bz2
    "application/x-xz": "zip.svg",  # .xz
    "application/vnd.android.package-archive": "zip.svg",  # .apk (Android Package)
    "application/x-iso9660-image": "zip.svg",  # .iso (Disk Image)
    "application/vnd.rar": "zip.svg",  # .rar (альтернативный MIME-тип)
    "application/zstd": "zip.svg",  # .zst (Zstandard)

    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "table.svg",  # .xlsx (новый формат Excel)
    "application/vnd.ms-excel": "table.svg",  # .xls (старый формат Excel)
    "application/vnd.ms-excel.sheet.macroEnabled.12": "table.svg",  # .xlsm (Excel с макросами)
    "application/vnd.openxmlformats-officedocument.spreadsheetml.template": "table.svg",  # .xltx (шаблон Excel)
    "application/vnd.ms-excel.template.macroEnabled.12": "table.svg",  # .xltm (шаблон Excel с макросами)
    "application/vnd.ms-excel.addin.macroEnabled.12": "table.svg",  # .xlam (надстройка Excel)
    "application/vnd.oasis.opendocument.spreadsheet": "table.svg",  # .ods (OpenDocument Spreadsheet)
    "text/csv": "table.svg",  # .csv (Comma-Separated Values)
    "application/csv": "table.svg",  # Альтернативный MIME-тип для .csv
    "text/tab-separated-values": "table.svg",  # .tsv (Tab-Separated Values)

    "image/jpeg": "image.svg",  # .jpg, .jpeg
    "image/png": "image.svg",  # .png
    "image/gif": "image.svg",  # .gif
    "image/webp": "image.svg",  # .webp
    "image/svg+xml": "image.svg",  # .svg
    "image/bmp": "image.svg",  # .bmp
    "image/tiff": "image.svg",  # .tif, .tiff
    "image/x-icon": "image.svg",  # .ico
    "image/vnd.microsoft.icon": "image.svg",  # .ico (альтернативный MIME-тип)
    "image/heif": "image.svg",  # .heif, .heic (формат Apple)
    "image/heic": "image.svg",  # .heic (второй вариант)
    "image/apng": "image.svg",  # .apng (анимированный PNG)
    "image/x-citrix-jpeg": "image.svg",  # Специфичный формат JPEG
    "image/x-citrix-png": "image.svg",  # Специфичный формат PNG

    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "powerpoint.svg",  # .pptx (новый формат PowerPoint)
    "application/vnd.ms-powerpoint": "powerpoint.svg",  # .ppt (старый формат PowerPoint)
    "application/vnd.ms-powerpoint.presentation.macroEnabled.12": "powerpoint.svg",  # .pptm (PowerPoint с макросами)
    "application/vnd.openxmlformats-officedocument.presentationml.template": "powerpoint.svg",  # .potx (шаблон PowerPoint)
    "application/vnd.ms-powerpoint.template.macroEnabled.12": "powerpoint.svg",  # .potm (шаблон PowerPoint с макросами)
    "application/vnd.ms-powerpoint.slideshow.macroEnabled.12": "powerpoint.svg",  # .ppsx (слайд-шоу PowerPoint)
    "application/vnd.openxmlformats-officedocument.presentationml.slideshow": "powerpoint.svg",  # .ppsx (новый формат слайд-шоу PowerPoint)
    "application/vnd.ms-powerpoint.addin.macroEnabled.12": "powerpoint.svg",  # .ppam (надстройка PowerPoint)
    "application/vnd.oasis.opendocument.presentation": "powerpoint.svg",  # .odp (OpenDocument Presentation)

    "application/json": "json.svg",  # .json (JSON-файлы)
    "application/ld+json": "json.svg",  # .json-ld (JSON для Linked Data)
    "application/vnd.api+json": "json.svg",  # .json-api (API JSON формат)

    "application/x-msdos-program": "exe.svg",  # .exe (Windows Executable)
    "application/x-executable": "exe.svg",  # .exe (альтернативный MIME-тип для исполнимых файлов)
    "application/vnd.microsoft.portable-executable": "exe.svg",  # .exe (Microsoft Portable Executable)

}