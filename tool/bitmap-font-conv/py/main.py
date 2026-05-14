import os
import re
import tempfile
from io import BytesIO, BufferedReader

from pyscript import when, window
from pyscript.ffi import is_none

from load_libs import load_monobit

await load_monobit()
import monobit
import frontend

FONT_SAVERS = monobit.storage.savers

EXPORT_FORMATS = {}
for fmt in sorted(FONT_SAVERS.get_formats()):
    file_ext = FONT_SAVERS.get_template(fmt)
    file_ext = re.sub(r'\{.*?\}', '*', file_ext)

    EXPORT_FORMATS[fmt] = f"{fmt} ({file_ext})"

frontend.start_app(EXPORT_FORMATS)

@when("click", "#font-upload-button")
def upload_font(event):
    frontend.font_upload.click()

@when("change", "#font-upload")
async def update_font_preview(event):
    frontend.preview.hidden = True

    files = event.target.files
    file = files.item(0)

    frontend.font_upload_name.textContent = file.name

    data: bytes = await frontend.get_file_data(file)

    try:
        reader = BufferedReader(BytesIO(data))
        font = monobit.load(reader)
        frontend.render_preview(monobit, font)
    except Exception as e:
        window.alert(f"Font preview failed: {e}")
        return

@when("click", "#preview")
def show_preview(event):
    target = event.target
    window.open(target.src, '_blank')

@when("click", "#convert-button")
async def start_conversion(event):
    files = frontend.font_upload.files
    file = files.item(0)

    font_format = "yaff"

    if len(frontend.export_format.value) > 0:
        font_format = str(frontend.export_format.value)

    if is_none(file):
        window.alert("Please input a font file")
        return

    data: bytes = await frontend.get_file_data(file)

    try:
        reader = BufferedReader(BytesIO(data))
        font = monobit.load(reader)
    except Exception as e:
        window.alert(f"Failed to load font: {e}")
        return

#     try:
#
#     except:
#         pass


    filename_noext = os.path.splitext(file.name)[0]
    name_template = FONT_SAVERS.get_template(font_format)

    with tempfile.TemporaryDirectory() as tmpdir:
        filename = None
        try:
            filename = name_template.format(name=filename_noext)
            monobit.save(font, os.path.join(tmpdir, filename), format=font_format)
        except Exception as e:
            window.alert(f"Failed to convert font: {e}")
            return

        entry_count = len(os.listdir(tmpdir))

        if entry_count <= 1:
            frontend.save_file(filename, open(os.path.join(tmpdir, filename), 'rb').read())
            return

        zip_io = frontend.mkzip_from_dir(tmpdir)
        frontend.save_file(f"{filename_noext}-{font_format}.zip", zip_io.getbuffer())
