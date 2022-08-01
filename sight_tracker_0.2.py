import math
from time import sleep
import cv2
import mediapipe_lib as mp
import pandas as pd
import pyautogui
from joblib import dump, load
from sklearn.neighbors import KNeighborsClassifier
from threading import Thread
import training_routine
import subprocess
import os.path
##################  Global vars ########################
model = "RidgeCVReg" # [knn_model, LinReg, RidgeCVReg]
model_x = load('Models/' + model + '_x.joblib')
model_y = load('Models/' + model + '_y.joblib')

import pyautogui #mouse movement
# pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
use_mode = "0"
training_mode = False
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
  if use_mode=="r":training_mode = True #<<<< True if you want csv output
  else: pass
df_header = []
df_rows = []

# For webcam input:
cap = cv2.VideoCapture(0)

with mp.face_mesh as face_mesh:
  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      print("Ignoring empty camera frame.")      
      continue

    results = mp.get_mesh(face_mesh, frame)
    
    # Draw points of interest in face           
    mp_landmarks = results.multi_face_landmarks[0].landmark # all points we get from mediapipe
    
    p_eyes = list(range(468,478)) # eye point ids   
    p_face = [9,10,108,151,337] # face point ids, refer to image > img/point_numbers.png
    
    all_p = p_eyes + p_face #all selected point ids
 
    points_list = []
    if len(mp_landmarks) > 0: # if no face is shown there are no points
      for p in all_p: 
        points_list.append(mp_landmarks[p]) #list with all points(with coodinates)  
      mp.draw_points(points_list, frame)
    

    if len(points_list) > 0:
      # Log cordenates in csv for model training
      if training_mode:        
        # if routine:          
        #   subprocess.run(r'python C:\Users\gabri\OneDrive\Documentos\GitHub\opencv_learning\training_routine.py') 
        #   routine = False
        #   sleep(6) # so you can click the window

        
        # Create dataframe with relative distances to point 151
        #  ----------------------151------
        df_header = p_eyes + ["head_rotation_hor"] + ["head_rotation_ver"] + ["head_pos"] + ["looking_pos"]

        row = list()

        x_base_distance = (abs(mp_landmarks[9].x - mp_landmarks[151].x) + abs(mp_landmarks[10].x - mp_landmarks[151].x))/2
        y_base_distance = (abs(mp_landmarks[108].x - mp_landmarks[151].x) + abs(mp_landmarks[337].x - mp_landmarks[151].x))/2
        
        for p in p_eyes:          
          p_x_distance = x_base_distance/(mp_landmarks[p].x - mp_landmarks[151].x)
          p_y_distance = y_base_distance/(mp_landmarks[p].y - mp_landmarks[151].y)

          row.append([p_x_distance,p_y_distance])
        
        head_rotation_hor = abs(mp_landmarks[108].x - mp_landmarks[151].x) - abs(mp_landmarks[337].x - mp_landmarks[151].x)
        row.append([head_rotation_hor])

        head_rotation_ver = abs(mp_landmarks[9].x - mp_landmarks[151].x) - abs(mp_landmarks[10].x - mp_landmarks[151].x)
        row.append([head_rotation_ver])

        head_pos = mp_landmarks[151]
        row.append([head_pos.x, head_pos.y])

          
        #Write DF to txt for modeling
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
        row.append([int(looking[0]), int(looking[1])])
        df_rows = df_rows + [row]
        if len(df_rows) >= 500:      #<<< Number of data points    
          break
        print(len(df_rows))
      
      else:
        # all_p = p_eyes + p_face
        row = list()
        
        
        x_base_distance = (abs(mp_landmarks[9].x - mp_landmarks[151].x) + abs(mp_landmarks[10].x - mp_landmarks[151].x))/2
        y_base_distance = (abs(mp_landmarks[108].x - mp_landmarks[151].x) + abs(mp_landmarks[337].x - mp_landmarks[151].x))/2
        
        for p in p_eyes:          
          p_x_distance = x_base_distance/(mp_landmarks[p].x - mp_landmarks[151].x)
          p_y_distance = y_base_distance/(mp_landmarks[p].y - mp_landmarks[151].y)

          row.append([p_x_distance,p_y_distance])
          # print(row)                    
          # z = int(cord[c].z)          
          
            #   456         457
            # [234, 52]  [214, 32]        
        looking_X = model_x.predict([row])
        looking_Y = model_y.predict([row])  

        # Average of last 10 positions for smoothing
        looking_X_stack.append(looking_X[0])        
        # >>>>>>>>>>\/\/<<<<<<<<< Find the best number
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
    cv2.imshow('MediaPipe Face Mesh', frame)
    # cv2.imshow('MediaPipe Face Mesh', cv2.rotate(cv2.flip(image, 1),cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(5) & 0xFF == 27:      
      break

if training_mode:
  df = pd.DataFrame(df_rows, columns = df_header)
  if os.path.exists("tracking.csv"):
    df.to_csv('tracking.csv', mode='a', header=False)
  else:
    df.to_csv('tracking.csv', mode='a', header=True)

cap.release()
