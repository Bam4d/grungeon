import os
from gym.utils import play

from griddly import GymWrapperFactory, gd, GymWrapper
# from griddly.RenderTools import VideoRecorder

# todo movement is right but the sprite rotation is wrong
# this seem to be based on pygame's event.key
KEYWORD_TO_KEY = {
    (ord('d'), ): [0, 1],
    (ord('w'),): [0, 2],
    (ord('a'),): [0, 3],
    (ord('s'),): [0, 4],
    (ord('e'),): [1, 1],
    (ord(' '),): [2, 1]
}

def callback(env):

    initial_global_obs = env.render(observer=0, mode="rgb_array")
    observation_shape = initial_global_obs.shape

    # recorder = VideoRecorder()
    # recorder.start("human_player_video_test.mp4", observation_shape)

    def _callback(prev_obs, obs, action, rew, env_done, info):

        global_obs = env.render(observer=0, mode="rgb_array")
        print(f"available actions = {env.game.get_available_actions(1)}")
        # recorder.add_frame(global_obs)
        if rew != 0:
            print(f'\nReward: {rew}')
        if env_done:
            print(f'Done!')

        if len(info) > 0:
            print(info)

    return _callback

if __name__ == '__main__':
    wrapper = GymWrapperFactory()
    name = 'stochasticity_env'
    current_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.abspath('../gdy/grungeon.yaml')

    env = GymWrapper(yaml_path,
                     player_observer_type=gd.ObserverType.SPRITE_2D,
                     global_observer_type=gd.ObserverType.SPRITE_2D,
                     image_path='../assets_/',
                     level=0)

    env.reset()
    global_visualization = env.render(observer='global', mode='rgb_array')

    play.play(env, callback=callback(env), fps=10, keys_to_action=KEYWORD_TO_KEY, zoom=1)
