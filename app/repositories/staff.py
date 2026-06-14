from sqlalchemy.orm import Session

from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


class StaffRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, staff_data: StaffCreate) -> Staff:
        try:
            staff = Staff(
                user_id=user_id,
                legajo=staff_data.legajo,
                sector=staff_data.sector,
                cargo=staff_data.cargo
            )
            self.db.add(staff)
            self.db.commit()
            self.db.refresh(staff)
            return staff
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_user_id(self, user_id: int) -> Staff | None:
        return self.db.query(Staff).filter(Staff.user_id == user_id).first()

    def get_by_legajo(self, legajo: str) -> Staff | None:
        return self.db.query(Staff).filter(Staff.legajo == legajo).first()

    def update(self, user_id: int, staff_update: StaffUpdate) -> Staff | None:
        try:
            staff = self.get_by_user_id(user_id)
            if not staff:
                return None
            if staff_update.sector: staff.sector = staff_update.sector
            if staff_update.cargo: staff.cargo = staff_update.cargo
            self.db.commit()
            self.db.refresh(staff)
            return staff
        except Exception as e:
            self.db.rollback()
            raise e