import sys

from sqlalchemy.orm import Session

from db.database import get_db
from tests import helpers

# Command line arguments:
#
# 0 - Name of the script (insert-alerts.py)
# 1 - Path to alert JSON file
# 2 (Optional) - Number of times to insert the alert, defaults to 1

if len(sys.argv) < 2:
    print("You must specify the path to the alert JSON file")
    sys.exit()

# When you specify the path to the JSON file, you do so from the perspective
# of outisde the container, so you preface it with backend/ so that you can
# use tab-completion on your local command line.
#
# However, this runs inside of the container, so the backend/ part of the path
# does not exist and must be removed so that it is a valid path inside the container.
#
# Example: db_api/app/tests/alerts/blah.json -> /app/tests/alerts/blah.json
json_path = sys.argv[1].replace("db_api", "")

num_alerts = 1
if len(sys.argv) == 3:
    num_alerts = int(sys.argv[2])

db: Session = next(get_db())

for i in range(num_alerts):
    helpers.create_alert_from_json_file(db=db, json_path=json_path, alert_name=f"Manual Alert {i}")
