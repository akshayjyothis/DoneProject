from django.http import HttpResponse
from django.shortcuts import render
from .models import Video
import subprocess
import face_recognition
import cv2
import numpy as np
import time


# Create your views here.
def index(request):
    Videos = Video.objects.all()
    return render(request, 'videos/index.html', context={"videos": Videos})


def device(request):
    device_def = """USB:

        USB 3.0 Bus:

        Host Controller Driver: AppleUSBXHCISPTLP
        PCI Device ID: 0x9d2f 
        PCI Revision ID: 0x0021 
        PCI Vendor ID: 0x8086 

        USB 3.1 Bus:

        Host Controller Driver: AppleUSBXHCIAR
        PCI Device ID: 0x15d4 
        PCI Revision ID: 0x0002 
        PCI Vendor ID: 0x8086 
        Bus Number: 0x00 

    """

    result = subprocess.run(["system_profiler", "SPUSBDataType"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True)
    device_details = result.stdout
    color = "green"
    if device_details == device_def:
        context = {"color": "red"}
        print("NO EXTERNAL DEVICE CONNECTED")
    else:
        # print("EXTERNAL DEVICE DETECTED")
        print("YESSSSS DEVICE DETECTED")
    print("SAAAFFUUVVAANN")
    return render(template_name='index.html',context= {'color': 'blue'})


# FACE DETECTION

def face(request):
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    obama_image = face_recognition.load_image_file("obama.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    # Load a second sample picture and learn how to recognize it.
    anu_image = face_recognition.load_image_file("anu.jpg")
    anu_face_encoding = face_recognition.face_encodings(anu_image)[0]

    akshay_image = face_recognition.load_image_file("akshay.jpg")
    akshay_face_encoding = face_recognition.face_encodings(akshay_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        obama_face_encoding,
        anu_face_encoding, akshay_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Anu", "Akshay"
    ]

    face_det = 0
    while True:
        face_det = 0
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = frame[:, :, ::-1]

        # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                if name == "Akshay":
                    face_det = 1
                else:
                    face_det = 0

            if ret == True:
                if face_det == 1:
                    print("FACE DETECTED")
                else:
                    t = 10
                    while t:
                        mins, secs = divmod(t, 60)
                        timer = '{:02d}:{:02d}'.format(mins, secs)
                        print(timer, end="\r")
                        time.sleep(1)
                        t -= 1
                        if face_det == 1:
                            break

                    print('FACE NOT DETECTED')

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
