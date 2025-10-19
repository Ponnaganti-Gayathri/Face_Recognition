import cv2
import face_recognition
import pickle
import os

folderpath = 'images'

if not os.path.exists(folderpath):
    print(f"❌ Folder '{folderpath}' not found. Please create it and add face images.")
    exit()

pathlist = os.listdir(folderpath)
imglist = []
empIds = []

print(f"🔍 Loading images from '{folderpath}'...")

for path in pathlist:
    curPath = os.path.join(folderpath, path)
    img = cv2.imread(curPath)

    if img is None:
        print(f"⚠️ Could not read image: {path} — skipping.")
        continue

    imglist.append(img)
    empIds.append(os.path.splitext(path)[0])

if not imglist:
    print("❌ No valid images found in the folder.")
    exit()


def findEncodings(imagesList):
    encodingsList = []
    for img, name in zip(imagesList, empIds):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faceLocs = face_recognition.face_locations(img_rgb)

        if len(faceLocs) == 0:
            print(f"⚠️ No face detected in image: {name} — skipping.")
            continue

        encode = face_recognition.face_encodings(img_rgb)[0]
        encodingsList.append(encode)
        print(f"✅ Face encoded for image: {name}")

    return encodingsList


print("⏳ Generating encodings...")
encodeListKnown = findEncodings(imglist)

if not encodeListKnown:
    print("❌ No faces were encoded. Please check your images.")
    exit()

encodeListKnownWithIds = [encodeListKnown, empIds]

with open("encodefile.p", "wb") as file:
    pickle.dump(encodeListKnownWithIds, file)

print(f"🎉 Encodings saved successfully for {len(encodeListKnown)} faces.")
