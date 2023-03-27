import time
import cv2
import numpy as np
import mediapipe_lib as mp

##################  Global vars ########################


#########################################################

class Face:

    def __init__(self):
        self.points_list = list()
        # df_header = []
        df_rows = []
        # For webcam input:
        self.cap = cv2.VideoCapture(2)
        self.see()

    def see(self):        
        if self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                # print("Ignoring empty camera frame.")

                results = mp.get_mesh(mp.face_mesh, frame)
                
                # Draw points of interest in face
                show_face = False    
                while not show_face:
                    
                    try:     
                        mp_landmarks = results.multi_face_landmarks[0].landmark # all points we get from mediapipe
                        show_face = True
                    except:
                        mp_landmarks = []
                        print("Ignoring empty camera frame.")
                        time.sleep(1)
                        success, frame = self.cap.read()
                        results = mp.get_mesh(mp.face_mesh, frame)
                    
                p_eyes = list(range(468,478)) # eye point ids   
                p_face = [9,10,108,151,337] # face point ids, refer to image > img/point_numbers.png
                
                all_p = p_eyes + p_face #all selected point ids
            
                self.points_list = []
                if len(mp_landmarks) > 0: # if no face is shown there are no points
                    for p in all_p: 
                        self.points_list.append(mp_landmarks[p]) #list with all points(with coodinates)  
                
                    mp.draw_points(self.points_list, frame)
                
                if len(self.points_list) > 0:       
                    cv2.imshow('MediaPipe Face Mesh', frame)

                # cv2.imshow('MediaPipe Face Mesh', cv2.rotate(cv2.flip(image, 1),cv2.ROTATE_90_COUNTERCLOCKWISE))
                return self.points_list

    def shut(self):
        self.cap.release()               


if __name__ == "__main__":
    vision = Face()
    
    while True:
        # time.sleep(1)
        vision.see()
        li = [[i.x, i.y, i.z] for i in vision.points_list]
        end_li = [x for l in li for x in l]        
    
        print(np.array(end_li))
        
        if cv2.waitKey(5) & 0xFF == 27:      
            vision.shut()
            break
