import numpy as np
import cv2
import imutils

# Laden der Cascade-Datei
gun_cascade = cv2.CascadeClassifier('cascade.xml')
if gun_cascade.empty():
    raise IOError("Konnte die Cascade-Datei nicht laden..")

# Zugriff auf die Kamera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    raise IOError("Konnte die Kamera nicht starten..")

firstFrame = None
gun_exist = False

try:
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))

        if len(gun) > 0:
            gun_exist = True

        for (x, y, w, h) in gun:
            frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if firstFrame is None:
            firstFrame = gray
            continue

        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    if gun_exist:
        print("Gun Detected")
    else:
        print("No Gun Detected")

finally:
    camera.release()
    cv2.destroyAllWindows()