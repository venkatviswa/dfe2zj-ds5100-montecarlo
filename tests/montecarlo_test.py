import unittest
import numpy as np
import pandas as pd

from Montecarlo.montecarlo import Die, Game, Analyzer


class DieTestCase(unittest.TestCase):

    def test_init(self):
        die=Die(np.array([1,2,3,4,5,6]))
        self.assertTrue(len(die.faces)==6)
    def test_change_weights(self):
        die = Die(np.array([1,2,3,4,5,6]))
        die.change_weights(3,0.5)
        self.assertTrue(die.current_state().loc[3,'weights']==0.5)
    def test_roll_die(self):
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        outcome=die.roll_die(3)
        self.assertTrue(len(outcome)==3)
    def test_current_state(self):
        die = Die(np.array([1, 2, 3, 4, 5, 6]))
        self.assertTrue(die.current_state is not None)

class GameTestCase(unittest.TestCase):
    def setUp(self):
        dieArray = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(dieArray)
        die1.change_weights(6, 5)
        die2 = Die(dieArray)
        die2.change_weights(6, 5)
        die3 = Die(dieArray)
        die3.change_weights(6, 5)
        self.list = [die1, die2, die3]
        self.g = Game(self.list)

    def test_init(self):
        dieArray = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(dieArray)
        die1.change_weights(6, 5)
        die2 = Die(dieArray)
        die2.change_weights(6, 5)
        die3 = Die(dieArray)
        die3.change_weights(6, 5)
        list = [die1, die2, die3]
        self.g = Game(self.list)
        self.assertEqual(len(self.g.diceList),len(list))

    def test_play(self):
        self.g.play(5)
        self.assertTrue(len(self.g.playdf.values.tolist())==5)

    def test_show_game_result(self):
        self.g.play(5)
        gamedef=self.g.show_game_result(format='wide')
        num_rows, num_cols = gamedef.shape
        self.assertEqual(num_rows, 5)
        self.assertEqual(num_cols, 3)

class AnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        dieArray = np.array([1, 2, 3, 4, 5, 6])
        die1 = Die(dieArray)
        die1.change_weights(6, 5)
        die2 = Die(dieArray)
        die2.change_weights(6, 5)
        die3 = Die(dieArray)
        die3.change_weights(6, 5)
        list = [die1, die2, die3]
        self.g = Game(list)
        self.g.play(10)

    def test_init(self):
        analyzer = Analyzer(self.g)
        self.assertIsNotNone(analyzer.game)
    def test_jackpot(self):
        analyzer = Analyzer(self.g)
        jackpotCount=analyzer.jackpot()
        self.assertTrue(jackpotCount>=0)

    def test_face_count_per_roll(self):
        analyzer = Analyzer(self.g)
        resultdf=analyzer.face_count_per_roll()
        num_rows, num_cols = resultdf.shape
        self.assertEqual(num_rows, 10)
        self.assertEqual(num_cols, 6)

    def test_combo_count(self):
        analyzer = Analyzer(self.g)
        resultdf=analyzer.combo_count()
        num_rows, num_cols = resultdf.shape
        self.assertEqual(num_rows, 10)
        self.assertEqual(num_cols, 2)

    def test_permutation_count(self):
        analyzer = Analyzer(self.g)
        resultdf=analyzer.permutation_count()
        self.assertIsNotNone(resultdf)



if __name__ == '__main__':
    unittest.main()
