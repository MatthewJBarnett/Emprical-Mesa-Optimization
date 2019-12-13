import Environment.envs.Gridworld
#import Agent
import time
import Utilities
import tensorflow as tf

import gym
from stable_baselines.common.policies import MlpPolicy, CnnPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO1

env = gym.make('CK-v0')

# Custom MLP policy of two layers of size 1024 each with relu activation function
policy_kwargs = dict(act_fun=tf.nn.relu, net_arch=[1024, 1024])

model = PPO1("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=0, tensorboard_log=".")
print("Training")
model.learn(total_timesteps=20e6)
model.save("MLP3")

del model

model = PPO1.load("MLP3")
total_reward = 0
obs = env.reset(True)
for j in range(100):
	for i in range(35):
		action, states = model.predict(obs)
		#print(action)
		obs, rewards, dones, info = env.step(action)
		env.draw()
		total_reward += rewards
		time.sleep(0.25)
	env.reset(True)
print(total_reward / 100.0)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# This generates training data right now
# Later I'll make a specialized function for it
'''
for i in range(12000):
	print(i)
	world = Gridworld.ChestsAndKeys((5, 5), 4, 2, drawing = False)
	agent = Agent.HeuristicAgent(world.state())
	trajectory = agent.trajectory(world.state())
	state = world.state()
	for action in trajectory:
		Utilities.write_state_action(state, action, "training.dat")
		state, reward = world.take_action(action)
		if world.item_count(3) < 1:
			break
'''
'''
# This currently gets samples from 'training.dat' and trains a neural network to predict labels
from sklearn.model_selection import train_test_split
import numpy as np

samples = Utilities.get_samples_from("training.dat", (5, 5))

points = [Gridworld.ChestsAndKeys.embed(sample[0]) for sample in samples]
X = np.array(points)
y = np.array([label[1] for label in samples])

X = X.reshape(X.shape[0],X.shape[1],X.shape[2],1)
b = np.zeros((y.shape[0], 5))
b[np.arange(y.shape[0]), y] = 1
y = b

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

ConvNet = NeuralNetwork.Convolutional(num_filters=100, filter_dimensions=(3,3), input_shape=(20,5,1), pooling_shape=(2,2), dense_shape=512, num_categories=5)

print(X_train.shape)
print(y_train.shape)
ConvNet.train(X_train, y_train)
ConvNet.save("model.h5")

#print(ConvNet.predict(X_test[0:10]), y_test[0:10])

world = Gridworld.ChestsAndKeys((5, 5), 2, 3, drawing = True)
agent = Agent.NeuralNetAgent(world.state(), ConvNet)
state = world.state()
while True:
	time.sleep(1)
	state, reward = world.take_action(Gridworld.Direction.get_direction_from_number(agent.action(state)))
	world.draw()
'''
