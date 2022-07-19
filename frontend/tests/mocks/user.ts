import { userCreate, userRead } from "@/models/user";
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
  username = "analyst",
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

export const userCreateFactory = ({
  defaultAlertQueue = "default",
  defaultEventQueue = "default",
  displayName = "Test Analyst",
  email = "test@analyst.com",
  enabled = false,
  roles = [],
  timezone = "",
  training = false,
  username = "analyst",
  uuid = "",
  password = "",
}: Partial<userCreate> = {}): userCreate => ({
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
  password: password,
});
