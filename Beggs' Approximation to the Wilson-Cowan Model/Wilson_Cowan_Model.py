import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools
from tqdm import tqdm

###########################################################
random_activity = 0.001  # Spontaneous activity of each neuron
connect_distance = 2  # Max connectivity distance
dimensions = [50, 50]  # Grid dimensions
thres = 2  # Activity threshold of each neuron
refractory_period = 6  # Refractory period in time steps
time_steps = 300  # Number of time steps
###########################################################


class Neuron:
    def __init__(self, random_activity, connect_distance, thres, refractory_period, i, j, dimensions):
        self.random_activity = random_activity
        self.connect_distance = connect_distance
        self.thres = thres
        self.refractory_period = refractory_period
        self.activity = np.random.binomial(1, random_activity)
        self.refractory_time = 0  # Initialize refractory time
        self.x = [i, j]
        self.dimensions = dimensions

    def get_indices(self, x=None, connect_distance=None):
        if x is None:
            x = self.x
        if connect_distance is None:
            connect_distance = self.connect_distance

        direct_indices = []
        for a in range(1, int(connect_distance + 1)):
            if x[0] - a < 0 or x[0] + a >= self.dimensions[0]:
                continue
            direct_indices.append([x[0] - a, x[1]])
            direct_indices.append([x[0] + a, x[1]])

            if x[1] - a < 0 or x[1] + a >= self.dimensions[1]:
                continue
            direct_indices.append([x[0], x[1] - a])
            direct_indices.append([x[0], x[1] + a])

        indirect_indices = []
        if int(connect_distance) + 0.5 == connect_distance:
            dist = connect_distance
        else:
            dist = connect_distance - 1
            for b, c in itertools.product(range(1, int(dist + 1)), repeat=2):
                if x[0] - b < 0 and x[1] - b < 0 and x[0] - c < 0 and x[1] - c < 0:
                    continue
                if x[0] + b >= self.dimensions[0] or x[1] + b >= self.dimensions[1] or x[0] + c >= self.dimensions[0] or x[1] + c >= self.dimensions[1]:
                    continue
                indirect_indices.append([x[0] - b, x[1] - c])
                indirect_indices.append([x[0] - b, x[1] + c])
                indirect_indices.append([x[0] + b, x[1] - c])
                indirect_indices.append([x[0] + b, x[1] + c])

        all_indices = direct_indices + indirect_indices
        return all_indices

    def update_activity(self, activity_history):
        if self.refractory_time > 0:
            self.refractory_time -= 1  # Decrease refractory time
            self.activity = 0
        else:
            indices = self.get_indices()
            neighbor_activity = sum(activity_history[t - 1][x][y] for x, y in indices)
            if neighbor_activity >= self.thres:
                self.activity = 1
                self.refractory_time = self.refractory_period  # Set refractory time
            else:
                self.activity = np.random.binomial(1, self.random_activity)


# Create grid of neurons
grid = [[Neuron(random_activity, connect_distance, thres, refractory_period, i, j, dimensions) for j in range(dimensions[1])] for i in range(dimensions[0])]

# Simulation loop
activity_history = np.zeros((time_steps, dimensions[0], dimensions[1]))  # Store activity history
for t in tqdm(range(time_steps), desc='Simulating'):
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            neuron = grid[i][j]
            neuron.update_activity(activity_history)
            activity_history[t, i, j] = neuron.activity



# Visualization
fig, ax = plt.subplots(dpi=150)
im = ax.imshow(activity_history[0], cmap='binary', interpolation='nearest')
time_text = ax.text(0.5, 1.05, 'Time Step: 0', transform=ax.transAxes, ha="center")

def update(frame):
    im.set_array(activity_history[frame])
    time_text.set_text(f'Time Step: {frame}')
    return im, time_text

ani = animation.FuncAnimation(fig, update, frames=time_steps, interval=100, blit=True)

# Calculate total frames
total_frames = len(list(ani.new_frame_seq()))

# Save animation using PillowWriter
pillow_writer = animation.PillowWriter(fps=15)
with tqdm(total=total_frames, desc='Saving animation') as pbar:
    def update_progress(frame, total_frames=total_frames):
        pbar.update(1)
        
    ani.save(f'N_(backgr.={random_activity}, dist.={connect_distance}, thres.={thres}, refr. t={refractory_period}).gif', writer=pillow_writer, progress_callback=update_progress)
