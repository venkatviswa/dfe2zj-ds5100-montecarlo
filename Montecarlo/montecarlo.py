import numpy as np
import pandas as pd


class Die:
    '''Die has N sides or faces and W weights and can be rolled to select a face. Die with N = 2 is a coin and N = 6 is a standard die.
    Each dice has same number of sides and faces but can have its own weights. Each side has an equal number of weights.Each side has an unique symbol.
    Weight defaults to 1 for each side but can be changed afterr initialization. Die has one behavior which is to be rolled one or more times
    '''

    def __init__(self, faces):
        ''' initializer that takes a list of faces as input'''
        if not isinstance(faces, np.ndarray):
            raise TypeError('faces must be a numpy array')
        print(faces.dtype)
        if faces.dtype == 'int64' or faces.dtype =='str':
            self.faces = faces
        else:
            raise TypeError('Data type of array must be integer or string')


        if len(self.faces) != len(np.unique(self.faces)):
            raise ValueError('faces must have unique values')
        self.weights = [1.0 for i in faces]
        self.df = pd.DataFrame(data=self.weights, index=self.faces,columns=['weights'])

    def change_weights(self, face, new_weight):
        ''' method to change weights of one face to another '''
        if face not in self.faces:
            raise IndexError('face does not exist')
        try:
            self.df.loc[face,'weights'] = float(new_weight)
        except ValueError:
            raise TypeError('new_weight must be a float')

    def roll_die(self, times=1):
        '''method to roll the dice n number of times and returns a list of outcomes '''
        #print(list(self.df.sample(n=times,weights=self.weights,replace=True)))
        outcomeList = self.df.sample(n=times,weights=self.weights,replace=True).index.tolist()
        print('after rolling dice')
        print(outcomeList)
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
        if (len(diceList) ==0):
            raise ValueError('Atleast one or more dice must be specified')
        self.diceList=diceList

    '''-   The data frame should be in wide format, i.e. have the roll number
as a named index, columns for each die number (using its list index
as the column name), and the face rolled in that instance in each
cell.'''
    def play(self,numtimes):
        ''' takes an integer that indicates how many times dice should be rolled '''
        columns=['die'+str(i+1) for i in range(len(self.diceList)+1)]
        print(columns)
        self.playdf=pd.DataFrame(columns=columns,index=[],data=[] )
        self.playdf.index.name='rollnumber'
        print(self.diceList)
        for dieindex,die in enumerate(self.diceList):

            print('outcome is')
            print(die.current_state())
            print(die.roll_die(numtimes))
            outcomelist=die.roll_die(numtimes)
            print(outcomelist)
            for rollindex,outcome in enumerate(outcomelist):
                print('roll'+str(rollindex),'die'+str(dieindex),outcome)

                #self.playdf.loc['roll'+rollindex]={'die'+str(dieindex):outcome[int(rollindex)]}
    def show_game_result(self,format='wide'):

        if format == 'wide':
            return self.playdf
        elif format == 'narrow':
            narrowdf = self.playdf.copy()
            return self.narrowdf.reset_index().set_index('rollnumber','dicenumber')
        else:
            raise ValueError('format must be either wide or narrow')


class Analyzer:
    ''' An Analyzer object takes the results of a single game and computes
various descriptive statistical properties about it.'''
    def __init__(self, game):
        self.game=game
        if not isinstance(game, Game):
            raise ValueError('Not a game object')
    def jackpot(self):
        """A jackpot is a result in which all faces are the same, e.g. all ones
for a six-sided die.Computes how many times the game resulted in a jackpot.
Returns an integer for the number of jackpots.					"""

        playdf =self.game.show_game_result()
#        for i in list(playdf.index)


if __name__ == "__main__":
    dieArray=np.array([1,2,3,4,5,6])
    die1=Die(dieArray)
    #print(die1.roll_die(3))
    die1.change_weights(6,2)
    #print(die1.roll_die(3))
    die1.change_weights(5, 3)
    #print(die1.roll_die(3))
    die2=Die(dieArray)
    list=[die1,die2]
    g=Game(list)
    g.play(5)
    print(g.show_game_result(format='wide'))