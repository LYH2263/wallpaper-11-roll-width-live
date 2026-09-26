from app.db import connect


def list_rolls():
    conn = connect()
    try:
        return [dict(r) for r in conn.execute("SELECT * FROM rolls ORDER BY id").fetchall()]
    finally:
        conn.close()


def get_roll(rid: int):
    conn = connect()
    try:
        row = conn.execute("SELECT * FROM rolls WHERE id=?", (rid,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def update_width(rid: int, width_m: float):
    conn = connect()
    try:
        conn.execute("UPDATE rolls SET width=? WHERE id=?", (width_m, rid))
        conn.commit()
    finally:
        conn.close()
