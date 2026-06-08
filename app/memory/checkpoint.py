from pathlib import Path
import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver

from app.config import CHECKPOINT_DB_PATH

_checkpointer = None


def get_checkpointer() -> SqliteSaver:
    global _checkpointer
    if _checkpointer is None:
        db_path = Path(CHECKPOINT_DB_PATH)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(db_path), check_same_thread=False)
        _checkpointer = SqliteSaver(connection)
    return _checkpointer


def delete_thread_checkpoint(thread_id: str) -> None:
    get_checkpointer().delete_thread(thread_id)
