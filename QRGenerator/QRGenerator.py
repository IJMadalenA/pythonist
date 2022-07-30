import qrcode

data = ""

qr = qrcode.QRCode(
    version=1,
    box_size=40,
    border=5
)

qr.add_data(data)

qr.make(fit=True)

img = qr.make_image(
    fill_color='black',
    back_color='whiter',
)

img.save("QRCode.png")
