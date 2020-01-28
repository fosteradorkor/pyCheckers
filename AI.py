'''
6/15/2015:
    this AI module has to paly checkers with a human player
    BASIC CONCEPT
        the AI should evaluate all posible moves and select the one which 
        would give the heighest  score     
'''

import math, random

UP,DOWN = -1,1
TOP,BOT,LFT,RGT = 1,2,3,4
_row,_col = 'row','col'
FROM, TO = 'from','to'

#returns the move that gives the highest score point
#@return a tuple of tuple (from,to) 
#from =(,), to=(,)
def getNextMove(board,player,direction=DOWN):
     for row in range(len(board)):
        for col in range(len(board[row])):
            enemies = None
            if board[row][col] == player:
               focusedMarble = {_row:row,_col:col}
               surrounding = getSurrounding(board,focusedMarble[_row],col,player) 

               for s in surrounding:
                    if s==None:
                        pass
                    if (board[s[0]][s[1]] % 2)!=(player % 2): # if enemy

                        pass

                    elif board[s[0]][s[1]] == 0: #if empty space
                        pass

                    pass

               #evaluate all enemies and check if can win

            print board[row][col],
        print

'''
return all enemies surrounding the specific marble
'''
def getSurrounding(board,row,col,ply):
   _ene = []
   v = ply % 2

   _temp = [getMarble(board,row,col,TOP,RGT),getMarble(board,row,col,TOP,LFT),getMarble(board,row,col,BOT,RGT),getMarble(board,row,col,BOT,LFT)]


   for t in _temp:
       if t:
           _ene.append(t)

   return _ene
   ##tr
   #mbl = getMarble(board,row,col,t,r)
   #if mbl and board[mbl[0]][mbl[1]] % 2 != v :
   #    _ene.append(mbl)
   ##tl
   #mbl = getMarble(board,row,col,t,l)
   #if mbl and board[mbl[0]][mbl[1]] % 2 != v:
   #    _ene.append(mbl)
   ##br
   #mbl = getMarble(board,row,col,b,r)
   #if mbl and board[mbl[0]][mbl[1]] % 2 != v:
   #    _ene.append(mbl)
   ##bl
   #mbl = getMarble(board,row,col,b,l)
   #if mbl and board[mbl[0]][mbl[1]] % 2 != v:
   #    _ene.append(mbl)
    
    
def getMarble(board,r,c,p1,p2):

    if p1==TOP:
        r -= 1
    if p1==BOT:
        r += 1
    if p2 == LFT:
        c -= 1
    if p2==RGT:
        c += 1
    
    if r<0 or c<0 or r>=len(board) or c>=len(board):
        return None
    else:
        return (r,c)

#returns the number of takedowns , 0 if no takedowns and -1 if cannot move
#dictionary format {nextmove, takedowns}
# def getAllPossibleMoves(board,focusedMarble):
#     moves=[]
#     takedown=[]
#     surrounding = getSurrounding(board,focusedMarble[_row],focusedMarble[_col],player)
#     for s in surrounding:
#         if s==None:
#             pass
#         elif (board[s[0]][s[1]] % 2)!=(player % 2): # if enemy
#             #try jump
#
#             pass
#
#         elif board[s[0]][s[1]] == 0: #if empty space
#             #move
#             moves.append[s]
#             pass
#
#         pass
#
#     return {'takedowns':takedown, 'moves':moves}
#get the possible move of a specific marble

def getMove(board,piece, direction):
    possibleMoves = getAllLegalMoves(board, piece, direction)

    print len(possibleMoves), ' possible moves'
    print possibleMoves

    if len(possibleMoves) > 0:
        jumpMoves = []
        validMoves = []



        for i in possibleMoves:
            #getting best move for regular marble
            _from  = i[FROM]
            if board[i[FROM][0]][i[FROM][1]] == piece:

                for j in i[TO]:
                   if math.fabs(_from[0] - j[0]) == 2:
                       jumpMoves.append({FROM:_from, TO: j})
                   else:
                       validMoves.append({FROM:_from, TO: j})

            else:

                # if len(i[TO]['win_jump']) > 0:
                #     # jumpMoves[TO] += i[TO]['win_jump']
                #     jumpMoves.append({FROM:_from, TO: i[TO]['win_jump']})
                #     pass

                for t in i[TO]['win_jump']:
                    jumpMoves.append({FROM:_from, TO: t})

                vms = i[TO]['valid_jump']
                for t in i[TO]['valid_jump']:
                    validMoves.append({FROM:_from, TO: t})

                #elif len(i[TO]['valid_jump']) > 0:
                #     validMoves.append({FROM:_from, TO: i[TO]['valid_jump']})

                pass
                
        if len(jumpMoves)>0:
            #TODO:: win jump for king marble fix
            return jumpMoves[random.randint(0,len(jumpMoves)-1)]
        else:
            # possibleMoves[random.randint(0,len(possibleMoves)-1)]
            rn = random.randint(0,len(validMoves) - 1)
            # f = possibleMoves[rn]
            # t = None
            # if board[f[FROM][0]][f[FROM][1]] == piece + 2:
            # rn = random.randint(0, len(f[TO]) - 1)
            # t = f[TO][rn]
            # else:
            #     rn = random.randint(0, len(f[TO]['valid_jump']) - 1)
            #     t = f[TO]['valid_jump'][rn]
            # return {FROM:f[FROM],TO:t}
            return (validMoves[rn])
    else:
        return None
    pass

#returns a list of all for a player in the game legal moves 
def checkKingMove(board, found_enemy, ncol, nrow, piece, valid_jump, win_jump):
    # if board[nrow][ncol] == 0 and found_enemy == True:  # empty space behind enemy
    #     win_jump.append((nrow, ncol))
    #     return True
    #     pass
    #
    # elif ((board[nrow][ncol] != piece or board[nrow][ncol] != piece + 2) or board[nrow][ncol] != 0) and found_enemy == False :  # enemy found
    #     return True
    #     pass
    #
    # elif found_enemy == False and ((board[nrow][ncol] != piece or board[nrow][ncol] != piece + 2)):
    #     pass
    #
    # elif board[nrow][ncol] != 0 and found_enemy:  # obstacle found
    #     return  None
    #     pass
    #
    # elif board[nrow][ncol] == 0 and found_enemy == False:  # just an empty space
    #     valid_jump.append((nrow, ncol))
    #     return False
    #     pass

    if found_enemy:
        #everything found here is found behind enemy
        if board[nrow][ncol] == 0:  # just an empty space
            win_jump.append((nrow, ncol))
            return True
            pass
        else:
            return None

    else:
        if board[nrow][ncol] == 0:  # just an empty space
            valid_jump.append((nrow, ncol))
            return False
            pass

        elif board[nrow][ncol] == piece or board[nrow][ncol] == piece + 2: #obstacle  - pal
            return  None

        elif   board[nrow][ncol] != piece or board[nrow][ncol] != piece + 2:    #found enemy
            return  True


    pass

def getAllLegalMoves(board, piece, direction):
    moves=[]
    mySur = []
    for row in range(len(board)):
        for col in range(len(board[row])):

            if board[row][col]  == piece:                               #found regualr piece
                sur = getSurrounding(board, row, col, piece)

                print('Debug :: AI analyzing row %s col %s' % (row, col))

                ret = {}
                ls=[]
                ret.update({FROM:(row,col)})
                for s in sur:   

                    pi = board[s[0]][s[1]]
                    if pi == 0:                                         #empty space
                        if row-s[0] == direction: 
                            ls.append(s)

                    elif (pi % 2) != (piece % 2):                           #enemy
                        #check if can jump
                        ld = getDiagonalMarble(row,col,s[0],s[1])

                        if ld and board[ld[0]][ld[1]]==0:
                            ls.append(ld)                      

                        pass

                ret.update({TO:ls})
                
                if len(ls) > 0:
                    mySur.append(ret)
                ls = []

            if board[row][col]  == piece + 2:               #found king piece

                ret = {}
                ls=[]
                ret.update({FROM:(row,col)})

                #get everything to the top left of king
                tl = min(row,col) + 1
                #get everything to the top right of king
                bl = min(len(board)-row-1,col) + 1
                #get everything to the bottom left of king
                tr = min(row,len(board[0])-col-1) + 1
                #get everything to the bottom right of king
                br = min(len(board)-row-1,len(board[0])-col-1) + 1

                #top left
                found_enemy = False
                win_jump = []
                valid_jump = []

                for i in range (1,tl):
                    # if board[row - i][col - i] != piece or board[row - i][col - i] != piece + 2 or board[row - i][col - 1] != piece

                    nrow = row - i
                    ncol = col - i

                    found_enemy = checkKingMove(board, found_enemy, ncol, nrow, piece, valid_jump, win_jump)
                    if found_enemy == None:
                        break
                #top right
                found_enemy = False
                for i in range (1,tr):
                    nrow = row - i
                    ncol = col + i

                    found_enemy = checkKingMove(board, found_enemy, ncol, nrow, piece, valid_jump, win_jump)
                    if found_enemy == None:
                        break

                    pass

                #bottom left
                found_enemy = False
                for i in range (1,bl):
                    nrow = row + i
                    ncol = col - i

                    found_enemy = checkKingMove(board, found_enemy, ncol, nrow, piece, valid_jump, win_jump)
                    if found_enemy == None:
                        break

                    pass

                #bottom right
                found_enemy = False
                for i in range (1,br):
                    nrow = row + i
                    ncol = col + i

                    found_enemy = checkKingMove(board, found_enemy, ncol, nrow, piece, valid_jump, win_jump)
                    if found_enemy == None:
                        break

                    pass

                if len(win_jump) > 0 or len(valid_jump) > 0:
                    mySur.append({FROM:(row,col), TO:{'win_jump':win_jump,'valid_jump':valid_jump}})

                pass

    return mySur
    pass

def getDiagonalMarble(s_row,s_col, d_row,d_col):
    
    ret = (d_row*2 - s_row,d_col*2 - s_col)

    if ret[0] < 0 or ret[1] < 0 or ret[0] >= 10 or ret[1] >= 10:
        return None

    return ret

    pass