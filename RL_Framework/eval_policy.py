#!/usr/bin/env python3
import gym
import torch
from simulatorv2.SimAlphaGardenWrapper import SimAlphaGardenWrapper
from simulatorv2.plant_type import PlantType
from simulatorv2.sim_globals import NUM_IRR_ACTIONS, NUM_PLANTS, PERCENT_NON_PLANT_CENTERS
import simalphagarden
from net import Net
from constants import TrainingConstants
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

max_z = max(TrainingConstants.CC_IMG_DIMS[0], TrainingConstants.RAW_DIMS[0], TrainingConstants.GLOBAL_CC_DIMS[0])
max_x = max(TrainingConstants.CC_IMG_DIMS[1], TrainingConstants.RAW_DIMS[1], TrainingConstants.GLOBAL_CC_DIMS[1])
max_y = max(TrainingConstants.CC_IMG_DIMS[2], TrainingConstants.RAW_DIMS[2], TrainingConstants.GLOBAL_CC_DIMS[2])


def init_env(rows, cols, depth, sector_rows, sector_cols, prune_window_rows,
             prune_window_cols, action_low, action_high, obs_low, obs_high, garden_time_steps,
             garden_step, num_plant_types):
    env = gym.make(
        'simalphagarden-v0',
        wrapper_env=SimAlphaGardenWrapper(garden_time_steps, rows, cols, sector_rows,
                                          sector_cols, prune_window_rows, prune_window_cols,
                                          step=garden_step),
        garden_x=rows,
        garden_y=cols,
        garden_z=depth,
        sector_rows=sector_rows,
        sector_cols=sector_cols,
        action_low=action_low,
        action_high=action_high,
        obs_low=obs_low,
        obs_high=obs_high,
        num_plant_types=num_plant_types,
        eval=True
    )
    return env


def evaluate_policy(env, policy, steps):
    obs = env.reset()
    for i in range(steps):
        curr_img = env.get_curr_img()
        if curr_img is None:
            sector_img = np.ones((max_z, max_x, max_y)) * 255
        else:
            sector_img = np.transpose(curr_img, (2, 0, 1))
            sector_img = np.pad(sector_img, (
                (0, max_z - TrainingConstants.CC_IMG_DIMS[0]), (0, max_x - TrainingConstants.CC_IMG_DIMS[1]),
                (0, max_y - TrainingConstants.CC_IMG_DIMS[2])), 'constant')

        raw = obs[1][:, :, :-1]
        raw = np.pad(np.transpose(raw, (2, 0, 1)), (
            (0, max_z - TrainingConstants.RAW_DIMS[0]), (0, max_x - TrainingConstants.RAW_DIMS[1]),
            (0, max_y - TrainingConstants.RAW_DIMS[2])), 'constant')

        global_cc_vec = env.get_global_cc_vec()[:-1]
        global_cc_vec = np.pad(np.expand_dims(global_cc_vec, axis=2), (
            (0, max_z - TrainingConstants.GLOBAL_CC_DIMS[0]), (0, max_x - TrainingConstants.GLOBAL_CC_DIMS[1]),
            (0, max_y - TrainingConstants.GLOBAL_CC_DIMS[2])), 'constant')

        x = np.dstack((sector_img, raw, global_cc_vec))
        x = torch.from_numpy(np.expand_dims(x, axis=0))
        action = torch.argmax(policy(x)).item()
        obs, rewards, _, _ = env.step(action)
    coverage, diversity, water_use = env.get_metrics()
    print(coverage, diversity, water_use)
    fig, ax = plt.subplots()
    plt.plot(coverage, label='coverage')
    plt.plot(diversity, label='diversity')
    plt.legend()
    plt.savefig('coverage_and_diversity.png', bbox_inches='tight', pad_inches=0.02)
    plt.clf()
    plt.plot(water_use, label='water use')
    plt.legend()
    plt.savefig('water_use.png', bbox_inches='tight', pad_inches=0.02)
    plt.close()

if __name__ == '__main__':
    rows = 150
    cols = 300
    num_plant_types = PlantType().num_plant_types
    depth = num_plant_types + 3  # +1 for 'earth' type, +1 for water, +1 for health
    sector_rows = 15
    sector_cols = 30
    prune_window_rows = 5
    prune_window_cols = 5
    garden_step = 1

    action_low = 0
    action_high = 1
    obs_low = 0
    obs_high = rows * cols

    garden_days = 10
    sector_obs_per_day = int(NUM_PLANTS + PERCENT_NON_PLANT_CENTERS * NUM_PLANTS)
    collection_time_steps = sector_obs_per_day * garden_days  # 210 sectors observed/garden_day * 200 garden_days
    water_threshold = 0.6

    moments = np.load('save/moments.npz')
    input_cc_mean, input_cc_std = moments['input_cc_mean'], moments['input_cc_std']
    input_raw_mean, input_raw_std = (moments['input_raw_vec_mean'], moments['input_raw_mean']), (
        moments['input_raw_vec_std'], moments['input_raw_std'])

    policy = Net(input_cc_mean, input_cc_std, input_raw_mean, input_raw_std)
    policy.load_state_dict(torch.load('save/net.pth', map_location=torch.device('cpu')))
    policy.eval()

    evaluate_policy(
        init_env(rows, cols, depth, sector_rows, sector_cols, prune_window_rows, prune_window_cols, action_low,
                 action_high, obs_low, obs_high, collection_time_steps, garden_step, num_plant_types),
        policy, collection_time_steps)
