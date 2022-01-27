import { alertQueueRead } from "@/models/alertQueue";
import { UUID } from "@/models/base";
import { eventQueueRead } from "@/models/eventQueue";
import { userRead } from "@/models/user";
import { userRoleRead } from "@/models/userRole";
import { genericObjectFactory } from "./genericObject";

export const userFactory = (
  defaultAlertQueue: alertQueueRead = genericObjectFactory(),
  defaultEventQueue: eventQueueRead = genericObjectFactory(),
  displayName = "Test Analyst",
  email = "test@analyst.com",
  enabled = false,
  roles: userRoleRead[] = [],
  timezone = "",
  training = false,
  username = "",
  uuid: UUID = "",
): userRead => ({
  defaultAlertQueue: defaultAlertQueue,
  defaultEventQueue: defaultEventQueue,
  displayName: displayName,
  email: email,
  enabled: enabled,
  roles: roles,
  timezone: timezone,
  training: training,
  username: username,
  uuid: uuid,
});
