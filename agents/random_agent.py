import gym
import sys
from gym.wrappers import Monitor
import gym_desktop
from pyinstrument import Profiler

# sample and perform random actions
# source: 
# https://github.com/openai/gym/blob/master/examples/agents/random_agent.py

profiler = Profiler()
profiler.start()

class RandomAgent(object):
    """The world's simplest agent!"""
    def __init__(self, action_space):
        self.action_space = action_space

    def act(self, observation, reward, done):
        return self.action_space.sample()

if __name__ == '__main__':
    # Run Environment
    env = gym.make('Desktop-v0')
    outdir = '/tmp/random-agent-results'
    env = Monitor(env, directory=outdir, force=True)
    agent = RandomAgent(env.action_space)
    episode_count = 100
    reward = 0
    done = False
   
    for episode in range(episode_count):
        state = env.reset(debug=False, noShow=False)
        if episode >= episode_count:
            done = True
        while True:
            if done:
                break
            action = agent.act(state, reward, done)
            next_state, reward, done, _ = env.step(action)
            env.render()
            state = next_state

    # Stop Environment
    env.close()
    profiler.stop()

print(profiler.output_text(unicode=True, color=True))