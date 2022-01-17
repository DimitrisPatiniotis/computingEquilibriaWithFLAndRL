# Computing Equilibria With Fictitious Play And Reinforcement Learning

## Table of contents
* [Games](#games)
* [Fictitious Play](#fictitious-play)
* [Reinforcement Learning](#reinforcement-learning)

## Games
The games used for the experiments are:
1. Odd Even
2. Attackers Defenders
3. Coordination Game

To open the html containing the matrix representation of a game run:

```
$ <browsername> <filename>
```

For example:

```
$ google-chrome matrix-attackers-deffenders.html
```

## Fictitious Play

Arguments expected (outcome only applies when testing Coordination game with Fictitious Play and takes as parameters 'fail' and 'succeed'): 

```
$ python3 compute_equilibria.py <algorithm> <game> <iterations> <outcome>
```

To test Fictitious Play with 10000 iterations for each game run:

```
$ python3 compute_equilibria.py fp oddeven 10000
$ python3 compute_equilibria.py fp attackersdefenders 10000
$ python3 compute_equilibria.py fp coordination 10000 fail
$ python3 compute_equilibria.py fp coordination 10000 succeed
```

## Reinforcement Learning

Same applies to Reinforcement Learning (in this case 'succeed' and 'fail' as the final parameters result in different starting policies)

To test Reinforcement Learning with 10000 iterations for each game run:

```
$ python3 compute_equilibria.py rl oddeven 10000
$ python3 compute_equilibria.py rl attackersdefenders 10000
$ python3 compute_equilibria.py rl coordination 10000 fail
$ python3 compute_equilibria.py rl coordination 10000 succeed
```
