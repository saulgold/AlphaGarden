import numpy as np
from simulatorv2.sim_globals import MAX_WATER_LEVEL, PRUNE_DELAY, PRUNE_THRESHOLD, PRUNE_RATE

def plant_in_area(plants, r, c, w, h, plant_idx):
    return np.any(plants[r:r+w,c:c+h,plant_idx])

def calc_potential_entropy(global_cc_vec, plants, sector_rows, sector_cols, prune_window_rows,
                           prune_window_cols, prune_rate):
    prune_window_cc = {}
    for i in range(1, len(global_cc_vec)):
        # Get cc for plants in prune sector
        if plant_in_area(plants, (sector_rows - prune_window_rows) // 2, (sector_cols - prune_window_cols) // 2, prune_window_rows, prune_window_cols, i):
            prune_window_cc[i] = prune_window_cc.get(i, 0) + 1

    for plant_id in prune_window_cc.keys():
        prune_window_cc[plant_id] = prune_window_cc[plant_id] * prune_rate
        global_cc_vec[plant_id] -= prune_window_cc[plant_id] 
    
    prob = global_cc_vec[1:] / np.sum(global_cc_vec[1:])
    prob = prob[np.where(prob > 0)]
    entropy = -np.sum(prob * np.log(prob))
    return entropy
    
def policy(timestep, state, global_cc_vec, sector_rows, sector_cols, prune_window_rows,
           prune_window_cols, step, water_threshold, num_irr_actions, sector_obs_per_day):
    plants_and_water = state[1][0]
    plants = plants_and_water[:,:,:-1]
    water_grid = plants_and_water[:,:,-1]
    
    # Prune
    if timestep > PRUNE_DELAY * sector_obs_per_day:
        prob = global_cc_vec[1:] / np.sum(global_cc_vec[1:]) # We start from 1 because we don't include earth in diversity
        prob = prob[np.where(prob > 0)]
        curr_entropy = -np.sum(prob * np.log(prob))
        future_entropy = calc_potential_entropy(global_cc_vec, plants, sector_rows, sector_cols,
                                                prune_window_rows, prune_window_cols, PRUNE_RATE)
        if future_entropy > curr_entropy:
            return [2]
    
    # Irrigate
    sector_water = np.sum(water_grid)
    maximum_water_potential = sector_rows * sector_cols * MAX_WATER_LEVEL * step * water_threshold
    if sector_water < maximum_water_potential:
        irr_policy = 0
        while sector_water < maximum_water_potential:
             irr_policy += 1
             sector_water += maximum_water_potential / num_irr_actions
        return [irr_policy]
    
    # No action
    return [0]
