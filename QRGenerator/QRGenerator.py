import qrcode
import numpy as np

# URL (or any "str") to convert in a QRCode.
data = "https://github.com/IJMadalena"

qr = qrcode.QRCode(
    version=1,
    box_size=40,
    border=5
)
# add data to the QR code
qr.add_data(data)
# compile the data into a QR code array
qr.make(fit=True)

# print the image shape.
print("The shape of the QR image: ", np.array(qr.get_matrix()).shape)

# transfer the array into an actual image
img = qr.make_image(
    fill_color='black',
    back_color='white',
)
# save it to a file
img.save("QRCode.png")
