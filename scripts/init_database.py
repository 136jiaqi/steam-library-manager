import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from auth.authentication import initialize_database
initialize_database(); print("数据库初始化完成。")
