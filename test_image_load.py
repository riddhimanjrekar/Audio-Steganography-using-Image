import cv2

path = r"C:\Users\omjanbhare\OneDrive\Desktop\AudioSteganography\cover_image.png"
img = cv2.imread(path)
print("Image loaded:", img is not None)