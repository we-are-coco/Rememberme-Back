from sqlalchemy import inspect

def row_to_dict(row) -> dict:
    """Convert a SQLAlchemy row to a dictionary."""
    if not row:
        return {}
    return {key: getattr(row, key, None) for key in inspect(row).attrs.keys()}