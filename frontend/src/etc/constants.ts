export const DISPOSITION_FILTER = "disposition";
export const DISPOSITION_USER_FILTER = "dispositionUser";
export const DISPOSITIONED_AFTER_FILTER = "dispositionedAfter";
export const DISPOSITIONED_BEFORE_FILTER = "dispositionedBefore";
export const EVENT_UUID_FILTER = "eventUuid";
export const EVENT_TIME_AFTER_FILTER = "eventTimeAfter";
export const EVENT_TIME_BEFORE_FILTER = "eventTimeBefore";
export const INSERT_TIME_AFTER_FILTER = "insertTimeAfter";
export const INSERT_TIME_BEFORE_FILTER = "insertTimeBefore";
export const NAME_FILTER = "name";
export const OBSERVABLE_FILTER = "observable";
export const OBSERVABLE_TYPES_FILTER = "observableTypes";
export const OBSERVABLE_VALUE_FILTER = "observableValue";
export const OWNER_FILTER = "owner";
export const QUEUE_FILTER = "queue";
export const TAGS_FILTER = "tags";
export const THREAT_ACTOR_FILTER = "threatActor";
export const THREATS_FILTER = "threats";
export const TOOL_FILTER = "tool";
export const TOOL_INSTANCE_FILTER = "toolInstance";
export const TYPE_FILTER = "type";

export const alertFilters = [
  DISPOSITION_FILTER,
  DISPOSITION_USER_FILTER,
  DISPOSITIONED_AFTER_FILTER,
  DISPOSITIONED_BEFORE_FILTER,
  EVENT_UUID_FILTER,
  EVENT_TIME_AFTER_FILTER,
  EVENT_TIME_BEFORE_FILTER,
  INSERT_TIME_AFTER_FILTER,
  INSERT_TIME_BEFORE_FILTER,
  NAME_FILTER,
  OBSERVABLE_FILTER,
  OBSERVABLE_TYPES_FILTER,
  OBSERVABLE_VALUE_FILTER,
  OWNER_FILTER,
  QUEUE_FILTER,
  TAGS_FILTER,
  THREAT_ACTOR_FILTER,
  THREATS_FILTER,
  TOOL_FILTER,
  TOOL_INSTANCE_FILTER,
  TYPE_FILTER,
] as const;
