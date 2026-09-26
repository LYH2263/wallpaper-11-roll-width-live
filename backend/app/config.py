import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("DATA_DIR", Path(__file__).resolve().parent.parent / "data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

# 卷材幅宽写入上限（厘米），可由环境变量覆盖
MAX_ROLL_WIDTH_CM = float(os.environ.get("MAX_ROLL_WIDTH_CM", "200"))
