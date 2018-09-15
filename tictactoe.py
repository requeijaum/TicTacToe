import time
import os
import textwrap


def full():
    if ' ' not in score:
        print('\nThe game has resulted into a catgame. ( ͡° ͜ʖ ͡°)')
        return True


def board_display(score):
    print(' '+score[6], '|', score[7], '|', score[8])
    print('---+---+---')
    print(' '+score[3], '|', score[4], '|', score[5])
    print('---+---+---')
    print(' '+score[0], '|', score[1], '|', score[2])


def check(char, posi1, posi2, posi3):
    if score[posi1] == char and score[posi2] == char and score[posi3] == char:
        return True


def checkall(char):
    if check(char, 0, 1, 2):
        return True
    if check(char, 3, 4, 5):
        return True
    if check(char, 6, 7, 8):
        return True
    if check(char, 0, 3, 6):
        return True
    if check(char, 1, 4, 7):
        return True
    if check(char, 2, 5, 8):
        return True
    if check(char, 0, 4, 8):
        return True
    if check(char, 2, 4, 6):
        return True
    return False


# print('Tic Tac Toe\n'.center(70))
banner = r'''
              _____  _  ____     _____  ____  ____     _____  ____  _____
             /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/
               / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \
               | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_
               \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\ '''

print(banner)
print('\nThe board is numbered in the form of the numpad keyboard as printed below.\n')
time.sleep(0.01)
score = ['1', '2', '3',
         '4', '5', '6',
         '7', '8', '9']

board_display(score)

value = 'The object of Tic Tac Toe is to get three in a row. You play on a three by three game board. The first player is known as X and the second is O. Players alternate placing Xs and Os on the game board until either opponent has three in a row or all nine squares are filled. X always goes first, and in the event that no one has three in a row, the stalemate is called a cat game.'
wrapper = textwrap.TextWrapper(width=72)
string = wrapper.fill(text=value)
print('\n', string)

print('\nChoose your cells accordingly.The game will begin in 10 seconds.')
time.sleep(10)

while True:
    score = [' ']*9
    while True:
        os.system('clear')
        board_display(score)
        if full():
            break
        while True:
            try:
                player1 = int(input('\nPlayer X, choose your position: '))
                if score[player1-1] != 'X' and score[player1-1] != 'O':
                    score[player1-1] = 'X'
                    break
                else:
                    print('\nThis position is already taken, please try again.')
                    continue
            except:
                print('\nKindly enter a valid value')
                continue
        os.system('clear')
        board_display(score)
        if checkall('X'):
            print('\nPlayer X is the winner')
            time.sleep(0.1)
            break
        if full():
            break
        while True:
            try:
                player2 = int(input('\nPlayer O, choose your position: '))
                if score[player2-1] != 'X' and score[player2-1] != 'O':
                    score[player2-1] = 'O'
                    break
                else:
                    print('\nThis position is already taken, please try again.')
                    continue
            except:
                print('\nKindly enter a valid value')
                continue
        os.system('clear')
        board_display(score)
        if checkall('O'):
            print('\nPlayer O is the winner')
            time.sleep(0.1)
            break
        if full():
            break
    again = input('\nDo you want to play again? Enter Yes or No: ')
    if again.lower() == 'yes':
        continue
    elif again.lower() == 'no':
        print()
        print('Thanks for playing TIC TAC TOE, do come again!!'.center(80))
        print('\nExiting in 3..')
        time.sleep(1)
        print('           2..')
        time.sleep(1)
        print('           1..')
        time.sleep(1)
        break
    else:
        print('\nEnter a correct choice')
