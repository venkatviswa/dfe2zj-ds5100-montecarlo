import numpy as np
import pandas as pd


class Die:
    def __init__(self, faces):
        if not isinstance(faces, np.ndarray):
            raise TypeError('faces must be a numpy array')
        self.faces = faces

        if len(self.faces) != len(np.unique(self.faces)):
            raise ValueError('faces must have unique values')
        self.weights = [1.0 for i in faces]
        self.df = pd.DataFrame(data=self.weights, index=self.faces)

    def change_weights(self, face, new_weight):
        if face not in self.faces:
            raise IndexError('face does not exist')
        try:
            self.df.loc[face] = float(new_weight)
        except ValueError:
            raise ValueError('new_weight must be a float')

    def roll_dice(self, times=1):
        return self.df.sample(times)

    def current_state(self):
        return self.df
