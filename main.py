# importing modules
import cv2 
import numpy as np
import dlib 
from math import hypot
# from random import randrange



# all defined funcutions


# finding midpoint of landmarks of eyes
def midpoint(p1,p2):
    return int((p1.x + p2.x)/2),int((p1.y+p2.y)/2)

# defining blinking ratio (unit = frames)
def Blinking_ratio(eye_points, facical_landmarks ):
    left_point = (facical_landmarks.part(eye_points[0]).x,facical_landmarks.part(eye_points[0]).y)
    right_point = (facical_landmarks.part(eye_points[3]).x,facical_landmarks.part(eye_points[3]).y)
    centre_top = midpoint(facical_landmarks.part(eye_points[1]),facical_landmarks.part(eye_points[2]))
    centre_bottom = midpoint(facical_landmarks.part(eye_points[5]),facical_landmarks.part(eye_points[4]))
       
    hor_line_length = hypot((left_point[0] - right_point[0]) ,(left_point[1] - right_point[1]))
    ver_line_length = hypot((centre_top[0] - centre_bottom[0]),(centre_top[1] - centre_bottom[1]))
        
    ratio = hor_line_length/ver_line_length
    return ratio

# finding facial landmarks.
def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye


    # drawing keyboard
def draw_menu():
    cv2.line(left_right_keyboard,(300,0),(300,500),(255,255,255),thickness=3)

    cv2.putText(left_right_keyboard,"Right",(10,70),font,2,(179,43,1))
    cv2.putText(left_right_keyboard,"KeyBoard",(10,150),font,1.5,(179,43,1))

    cv2.putText(left_right_keyboard,"Left",(370,70),font,2,(179,43,1))
    cv2.putText(left_right_keyboard,"KeyBoard",(310,150),font,1.5,(179,43,1))


# finding gaze ratio
def get_gaze_ratio(eye_points, facical_landmarks):
    
        # Gaze Detection
        eye_region = np.array([ (facical_landmarks.part(eye_points[0]).x, facical_landmarks.part(eye_points[0]).y),
                                     (facical_landmarks.part(eye_points[1]).x, facical_landmarks.part(eye_points[1]).y),
                                     (facical_landmarks.part(eye_points[2]).x, facical_landmarks.part(eye_points[2]).y),
                                     (facical_landmarks.part(eye_points[3]).x, facical_landmarks.part(eye_points[3]).y),
                                     (facical_landmarks.part(eye_points[4]).x, facical_landmarks.part(eye_points[4]).y),
                                     (facical_landmarks.part(eye_points[5]).x, facical_landmarks.part(eye_points[5]).y)],np.int32) #after tha array ***(landmarks.part(41)), landmarks.part(41).y],np.int32)***  video 3

       

        height,width,_ = frame.shape
        mask = np.zeros((height,width), np.uint8)
        cv2.polylines(mask,[eye_region],True,255,2)
        cv2.fillPoly(mask,[eye_region],255)
        eye = cv2.bitwise_and(gray,gray,mask=mask)


        min_x = np.min(eye_region[:,0])
        max_x = np.max(eye_region[:,0])
        min_y = np.min(eye_region[:,1])
        max_y = np.max(eye_region[:,1])

        

        gray_eye = eye[min_y:max_y,min_x:max_x]
        
        _,threshold_eye = cv2.threshold(gray_eye,70,255, cv2.THRESH_BINARY)
        
        
        # dividing left eye in two parts(left, right)
        height,width = threshold_eye.shape
        left_side_threshold = threshold_eye[0:height,0:int(width/2)]
        left_side_white = cv2.countNonZero(left_side_threshold)
        
        
        # dividing left eye in two parts(left, right)
        
        right_side_threshold = threshold_eye[0:height,int(width/2):width]
        right_side_white = cv2.countNonZero(right_side_threshold)

        if right_side_white == 0:
            gaze_ratio = 5
            
        elif left_side_white == 0:
            gaze_ratio = 1
        else:
            gaze_ratio = left_side_white/ right_side_white
        return gaze_ratio
            

# all defined variable(Global)
font = cv2.FONT_HERSHEY_TRIPLEX
# using webcam
cap = cv2.VideoCapture(0)
detetor = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
# counter
frames = 0
letter_index = 0
blinking_frames =0
frames_to_blink = 6
frames_active_letter = 9

# Text and Keyboard 
text =""
keyboard_selected = "left"
last_keyboard_selected = "left"
select_keyboard_menu = True
keyboard_selection_frames = 0

new_frame = np.zeros((500,500,3),np.uint8)

# preparing the board for presenting text
board = np.zeros((500,500),np.uint8)
board[:]=0

keyboard = np.zeros((500,565,3),np.uint8)

keys_set_1= {
    0:"Q",1:"W",2:"E",3:"R",4:"T",
    5:"A",6:"S",7:"D",8:"F",9:"G",
    10:"Z",11:"X",12:"C",13:"V",14:"<",
    15:"<-"


}
keys_set_2 = {
    0:"Y",1:"U",2:"I",3:"O",4:"P",
    5:"H",6:"J",7:"K",8:"L",9:"_",
    10:"V",11:"B",12:"N",13:"M",14:"<",
    15:"En"
}

left_right_keyboard = np.zeros((250,600,3),np.uint8)


def letter(letter_index,text,letter_light):

    # Keys
    if letter_index == 0:
        x = 10
        y = 10
    elif letter_index == 1:
        x = 120
        y = 10
    elif letter_index == 2:
        x = 230
        y = 10
    elif letter_index == 3:
        x = 340
        y = 10
    elif letter_index == 4:
        x = 450
        y = 10
    elif letter_index == 5:
        x = 10
        y = 120
    elif letter_index == 6:
        x = 120
        y = 120
    elif letter_index == 7:
        x = 230
        y = 120
    elif letter_index == 8:
        x = 340
        y = 120
    elif letter_index == 9:
        x = 450
        y = 120
    elif letter_index == 10:
        x = 10
        y = 230
    elif letter_index == 11:
        x = 120
        y = 230
    elif letter_index == 12:
        x = 230
        y = 230
    elif letter_index == 13:
        x = 340
        y = 230
    elif letter_index == 14:
        x = 450
        y = 230
    # elif letter_index == 15:
    #     x = 225
    #     y = 340
    # elif letter_index == 15:
    #     x = 230
    #     y = 340
    # width , height of boxes of letters
    width = 100
    height = 100
    th = 3 #thickness
    if letter_light is True:
        cv2.rectangle(keyboard,(x+th,y+th),(x+width-th,y+height-th),(255,0,0),-1)
    else:
        cv2.rectangle(keyboard,(x+th,y+th),(x+width-th,y+height-th),(255,0,0),3)

    # Text Settings
    font_letter = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 3
    font_th = 3
    text_size = cv2.getTextSize(text,font_letter,font_scale,font_th)[0]
    width_text, height_text = text_size[0],text_size[1]
    text_x = int((width-width_text)/2) +x
    text_y = int((height + height_text)/2) +y
    cv2.putText(keyboard,text,(text_x,text_y),font_letter,font_scale,(0,255,0),font_th)



while True:
    _,frame = cap.read()
    rows, cols, _ = frame.shape
    keyboard[:] =  (0,0,0)
    frames += 1
    
    # normal to gray
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    # Draw a white space for loading bar
    frame[rows - 50: rows, 0: cols] = (255, 255, 255)

    if select_keyboard_menu is True:
        draw_menu()

    # Keyboard selected
    if keyboard_selected == "left":
        keys_set = keys_set_1
        
    else:
        keys_set = keys_set_2
    active_letter = keys_set[letter_index]




    # face detecting
    faces = detetor(gray)
    for face in faces:

        # predicting landmarks
        landmarks = predictor(gray,face)

        
        # finding facial landmarks.
        left_eye, right_eye = eyes_contour_points(landmarks)


        # defining ratios         
        left_eye_ratio = Blinking_ratio([36,37,38,39,40,41],landmarks)
        right_eye_ratio = Blinking_ratio([42,43,44,45,46,47],landmarks)
        blinking_ratio = (left_eye_ratio+right_eye_ratio)/2

         # Locating Eyes 
        cv2.polylines(frame, [left_eye], True, (0, 0, 255), 2)
        cv2.polylines(frame, [right_eye], True, (0, 0, 255), 2)

        if select_keyboard_menu is True:
            # Detecting gaze to select Left or Right keybaord
            gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
            gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
            gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2



            # keyboard selection
            if 3>gaze_ratio>=0:
                new_frame[:]= (0,255,0)
                keyboard_selected = "right"
                keyboard_selection_frames += 1
                # If Kept gaze on one side more than 15 frames, move to keyboard
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = False
                    # Set frames count to 0 when keyboard selected
                    frames = 0
                    keyboard_selection_frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
            elif gaze_ratio>3.5:#3.8,4.2#2.8,3.0
                keyboard_selected = "left"
                keyboard_selection_frames += 1
                
                # gaze on one side must be more than 15 frames to move to keyboard
                if keyboard_selection_frames == 15:
                    select_keyboard_menu = False
                    # Set frames count to 0 when keyboard selected
                    frames = 0
                if keyboard_selected != last_keyboard_selected:
                    last_keyboard_selected = keyboard_selected
                    keyboard_selection_frames = 0
            else:
                pass
            # cv2.putText(frame,str(gaze_ratio),(50,150),font,2,(0,255,0),3)
            
            
            

        else:
            # Detect the blinking to select the key that is lighting up
            if blinking_ratio > 4:
                blinking_frames += 1
                frames -= 1

                # Show blue eyes when closed
                cv2.polylines(frame, [left_eye], True, (255, 0, 0), 2)
                cv2.polylines(frame, [right_eye], True, (255, 0, 0), 2)

                # Typing letter
                if blinking_frames == frames_to_blink:
                    if active_letter != "<" and active_letter != "_" and active_letter != "En" and active_letter != "<-" :
                        text += active_letter
                        
                    if active_letter == "_":
                        text += " "
                    
                   
                    select_keyboard_menu = True
                    
            else:
                blinking_frames = 0


            # cv2.putText(frame,str(gaze_ratio),(50,150),font,2,(0,255,0),3)
            
    # Display letters on the keyboard
    if select_keyboard_menu is False:
        if frames == frames_active_letter:
            letter_index += 1
            frames = 0
        if letter_index == 16:
            letter_index = 0
        for i in range(15):
            if i == letter_index:
                light = True
            else:
                light = False
            letter(i, keys_set[i], light)

    # writing on the board
    cv2.putText(board, text, (10, 100), font,2,255,3)
    

    # Blinking loading bar
    percentage_blinking = blinking_frames / frames_to_blink
    loading_x = int(cols * percentage_blinking)
    cv2.rectangle(frame, (0, rows - 50), (loading_x, rows), (51, 51, 51), -1)

        



   
    # presenting left right keyboard
    cv2.imshow("Keyborad", left_right_keyboard)
    #showing keyboard
    cv2.imshow("Virtual KeyBoard",keyboard)
    #presenting board where your text is shown
    cv2.imshow("Board",board)
    #presenting face
    cv2.imshow("Preview",frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# closing webcam presentation
cap.release()
cv2.destroyAllWindows()

#362