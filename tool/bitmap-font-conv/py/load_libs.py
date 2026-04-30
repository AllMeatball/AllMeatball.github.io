import frontend
import micropip

async def load_monobit():
    dependencies = [
        "lzma",
        "reportlab",
        "pillow",
        "python-bidi",
        "arabic-reshaper",
        "uniseg",
        "fonttools",
        "libarchive-c",
        # "ncompress",
        # "acefile"
    ]

    frontend.preload_print("Downloading monobit...")
    await micropip.install("monobit", deps=False)
    frontend.preload_print("Done Downloading monobit...")

    for dep in dependencies:
        frontend.preload_print(f"Downloading {dep}...")
        await micropip.install(dep)
        frontend.preload_print(f"Done Downloading {dep}...")
