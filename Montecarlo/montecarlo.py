import numpy as np
import pandas as pd
from itertools import groupby


class Die:
    '''Die has N sides or faces and W weights and can be rolled to select a face. Die with N = 2 is a coin and N = 6 is a standard die.
    Each dice has same number of sides and faces but can have its own weights. Each side has an equal number of weights.Each side has an unique symbol.
    Weight defaults to 1 for each side but can be changed afterr initialization. Die has one behavior which is to be rolled one or more times
    '''

    def __init__(self, faces):
        ''' initializer that takes a list of faces as input'''
        if not isinstance(faces, np.ndarray):
            raise TypeError('faces must be a numpy array')
        #print(faces.dtype)
        if faces.dtype == 'int64' or '<U' in faces.dtype.str:
            self.faces = faces
        else:
            raise TypeError('Data type of array must be integer or string')

        if len(self.faces) != len(np.unique(self.faces)):
            raise ValueError('faces must have unique values')
        self.weights = [1.0 for i in faces]
        self.df = pd.DataFrame(data=self.weights, index=self.faces, columns=['weights'])

    def change_weights(self, face, new_weight):
        ''' method to change weights of one face to another '''
        if face not in self.faces:
            raise IndexError('face does not exist')
        try:
            self.df.loc[face, 'weights'] = float(new_weight)
        except ValueError:
            raise TypeError('new_weight must be a float')

    def roll_die(self, times=1):
        '''method to roll the dice n number of times and returns a list of outcomes '''
        #print(list(self.df.sample(n=times,weights=self.weights,replace=True)))
        outcomeList = self.df.sample(n=times, weights=self.weights, replace=True).index.tolist()
        #print('after rolling dice')
        #print(outcomeList)
        return outcomeList

    def current_state(self):
        ''' returns the current state of the die'''
        return self.faces

    def __str__(self):
        return self.faces


class Game:
    ''' Represents a Game which consists of rolling one or more dice one or more times. Each die should have the same
     number of sides and faces but each die can have its own weights.'''

    def __init__(self, diceList):
        ''' initalizes a game by a list of dice '''
        if (len(diceList) == 0):
            raise ValueError('Atleast one or more dice must be specified')
        self.diceList = diceList

    '''-   The data frame should be in wide format, i.e. have the roll number
as a named index, columns for each die number (using its list index
as the column name), and the face rolled in that instance in each
cell.'''

    def play(self, numtimes):
        ''' takes an integer that indicates how many times dice should be rolled '''
        columns = ['die' + str(i + 1) for i in range(len(self.diceList))]
        #print(columns)
        self.playdf = pd.DataFrame(columns=columns, index=[], data=[])
        self.playdf.index.name = 'rollnumber'
        #print(self.diceList)
        for dieindex, die in enumerate(self.diceList):
            #print('die number ' + str(dieindex + 1))
            #print(die.current_state())
            #print(die.roll_die(numtimes))
            outcomelist = die.roll_die(numtimes)
            #print(outcomelist)
            for rollindex, outcome in enumerate(outcomelist):
                #print('roll' + str(rollindex + 1), 'die' + str(dieindex + 1), outcome)
                self.playdf.loc['roll' + str(rollindex + 1), 'die' + str(dieindex + 1)] = outcome

    def show_game_result(self, format='wide'):
        """This method just returns a copy of the private play data frame to the user.
           Takes a parameter to return the data frame in narrow or wide form which defaults to wide form.
           The narrow form will have a MultiIndex, comprising the roll number and the die number (in that order),
           and a single column with the outcomes (i.e. the face rolled).
          This method should raise a ValueError if the user passes an invalid option for narrow or wide"""

        if format == 'wide':
            return self.playdf
        elif format == 'narrow':
            narrowdf = self.playdf.copy()
            narrowdf = self.playdf.stack().to_frame('val')
            return narrowdf
        else:
            raise ValueError('format must be either wide or narrow')


class Analyzer:
    ''' An Analyzer object takes the results of a single game and computes
various descriptive statistical properties about it.'''

    def all_equal(self,iterable):
        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    def __init__(self, game):
        self.game = game
        if not isinstance(game, Game):
            raise ValueError('Not a game object')

    def jackpot(self):
        """A jackpot is a result in which all faces are the same, e.g. all ones
for a six-sided die.Computes how many times the game resulted in a jackpot.
Returns an integer for the number of jackpots.					"""

        gamedf = self.game.show_game_result(format='wide')
        jackpotCount=0
        #print('printing row by row')
        for  row in gamedf.values.tolist():
            #print(row)
            if self.all_equal(iter(row)):
                #print('jackpot row ' + str(row))
                jackpotCount+=1
            #else:
                #print('non jackpot row ' + str(row))
        return jackpotCount

    def face_count_per_roll(self):
        df2=self.game.show_game_result(format='narrow')
        #print('resetting index')
        df2.reset_index()
        #print('resetting index done')
        #print(df2.groupby("rollnumber").count())
        return df2.pivot_table(index="rollnumber",columns="val",aggfunc='size',fill_value=0)
        #return self.game.show_game_result('narrow').reset_index().set_index("rollnumber").pivot_table(values="rollnumber",columns=["val"],aggfunc=np.sum)
        '''Computes how many times a given face is rolled in each event.
           For example, if a roll of five dice has all sixes, then the counts for this roll would be   for the face value ‘6’ and   for the other faces.
           Returns a data frame of results.
           The data frame has an index of the roll number, face values as columns, and count values in the cells (i.e. it is in wide format)..'''

    def combo_count(self):
        '''A combo count method.
            Computes the distinct combinations of faces rolled, along with their counts.
            Combinations are order-independent and may contain repetitions.
            Returns a data frame of results.
            The data frame should have an MultiIndex of distinct combinations and a column for the associated counts.'''

        combo_copy=self.game.show_game_result().copy()
        combo_copy= combo_copy.reset_index().set_index(combo_copy.columns.tolist())
        print(combo_copy)
        combo_copy=combo_copy.groupby(combo_copy.columns.tolist()).count()
        #combo_copy.drop(['rollnumber'], axis=1)
        print(combo_copy)

    def permutation_count(self):
        '''An permutation count method.
            Computes the distinct permutations of faces rolled, along with their counts.
            Permutations are order-dependent and may contain repetitions.
            Returns a data frame of results.
            The data frame should have an MultiIndex of distinct permutations and a column for the associated counts'''


if __name__ == "__main__":

    #dieArray = np.array(['head', 'tail'])

    dieArray = np.array([1,2,3,4,5,6])
    die1 = Die(dieArray)
    #print(die1.roll_die(3))
    #die1.change_weights('head', 2)
    die1.change_weights(6, 5)
    #print(die1.roll_die(3))
    #print(die1.roll_die(3))
    die2 = Die(dieArray)
    die2.change_weights(6, 5)
    die3 = Die(dieArray)
    die3.change_weights(6, 5)
    list = [die1, die2, die3]
    print("Game starting with 3 dices and 10 rounds")
    g = Game(list)
    g.play(10)
    print("result in wide format")
    print(g.show_game_result(format='wide'))

    print("Result in narrow format")
    print(g.show_game_result(format='narrow'))

    analyzer = Analyzer(g)
    print("checking for jackpots")
    print(analyzer.jackpot())
    print("checking for face counts per roll")
    print(analyzer.face_count_per_roll())
    print("checking unique combinations")
    print(analyzer.combo_count())
