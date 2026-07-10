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


print("------------------------------ QR CODE GENERATED ------------------------------")
print(f"QR code generated and saved to {file_path}")
