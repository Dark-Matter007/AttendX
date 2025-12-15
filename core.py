import cv2
import face_recognition
import numpy as np
import os

def load_known_faces(path):
    """
    Loads known face images and encodes them for recognition.
    Args:
        path (str): Path to folder containing face images.
    Returns:
        encodeList (list): Encoded face representations.
        names (list): Corresponding student names (formatted).
    """
    images, names = [], []

    # --- Ensure folder exists ---
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"⚠️ Folder '{path}' created. Add face images inside it.")
        return [], []

    file_list = [f for f in os.listdir(path) if not f.startswith('.')]

    if not file_list:
        print(f"⚠️ No images found in '{path}'. Please add face photos.")
        return [], []

    print(f"🧠 Loading {len(file_list)} images from '{path}' ...")

    # --- Process each file ---
    for file in file_list:
        file_path = os.path.join(path, file)
        img = cv2.imread(file_path)

        if img is None:
            print(f"⚠️ Skipped unreadable file: {file}")
            continue

        # Convert to RGB for face_recognition
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)

        if len(encodings) > 0:
            # Remove file extension and capitalize for clean display
            name = os.path.splitext(file)[0].capitalize()
            images.append(img)
            names.append(name)
        else:
            print(f"⚠️ No face detected in {file}, skipping it.")

    if not images:
        print("❌ No valid faces found. Please check your images.")
        return [], []

    # --- Encode all known faces ---
    encodeList = []
    for img, name in zip(images, names):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        enc = face_recognition.face_encodings(img_rgb)[0]
        encodeList.append(enc)
        print(f"✅ Encoded: {name}")

    print(f"✨ Encoding complete: {len(encodeList)} faces loaded.")
    print(f"✅ Known faces loaded: {names}")

    return encodeList, names


def recognize_faces_in_frame(frame, encodeListKnown, studentNames):
    """
    Detects and recognizes faces in a given video frame or image.
    Args:
        frame (ndarray): The current frame from camera or photo.
        encodeListKnown (list): Encoded faces of known students.
        studentNames (list): Names of known faces.
    Returns:
        recognized_names (list): Names of people detected in this frame.
    """
    if not encodeListKnown or not studentNames:
        print("⚠️ No known faces available for recognition.")
        return []

    # Downscale for faster processing (¼ size)
    imgS = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    recognized_names = []

    # --- Compare detected faces with known ones ---
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = studentNames[matchIndex]
            recognized_names.append(name)

            # Scale face box back to original frame size
            y1, x2, y2, x1 = [v * 4 for v in faceLoc]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2 - 35), (x2, y2),
                          (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (255, 255, 255), 2)
            print(f"🧍 Recognized: {name}")

    return recognized_names
