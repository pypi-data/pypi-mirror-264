from stable_baselines3 import PPO
import robohive
from robohive.utils.import_utils import import_gym; gym = import_gym()
env = gym.make('myoElbowPose1D6MRandom-v0')
model = PPO("MlpPolicy", env, verbose=0)
print("========================================")
print("Starting policy learning")
print("========================================")
