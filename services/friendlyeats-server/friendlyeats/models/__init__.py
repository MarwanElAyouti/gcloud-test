# List all your DB models here if you want it be visible for alembic

from collections.abc import Sequence

from friendlyeats.models.base import Base

"""
    e.g.:
        from collections.abc import Sequence

        from friendlyeats.models.{model_name} import SomeModel

        __all__: Sequence = (Base, SomeModel)
"""

__all__: Sequence = (Base,)
