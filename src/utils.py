"""Shared utilities for the CSE437 air-quality notebooks."""

from pathlib import Path
import random

import numpy as np


RANDOM_SEED = 42


def get_project_paths(project_root=Path("."), storage_root=None):
    """Return repository paths plus persistent data/model storage paths."""
    root = Path(project_root)
    storage = Path(storage_root) if storage_root is not None else root

    return {
        "root": root,
        "raw": storage / "raw" if storage != root else root / "data" / "raw",
        "processed": storage / "processed" if storage != root else root / "data" / "processed",
        "models": storage / "models" if storage != root else root / "models",
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
