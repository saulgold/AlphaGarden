import numpy as np
from simulatorv2.plant import Plant
from simulatorv2.plant_presets import PLANT_TYPES
from simulatorv2.sim_globals import NUM_PLANTS, NUM_PLANT_TYPES_USED

class PlantType:
    def __init__(self):
        self.plant_names = list(PLANT_TYPES.keys())
        self.plant_types = list(PLANT_TYPES.items())
        self.num_plant_types = len(PLANT_TYPES)
        self.plant_centers = []
        self.non_plant_centers = []
        self.plant_in_bounds = 0

    def get_random_plants(self, seed, rows, cols, sector_rows, sector_cols):
        self.plant_in_bounds = 0
        self.plant_centers = []
        self.non_plant_centers = []
        
        np.random.seed(seed)
        plants = []
        sector_rows_half = sector_rows // 2
        sector_cols_half = sector_cols // 2
        
        def in_bounds(r, c):
            return r > sector_rows_half and r < rows - sector_rows_half and c > sector_cols_half and c < cols - sector_cols_half
        
        coords = [(r, c) for c in range(cols) for r in range(rows)]
        np.random.shuffle(coords)
        # If using a subset of the plant types defined in plant_presets.py, uncomment and modify the two lines below.
        # self.plant_types = self.plant_types[:]
        # self.num_plant_types = NUM_PLANT_TYPES_USED
        for _ in range(NUM_PLANTS):
            name, plant = self.plant_types[np.random.randint(0, self.num_plant_types)]
            coord = coords.pop(0)
            r, c = coord[0], coord[1]
            plants.extend([Plant(r, c, c1=plant['c1'], growth_time=plant['growth_time'],
                                    color=plant['color'], plant_type=name, stopping_color=plant['stopping_color'], color_step=plant['color_step'])])
            self.plant_in_bounds += 1
            self.plant_centers.append(tuple((r, c)))
        self.non_plant_centers = [c for c in coords if in_bounds(c[0], c[1])]

        return plants


    def get_same_plants(self, seed, rows, cols, sector_rows, sector_cols):
        self.plant_in_bounds = 0
        self.plant_centers = []
        self.non_plant_centers = []
        
        np.random.seed(seed)
        plants = []
        sector_rows_half = sector_rows // 2
        sector_cols_half = sector_cols // 2
        
        def in_bounds(r, c):
            return r > sector_rows_half and r < rows - sector_rows_half and c > sector_cols_half and c < cols - sector_cols_half
        
        coords = [(r, c) for c in range(cols) for r in range(rows)]
        np.random.shuffle(coords)
        idx = np.random.randint(0, self.num_plant_types)
        for i in range(NUM_PLANTS):
            name, plant = self.plant_types[idx]
            coord = coords.pop(0)
            r, c = coord[0], coord[1]
            plants.extend([Plant(r, c, c1=plant['c1'], growth_time=plant['growth_time'],
                                    color=plant['color'], plant_type=name, stopping_color=plant['stopping_color'], color_step=plant['color_step'])])
            self.plant_in_bounds += 1
            self.plant_centers.append(tuple((r, c)))
        self.non_plant_centers = [c for c in coords if in_bounds(c[0], c[1])]
        return plants

    def get_diff_num_plants(self, seed, rows, cols, sector_rows, sector_cols):
        self.plant_in_bounds = 0
        self.plant_centers = []
        self.non_plant_centers = []
        
        np.random.seed(seed)
        plants = []
        sector_rows_half = sector_rows // 2
        sector_cols_half = sector_cols // 2
        
        def in_bounds(r, c):
            return r > sector_rows_half and r < rows - sector_rows_half and c > sector_cols_half and c < cols - sector_cols_half
        
        coords = [(r, c) for c in range(cols) for r in range(rows)]
        np.random.shuffle(coords)

        curr_num = 1
        checksum = 0
        for plant_type in self.plant_types:
            name, plant = plant_type
            for _ in range(curr_num):
                coord = coords.pop(0)
                r, c = coord[0], coord[1]
                plants.extend([Plant(r, c, c1=plant['c1'], growth_time=plant['growth_time'],
                                        color=plant['color'], plant_type=name, stopping_color=plant['stopping_color'], color_step=plant['color_step'])])
                self.plant_in_bounds += 1
                self.plant_centers.append(tuple((r, c)))

            checksum += curr_num
            curr_num += 1

        assert checksum == NUM_PLANTS

        self.non_plant_centers = [c for c in coords if in_bounds(c[0], c[1])]
        return plants

    def get_plants_with_invasive_species(self, seed, rows, cols, sector_rows, sector_cols):
        self.plant_in_bounds = 0
        self.plant_centers = []
        self.non_plant_centers = []
        
        np.random.seed(seed)
        plants = []
        sector_rows_half = sector_rows // 2
        sector_cols_half = sector_cols // 2
        
        def in_bounds(r, c):
            return r > sector_rows_half and r < rows - sector_rows_half and c > sector_cols_half and c < cols - sector_cols_half
        
        coords = [(r, c) for c in range(cols) for r in range(rows)]
        np.random.shuffle(coords)
        num_invasive = np.random.randint(0, NUM_PLANTS)

        # plant invasive plantss
        for i in range(num_invasive):
            name, plant = self.plant_types[0]
            coord = coords.pop(0)
            r, c = coord[0], coord[1]
            plants.extend([Plant(r, c, c1=plant['c1'], growth_time=plant['growth_time'],
                                    color=plant['color'], plant_type=name, stopping_color=plant['stopping_color'], color_step=plant['color_step'])])
            self.plant_in_bounds += 1
            self.plant_centers.append(tuple((r, c)))

        for i in range(NUM_PLANTS - num_invasive):
            name, plant = self.plant_types[np.random.randint(1, self.num_plant_types)]  # random plant type excluding invasive
            coord = coords.pop(0)
            r, c = coord[0], coord[1]
            plants.extend([Plant(r, c, c1=plant['c1'], growth_time=plant['growth_time'],
                                    color=plant['color'], plant_type=name, stopping_color=plant['stopping_color'], color_step=plant['color_step'])])
            self.plant_in_bounds += 1
            self.plant_centers.append(tuple((r, c)))
        self.non_plant_centers = [c for c in coords if in_bounds(c[0], c[1])]
        return plants