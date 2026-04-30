from js import document, window, Uint8Array
from pyodide.ffi.wrappers import add_event_listener

from io import BytesIO

import os
import urllib
import base64
import zipfile

app = document.getElementById("app")
preloader = document.getElementById("preloader")
font_file = document.getElementById("font-file")
font_format = document.getElementById("font-format")
font_preview = document.getElementById("font-preview")

# https://pyscript.recipes/latest/basic/file-upload/
async def get_file_data(file):
    array_buf = await file.arrayBuffer()
    return array_buf.to_bytes()

def save_file(name: str, data):
    js_data = Uint8Array.new(len(data))
    js_data.assign(data)

    file_obj = window.File.new([js_data], name)

    blob = window.URL.createObjectURL(file_obj)
    link = document.createElement("a")
    link.setAttribute("download", name)
    link.setAttribute("href", blob)
    link.click()

    window.URL.revokeObjectURL(blob)

def render_preview(monobit, font):
    writer = BytesIO()
    monobit.save(font, writer, format="image")

    b64_data = base64.b64encode(writer.getvalue())
    data_url = "data:image/png;base64," + urllib.parse.quote(b64_data.decode('ascii'))

    font_preview.setAttribute("src", data_url)
    font_preview.hidden = False

def mkzip_from_dir(dir_path):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                full_name = os.path.join(root, file)
                archive_name = os.path.relpath(full_name, dir_path)
                zf.write(full_name, archive_name)

    return zip_buffer

def start_app(export_formats):
    preloader.hidden = True
    app.hidden = False

    for raw_name, name in export_formats.items():
        # print(raw_name, name)
        option = document.createElement('option')
        option.setAttribute("value", raw_name)
        option.textContent = name

        font_format.appendChild(option)

    font_format.value = "yaff"

def preload_print(text: str):
    msg = document.getElementById("preloader-msg")
    msg.textContent = text
    print(text)


