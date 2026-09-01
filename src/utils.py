"""Small shared utilities for the CSE437 air-quality notebooks."""

from pathlib import Path
import random

import numpy as np


RANDOM_SEED = 42


def get_project_paths(project_root=Path(".")):
    """Return the repository's standard directories as relative Path objects."""
    root = Path(project_root)
    return {
        "root": root,
        "raw": root / "data" / "raw",
        "processed": root / "data" / "processed",
        "models": root / "models",
        "figures": root / "figures",
        "report": root / "report",
    }


def ensure_output_directories(paths):
    """Create directories that notebooks are allowed to write to."""
    for name in ("processed", "models", "figures"):
        paths[name].mkdir(parents=True, exist_ok=True)


def set_random_seed(seed=RANDOM_SEED):
    """Seed Python and NumPy for reproducible notebook runs."""
    random.seed(seed)
    np.random.seed(seed)

