from fastapi import APIRouter

from api.routes.alert_disposition import router as alert_disposition_router
from api.routes.analysis import router as analysis_router
from api.routes.analysis_module_type import router as analysis_module_type_router
from api.routes.auth import router as auth_router
from api.routes.event import router as event_router
from api.routes.event_comment import router as event_comment_router
from api.routes.event_prevention_tool import router as event_prevention_tool_router
from api.routes.event_remediation import router as event_remediation_router
from api.routes.event_severity import router as event_severity_router
from api.routes.event_source import router as event_source_router
from api.routes.event_status import router as event_status_router
from api.routes.event_type import router as event_type_router
from api.routes.event_vector import router as event_vector_router
from api.routes.metadata_critical_point import router as metadata_critical_point_router
from api.routes.metadata_detection_point import router as metadata_detection_point_router
from api.routes.metadata_directive import router as metadata_directive_router
from api.routes.metadata_display_type import router as metadata_display_type_router
from api.routes.metadata_display_value import router as metadata_display_value_router
from api.routes.metadata_tag import router as metadata_tag_router
from api.routes.metadata_time import router as metadata_time_router
from api.routes.observable import router as observable_router
from api.routes.observable_relationship import router as observable_relationship_router
from api.routes.observable_relationship_type import router as observable_relationship_type_router
from api.routes.observable_type import router as observable_type_router
from api.routes.ping import router as ping_router
from api.routes.queue import router as queue_router
from api.routes.submission import router as submission_router
from api.routes.submission_comment import router as submission_comment_router
from api.routes.submission_tool import router as submission_tool_router
from api.routes.submission_tool_instance import router as submission_tool_instance_router
from api.routes.submission_type import router as submission_type_router
from api.routes.test import router as test_router
from api.routes.threat import router as threat_router
from api.routes.threat_actor import router as threat_actor_router
from api.routes.threat_type import router as threat_type_router
from api.routes.user import router as user_router
from api.routes.user_role import router as user_role_router


router = APIRouter()

router.include_router(alert_disposition_router)
router.include_router(analysis_router)
router.include_router(analysis_module_type_router)
router.include_router(auth_router)
router.include_router(event_router)
router.include_router(event_comment_router)
router.include_router(event_prevention_tool_router)
router.include_router(event_remediation_router)
router.include_router(event_severity_router)
router.include_router(event_source_router)
router.include_router(event_status_router)
router.include_router(event_type_router)
router.include_router(event_vector_router)
router.include_router(metadata_critical_point_router)
router.include_router(metadata_detection_point_router)
router.include_router(metadata_directive_router)
router.include_router(metadata_display_type_router)
router.include_router(metadata_display_value_router)
router.include_router(metadata_tag_router)
router.include_router(metadata_time_router)
router.include_router(observable_router)
router.include_router(observable_relationship_router)
router.include_router(observable_relationship_type_router)
router.include_router(observable_type_router)
router.include_router(ping_router)
router.include_router(queue_router)
router.include_router(submission_comment_router)
router.include_router(submission_router)
router.include_router(submission_tool_router)
router.include_router(submission_tool_instance_router)
router.include_router(submission_type_router)
router.include_router(test_router)
router.include_router(threat_router)
router.include_router(threat_actor_router)
router.include_router(threat_type_router)
router.include_router(user_router)
router.include_router(user_role_router)
