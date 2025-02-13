from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

reg = registry()


@reg.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    category: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, insert_default=func.now()
    )
