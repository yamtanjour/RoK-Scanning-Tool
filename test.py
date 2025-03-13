from PIL import Image

full_image = Image.open("player_profile1.png")
# Example coordinates – adjust these as needed!
name_crop = (750, 230, 1100, 280)
power_crop = (750, 310, 1100, 360)
kp_crop = (750, 390, 1100, 440)

name_img = full_image.crop(name_crop)
power_img = full_image.crop(power_crop)
kp_img = full_image.crop(kp_crop)

name_img.save("debug_name.png")
power_img.save("debug_power.png")
kp_img.save("debug_kp.png")
