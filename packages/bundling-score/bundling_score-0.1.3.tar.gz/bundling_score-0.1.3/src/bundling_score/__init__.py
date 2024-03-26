"""
Copyright (c) 2023 Ghislain de Labbey. All rights reserved.

bundling_score: Compute bundling score
"""


from __future__ import annotations

# read version from installed package
from importlib.metadata import version

__version__ = version(__name__)

__all__ = ("__version__",)
