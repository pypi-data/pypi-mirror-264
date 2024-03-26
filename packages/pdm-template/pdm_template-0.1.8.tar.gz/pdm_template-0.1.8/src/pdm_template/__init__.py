import os
import logging
import logging.handlers


logger = logging.getLogger("pdm_copier_logger")
logger.setLevel(os.environ.get("LOGLEVEL", "INFO").upper())
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
