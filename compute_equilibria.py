import numpy as np
import matplotlib.pyplot as plt
import sys

def main():
    try:
        if sys.argv[1] == 'fl':
            fictitious_play()
        if sys.argv[1] == 'rl':
            reinforcement_learning()
    except:
        print('Invalid input')
        print('Arguments expected: <algorithm> <game> <iterations>')
        print('Algorithms: \nFictitious Play \'fl\'\nReinforcement Learning \'rl\'')
        print('Game: \nOdd Even: oddeven\nattackersdefenders')

def fictitious_play():
    try:
        iteration = int(sys.argv[3])
        if iteration <= 0:
            print('Iteration nubmer is invalid, setting it to 10.000 (default)')
            iteration = 10000
    except:
        print('Iteration nubmer is invalid, setting it to 10.000 (default)')
        iteration = 10000

    if sys.argv[2] == 'oddeven':
        pay_matrix_player_1 = np.array([
            [1, -1],
            [-1, 1]
        ])
    elif sys.argv[2] == 'attackersdefenders':
        pay_matrix_player_1 = np.array([
            [-2, 3],
            [3, -4]
        ])
    else:
        print('Please choose a valid input')
        print('Odd Even: oddeven')
        print('Attackers Defenders: attackersdefenders')

    # Setting starting values
    pay_one = np.array([1 , 0])
    pay_two = np.array([0, 1])

    # Getting max payof move when havving
    def get_same(matrix):
        if matrix[0] >= matrix[1]:
            return 0
        else:
            return 1

    def get_dif(matrix):
        if matrix[0] >= matrix[1]:
            return 1
        else:
            return 0

    def take_action(matrix, player):
        if player == 1:
            return get_same(matrix)
        elif player == 2:
            return get_dif(matrix)

    player1play =[]
    player2play =[]
    play1average =[]
    play2average = []
    totalpayoff1 = 0
    totalpayoff2 = 0

    for i in range(iteration):
        action_one = take_action(pay_one, 1)
        action_two = take_action(pay_two, 2)
        payoff1 = pay_matrix_player_1[action_one,action_two]

        if payoff1 < 0:
            payoff2 = abs(payoff1)
        else:
            payoff2 = 0 - payoff1
        totalpayoff1 += payoff1
        totalpayoff2 += payoff2
        if i>0:
            play1average.append(np.average(player1play))
            play2average.append(np.average(player2play))
        # print(payoff1, payoff2)
        # print('Column player matrix: ' + str(pay_one) + ' so action taken ' +  str(action_one) + ' with eventual payoff ' + str(payoff1))
        # print('Row player matrix: ' + str(pay_two) + ' so action taken ' +  str(action_two) + ' with eventual payoff ' + str(payoff2) + '\n')
        
        pay_one[action_two] += 1
        pay_two[action_one] += 1
        player1play.append(action_one)
        player2play.append(action_two)


    player1strategy = []
    player2strategy = []
    rateof0 = player1play.count(0) / (len(player1play))
    rateof1 = player1play.count(1) / (len(player1play))
    player1strategy.append(rateof0)
    player1strategy.append(rateof1)
    rateof0 = player2play.count(0) / (len(player2play))
    rateof1 = player2play.count(1) / (len(player2play))
    player2strategy.append(rateof0)
    player2strategy.append(rateof1)

    x = np.arange(0, (iteration-1), 1)
    if sys.argv[2] == 'oddeven':
        plt.title('Odd Even with Fictitious Play')
    elif sys.argv[2] == 'attackersdefenders':
        plt.title('Attackers Defenders with Fictitious Play')
    plt.xlabel("Iterations")
    plt.ylabel("Relative move frequencey")
    plt.plot(x, play1average, label='Column Player')
    plt.plot(x, play2average, label='Row Player')
    plt.legend()
    plt.show()

    # Players final stats
    print('After {} iterations we get:'.format(iteration))
    print('Column player')
    print(player1strategy, totalpayoff1)
    print('Row player')
    print(player2strategy, totalpayoff2)

def reinforcement_learning():
    print('Reinforcement Learning Not Yet Available')

if __name__ == "__main__":
    main()