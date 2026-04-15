import logging
import os
from datetime import datetime


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(
                f"logs/pedidoservice_{datetime.now().date()}.log", encoding="utf8"
            ),
            logging.StreamHandler(),
        ],
    )
