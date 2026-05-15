from js import document, window, Uint8Array, File, Blob, URL
from pyodide.ffi.wrappers import add_event_listener
from pyodide.ffi import to_js

from io import BytesIO

import os
import urllib
import base64
import zipfile

app = document.getElementById("app")
preloader = document.getElementById("preloader")

font_upload = document.getElementById("font-upload")
import_format = document.getElementById("import-format")
export_format = document.getElementById("export-format")
preview = document.getElementById("preview")

font_upload_button = document.getElementById("font-upload-button")
font_upload_name   = document.getElementById("font-upload-name")

# https://pyscript.recipes/latest/basic/file-upload/
async def get_file_data(file):
    array_buf = await file.arrayBuffer()
    return array_buf.to_bytes()

def save_file(name: str, data):
    js_data = Uint8Array.new(len(data))
    js_data.assign(data)

    file_obj = File.new([js_data], name)

    blob = URL.createObjectURL(file_obj)
    link = document.createElement("a")
    link.setAttribute("download", name)
    link.setAttribute("href", blob)
    link.click()

    URL.revokeObjectURL(blob)

def render_preview(monobit, font):
    writer = BytesIO()
    monobit.save(font, writer, format="image")

    if preview.src:
        URL.revokeObjectURL(preview.src)

    data = writer.getbuffer()
    js_data = Uint8Array.new(data)

    blob = Blob.new([js_data], to_js({ 'type': 'image/png' }))

    obj_url = URL.createObjectURL(blob)

    preview.setAttribute("src", obj_url)
    preview.hidden = False

def mkzip_from_dir(dir_path):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                full_name = os.path.join(root, file)
                archive_name = os.path.relpath(full_name, dir_path)
                zf.write(full_name, archive_name)

    return zip_buffer

def start_app(import_formats, export_formats):
    preloader.hidden = True
    app.hidden = False

    for raw_name, name in import_formats.items():
        # print(raw_name, name)
        option = document.createElement('option')
        option.setAttribute("value", raw_name)
        option.textContent = name

        import_format.appendChild(option)

    for raw_name, name in export_formats.items():
        # print(raw_name, name)
        option = document.createElement('option')
        option.setAttribute("value", raw_name)
        option.textContent = name

        export_format.appendChild(option)

    import_format.value = "!auto"
    export_format.value = "yaff"

def preload_print(text: str):
    msg = document.getElementById("preloader-msg")
    msg.textContent = text
    print(text)


