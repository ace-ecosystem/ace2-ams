from sqlalchemy.orm import Session

from db.database import get_db
from tests import helpers

db: Session = next(get_db())
helpers.create_realistic_alert(db=db)
