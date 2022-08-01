from time import sleep
import cv2
import mediapipe as mp
import pandas as pd
import pyautogui
from joblib import dump, load
from sklearn.neighbors import KNeighborsClassifier
from threading import Thread
import training_routine
import subprocess
##################  Global vars ########################
model = "RidgeCVReg" # [knn_model, LinReg, RidgeCVReg]
model_x = load('Models/' + model + '_x.joblib')
model_y = load('Models/' + model + '_y.joblib')

import pyautogui #mouse movement
# pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
use_mode = "0"
cord_log = False
routine = True
looking = []

looking_X_stack = []
looking_Y_stack = []

def thread_run ():
            training_routine.main()
          
mythread = Thread(target = thread_run, daemon = True)
#########################################################


while use_mode not in ["r", "t"]:
  print("Record(r) or Test(t)")
  use_mode = input()
  if use_mode=="r":cord_log = True #<<<< True if you want csv output
  else: pass
df_header = []
df_rows = []
face_show = False

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as face_mesh:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = cv2.rotate(image,cv2.ROTATE_90_CLOCKWISE) # <<<< Rotate if needed
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:       
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_LEFT_EYE,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())       
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_RIGHT_EYE,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
    
    # Draw points of interest in face           
    try:
      face_show = True
      cord = results.multi_face_landmarks[0].landmark
      cord_eyes = list(range(468,478))
      cord_face = [21,70,71,251,300,301,109,10,338,138,367,8,9,164]
      for c in cord_eyes:
        shape = image.shape 
        relative_x = int(cord[c].x * shape[1])
        relative_y = int(cord[c].y * shape[0])
        image = cv2.circle(image, (relative_x,relative_y), radius=2, color=(0, 0, 255), thickness=-1)
        # image = cv2.putText(image, str(c), (relative_x,relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, color=(0, 0, 255), thickness=1)
      for c in cord_face:
        shape = image.shape 
        relative_x = int(cord[c].x * shape[1])
        relative_y = int(cord[c].y * shape[0])
        image = cv2.circle(image, (relative_x,relative_y), radius=2, color=(0, 0, 255), thickness=-1)
        image = cv2.putText(image, str(c), (relative_x,relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, color=(0, 0, 255), thickness=1)
    except:
      face_show = False
      continue
       
    
    if face_show:
      # Log cordenates in csv for model training
      if cord_log:
        
        if routine:          
          subprocess.run(r'python C:\Users\gabri\OneDrive\Documentos\GitHub\opencv_learning\training_routine.py') 
          # mythread.start()
          routine = False
          sleep(6) # so you can click the window

        all_cord = cord_eyes + cord_face 
        # Create dataframe with relative cordenates 
        df_header = all_cord + ["looking_pos"]

        row = []
        for c in all_cord:
          shape = image.shape 
          relative_x = int(cord[c].x * shape[1])
          relative_y = int(cord[c].y * shape[0])
          # z = int(cord[c].z)
          
          row = row + [[relative_x,relative_y]]
            #    456        457 
            # [234, 52]  [214, 32]

        # row = row + [[pyautogui.position().x, pyautogui.position().y]]
        
        looking_old = looking
        with open(r'C:\Users\gabri\OneDrive\Documentos\GitHub\opencv_learning\training_pos.txt') as f:
          try:
            doc = f.readlines()[0]          
            looking = doc.replace('[', "").replace(']', "").split(",")
          except:
            print("weird error")
            continue          
        if(looking_old != looking):
          sleep(1.5)
        row = row + [[int(looking[0]), int(looking[1])]]
        df_rows = df_rows + [row]
        if len(df_rows) >= 5000:          
          break
        print(len(df_rows))
      else:
        all_cord = cord_eyes + cord_face 
        row = []
        
        for c in all_cord:
          shape = image.shape 
          relative_x = int(cord[c].x * shape[1])
          row.append(relative_x)
          relative_y = int(cord[c].y * shape[0])
          row.append(relative_y)
          # print(row)                    
          # z = int(cord[c].z)          
          
            #   456         457
            # [234, 52]  [214, 32]        
        looking_X = model_x.predict([row])
        looking_Y = model_y.predict([row])  

        # >>>>>>>>>>>>>>>>>>>>>>>>\/\/<<<<<<<<< Find the best number
        looking_X_stack.append(looking_X[0])

        n_last_pos = 10

        if len(looking_X_stack) > n_last_pos:  
          looking_X_stack.pop(0)

        looking_Y_stack.append(looking_Y[0])
        if len(looking_Y_stack) > n_last_pos:  
          looking_Y_stack.pop(0)
        
        def Average(lst):
          pos_avg = sum(lst) / len(lst)
          return round(int(pos_avg))
        
        lx = Average(looking_X_stack)
        ly = Average(looking_Y_stack)

        pyautogui.moveTo(lx, ly)

        # sleep(1)

        print(looking_X)

        print(looking_X_stack)

        print(str(lx) + " | " + str(ly))
    # cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    cv2.imshow('MediaPipe Face Mesh', image)
    # cv2.imshow('MediaPipe Face Mesh', cv2.rotate(cv2.flip(image, 1),cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(5) & 0xFF == 27:      
      break

if cord_log:
  df = pd.DataFrame(df_rows, columns = df_header)
  df.to_csv('tracking.csv', mode='a', header=False)

cap.release()
