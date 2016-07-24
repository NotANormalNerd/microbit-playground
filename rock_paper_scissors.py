from microbit import *
import radio
import random

radio.on()

MY_NUMBER = random.randrange(100000)
COMP_NUMBER = 0
MASTER = False

GAME_MESSAGE = 'lets_play'
GAME_ROUNDS = 10
GAME_CHOISES = ['ROCK', 'SCISSORS', 'PAPER']

def has_won(my_hand, game_hand):
    if my_hand == GAME_CHOISES[0] and game_hand == GAME_CHOISES[1]:
        return True
    if my_hand == GAME_CHOISES[1] and game_hand == GAME_CHOISES[2]:
        return True
    if my_hand == GAME_CHOISES[2] and game_hand == GAME_CHOISES[0]:
        return True
    return False

def battle_me():
    display.show(Image.YES)
    play_number = MY_NUMBER + COMP_NUMBER
    games_won = 0

    prepared_choises = [random.choice(GAME_CHOISES) for i in range(GAME_ROUNDS)]

    ctr = 1
    while True:
        radio.send("{pn} {ctr} {gc}".format(pn=str(play_number),
                                            ctr=ctr,
                                            gc=prepared_choises[ctr-1]))
        #display.scroll(str(ctr))
        sleep(100)
        received = radio.receive()
        if received and received.startswith(str(play_number)):
            #display.scroll(received)
            _, game_round, game_choice = received.split(" ")
            if int(game_round) != ctr:
                radio.send("{pn} {ctr} {gc}".format(pn=str(play_number),
                                                    ctr=game_round,
                                                    gc=prepared_choises[int(game_round) - 1]))
                continue
            if has_won(prepared_choises[int(game_round)-1], game_choice):
                games_won += 1
            ctr += 1

            if ctr >= GAME_ROUNDS:
                break

    while True:
        display.scroll(str(games_won))
        display.scroll(str(ctr))

def handshake():
    global COMP_NUMBER
    while True:
        if button_a.was_pressed():
            radio.send("".join((GAME_MESSAGE, str(MY_NUMBER))))

        listening = radio.receive()
        if listening and listening.startswith(GAME_MESSAGE):
            game_str = listening[len(GAME_MESSAGE):]

            if '+' in game_str:
                my_rec_number, comp_number = game_str.split('+')[:2]
                if MY_NUMBER == int(my_rec_number) and COMP_NUMBER == int(comp_number):
                    radio.send("{gm} {gn}+{mn}".format(gm=GAME_MESSAGE, mn=MY_NUMBER, gn=COMP_NUMBER))
                    display.show(Image.HEART)
                    sleep(1000)
                    break
            elif not COMP_NUMBER:
                COMP_NUMBER = int(game_str)
                radio.send("{gm} {gn}+{mn}".format(gm=GAME_MESSAGE, mn=MY_NUMBER, gn=COMP_NUMBER))


display.scroll("Ready")
handshake()
battle_me()

