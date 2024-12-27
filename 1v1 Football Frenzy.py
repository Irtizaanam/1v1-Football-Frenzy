from OpenGL.GL import *
from OpenGL.GLUT import *
from math import sin, cos, pi

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 800

CATCHER_WIDTH = 150 
CATCHER_HEIGHT = 30
WHITE = (1.0, 1.0, 1.0)
catcher_color = WHITE
catcher_x = SCREEN_WIDTH - 50 
catcher_y = SCREEN_HEIGHT // 2

game_over = False
paused = False
exit_game = False
RETRY_BUTTON_LOCATION = (20, SCREEN_HEIGHT - 50)
PAUSE_BUTTON_LOCATION = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
EXIT_BUTTON_LOCATION = (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)

retry_color =  (1.0, 1.0, 1.0)
pause_color =  (1.0, 1.0, 1.0)
exit_color =  (1.0, 1.0, 1.0)


football_field_color = [0.529, 0.808, 0.922]  
current_color_flag = 0  


ball_radius = 15
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed = 1.5
ball_direction = [0, 0]  


player_radius = 30
player1_x = SCREEN_WIDTH // 3
player1_y = SCREEN_HEIGHT // 2

player2_x = 2 * SCREEN_WIDTH // 3
player2_y = SCREEN_HEIGHT // 2

player1_speed = 5
player2_speed = 5

player1_score = 0
player2_score = 0

player1_movement = {'W': False, 'A': False, 'S': False, 'D': False}
player2_movement = {'I': False, 'J': False, 'K': False, 'L': False}

#_______________________________________________________________Football______________________________________________________

class Football:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = [0, 0] 

    def move(self): 
    
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

        
        if self.x - self.radius < 50 or self.x + self.radius > SCREEN_WIDTH - 50:
            self.direction[0] *= -1 

        if self.y - self.radius < 50 or self.y + self.radius > SCREEN_HEIGHT - 50:
            self.direction[1] *= -1  
            
#___________________________________________button______________________________________________________________________________________________________________________________________________________________

def draw_retry_button(x, y, color=retry_color):
    draw_midpoint_line(x, y, x + 20, y - 20, color)
    draw_midpoint_line(x, y, x + 20, y + 20, color)
    draw_midpoint_line(x, y, x + 50, y, color)

def draw_pause_button(x, y, color=pause_color):
    draw_midpoint_line(x + 10, y + 20, x + 10, y - 20, color)
    draw_midpoint_line(x - 10, y + 20, x - 10, y - 20, color)

def draw_play_button(x, y, color=pause_color):
    draw_midpoint_line(x - 10, y + 20, x - 10, y - 20, color)
    draw_midpoint_line(x - 10, y + 20, x + 10, y, color)
    draw_midpoint_line(x - 10, y - 20, x + 10, y, color)

def draw_exit(x, y, color=exit_color):
    draw_midpoint_line(x - 10, y + 10, x + 10, y - 10, color)
    draw_midpoint_line(x - 10, y - 10, x + 10, y + 10, color)
    

def handle_mouse(button, state, x, y): 
    global paused, exit_game, game_over, player1_score, player2_score

    y = SCREEN_HEIGHT - y 

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: 

        if (PAUSE_BUTTON_LOCATION[0] - 20 <= x <= PAUSE_BUTTON_LOCATION[0] + 20 
            and PAUSE_BUTTON_LOCATION[1] - 20 <= y <= PAUSE_BUTTON_LOCATION[1] + 20):
            paused = not paused
            if paused:
                print("Game Paused")
            else:
                print("Game Resumed")

        elif (EXIT_BUTTON_LOCATION[0] - 10 <= x <= EXIT_BUTTON_LOCATION[0] + 10 
            and EXIT_BUTTON_LOCATION[1] - 10 <= y <= EXIT_BUTTON_LOCATION[1] + 10):
            print("Exiting Game")
            glutLeaveMainLoop()  

        elif (RETRY_BUTTON_LOCATION[0] <= x <= RETRY_BUTTON_LOCATION[0] + 50
            and RETRY_BUTTON_LOCATION[1] <= y <= RETRY_BUTTON_LOCATION[1] + 20):
            print("Resetting Game")
            reset_game()
            reset_ball()


#___________________________________________CATCHER________________________________________________________________________________________
def draw_catcher():
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(catcher_x, catcher_y, 0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)  
    glTranslatef(-catcher_x, -catcher_y, 0.0)

    x1, x2 = catcher_x - CATCHER_WIDTH / 2, catcher_x + CATCHER_WIDTH / 2 
    x3, x4 = x1 + 40, x2 - 40 
    y1, y2 = catcher_y, catcher_y - 40 
    draw_midpoint_line(x1, y1, x2, y1, catcher_color)
    draw_midpoint_line(x3, y2, x4, y2, catcher_color)
    draw_midpoint_line(x2, y1, x4, y2, catcher_color)
    draw_midpoint_line(x1, y1, x3, y2, catcher_color)

    glPopMatrix()

def draw_second_catcher():
    second_catcher_x = SCREEN_WIDTH // 30  
    second_catcher_y = SCREEN_HEIGHT // 2

    glPushMatrix()
    glTranslatef(second_catcher_x, second_catcher_y, 0.0)
    glRotatef(-90.0, 0.0, 0.0, 1.0) 
    glTranslatef(-second_catcher_x, -second_catcher_y, 0.0)

    x1, x2 = second_catcher_x - CATCHER_WIDTH / 2, second_catcher_x + CATCHER_WIDTH / 2
    x3, x4 = x1 + 40, x2 - 40
    y1, y2 = second_catcher_y, second_catcher_y - 40
    draw_midpoint_line(x1, y1, x2, y1, catcher_color)
    draw_midpoint_line(x3, y2, x4, y2, catcher_color)
    draw_midpoint_line(x2, y1, x4, y2, catcher_color)
    draw_midpoint_line(x1, y1, x3, y2, catcher_color)

    glPopMatrix()


#_______________________________________________________Midpoint Line Algo___________________________________________________

def draw_midpoint_line(x1, y1, x2, y2, color): 
    zone = find_zone(x1, y1, x2, y2)
    x1, y1 = to_zone0(zone, x1, y1) 
    x2, y2 = to_zone0(zone, x2, y2)

    dx = x2 - x1 
    dy = y2 - y1 

    d = 2 * dy - dx 
    incrE = 2 * dy 
    incrNE = 2 * (dy - dx) 

    x = x1 
    y = y1
    x0, y0 = to_zoneM(zone, x, y)

    draw_points(x0, y0, color)
    while x < x2:
        if d <= 0:  
            d = d + incrE 
            x = x + 1 
        else:
            d = d + incrNE 
            x = x + 1 
            y = y + 1 
        x0, y0 = to_zoneM(zone, x, y)

        draw_points(x0, y0, color)

    
def to_zone0(zone, x, y): 
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def to_zoneM(zone, x, y): 
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y
    else:
        raise ValueError("Zone must be in [0, 7]")

def find_zone(x1, y1, x2, y2): 
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy): 
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy <= 0:
            return 7
        elif dx <= 0 and dy >= 0:
            return 3
        elif dx <= 0 and dy <= 0:
            return 4
    else:                 
        if dx >= 0 and dy >= 0:
            return 1
        elif dx <= 0 and dy >= 0:
            return 2
        elif dx <= 0 and dy <= 0:
            return 5
        elif dx >= 0 and dy <= 0:
            return 6
        
def draw_points(x, y, color=WHITE, size=2):
    glColor3fv(color)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
     
#_____________________________________________Midpoint Circle Algo_________________________________________________________    

def circ_point(x, y, cx, cy):               
    glVertex2f(cx + x, cy + y) 
    glVertex2f(cx + y, cy + x) 
    glVertex2f(cx + y, cy - x) 
    glVertex2f(cx + x, cy - y) 
    glVertex2f(cx - x, cy - y) 
    glVertex2f(cx - y, cy - x) 
    glVertex2f(cx - y, cy + x) 
    glVertex2f(cx - x, cy + y) 

def mid_circle(cx, cy, radius): 
    d = 1 - radius 
    x = 0
    y = radius

    glBegin(GL_POINTS) 
    circ_point(x, y, cx, cy)

    while x < y:
        if d < 0: 
            d = d + 2 * x + 3 
        else: 
            d = d + 2 * x - 2 * y + 5 
            y = y - 1 

        x = x + 1 
        circ_point(x, y, cx, cy)

    glEnd()

def draw_circle(x, y, radius):
    mid_circle(x, y, radius)

def draw_filled_circle(x, y, radius):
    num_segments = 100
    delta_theta = 2.0 * pi / num_segments

    glBegin(GL_POLYGON)
    for _ in range(num_segments):
        theta = _ * delta_theta
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()

#________________________________________________Simple Line Drawing________________________________________________________

def draw_football_field():
    draw_line(50, 50, SCREEN_WIDTH - 50, 50)  
    draw_line(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50)  
    draw_line(50, 50, 50, SCREEN_HEIGHT - 50) 
    draw_line(SCREEN_WIDTH - 50, 50, SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50) 

    draw_line(SCREEN_WIDTH // 2, 50, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    mid_circle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 50)

    draw_rectangle_with_points(50, SCREEN_HEIGHT // 2 - 100, 150, SCREEN_HEIGHT // 2 + 100)  # Left penalty area
    draw_rectangle_with_points(SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 100, SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2 + 100)  # Right penalty area



def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()


def mid_circle(cx, cy, radius):
    x = 0
    y = radius
    d = 1 - radius

    glBegin(GL_POINTS)
    while x <= y:
        glVertex2f(cx + x, cy + y)
        glVertex2f(cx - x, cy + y)
        glVertex2f(cx + x, cy - y)
        glVertex2f(cx - x, cy - y)
        glVertex2f(cx + y, cy + x)
        glVertex2f(cx - y, cy + x)
        glVertex2f(cx + y, cy - x)
        glVertex2f(cx - y, cy - x)
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
    glEnd()


def draw_rectangle_with_points(x1, y1, x2, y2):
    draw_line(x1, y1, x2, y1)  
    draw_line(x1, y2, x2, y2)  
    draw_line(x1, y1, x1, y2)  
    draw_line(x2, y1, x2, y2)  


def draw_player(x, y):
    glColor3f(1.0, 1.0, 1.0)                           
    mid_circle(x, y, player_radius)
    draw_filled_circle(x, y, player_radius)

def draw_player2(x, y):
    glColor3f(0.0, 0.0, 0.0)                           
    mid_circle(x, y, player_radius)
    draw_filled_circle(x, y, player_radius)


def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)


#________________________________________________Player Movement_________________________________________________________________

def update_player_positions():
    
    global player1_x, player1_y, player2_x, player2_y, player1_speed, player2_speed, paused
    
    if paused != True:
        player1_dx = 0
        player1_dy = 0
        if player1_movement['W']:
            player1_dy += player1_speed        
        if player1_movement['A']:
            player1_dx -= player1_speed
        if player1_movement['S']:
            player1_dy -= player1_speed
        if player1_movement['D']:
            player1_dx += player1_speed

        player1_x += player1_dx
        player1_y += player1_dy


        player2_dx = 0
        player2_dy = 0
        if player2_movement['I']:
            player2_dy += player2_speed
        if player2_movement['J']:
            player2_dx -= player2_speed
        if player2_movement['K']:
            player2_dy -= player2_speed
        if player2_movement['L']:
            player2_dx += player2_speed

        player2_x += player2_dx
        player2_y += player2_dy
            

def keyboard(key, x, y):
    global player1_movement, player2_movement, football_field_color, current_color_flag

    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = True
    elif key == b'A' or key == b'a':
        player1_movement['A'] = True
    elif key == b'S' or key == b's':
        player1_movement['S'] = True
    elif key == b'D' or key == b'd':
        player1_movement['D'] = True

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = True
    elif key == b'J' or key == b'j':
        player2_movement['J'] = True
    elif key == b'K' or key == b'k':
        player2_movement['K'] = True
    elif key == b'L' or key == b'l':
        player2_movement['L'] = True
        
        
    # Change football field color
    
    if key == b'1':
        football_field_color = [0.0, 1.0, 0.0]  # Green
        current_color_flag = 1
    elif key == b'2':
        football_field_color = [0.0, 0.0, 1.0]  # Blue
        current_color_flag = 2
    elif key == b'3':
        football_field_color = [1.0, 0.0, 0.0]  # Red
        current_color_flag = 3
    elif key == b'4':
        football_field_color = [0.529, 0.808, 0.922]  # Light blue (default)
        current_color_flag = 0

    glutPostRedisplay()


def keyboard_release(key, x, y):
    global player1_movement, player2_movement

    # Player 1 controls
    if key == b'W' or key == b'w':
        player1_movement['W'] = False
    elif key == b'A' or key == b'a':
        player1_movement['A'] = False
    elif key == b'S' or key == b's':
        player1_movement['S'] = False
    elif key == b'D' or key == b'd':
        player1_movement['D'] = False

    # Player 2 controls
    elif key == b'I' or key == b'i':
        player2_movement['I'] = False
    elif key == b'J' or key == b'j':
        player2_movement['J'] = False
    elif key == b'K' or key == b'k':
        player2_movement['K'] = False
    elif key == b'L' or key == b'l':
        player2_movement['L'] = False

    glutPostRedisplay()

football = Football(ball_x, ball_y, ball_radius, ball_speed)

#__________________________________________________________Ball Movement________________________________________________

def check_collision(player_x, player_y, player_radius, ball):
    distance = ((player_x - ball.x) ** 2 + (player_y - ball.y) ** 2) ** 0.5 
    if distance < player_radius + ball.radius and distance > 0:  
       
        dx = ball.x - player_x
        dy = ball.y - player_y
        length = (dx**2 + dy**2)**0.5
        ball.direction = [dx / length, dy / length]
        
def update_timer(value):
    global paused

    if not paused:
        football.move()
        update_ball_position()
        glutPostRedisplay()

    glutTimerFunc(10, update_timer, 0)



def update_ball_position():
    global ball_x, ball_y, SCREEN_WIDTH, SCREEN_HEIGHT, paused,player1_score, player2_score 

    if paused != True:
        football.move()
        check_collision(player1_x, player1_y, player_radius, football)
        check_collision(player2_x, player2_y, player_radius, football)

        if (football.x + ball_radius > SCREEN_WIDTH - 50) and \
        (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
            print("Player1: Goal!!!")
            player1_score += 1
            print('Player1',player1_score,':',player2_score,'player2')
            reset_ball()

        elif (football.x - ball_radius < 50) and \
            (SCREEN_HEIGHT // 2 - 100 < football.y < SCREEN_HEIGHT // 2 + 100):
            print("Player2: Goal!!!")
            player2_score += 1
            print('Player1',player1_score,':',player2_score,'player2')
            reset_ball()

    if player1_score ==5:
        print('Player 1 wins the game')
        print('Game Over!')
        reset_game() 
        reset_ball()
    elif player2_score ==5:
        print('Player 1 wins the game')
        print('Game Over!')
        reset_game() 
        reset_ball()



def reset_ball():
    global ball_x, ball_y, ball_direction
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    ball_direction = [0, 0]  
    
def reset_game():
    global player1_x, player1_y, player2_x, player2_y, ball_x, ball_y, ball_direction, player1_score, player2_score, ball_speed, paused
    player1_x = SCREEN_WIDTH // 3
    player1_y = SCREEN_HEIGHT // 2
    player2_x = 2 * SCREEN_WIDTH // 3
    player2_y = SCREEN_HEIGHT // 2
    ball_x = SCREEN_WIDTH // 2
    ball_y = SCREEN_HEIGHT // 2
    football.x = ball_x
    football.y = ball_y
    ball_direction = [0, 0] 
    player1_score = 0
    player2_score = 0
    
    paused = True  

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)  
    glPointSize(2.0)

    update_player_positions()
    football.move()
    update_ball_position()
    reset_ball()
    draw_football_field()
    draw_player(player1_x, player1_y) 
    draw_player2(player2_x, player2_y)  
    glColor3f(1.0, 1.0, 0.0)
    draw_filled_circle(football.x, football.y, ball_radius)
    global catcher_color
    draw_catcher()
    catcher_color = (0.0, 0.0, 0.0)  
    draw_second_catcher()
    
    
    draw_retry_button(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    draw_exit(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])
    if not paused:
        draw_pause_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else:
        draw_play_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    glutSwapBuffers()

    
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b"Football")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutKeyboardUpFunc(keyboard_release)  
    glutTimerFunc(0, update_timer, 0)
    glClearColor(0.529, 0.808, 0.922, 1.0)
    glutMouseFunc(handle_mouse)

    glutMainLoop()

if __name__ == "__main__":
    main()