from sqlalchemy.ext.asyncio import AsyncSession

from app.common.logger import LoggerManager
from app.common.services import CrudRepository
from app.modules.user.models import InvitationModel
from app.modules.user.schemas.invitation import InvitationCreate, InvitationUpdate

logger = LoggerManager.get_code_logger()


class InvitationRepository(CrudRepository[InvitationModel, InvitationCreate, InvitationUpdate]):
    """Класс для всех взаимодействий с таблицей Invitation"""

    def __init__(self, db: AsyncSession):
        super().__init__(InvitationModel, db)

    pass
