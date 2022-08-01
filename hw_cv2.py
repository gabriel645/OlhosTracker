import cv2
import mediapipe_lib as mp
# xml= "viola.xml"
# xml= "iris.xml"

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

# For webcam input:
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
cap = cv2.VideoCapture(3)
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
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_TESSELATION,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_tesselation_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_CONTOURS,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_LEFT_EYE,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_LEFT_IRIS,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_iris_connections_style())
        mp_drawing.draw_landmarks(
            image=image,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_RIGHT_EYE,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_RIGHT_IRIS,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_iris_connections_style())
        # mp_drawing.draw_landmarks(
        #     image=image,
        #     landmark_list=face_landmarks,
        #     connections=mp_face_mesh.FACEMESH_IRISES,
        #     landmark_drawing_spec=None,
        #     connection_drawing_spec=mp_drawing_styles
        #     .get_default_face_mesh_iris_connections_style())
    # Flip the image horizontally for a selfie-view display.
    
    # rows,cols = image.shape
    # M = cv2.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)

    
    try:
      cord = results.multi_face_landmarks[0].landmark
      cord_eyes = range(468,478) 
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
      continue

    # try:
    #   cord = results.multi_face_landmarks[0].landmark
    #   for c in range(0,len(cord)):
    #     shape = image.shape 
    #     relative_x = int(cord[c].x * shape[1])
    #     relative_y = int(cord[c].y * shape[0])
    #     image = cv2.circle(image, (relative_x,relative_y), radius=2, color=(0, 0, 255), thickness=-1)
    #     image = cv2.putText(image, str(c), (relative_x,relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, color=(0, 0, 255), thickness=1)

    # except:
    #   continue
    # cord = results.multi_face_landmarks[0].landmark
    # for c in range(0,len(cord)):
    #   shape = image.shape 
    #   relative_x = int(cord[c].x * shape[1])
    #   relative_y = int(cord[c].y * shape[0])
    #   image = cv2.circle(image, (relative_x,relative_y), radius=2, color=(0, 0, 255), thickness=-1)
    #   image = cv2.putText(image, str(c), (relative_x,relative_y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.3, color=(0, 0, 255), thickness=1)

    

    # cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
    cv2.imshow('MediaPipe Face Mesh', image)
    # cv2.imshow('MediaPipe Face Mesh', cv2.rotate(cv2.flip(image, 1),cv2.ROTATE_90_COUNTERCLOCKWISE))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()







                                    ### OPEN_CV USING CASCADE CLASSIFIER ###
# faceClassifier = cv2.CascadeClassifier(xml)
# capture = cv2.VideoCapture(0)


# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# while not cv2.waitKey(16) & 0xFF == ord("q"):
#     ret, frame_color = capture.read()
#     gray = cv2.cvtColor(frame_color, cv2.COLOR_BGR2GRAY)

#     faces = faceClassifier.detectMultiScale(gray)

#     for x, y, w, h in faces:
#         cv2.rectangle(frame_color, (x,y), (x+w, y+h), (0,0,255), 2)

#     cv2.imshow('color', frame_color)
#     # cv2.imshow('gray', gray)


