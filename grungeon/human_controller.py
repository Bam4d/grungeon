import os
from gym.utils import play

from griddly import GymWrapperFactory, gd, GymWrapper
# from griddly.RenderTools import VideoRecorder

# todo movement is right but the sprite rotation is wrong
# this seem to be based on pygame's event.key
from grungeon.map_rooms_grid import Map

KEYWORD_TO_KEY = {
    (ord('d'), ): [0, 1],
    (ord('w'),): [0, 2],
    (ord('a'),): [0, 3],
    (ord('s'),): [0, 4],
    (ord('e'),): [1, 1],
    (ord('r'),): [2, 1],
    (ord('1'),): [3, 1],
}

def callback(env):

    def _callback(prev_obs, obs, action, rew, env_done, info):

        #print(f"available actions = {env.game.get_available_actions(1)}")
        # recorder.add_frame(global_obs)

        #env.render(observer='global')
        if rew != 0:
            print(f'\nReward: {rew}')
        if env_done:
            print(f'Done!')

        if len(info) > 0:
            print(info)

    return _callback

if __name__ == '__main__':
    wrapper = GymWrapperFactory()
    name = 'grungeon_env'
    current_path = os.path.dirname(os.path.realpath(__file__))
    yaml_path = os.path.abspath('../gdy/grungeon.yaml')

    env = GymWrapper(yaml_path,
                     player_observer_type=gd.ObserverType.SPRITE_2D,
                     global_observer_type=gd.ObserverType.SPRITE_2D,
                     image_path='../assets_/',
                     shader_path='../shaders')

    print(env.game.get_object_names())

    world = Map(
        room_width=8,
        room_height=8,
        wall_width=1,
        num_rooms_horizontal=5,
        num_rooms_vertical=5
    )
    world.build()
    level_string = world.get_map()

    #env.reset(level_string=level_string)
    env.reset()

    play.play(env, callback=callback(env), fps=60, keys_to_action=KEYWORD_TO_KEY, zoom=1)
