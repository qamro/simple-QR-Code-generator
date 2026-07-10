import qrcode

url = input("Enter the URL to generate QR code: ").strip() 
# we used strip() to remove any leading or trailing whitespace from the input

file_path = input("Enter the file path to save the QR code (e.g., 'qrcode.png'): ").strip()

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)   
qr.add_data(url)

img = qr.make_image()