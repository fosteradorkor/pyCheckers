import  pygame,sys,math,AI,json
from pygame import font
from pygame.locals import *
from AI import *

#from __builtin__ import True, False

import random


#VARIABLES
debug = True

sound = None
SCREEN_SIZE = (800,600)

gameRunning = True

FPS = 10

clock = pygame.time.Clock()

gameStates = ['MENU', 'ACTIVE', 'EXIT']

currentGameState = 'MENU'
GAME_TITLE = 'C H E Q E R S'


BOX = [680,540,100,40]      #back btn


BOARD = [[1,0,0,0,0,0,0,0,0,0],
         [0,2,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0,0,0],]

SCREEN = None

TimeRunning = 0

CPU,PLY=1,2
CPU_K,PLY_K = 3,4

currentPlayer = CPU             #will be changed later to make random choices on player

noOfCheckers = 10

PLY_SCORE, CPU_SCORE = 0, 0

checkersWidth = 50
marbleWidth = 40

marbleOffset = (checkersWidth - marbleWidth)/2

boardPt = (30,40)

borderOffset = 10

score_positionX = 550

# colors we will use in RGB format
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE = ( 0, 0, 255)
GREEN = ( 0, 255, 0)
RED = (255, 0, 0)
BG_COLOR = (255,251,210)
DARK_BROWN = (100, 0, 0)
DARK_GREEN = (66, 150, 86)
GRAY_1 = (220, 220, 220)
BG_MENU = (0,67,171)
MENU_TITLE_COLOR = (0,0,0)

menu_color_timer = 0

#imgaes
dialog_win = None
dialog_lose =  None

dialog_window = None

dialog_items =['Play again','Menu']

#ingame vars
SM = None
SD = None

#MENU VARS
rtectH, rtectW = 50, 150

rectPX = SCREEN_SIZE[0]/2 - rtectW/2

RECTANGLE = (rectPX,200,rtectW,rtectH)
RECTANGLE1 = (rectPX,300,rtectW,rtectH)
RECTANGLE2 = (rectPX,400,rtectW,rtectH)

menu_items = ['NEW GAME','ABOUT', 'EXIT']

music_volume = 0.1



#METHODS
def centerText(font, text, window):
    sz = font.size(text)
    return window[0]/2 - sz[0]/2, window[1]/2 - sz[1]/2 
    
def main():
    
    #resetBoard()
    #print (getAllLegalMoves(BOARD,CPU,AI.UP))
    printBoard(BOARD)


    while gameRunning:
        clock.tick(FPS)
        #check input
        update()
        handelInput()
        draw()

        pygame.display.update()


def init():
    global SCREEN,score_font, data_font,cheqer_font,score_font1 , sound ,dialog_win, dialog_lose, dialog_font_L, dialog_font_S
    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    pygame.init()
    score_font = font.Font('media/font/ComputerAmok.ttf',40)
    data_font = font.Font('media/font/orange juice 2.0.ttf',27)
    cheqer_font = font.Font('media/font/orange juice 2.0.ttf',95)
    score_font1 = font.Font('media/font/CHECKBK0.TTF',25)
    sound = pygame.mixer.Sound('media/sounds/Purity.ogg')
    dialog_font_L = font.Font('media/font/Gecko.ttf',40)
    dialog_font_S = font.Font('media/font/Gecko.ttf',25)
    sound.set_volume(music_volume)
    sound.play()

    pass

def draw():
    global SCREEN, MENU_TITLE_COLOR,menu_color_timer

    if currentGameState == 'ABOUT':
        SCREEN.fill(BLACK)

        SCREEN.blit(data_font.render('BACK',True, WHITE),(700,550))
        rect = Rect(BOX)

        pass


    elif currentGameState == 'MENU' :
        SCREEN.fill(BG_MENU)


        #changing menu title color

        if menu_color_timer >= FPS *0.3:
            MENU_TITLE_COLOR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            menu_color_timer = 0
        else:
            menu_color_timer += 1
        
        SCREEN.blit(cheqer_font.render(GAME_TITLE,True, MENU_TITLE_COLOR),(200,95))

        # for s in range (len(GAME_TITLE)):
        #     sz =  cheqer_font.size(GAME_TITLE[:s+1])

        startY = 215

        #draw square under label

        for i in range (len(menu_items)):
            bgRect =Rect([int(SCREEN_SIZE[0]*0.40),startY - 5,160,32])
            
            if bgRect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                pygame.draw.rect(SCREEN, DARK_BROWN, bgRect)

            SCREEN.blit(score_font1.render(menu_items[i],True, GREEN),(centerText(score_font1,menu_items[i],SCREEN_SIZE)[0],startY))
            startY += 50
      


    elif currentGameState == 'ACTIVE'  :

        SCREEN.fill(BG_COLOR)

        pygame.draw.rect(SCREEN, DARK_BROWN, [boardPt[0]-borderOffset, boardPt[1]-borderOffset,checkersWidth* noOfCheckers+borderOffset*2, checkersWidth* noOfCheckers+borderOffset*2],4)

        for row in range(noOfCheckers):
            for col in range(noOfCheckers):
                if isWhiteSpace(row,col):
                    pygame.draw.rect(SCREEN, BG_COLOR, [row*checkersWidth + boardPt[0], col*checkersWidth + boardPt[1],checkersWidth, checkersWidth])
                else:
                    pygame.draw.rect(SCREEN, DARK_BROWN, [row*checkersWidth + boardPt[0], col*checkersWidth + boardPt[1],checkersWidth, checkersWidth])
    


        for r in range (len(BOARD)):
           for c in range (len(BOARD[r])):

               if BOARD[r][c] != 0:
                  
                   if BOARD[r][c] % 2 == CPU % 2:
                       pygame.draw.ellipse(SCREEN, BLUE, [c*checkersWidth + boardPt[0] + marbleOffset, r*checkersWidth + boardPt[1] + marbleOffset, checkersWidth-10, checkersWidth-10])
                   elif BOARD[r][c] % 2 == PLY % 2:
                       pygame.draw.ellipse(SCREEN, GREEN, [c*checkersWidth + boardPt[0]+ marbleOffset, r*checkersWidth + boardPt[1]+ marbleOffset, checkersWidth-10, checkersWidth-10])         

                   if BOARD[r][c] == CPU_K or BOARD[r][c] == PLY_K:             #king
                       pygame.draw.ellipse(SCREEN, BLACK, [c*checkersWidth + boardPt[0] + marbleOffset, r*checkersWidth + boardPt[1] + marbleOffset, checkersWidth-10, checkersWidth-10],2)


        #show mouse location on board
        if pygame.mouse.get_pos()[0] >boardPt[0] and pygame.mouse.get_pos()[0] < (boardPt[0] + checkersWidth* noOfCheckers):
            if pygame.mouse.get_pos()[1] >boardPt[1] and pygame.mouse.get_pos()[1] < (boardPt[1] + checkersWidth* noOfCheckers):
                mX,mY = (pygame.mouse.get_pos()[0]-boardPt[0])/checkersWidth,(pygame.mouse.get_pos()[1]-boardPt[1])/checkersWidth  #row = y col = x
                #print(str(mX)+' ' +str(mY))

                if isValidSpace(mY,mX,currentPlayer) and  SM:
                    #if:
                        pygame.draw.rect(SCREEN, BLACK,[mX*checkersWidth + boardPt[0],mY*checkersWidth + boardPt[1],checkersWidth,checkersWidth],2)

    #elif currentGameState== 'EXIT'
       #rendering font
        SCREEN.blit(score_font.render('SCORE',True, BLACK),(score_positionX,30))
        SCREEN.blit(data_font.render('player: '+ str(PLY_SCORE),True, DARK_GREEN),(score_positionX,80))
        SCREEN.blit(data_font.render('cpu: '+ str(CPU_SCORE),True, BLUE),(score_positionX,110))

        #back btn

        pygame.draw.rect(SCREEN, BG_COLOR, BOX)
        SCREEN.blit(data_font.render('BACK',True, BLUE),(700,550))
        #SCREEN.blit(data_font.render('RESET',True, BLUE),(600,550))
        pass
    # elif currentGameState == 'SETTINGS':
    #     SCREEN.fill(BLACK)
    #     #SCREEN.blit(data_font.render('Music Volume:   ' + str(int(settings['volume'] * 10)),True, GREEN),(100,100))
    #
    #     SCREEN.blit(data_font.render('Music:   ' + 'Song.ogg',True, GREEN),(100,300))
    elif currentGameState == "Won_Screen":
        #SCREEN.fill(BLACK)

        pygame.draw.rect(SCREEN, DARK_GREEN, [SCREEN_SIZE[0]/2  - 200, 100,400, 300])


        if currentPlayer == CPU:        #cpu won
            SCREEN.blit(dialog_font_L.render('Sorry',True,GREEN),
                        (centerText(dialog_font_L,'Sorry',SCREEN_SIZE)[0],130))
            SCREEN.blit(dialog_font_L.render('You Lost',True,GREEN),
                        (centerText(dialog_font_L,'You Lost',SCREEN_SIZE)[0],190))
        else:                           #ply won
            SCREEN.blit(dialog_font_L.render('Congratulations',True,GREEN),
                    (centerText(dialog_font_L,'Congratulations',SCREEN_SIZE)[0],130))
            SCREEN.blit(dialog_font_L.render('You Won',True,GREEN),
                        (centerText(dialog_font_L,'You Won',SCREEN_SIZE)[0],190))




        startY = 280
        for i in range(len(dialog_items)):
            item_rect = Rect([320,startY-4,130,30])
            if item_rect.collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                pygame.draw.rect(SCREEN, DARK_BROWN, item_rect)
            SCREEN.blit(dialog_font_S.render(dialog_items[i],True,GREEN),(330,startY))
            startY += 35



    # elif currentGameState == 'SETTINGS':
    #     SCREEN.fill(BLACK)
    #     SCREEN.blit(data_font.render('Music Volume:   ' + str(int(settings['volume'] * 10)),True, GREEN),(100,100))
    #
    #     SCREEN.blit(data_font.render('Music:   ' + 'Song.ogg',True, GREEN),(100,300))

def update():
    global SM,SD, currentPlayer,PLY_SCORE,CPU_SCORE,TimeRunning,currentGameState

    if currentGameState == 'MENU' :

        pass

    elif currentGameState == 'ACTIVE' :

        #print(SM)
        if SM and SD:
           if  validMove(SM[0],SM[1],SD[0],SD[1]):
                item = move(SM,SD)

                #checking if jumped over opponent
                won = HasWon(currentPlayer)
                if item:
                    if item == CPU:
                        #increase PLY score
                        PLY_SCORE+=10
                        pass   
                    elif item == PLY:
                        #increase CPU score
                        CPU_SCORE += 10
                        pass  
                    elif item == CPU_K:
                        #increase PLY score
                        PLY_SCORE+=10
                        pass
                    elif item == PLY_K:
                        #increase CPU score
                        CPU_SCORE+=10
                        pass
                if won:
                    currentGameState = "Won_Screen"

                    if currentPlayer == PLY:
                        print 'you have won'
                    else:
                        print 'cpu has won'

                if not won:
                    if currentPlayer == PLY:
                        won = HasWon(currentPlayer)
                        currentPlayer = 'w'

                        #currentPlayer = CPU                        #debug

                    elif currentPlayer == CPU:
                        won = HasWon(currentPlayer)
                        currentPlayer = PLY



           else:
                SM,SD = None,None

        if  currentPlayer == 'w':
            #print 'TimeRunning = '+str(TimeRunning)
            if TimeRunning >= FPS*1:
                currentPlayer = CPU
                TimeRunning = 0
            else:
                TimeRunning += 1

        if currentPlayer == PLY:
       
            pass

        #cpu is playing
        if currentPlayer == CPU:
            cpu_move = getMove(BOARD, CPU, UP)      #AI gets most suitable move

            if cpu_move:    #if can move
                SM = cpu_move[FROM]
                SD = cpu_move[TO]
            else:       #if can not move
                currentPlayer == PLY

            print(cpu_move)

            #swaping player
            if not cpu_move:
                if currentPlayer == PLY:
                    currentPlayer = CPU
                else:
                    currentPlayer = PLY
            #if len(moves) > 0:
            #    #generate random number 
            #    rn = random.randint(0,len(moves) - 1)
            #    print('selected move index %s value %s' %(rn, moves[rn] ))
            #    selectedMove = moves[rn]
            #    SM = selectedMove[FROM]
            #    rn = random.randint(0, len(selectedMove[TO]) - 1)
            #    print('selected destinations index %s list %s ' %(rn, str(selectedMove[TO])))
            #    SD = selectedMove[TO][rn]
            #else:
            #    currentPlayer == PLY
            #pass
    elif currentGameState == "Won_Screen":
        if currentPlayer == PLY:
            dialog_items[0] = 'Play Again'
        elif currentPlayer == CPU:
            dialog_items[0] = 'Try Again'

def handelInput():
    #handeling input
    for event in pygame.event.get():
        if event.type == QUIT:
            print('exiting')
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            print('key down')
        elif event.type == KEYUP:
            print('key up')
        elif event.type == MOUSEBUTTONDOWN:
            mouseClickHandler(pygame.mouse.get_pos())
            pass
        pass

def mouseClickHandler(pos):
    global SM,SD, currentGameState, menu_items
   
    print(pos)
    rect = Rect(BOX)

    if currentGameState == 'ACTIVE':

        mX,mY = (pygame.mouse.get_pos()[0]-boardPt[0])/checkersWidth,(pygame.mouse.get_pos()[1]-boardPt[1])/checkersWidth  #row = y col = x
        print(str(mX)+' ' +str(mY))
        p = onBoard((mY,mX))


        if rect.collidepoint(pos):
            currentGameState = 'MENU'
            if menu_items[0] != 'CONTINUE':  #adding continue option to menu items
                menu_items = ['CONTINUE']+ menu_items
            print 'back'

        if p:
            #print('onboard')
            #if BOARD[p[0]][p[1]] == PLY:
            if currentPlayer == PLY:
                if BOARD[p[0]][p[1]] == PLY or BOARD[p[0]][p[1]] == PLY_K:
                    SD = None
                    SM = p
                    pass
                elif SM != None:
                    SD = p

            print('selected marble = ' + str(SM))
            print('selected destination = ' + str(SD))

    elif currentGameState == 'ABOUT':
        if rect.collidepoint(pos):
            currentGameState = 'MENU'

            print 'back'


    elif currentGameState == 'MENU':
            startY = 215
            for i in range (len(menu_items)):
                _rect =Rect([int(SCREEN_SIZE[0]*0.40),startY - 5,160,32]) #Rect(startY,centerText(score_font1,menu_items[i],SCREEN_SIZE)[0], score_font1.size(menu_items[i])[1],score_font1.size(menu_items[i])[0])
                if _rect.collidepoint((pos[0],pos[1])):
                    print menu_items[i]
                    if menu_items[i] =='NEW GAME':
                        currentGameState = 'ACTIVE'
                        resetBoard()
                    elif menu_items[i] =='SETTINGS':
                        currentGameState = 'SETTINGS'

                    elif menu_items[i] == 'EXIT':
                        #pygame.exit()
                        sys.exit()

                    elif menu_items[i]== 'CONTINUE':
                        currentGameState= 'ACTIVE'
                    elif menu_items[i] == 'ABOUT':
                        currentGameState ='ABOUT'

                startY+= 50 #+ score_font1.size(menu_items[i])[1]
            return None

    elif currentGameState == "Won_Screen":
        # for i in range (len(dialog_items)):
        #     startY = 270
        #     item_rect = Rect([320,startY-4,130,30])
        #     if item_rect.collidepoint(pos):
        #         print(dialog_items[i])
                # if i == 0:
                #     resetBoard()
                #     currentGameState = 'ACTIVE'
                # if i == 1:
                #     currentGameState = "MENU"

        startY = 280
        for i in range(len(dialog_items)):
            item_rect = Rect([320,startY-4,130,30])
            if item_rect.collidepoint(pos):
            #     pygame.draw.rect(SCREEN, DARK_BROWN, item_rect)
            # SCREEN.blit(score_font1.render(dialog_items[i],True,GREEN),(330,startY))
                if i == 0:
                    resetBoard()
                    currentGameState  = 'ACTIVE'
                elif i == 1:
                    currentGameState = 'MENU'
            startY += 35

def onBoard(pos):
    if pos[0] < noOfCheckers and pos[0] >= 0 and  pos[1] < noOfCheckers and pos[0] >= 0 and isWhiteSpace(pos[1],pos[0]):
        return pos
    else:
        return None

def resetBoard():
    global BOARD, PLY_SCORE, CPU_SCORE
    PLY_SCORE =0
    CPU_SCORE= 0
    for r in range (0,len(BOARD)):
        for c in range (len(BOARD[r])):
            if isWhiteSpace(r,c):
                if r < 4:
                     BOARD[r][c] = CPU
                elif r > 5:
                      BOARD[r][c] = PLY
                else:
                     BOARD[r][c] = 0
    
def printBoard(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            print board[r][c],
        print

def isWhiteSpace(r,c):
    return r%2 == c%2

def isValidSpace(r,c,player):
    return (BOARD[r][c] == player or BOARD[r][c] == 0) and isWhiteSpace(r,c)

#move marbles on the board
def move(oldPos, newPos):
    global BOARD,SM,SD,currentPlayer

    def dir(ps, pe):
        ''' returns 1 or -1 to show direction in which the perble moves '''
        return int((pe - ps)/ math.fabs(pe - ps))

    '''
    #canMove()
    if currentPlayer == PLY and BOARD[newPos[0]][newPos[1]]==0:
        BOARD[oldPos[0]][oldPos[1]] = 0
        BOARD[newPos[0]][newPos[1]] = PLY
        SM,SD = None,None
        #currentPlayer = CPU
        pass
    elif currentPlayer == CPU and BOARD[newPos[0]][newPos[1]]==0:
        BOARD[oldPos[0]][oldPos[1]] = 0
        BOARD[newPos[0]][newPos[1]] = CPU

    '''
    if BOARD[newPos[0]][newPos[1]]==0:

        temp = BOARD[oldPos[0]][oldPos[1]]
        BOARD[oldPos[0]][oldPos[1]] = 0
        BOARD[newPos[0]][newPos[1]] = temp#(BOARD[oldPos[0]][oldPos[1]]) % 2

        if newPos[0] == 0 and currentPlayer == PLY:
            BOARD[newPos[0]][newPos[1]] = currentPlayer+2
        elif newPos[0] == 9 and currentPlayer == CPU:
            BOARD[newPos[0]][newPos[1]] = currentPlayer+2

        #SM,SD = None,None
        if math.fabs(SM[0] - SD[0]) > 1:
            #find direction in which we are moving
            v = dir(SM[0],SD[0])
            h = dir(SM[1],SD[1])
            
            val = BOARD[SM[0]+v][SM[1]+h]
            #BOARD[SM[0]+v][SM[1]+h] = 0
            for i in range(int(math.fabs(SM[0]-SD[0])-1)):
              isempty = BOARD[SM[0] + (i+1)*v][SM[1] + (i+1)*h] == 0
              isking = BOARD[SM[0] + (i+1)*v][SM[1] + (i+1)*h] == currentPlayer+2
              iscurrentplayer = BOARD[SM[0] + (i+1)*v][SM[1] + (i+1)*h] == currentPlayer
              if not isempty :
                  val = BOARD[SM[0] + (i+1)*v][SM[1] + (i+1)*h]
                  BOARD[SM[0] + (i+1)*v][SM[1] + (i+1)*h] = 0
            return val
        #elif  BOARD[newPos[0]][newPos[1]] ==  currentPlayer+2:
              
         
        SM,SD = None,None
    else:
        pass
    
def canMove():
    if SM:
        if BOARD[SD[1]][SD[0]] == 0:  #destination empty
            diff = {'c':SD[0]-SM[0],'r':SD[1]-SM[1]}
            if currentPlayer == PLY:
                #checking vertical
                if diff['r'] < 0:                       #moving foward 

                    #for regualr marble
                    if BOARD[SM[1]][SM[0]] == PLY:
                        return diff['r'] == -1 and math.fabs(diff['c']) == 1

                    #checking horizontal
                        #return math.fabs(diff['c']) == math.fabs(diff['r'])
                                              
                    pass
                
                elif diff['r'] > 0:  
                    pass
                #if SD
                pass
            elif currentPlayer == CPU:
                return diff['r'] == 1 and math.fabs(diff['c']) == 1
                pass
            pass  

            pass
        else:
            return False
       
    else:
        return False

def validMove(s_row,s_col,d_row,d_col):
    global BOARD
    if BOARD[d_row][d_col] == 0 and isWhiteSpace(d_row,d_col):
        diff_cols = d_col - s_col
        diff_rows = d_row - s_row
        

        if math.fabs(diff_cols) == math.fabs(diff_rows):

            if BOARD[s_row][s_col] == PLY_K:
                unit_inc_r,unit_inc_c = int(math.fabs(diff_rows)/diff_rows), int(math.fabs(diff_cols)/diff_cols)

                count = []

                for i in range(diff_rows):
                    if BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != 0 and (BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != BOARD[s_row][s_col] or  BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != BOARD[s_row][s_col] + 2 ):
                        count.append((s_row + (i+1)*unit_inc_r,s_col + (i+1)*unit_inc_c))

                if len(count) == 0:          #if no obstacle between start and destination
                    return True

                elif len(count) == 1:        #if 1 enemy between start and destination
                    #BOARD[count[0][0]][count[0][1]] == 0
                    return True
                   
                else:
                    return False

                    return True
            elif BOARD[s_row][s_col] == CPU_K:
                return True
                #else:
                #    return False

            elif  math.fabs(diff_rows) == 1:                  #move
                if currentPlayer == PLY and diff_rows == AI.UP:
                    return True
                elif currentPlayer == CPU and diff_rows == AI.DOWN:
                    return True
                
            elif math.fabs(diff_rows) == 2:                 #jump
                #check if jumpOverPiece is enemy
                JOP = (s_row+diff_rows/2, s_col+diff_cols/2)
                print 'jump over ' + str(JOP)
                if BOARD[JOP[0]][JOP[1]] % 2 != BOARD[s_row][s_col] % 2:
                    return True
                else:
                    return False
            elif math.fabs(diff_cols) == math.fabs(diff_rows) and (BOARD[d_row][d_col] == CPU_K  or BOARD[d_row][d_col] == PLY_K):
                #if BOARD[d_row][d_col] == CPU_K:
                #    #check direction to 
                #    pass
                #elif BOARD[d_row][d_col] == PLY_K:
                #    pass
                
                #check path

                unit_inc_r,unit_inc_c = math.fabs(diff_rows)/diff_rows, math.fabs(diff_cols)/diff_cols

                count = []

                for i in range(diff_rows):
                    if BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != 0 and (BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != BOARD[s_row][s_col] or  BOARD[s_row + (i+1)*unit_inc_r][s_col + (i+1)*unit_inc_c] != BOARD[s_row][s_col] + 2 ):
                        count.append((s_row + (i+1)*unit_inc_r,s_col + (i+1)*unit_inc_c))

                if len(count) == 0:          #if no obstacle between start and destination
                    return True

                elif len(count) == 1:        #if 1 enemy between start and destination
                    #BOARD[count[0][0]][count[0][1]] == 0
                    return True
                   
                else:
                    return False


    return False

def HasWon(currentPlayer):

    #return true if current player has won else return false
    for r in range (0,len(BOARD)):
        for c in range (len(BOARD[r])):
            cv = BOARD[r][c]

            is_mine = (cv % 2) == (currentPlayer % 2)
            is_empty = cv == 0
            if not is_empty:
                if not is_mine:
                    return False

    return True

if __name__ == '__main__':


    init()
    main()