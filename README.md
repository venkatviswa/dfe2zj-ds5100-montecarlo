ReadMe

Metadata
This project implements a MonteCarlo Simulation in Python.All Python classes and associated test classes are available in the repository. 
The core classes used to implement the functionality are Game,Die and Analyzer
Montecarlo : This direcrtory has the classes that implement the simulation
test : This directory has the test classes

Synopsis
Die : Create an instance of a Die by passing the list of faces. NUmber of faces could be 2 for a coin , 6 for dice and so on.
example :         
        dieArray = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(dieArray)
Game : Create a instance of Game by passing one or more die
example: list = [die1, die2, die3]
         g = Game(list)
Analyzer: Create an instance of Analyzer class by passing an instance of Game that was played 
example : analyzer = Analyzer(g)

API Info

Class Die 
Methods : __init__(faces) , Change_Weights(faces,new_weight), roll_dice(times) , current_state()

Class Game
Methods: __init__(dielist),play(numtimes),show_game_result(format)

Class Analyzer
Methods:__init__(game),jackpot(),face_count_per_roll(),combo_count(),permutation_count()
