from dataclasses import dataclass


@dataclass
class ArgonEntity:
    timeCost: int
    memoryCostLow: int
    memoryCostHigh: int
    parallelism: int
    randomLow: int
    randomHigh: int