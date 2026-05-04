# import qrcode

# # The data you want to encode
# data = "https://www.facebook.com/deepak.baij.2025"

# # Generate the image
# img = qrcode.make(data)

# # Save the file
# img.save("kiran.png")





import secrets

otp = ''.join(secrets.choice("0123456789") for _ in range(4))

print(otp)