from random import random, choices
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import sys


odd_even_player_1_payoff = np.array([
            [1, -1],
            [-1, 1]
        ])
attackers_defenders_player_1_payoff = np.array([
            [-2, 3],
            [3, -4]
        ])
coordination_player_1_payoff = np.array([
            [1, -1],
            [-1, 1]
        ])

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
        pay_matrix_player_1 = odd_even_player_1_payoff
        game_type = 'zero_sum'
    elif sys.argv[2] == 'attackersdefenders':
        pay_matrix_player_1 = attackers_defenders_player_1_payoff
        game_type = 'zero_sum'
    elif sys.argv[2] == 'coordination':
        if sys.argv[4]:
            pay_matrix_player_1 = coordination_player_1_payoff
            game_type = 'coordination'
        else:
            print('Please choose a valid input')
            print('Please choose \'fail\' or \'succeed\'')
    else:
        print('Please choose a valid input')
        print('Odd Even: oddeven')
        print('Attackers Defenders: attackersdefenders')

    # Setting starting values
    if game_type == 'zero_sum':
        pay_one = np.array([0 , 0.5])
        pay_two = np.array([0.5, 0])
    elif sys.argv[4] == 'fail':
        pay_one = np.array([0 , 0.5])
        pay_two = np.array([0.5, 0])
    elif sys.argv[4] == 'succeed':
        pay_one = np.array([0 , 0.5])
        pay_two = np.array([0, 0.5])

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
        if game_type == 'zero_sum':
            if player == 1:
                return get_same(matrix)
            elif player == 2:
                return get_dif(matrix)
        elif game_type == 'coordination':
            return get_same(matrix)

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
        
        if game_type == 'zero_sum':
            if payoff1 < 0:
                payoff2 = abs(payoff1)
            else:
                payoff2 = 0 - payoff1
        elif game_type == 'coordination':
            payoff2 = payoff1

        totalpayoff1 += payoff1
        totalpayoff2 += payoff2
        if i>0:
            play1average.append(np.average(player1play))
            play2average.append(np.average(player2play))
        
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

    # Players final stats
    print('After {} iterations we get:'.format(iteration))
    print('Column player strategy:')
    print(str(player1strategy) + '\nTotal column player payoff:\n' + str(totalpayoff1))
    print('Row player strategy:')
    print(str(player2strategy) + '\nTotal row player payoff:\n' + str(totalpayoff2))

    x = np.arange(0, (iteration-1), 1)
    if sys.argv[2] == 'oddeven':
        plt.title('Odd Even with Fictitious Play')
    elif sys.argv[2] == 'attackersdefenders':
        plt.title('Attackers Defenders with Fictitious Play')
    elif sys.argv[2] == 'coordination':
        plt.title('Coordination with Fictitious Play {}'.format(sys.argv[4]))
    plt.xlabel("Iterations")
    plt.ylabel("Relative move frequency")
    plt.plot(x, play1average, label='Column Player')
    plt.plot(x, play2average, label='Row Player')
    plt.legend()
    plt.show()



def reinforcement_learning():
    try:
        iteration = int(sys.argv[3])
        if iteration <= 0:
            print('Iteration nubmer is invalid, setting it to 10.000 (default)')
            iteration = 10000
    except:
        print('Iteration nubmer is invalid, setting it to 10.000 (default)')
        iteration = 10000

    if sys.argv[2] == 'oddeven':
        pay_matrix_player_1 = odd_even_player_1_payoff
        game_type = 'zero_sum'
    elif sys.argv[2] == 'attackersdefenders':
        pay_matrix_player_1 = attackers_defenders_player_1_payoff
        game_type = 'zero_sum'
    elif sys.argv[2] == 'coordination':
        pay_matrix_player_1 = coordination_player_1_payoff
        game_type = 'coordination'
    else:
        print('Please choose a valid input')
        print('Odd Even: oddeven')
        print('Attackers Defenders: attackersdefenders')
    
    if game_type == 'zero_sum':
        pay_one = np.array([0.1, 0.9])
        pay_two = np.array([0.1, 0.9])
    elif sys.argv[4] == 'fail':
        pay_one = np.array([ 0.1, 0.9])
        pay_two = np.array([0.9, 0.1])
    elif sys.argv[4] == 'succeed':
        pay_one = np.array([0.1 , 0.9])
        pay_two = np.array([0.1, 0.9])

    moves = np.array([0,1])
    #Init Values PLAYER1
    valueQ_p1 = np.array([[1,1],[1,1]])
    valueV_p1 = 1.0
    valueP_p1 = pay_one
    #Init Values PLAYER2
    valueQ_p2 = np.array([[1.0,1.0],[1.0,1.0]])
    valueV_p2 = 1.0
    valueP_p2 = pay_two

    def Reward(action1,action2, player):
        player1reward = pay_matrix_player_1[action1][action2]
        if game_type == 'zero_sum':
            if player == 1:
                return player1reward
            elif player == 2:
                if player1reward < 0:
                    return(abs(player1reward))
                else:
                    return 0-player1reward
        elif game_type == 'coordination':
            return player1reward

    def chooseMove(moves,weights):
        # choose between two moves via weights
        return choices(moves,weights,k=1)[0]

    def updateQvalues(alpha, reward, move,moveOp, player):
        if player == 1:
            return (1-alpha)*valueQ_p1[move][moveOp] + alpha*move
        elif player == 2:
            return (1-alpha)*valueQ_p2[move][moveOp] + alpha*move

    def solveLinearProgram(Q):
        c = np.array([[0.0,0.0,1.0]])
        b_ub = np.array([0.0,0.0])
        b_eq = np.array([1.0])
        A_eq = np.array([[1.0,1.0,0.0]])
        bounds = [(0.0,1.0), (0.0,1.0), (-1.0, 1.0)]

        #Inequality constrain matrix
        A_ub = []
        A_ub.append([Q[0][0], Q[1][0], 1])
        A_ub.append([Q[0][1], Q[1][1], 1])

        result = linprog(c,A_ub,b_ub,A_eq,b_eq,bounds)

        if result.success:
            return result.x[0],result.x[1]
        else:
            print('Linear Program Fail')           

    def choose_random_or_policy(valueP):
        if random() > exploration:
            return valueP
        else:
            return np.array([0.5,0.5])

    def computeValue(policy,Q, player):
        if player == 1:
            move1 = policy[0]*Q[0][0] + policy[1]*Q[1][0]
            move2 = policy[0]*Q[0][1] + policy[1]*Q[1][1]
            return min(move1,move2)
        elif player == 2:
            move1 = policy[0]*Q[0][0] + policy[1]*Q[1][0]
            move2 = policy[0]*Q[0][1] + policy[1]*Q[1][1]
            return max(move1,move2)

    alpha = 1
    exploration = 0.5
    decay = 0.95

    player1play =[]
    player2play =[]
    play1average =[]
    play2average = []
    totalpayoff1 = 0
    totalpayoff2 = 0

    for i in range(iteration):

        # Next move randomness
        weights1 = choose_random_or_policy(valueP_p1)
        weights2 = choose_random_or_policy(valueP_p2)

        # Get Player Move
        move_p1 = chooseMove(moves,weights1)  
        move_p2 = chooseMove(moves,weights2)

        player1play.append(move_p1)
        player2play.append(move_p2)
        if i>0:
            play1average.append(np.average(player1play))
            play2average.append(np.average(player2play))

        # Getting last move reward
        rewardp1 = Reward(move_p1,move_p2, player = 1)
        rewardp2 = Reward(move_p2,move_p1,  player = 2)

        totalpayoff1 += rewardp1
        totalpayoff2 += rewardp2

        # Updating Q values
        valueQ_p1[move_p1][move_p2] = updateQvalues(alpha,rewardp1,move_p1,move_p2, player = 1)
        valueQ_p2[move_p2][move_p1] = updateQvalues(alpha,rewardp1,move_p2,move_p1, player = 2)

        # Player Q values
        player1_Qvalues = [valueQ_p1[0][0], valueQ_p1[1][0], valueQ_p1[0][1], valueQ_p1[1][1]]
        player2_Qvalues = [valueQ_p2[0][0], valueQ_p2[1][0], valueQ_p2[0][1], valueQ_p2[1][1]]

        # Policy Iteration
        valueP_p1[0], valueP_p1[1] = solveLinearProgram(valueQ_p1)
        valueP_p2[0], valueP_p2[1] = solveLinearProgram(valueQ_p2)

        # Game Value
        value_game_p1 = computeValue(valueP_p1,valueQ_p1, 1)
        value_game_p2 = computeValue(valueP_p2,valueQ_p2, 2)

        # Updating alpha
        alpha = alpha*decay

    # Displaying Results
    print(value_game_p1)
    print(value_game_p2)
    player1strategy = valueP_p1
    player2strategy = valueP_p2
    print('After {} iterations we get:'.format(iteration))
    print('Column player strategy:')
    print(str(player1strategy) + '\nTotal column player payoff:\n' + str(totalpayoff1))
    print('Row player strategy:')
    print(str(player2strategy) + '\nTotal row player payoff:\n' + str(totalpayoff2))
    x = np.arange(0, (iteration-1), 1)
    if sys.argv[2] == 'oddeven':
        plt.title('Odd Even with Reinforcement Learning')
    elif sys.argv[2] == 'attackersdefenders':
        plt.title('Attackers Defenders with Reinforcement Learning')
    elif sys.argv[2] == 'coordination':
        plt.title('Coordination with Reinforcement Learning')
    plt.xlabel("Iterations")
    plt.ylabel("Relative move frequency")
    plt.plot(x, play1average, label='Column Player')
    plt.plot(x, play2average, label='Row Player')
    plt.legend()
    plt.show()


def main():
    if sys.argv[1] == 'fp':
        if sys.argv[2] == 'coordination':
            try:
                if sys.argv[4] == 'fail' or sys.argv[4] == 'succeed':
                    fictitious_play()
                else:
                    print('Please choose \'fail\' or \'succeed\' for your coordination game')
            except:
                print('Please choose \'fail\' or \'succeed\' for your coordination game')
        else:
            fictitious_play()
    elif sys.argv[1] == 'rl':
        reinforcement_learning()
    else:
        print('Invalid input')
        print('Arguments expected: <algorithm> <game> <iterations> <outcome>')
        print('Algorithms: \nFictitious Play \'fp\'\nReinforcement Learning \'rl\'')
        print('Game: \nOdd Even: oddeven\nattackersdefenders')
        print('If you choose coordination as a final argument choose \'fail\' or \'succeed\'')


if __name__ == "__main__":
    main()