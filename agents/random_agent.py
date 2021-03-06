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
    try:
        # Run Environment
        env = gym.make('Desktop-v0', steplimit=100, debug=False, show=True)
        outdir = '/tmp/random-agent-results'
        env = Monitor(env, directory=outdir, force=True)
        agent = RandomAgent(env.action_space)
        episodes = 10
    
        for episode in range(episodes):
            state = env.reset()
            reward = 0
            done = False
            print('episode:' , episode)
            while True:
                if done is True:
                    break
                action = agent.act(state, reward, done)
                next_state, reward, done, _ = env.step(action)
                env.render()
                state = next_state
            print('reward:', reward)
    except ConnectionRefusedError:
        print('FAILED: Unable to Connect. Try running in debug mode.')
    except:
        print ("FAILED: Unexpected error:", sys.exc_info()[0])
        raise        
    finally:    
        env.close()
        profiler.stop()

print(profiler.output_text(unicode=True, color=True))