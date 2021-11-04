import os
import cv2
import numpy as np
import face_recognition as fr
from flask import url_for, flash, redirect
from flask_login import current_user
from datetime import datetime
import xlsxwriter


def write_attendance():
    uname = current_user.username
    time_now = datetime.now()
    time = time_now.strftime('%H:%M:%S')
    date = time_now.strftime('%d/%m/%Y')

    workbook = xlsxwriter.Workbook('attendance_sheet.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'ID')
    worksheet.write('B1', 'Date')
    worksheet.write('C1', 'Time')
    worksheet.write('A2', uname)
    worksheet.write('B2', date)
    worksheet.write('C2', time)
    workbook.close()


def face_checker():
    path = 'blog/static/profile_pics/'
    imList = os.listdir(path)
    locList = []

    for fn in imList:
        tvar = 'blog/static/profile_pics/' + fn
        locList.append(tvar)

    for imLoc in locList:
        video_capture = cv2.VideoCapture(0)

        user_image = fr.load_image_file(imLoc)
        user_face_encoding = fr.face_encodings(user_image)[0]

        known_face_encodings = [user_face_encoding]
        known_face_names = ["You"]

        while True:
            ret, frame = video_capture.read()
            rgb_frame = frame[:, :, ::-1]

            face_locations = fr.face_locations(rgb_frame)
            face_encodings = fr.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), name in zip(face_locations, face_encodings):
                for face_encoding in face_encodings:
                    matches = fr.compare_faces(known_face_encodings, face_encoding)
                    name = "Random"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]

                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

                    if (name != "Random"):
                        write_attendance()
                        flash('Your attendance has been updated!', 'success')
                        return redirect(url_for('home'))
                        video_capture.release()
                        cv2.destroyAllWindows()

            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()
