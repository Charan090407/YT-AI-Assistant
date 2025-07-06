import cv2


img = cv2.imread("anime.jpeg")
img = cv2.resize(img, (512, 512))


x1, x2 = 250, 320 
y1, y2 = 235, 260  

# Draw box
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow("Mouth Locator", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
