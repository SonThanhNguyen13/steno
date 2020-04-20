import cv2
import pywt
import pywt.data
import numpy as np

img = cv2.imread('dog.jpg', cv2.IMREAD_GRAYSCALE)
#img = pywt.data.camera()
img = np.float32(img)
print(img.shape)
coeffs2 = pywt.dwt2(img, 'haar')
LL, (LH, HL, HH) = coeffs2
result = []
result.append(LL)
result.append(LH)
result.append(HL)
result.append(HH)

for i in result:
    print(i.shape)
    cv2.imshow('a', i)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
for i in result:
    i /= 255
data = (result[0], (result[1], result[2], result[3]))
rmk = pywt.idwt2(data, 'haar')
print(rmk.shape)
cv2.imshow('b', rmk)
cv2.waitKey(0)
cv2.destroyAllWindows()