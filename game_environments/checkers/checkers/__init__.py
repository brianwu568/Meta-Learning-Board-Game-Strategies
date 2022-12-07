from gym.envs.registration import register

register(
    id='Checkers-v0',
    entry_point='checkers.envs:CheckersEnv',
)


