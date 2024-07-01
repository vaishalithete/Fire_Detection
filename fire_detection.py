import cv2
import numpy as np
import playsound
import time
import smtplib

Fire_Reported = 0
Alarm_Status = False
Alarm_Duration = 5  # Duration in seconds
Email_Status = False
Video_Resize = (1000, 600)
Threshold_Size = 15000

def play_audio():
    playsound.playsound("alarm-sound.mp3", True)

def send_mail_function(subject="Fire Detected"):
    recipientEmail = "abc@gmail.com"  # Update with your recipient's email address
    recipientEmail = recipientEmail.lower()
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login("xyz@gmail.com", 'ABC')  # There is a email that send you message

        email_subject = f"Subject: {subject}\n\n"
        email_body = "Warning: A Fire Accident has been reported on ABC Company"

        message = email_subject + email_body

        server.sendmail("xyz@gmail.com", recipientEmail, message)
        print("Email sent to {}".format(recipientEmail))
        server.close()
    except Exception as e:
        print("Error sending email:", e)

# Update the video file name to a simpler one
video = cv2.VideoCapture("video.mp4")

if not video.isOpened():
    print("Error: Could not open video file.")
    exit()

start_time = time.time()

while True:
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read frame. Exiting...")
        break

    frame = cv2.resize(frame, Video_Resize)
    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    lower = np.array([18, 50, 50])
    upper = np.array([35, 255, 255])
    lower = np.array(lower, dtype='uint8')
    upper = np.array(upper, dtype='uint8')
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, hsv, mask=mask)

    cv2.imshow("output", output)
    size = cv2.countNonZero(mask)
    elapsed_time = time.time() - start_time

    if size > Threshold_Size and not Alarm_Status and elapsed_time >= Alarm_Duration:
        Fire_Reported += 1
        play_audio()
        Alarm_Status = True       
        if not Email_Status:
            send_mail_function(subject="Fire Detected")
            Email_Status = True

    if cv2.waitKey(30) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
video.release()