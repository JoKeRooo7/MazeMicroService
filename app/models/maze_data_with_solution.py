import numpy as np
from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass
class MazeDataWithSolution:
    rows: Optional[int] = None
    cols: Optional[int] = None
    right_walls: Optional[np.ndarray] = None
    lower_walls: Optional[np.ndarray] = None
    start_point: Tuple[int, int] = None
    end_point: Tuple[int, int] = None 
    solution_coordinates: List[Tuple[int, int]] = None
    step: Optional[int] = 0 
