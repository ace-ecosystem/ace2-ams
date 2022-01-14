import sys

from sqlalchemy.orm import Session

from db.database import get_db
from tests import helpers

# Command line arguments:
#
# 0 - Name of the script (insert-event.py)
# 1 - Path to alert JSON file to add into the event
# 2 - Name of the event (no spaces)
# 3 (Optional) - Number of times to insert the alert, defaults to 1

if len(sys.argv) < 3:
    print("You must specify the path to the alert JSON file and event name")
    sys.exit()

# When you specify the path to the JSON file, you do so from the perspective
# of outisde the container, so you preface it with backend/ so that you can
# use tab-completion on your local command line.
#
# However, this runs inside of the container, so the backend/ part of the path
# does not exist and must be removed so that it is a valid path inside the container.
#
# Example: backend/app/tests/alerts/blah.json -> /app/tests/alerts/blah.json
json_path = sys.argv[1].replace("backend", "")

num_alerts = 1
if len(sys.argv) == 4:
    num_alerts = int(sys.argv[3])

db: Session = next(get_db())

for _ in range(num_alerts):
    event = helpers.create_event(name=sys.argv[2], db=db)
    alert_tree = helpers.create_alert_from_json_file(db=db, json_path=json_path)
    alert_tree.node.event_uuid = event.uuid

    db.commit()
