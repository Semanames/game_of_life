import numpy as np
import matplotlib. pyplot as plt
from matplotlib import animation


class Life:

    def __init__(self, array):
        self.array = array
        fig, ax = plt.subplots()
        self.figure = fig
        self.axis = ax

    def __iter__(self):
        return self

    def __next__(self):
        self.life_iteration()

    def life_iteration(self):

        field = np.zeros([self.array.shape[0] + 2, self.array.shape[1] + 2])
        field[1:-1, 1:-1] = self.array

        decision_field = (field[:-2, 1:-1] + field[2:, 1:-1] + field[1:-1, :-2] + field[1:-1, 2:] +
                          field[:-2, :-2] + field[2:, 2:] + field[:-2, 2:] + field[2:, :-2])

        underpopulation = decision_field < 2
        overpopulation = decision_field > 3
        new_generation = decision_field == 3

        self.array *= ~underpopulation
        self.array *= ~overpopulation
        self.array += (new_generation * (~(self.array == 1)) * 1)

    def create_animation(self, animation_path, frames, interval, dpi, fps):

        def init():
            self.axis.imshow(self.array, cmap='Greys_r', interpolation='nearest')
            return self.figure,

        def animate(_):
            next(self)
            self.axis.imshow(self.array, cmap='Greys_r', interpolation='nearest')
            return self.figure,

        anim = animation.FuncAnimation(self.figure,
                                       animate,
                                       frames=frames,
                                       init_func=init,
                                       interval=interval,
                                       blit=True)

        anim.save(animation_path, dpi=dpi, fps=fps, extra_args=['-vcodec', 'libx264'])
