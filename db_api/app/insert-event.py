import argparse

from sqlalchemy.orm import Session

from db.database import get_db
from tests import helpers

parser = argparse.ArgumentParser()

# Required
parser.add_argument("alert_json_path", type=str, help="Path to the alert JSON template file to add to the event")
parser.add_argument("event_name", type=str, help="The name of the event to create (without any space)")

# Optional
parser.add_argument("--num_alerts", type=int, default=1, help="The number of copies of the alert to add to the event")
parser.add_argument("--owner", type=str, help="The username of the user to use as the event owner")
parser.add_argument("--prevention_tools", type=str, help="Comma-separated list of prevention tools")
parser.add_argument("--queue", type=str, help="The event queue")
parser.add_argument("--remediations", type=str, help="Comma-separated list of remediations")
parser.add_argument("--risk_level", type=str, help="The event risk level")
parser.add_argument("--source", type=str, help="The event source")
parser.add_argument("--status", type=str, help="The event status")
parser.add_argument("--tags", type=str, help="Comma-separated list of tags for the event")
parser.add_argument("--threat_actors", type=str, help="Comma-separated list of threat actors to add to the event")
parser.add_argument("--threats", type=str, help="Comma-separated list of threats to add to the event")
parser.add_argument("--type", type=str, help="The event type")
parser.add_argument("--vectors", type=str, help="Comma-separated list of vectors to add to the event")

args = parser.parse_args()

# When you specify the path to the JSON file, you do so from the perspective
# of outisde the container, so you preface it with db_api/ so that you can
# use tab-completion on your local command line.
#
# However, this runs inside of the container, so the db_api/ part of the path
# does not exist and must be removed so that it is a valid path inside the container.
#
# Example: db_api/app/tests/alerts/blah.json -> /app/tests/alerts/blah.json
alert_json_path = args.alert_json_path.replace("db_api", "")

db: Session = next(get_db())

event = helpers.create_event(name=args.event_name, db=db)

if args.owner:
    event.owner = helpers.create_user(username=args.owner, db=db, display_name=args.owner)

if args.prevention_tools:
    event.prevention_tools = [
        helpers.create_event_prevention_tool(value=p, db=db) for p in args.prevention_tools.split(",")
    ]

if args.queue:
    event.queue = helpers.create_queue(value=args.queue, db=db)

if args.remediations:
    event.remediations = [helpers.create_event_remediation(value=r, db=db) for r in args.remediations.split(",")]

if args.risk_level:
    event.risk_level = helpers.create_event_risk_level(value=args.risk_level, db=db)

if args.source:
    event.source = helpers.create_event_source(value=args.source, db=db)

if args.status:
    event.status = helpers.create_event_status(value=args.status, db=db)

if args.tags:
    event.tags = [helpers.create_node_tag(value=t, db=db) for t in args.tags.split(",")]

if args.threat_actors:
    event.threat_actors = [helpers.create_node_threat_actor(value=t, db=db) for t in args.threat_actors.split(",")]

if args.threats:
    event.threats = [helpers.create_node_threat(value=t, db=db) for t in args.threats.split(",")]

if args.type:
    event.type = helpers.create_event_type(value=args.type, db=db)

if args.vectors:
    event.vectors = [helpers.create_event_vector(value=v, db=db) for v in args.vectors.split(",")]

for i in range(args.num_alerts):
    alert_tree = helpers.create_alert_from_json_file(db=db, json_path=alert_json_path, alert_name=f"Manual Alert {i}")
    alert_tree.node.event_uuid = event.uuid

db.commit()
