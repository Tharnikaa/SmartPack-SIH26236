"""
SmartPack Model Loader
Loads and caches the trained Random Forest model bundle.
"""

import os
import joblib
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ModelLoader:
    def __init__(self, model_path: str = "models/packaging_suitability_model.pkl"):
        self.model_path = model_path
        self._bundle = None
        self._last_mtime = 0.0

    def reload(self) -> Optional[Dict[str, Any]]:
        self._bundle = None
        return self.get_bundle()

    def get_bundle(self) -> Optional[Dict[str, Any]]:
        # Find absolute path if needed
        path = self.model_path
        if not os.path.exists(path) and os.path.exists(os.path.join("..", path)):
            path = os.path.join("..", path)

        if not os.path.exists(path):
            return None

        current_mtime = os.path.getmtime(path)
        if self._bundle is not None and current_mtime == self._last_mtime:
            return self._bundle

        try:
            self._bundle = joblib.load(path)
            self._last_mtime = current_mtime
            logger.info(f"Loaded trained ML model bundle from {path}")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self._bundle = None
        return self._bundle

model_loader = ModelLoader()
