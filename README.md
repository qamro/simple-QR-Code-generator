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

1. **No `qr.make(fit=True)` call.** The QR version is fixed at `version=1` and `make()` is never called, so long URLs could produce a broken or truncated QR code instead of automatically resizing.
2. **No error handling.** Empty input, invalid paths, or bad permissions will crash the script with a raw traceback instead of a clean error message.
3. **No `.png` extension check.** If the user doesn't type an extension, saving can fail or guess the wrong format.
4. **No directory check.** If the user enters a folder path instead of a file path, it crashes with `IsADirectoryError` instead of handling it gracefully (this actually happened to me while testing).
5. **No CLI arguments.** It only works interactively — there's no way to run it non-interactively with flags like `--url` or `--output`.

I know how to fix these, I just haven't updated the script yet.

## License

MIT License — do whatever you want with this code. Fork it, fix the gaps above, rewrite it entirely, use it commercially, whatever. No attribution required (though appreciated).

```
MIT License

Copyright (c) 2026 qamro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
