import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

# 卷材幅宽（厘米）允许写入的上限；可被 settings 表中的 max_width_cm 覆盖
MAX_ROLL_WIDTH_CM = float(os.environ.get("MAX_ROLL_WIDTH_CM", "150"))
