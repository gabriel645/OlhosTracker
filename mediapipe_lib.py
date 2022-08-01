from email.mime import image
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

face_mesh = mp.solutions.face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) 

def get_mesh(face_mesh, frame):
        # To improve performance, optionally mark the frame as not writeable to
        # pass by reference.
        frame.flags.writeable = False            
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE) # <<<< Rotate if needed
        results = face_mesh.process(frame)

        # Draw the face mesh annotations on the frame.
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_face_landmarks:            
            for face_landmarks in results.multi_face_landmarks:       
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_LEFT_EYE,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())       
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_RIGHT_EYE,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles
                    .get_default_face_mesh_tesselation_style())
        
        return results

# get list of points and draw on frame
def draw_points(points, frame):
    try:        
        for point in points:
            shape = frame.shape 
            relative_x = int(point.x * shape[1])
            relative_y = int(point.y * shape[0])
            frame = cv2.circle(frame, (relative_x,relative_y), radius=2, color=(0, 0, 255), thickness=-1)
            # \/\/\/ if want to put number on each point \/\/\/
            # frame = cv2.putText(frame, str(c), (relative_x,relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, color=(0, 0, 255), thickness=1)
        return frame
    except:
        return frame