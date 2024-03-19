This simple neural network model was described by John M. Beggs (2022): "The Cortex and the Critical Point Understanding the Power of Emergence". The MIT Press, pp. 35-42. https://doi.org/10.7551/mitpress/13588.001.0001.

It is a simple, digital approximation with the following characteristics:

- Neurons are arranged in a 2D grid.
- Neurons can either be active (1) or inactive (0).
- The maximal connectivity distance determines the number of neighbors that contribute to synaptic inputs.
- A neuron's activity at time t=i depends on the summed activity of its neighbors at time t=i–1.
- This sum must reach a specific threshold to result in the respective neuron being active.
- A refractory period determines the number of time steps needed for neurons to become excitable again.

Some parameters restrict activity (inhibitory) whereas others promote activity (excitatory). Each combination of parameters can result in one of the following "phases" of activity:

- Ordered activity: Periodic, repetitive patterns of activity.
- Complex activity: Intermittent pulse-like phases of activity. The narrow zone where this behavior can occur can be referred to as the phase transition zone.
- Unordered activity: Solely random background activity.