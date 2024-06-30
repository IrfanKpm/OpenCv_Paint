import cv2
import mediapipe as mp
import math
import time 


# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
max_num_hands = 1
min_detection_confidence = 0.5  
min_tracking_confidence = 0.5 
hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=min_detection_confidence,
    min_tracking_confidence=min_tracking_confidence
)

# Define drawing specifications for landmarks and connections
drawLandmark = mp.solutions.drawing_utils
landmark_spec = drawLandmark.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=3)
connection_spec = drawLandmark.DrawingSpec(color=(180, 180, 180), thickness=2)




# Define color constants
white = (255, 255, 255)
orange = (0, 165, 255)
red = (0, 0, 255)
cyan = (255, 255, 0)
green = (0, 255, 0)
blue = (255, 0, 0)
magenta = (255, 0, 255)
yellow = (0, 255, 255)
black = (0, 0, 0)

# Initialize variables for painting
last_click_time = time.time()
selected_color = black
selected_tool = None
fill_mode = False
circle_data = [] 
line_data = []
re_data = []
pen_x = []
pen_y = []
msg = 'Welcome To OpenCv Paint v1.0'

def set_cooldown_period():
   if selected_tool == "pen":
      return 0
   else:
      return 0.8


border_color = (138, 11, 246) 
def colorBar(frame):
    cv2.rectangle(frame, (10, 10), (80, 80), white, -1)
    cv2.rectangle(frame, (90, 10), (160, 80), orange, -1)
    cv2.rectangle(frame, (170, 10), (240, 80), red, -1)
    cv2.rectangle(frame, (250, 10), (320, 80), cyan, -1)
    cv2.rectangle(frame, (330, 10), (400, 80), green, -1)
    cv2.rectangle(frame, (410, 10), (480, 80), blue, -1)
    cv2.rectangle(frame, (490, 10), (560, 80), magenta, -1)
    cv2.rectangle(frame, (570, 10), (640, 80), yellow, -1)
    cv2.rectangle(frame, (650, 10), (720, 80), black, -1)
    cv2.rectangle(frame, (730, 10), (800, 80), border_color, -1)
    cv2.rectangle(frame, (735, 15), (795, 75), selected_color, -1)


# Function to calculate distance between two points
def disx(pt1,pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 3)

# Function to paste image onto frame
def PasteImg(frame, img, pos):
    x, y = pos[0], pos[1]
    img = cv2.resize(img,(100,100))
    frame[y:y+100, x:x+100] = img

# Function to create rectangle on frame
def CreateRect(frame, pt1, pt2,color,fill):
    x1, y1 = pt1
    x2, y2 = pt2
    fill = -1 if fill else 1
    cv2.rectangle(frame, (x1, y1), (x2, y2), color,fill)

# Display tools icons
sqr = cv2.imread('toolimg/sqr.png')
circ = cv2.imread('toolimg/circle.png')
line = cv2.imread('toolimg/line.png')
re = cv2.imread('toolimg/re.png')
buck = cv2.imread('toolimg/buck.jpg')
none = cv2.imread('toolimg/none.png')
undo = cv2.imread('toolimg/undo.png')
pen = cv2.imread("toolimg/pen.png")

cap = cv2.VideoCapture(0)
while cap.isOpened():
    stat, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not stat:
        print("Error: Couldn't read frame.")
        break
    height, width, _ = frame.shape
    h = int(height * 1.4)
    w = int(width * 1.4)
    frame = cv2.resize(frame, (w, h))
    rgb = image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    ############################
    cv2.putText(frame,str(msg), (200, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,red, 4)
    cv2.putText(frame,f'tool : {selected_tool}', (650, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8,red, 2)
    cv2.putText(frame,f'fill_mode : {fill_mode}', (650, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.8,red, 2)
    colorBar(frame)
    PasteImg(frame,pen,(20,110))
    PasteImg(frame,circ,(20,220))
    PasteImg(frame,line,(20,330))
    PasteImg(frame,re,(20,440))
    PasteImg(frame,buck,(20,550))
    PasteImg(frame,undo,(140,280))
    PasteImg(frame,none,(140,390))
    if len(circle_data) != 0:
       for data in circle_data:
          fill = -1 if data[3] else 1
          cv2.circle(frame,data[0],data[1],data[2],fill)
    if len(line_data) != 0:
       for data in line_data:
          cv2.line(frame,data[0],data[1],data[2],2)
    if len(re_data) != 0:
       for data in re_data:
          CreateRect(frame,data[0],data[1],data[2],data[3])
    ############################
    # Process hand landmarks
    if results.multi_hand_landmarks:
       for hand_landmarks in results.multi_hand_landmarks:
        points = []
        drawLandmark.draw_landmarks(frame, hand_landmarks, 
                                      mp_hands.HAND_CONNECTIONS,
                                      landmark_drawing_spec=landmark_spec,
                                      connection_drawing_spec=connection_spec
                                      )
        for idx, landmark in enumerate(hand_landmarks.landmark):
            if idx == 8:
              cx8, cy8 = int(landmark.x * w), int(landmark.y * h)
              cv2.circle(frame,(cx8,cy8),6,(255,0,0),-1)
              points.append((cx8, cy8))
            if idx == 4:
              cx4, cy4 = int(landmark.x * w), int(landmark.y * h)
              cv2.circle(frame,(cx4,cy4),6,(255,0,0),-1)
              points.append((cx4, cy4))
  
            if len(points) == 2:
             cv2.line(frame, points[0], points[1], (0, 255, 0), 2)
             midpoint = ((points[0][0] + points[1][0]) // 2, (points[0][1] + points[1][1]) // 2)
             cv2.circle(frame,midpoint,6,(0,0,180),-1)
             dis = disx(points[0],midpoint)
             if dis < 25:
               current_time = time.time()
               cooldown_period = set_cooldown_period()
               if current_time - last_click_time > cooldown_period:
                 last_click_time = time.time()
                 x = midpoint[0]
                 y = midpoint[1]
                 ##############
                 if 10 < x < 80 and 10 < y < 80:
                    selected_color = white
                    msg = '[white] color selected'
                 elif 90 < x < 160 and 10 < y < 80:
                    selected_color = orange
                    msg = '[orange] color selected'
                 elif 170 < x < 240 and 10 < y < 80:
                     selected_color = red
                     msg = '[red] color selected'
                 elif 250 < x < 320 and 10 < y < 80:
                     selected_color = cyan
                     msg = '[cyan] color selected'
                 elif 330 < x < 400 and 10 < y < 80:
                     selected_color = green
                     msg = '[green] color selected'
                 elif 410 < x < 480 and 10 < y < 80:
                     selected_color = blue
                     msg = '[blue] color selected'
                 elif 490 < x < 560 and 10 < y < 80:
                     selected_color = magenta
                     msg = '[magenta] color selected'
                 elif 570 < x < 640 and 10 < y < 80:
                     selected_color = yellow
                     msg = '[yellow] color selected'
                 elif 650 < x < 720 and 10 < y < 80:
                     selected_color = black
                     msg = '[black] color selected'
                 elif 140 < x < 240 and 390 < y < 490:
                    msg = '[NO] tool selected'
                    selected_tool = None
                 elif 20 < x < 120 and 220 < y < 320:
                    msg = '[circle] tool selected'
                    circle_points = []
                    selected_tool = 'circle'
                 elif 20 < x < 120 and 330 < y < 430:
                    msg = '[line] tool selected'
                    selected_tool = 'line'
                    line_points = []
                 elif 20 < x < 120 and 440 < y < 540:
                    msg = '[rectangle] tool selected'
                    selected_tool = 'rect'
                    re_points = []
                 elif 20 < x < 120 and 110 < y < 210:
                     msg = '[pen] tool selected'
                     selected_tool = 'pen'
                 elif 20 < x < 120 and 550 < y < 650:
                    msg = '[fill_mode] changed'
                    fill_mode = not fill_mode
                 elif 140 < x < 240 and 280 < y < 380:
                    msg = '[Undo] cliked'
                    if selected_tool == 'circle':
                       circle_data = circle_data[:-1]
                    elif selected_tool == 'sqr':
                       sqr_data = sqr_data[:-1]
                    elif selected_tool == 'rect':
                       re_data = re_data[:-1]
                    elif selected_tool == 'line':
                       line_data =line_data[:-1]
                 else:
                    if selected_tool == 'circle':
                        if len(circle_points) != 2:
                          circle_points.append((x,y))
                        if len(circle_points) == 2:
                           pt1 = circle_points[0]
                           pt2 = circle_points[1]
                           circle_points = []
                           r = int(disx(pt1,pt2))
                           circle_data.append([pt1,r,selected_color,fill_mode])
                    elif selected_tool == 'line':
                        if len(line_points) != 2:
                          line_points.append((x,y))
                        if len(line_points) == 2:
                           pt1 = line_points[0]
                           pt2 = line_points[1]
                           line_points = []
                           line_data.append([pt1,pt2,selected_color])
                    elif selected_tool == 'sqr':
                        if len(sqr_points) != 2:
                          sqr_points.append((x,y))
                        if len(sqr_points) == 2:
                           pt1 = sqr_points[0]
                           pt2 = sqr_points[1]
                           sqr_points = []
                           sqr_data.append([pt1,pt2,selected_color])
                    elif selected_tool == 'rect':
                        if len(re_points) != 2:
                          re_points.append((x,y))
                        if len(re_points) == 2:
                           pt1 = re_points[0]
                           pt2 = re_points[1]
                           re_points = []
                           re_data.append([pt1,pt2,selected_color,fill_mode])   
                    elif selected_tool == "pen":
                        pen_x.append(x)
                        pen_y.append(y)    
                        if len(pen_x) > 100:
                           pen_x.pop(0)  # Remove oldest data point
                           pen_y.pop(0)     

    for (x1, y1), (x2, y2) in zip(zip(pen_x,pen_y), zip(pen_x[1:], pen_y[1:])):
      cv2.line(frame, (x1, y1), (x2, y2),selected_color, 4)        
    cv2.imshow('Frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
     break
cap.release()
cv2.destroyAllWindows()


