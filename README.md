# Simple QR Code Generator

A simple Python script that generates a QR code from a URL and saves it as an image file.

## What it does

- Asks the user for a URL
- Asks the user for a file path to save the QR code image
- Generates the QR code using the `qrcode` library
- Saves it as a PNG image

## Requirements

- Python 3.12+
- `qrcode` and `Pillow` (Pillow is pulled in via the `pil` extra)

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install qrcode[pil]
```

## Usage

```bash
python QR-code.py
```

You'll be prompted for:
1. The URL to encode
2. The file path to save the QR code (e.g. `qrcode.png`)

## Code

```python
import qrcode
# we use strip() to remove any leading or trailing whitespace from the input
url = input("Enter the URL to generate QR code: ").strip() 
file_path = input("Enter the file path to save the QR code (e.g., 'qrcode.png'): ").strip()
#here we can use just qr = qrcode.QRCode(), but we add some parameters to customize the QR code generation.
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)  
qr.add_data(url)
img = qr.make_image()
img.save(file_path)
print("---------------------------------------------")
print(f"QR code generated and saved to {file_path}")
print("---------------------------------------------")
```

## Known gaps (I'm aware of these)

I'm keeping the code above as-is for now, but I know it's not perfect. Here's what's missing, one by one:

1. **No `qr.make(fit=True)` call.** QR codes come in versions 1–40, where each version defines a fixed grid size — version 1 is 21×21 modules (squares), version 2 is 25×25, and so on up to version 40 at 177×177. The bigger the grid, the more data it can hold. At version 1 with low error correction, you get roughly 25 characters of capacity. That's the entire budget — URL included.
   In this script, `qrcode.QRCode(version=1, ...)` explicitly pins the QR code to that smallest grid. Normally, the `qrcode` library is designed so that after you call `add_data()`, you also call `qr.make(fit=True)` — this tells it "check how much data was added, and if it doesn't fit in the version I specified, automatically bump up to a bigger version that does." That's the whole point of `fit=True`: it turns `version=1` into a *starting suggestion* rather than a hard limit.
   Since `.make()` is never called here, that resizing step never happens. The code still runs without crashing because `add_data()` does some internal handling on its own — but it's not the same safety net. The QR grid stays locked at version 1's tiny capacity no matter how much data you feed it.
   For a short URL like `https://github.com/qamro`, this isn't a problem — it comfortably fits in 25 characters. But real-world URLs are often much longer: query strings, tracking parameters (`?utm_source=...`), long slugs, redirect links, etc. Once the data exceeds what a 21×21 grid can physically encode, one of two things happens: the library raises a `DataOverflowError`, or — worse — it produces a QR image that looks fine but doesn't decode correctly, because the data got cut off or misencoded into a grid too small to represent it.
   The fix is one line:
```python
   qr.add_data(url)
   qr.make(fit=True)   # <- resizes the grid to match the actual data length
   img = qr.make_image()
```
   This keeps `version=1` as a minimum/starting point, but lets the library grow the grid as large as needed to safely fit whatever URL is entered — so short URLs still get a small, clean QR code, and long URLs automatically get a bigger one instead of failing silently.

2. **No error handling.** Empty input, invalid paths, or bad permissions will crash the script with a raw traceback instead of a clean error message.
3. **No `.png` extension check.** If the user doesn't type an extension, saving can fail or guess the wrong format.
4. **No directory check.** If the user enters a folder path instead of a file path, it crashes with `IsADirectoryError` instead of handling it gracefully (this actually happened to me while testing).
5. **No CLI arguments.** It only works interactively — there's no way to run it non-interactively with flags like `--url` or `--output`.

I know how to fix these, I just haven't updated the script yet.

## License

**MIT License** 
Do whatever you want with this code. Fork it, fix the gaps above, rewrite it entirely, use it commercially, whatever. No attribution required (though appreciated).

```
MIT License

Copyright (c) 2026 qamro

```
