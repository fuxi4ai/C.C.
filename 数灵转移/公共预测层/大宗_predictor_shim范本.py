"""大宗 src/core/predictor.py 的 repoint shim 范本。
本地副本退役，统一用公共引擎 guanxing_engine（需 Projects/_shared 在 PYTHONPATH）。"""
from guanxing_engine import (GuanxingPredictor, StargazerPredictor, PredictionResult,
                             load_samples_from_config, load_samples_from_file)
__all__ = ["GuanxingPredictor", "StargazerPredictor", "PredictionResult",
           "load_samples_from_config", "load_samples_from_file"]
