import { userRead } from "@/models/user";
import { genericObjectReadFactory } from "./genericObject";

export const userReadFactory = ({
  defaultAlertQueue = genericObjectReadFactory(),
  defaultEventQueue = genericObjectReadFactory(),
  displayName = "Test Analyst",
  email = "test@analyst.com",
  enabled = false,
  roles = [],
  timezone = "",
  training = false,
  username = "",
  uuid = "",
}: Partial<userRead> = {}): userRead => ({
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
