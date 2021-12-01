export const filterTypes = {
  MULTISELECT: "multiselect",
  CHIPS: "chips",
  SELECT: "select",
  DATE: "date",
  INPUT_TEXT: "inputText",
  CATEGORIZED_VALUE: "categorizedValue",
};

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
  {
    name: DISPOSITION_FILTER,
    label: "Disposition",
    type: filterTypes.SELECT,
    options: "alertDisposition",
  },
  {
    name: DISPOSITION_USER_FILTER,
    label: "Dispositioned By",
    type: filterTypes.SELECT,
    options: "users",
    optionValue: "displayName",
  },
  {
    name: DISPOSITIONED_AFTER_FILTER,
    label: "Dispositioned After",
    type: filterTypes.DATE,
  },
  {
    name: DISPOSITIONED_BEFORE_FILTER,
    label: "Dispositioned Before",
    type: filterTypes.DATE,
  },
  { name: EVENT_UUID_FILTER, label: "Event" },
  {
    name: EVENT_TIME_AFTER_FILTER,
    label: "Event Time After",
    type: filterTypes.DATE,
  },
  {
    name: EVENT_TIME_BEFORE_FILTER,
    label: "Event Time Before",
    type: filterTypes.DATE,
  },
  {
    name: INSERT_TIME_AFTER_FILTER,
    label: "Insert Time After",
    type: filterTypes.DATE,
  },
  {
    name: INSERT_TIME_BEFORE_FILTER,
    label: "Insert Time Before",
    type: filterTypes.DATE,
  },
  {
    name: NAME_FILTER,
    label: "Name",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: OBSERVABLE_FILTER,
    label: "Observable",
    type: filterTypes.CATEGORIZED_VALUE,
    options: "observableType"
  },
  {
    name: OBSERVABLE_TYPES_FILTER,
    label: "Observable Types",
    type: filterTypes.MULTISELECT,
    options: "observableType",
  },
  {
    name: OBSERVABLE_VALUE_FILTER,
    label: "Observable Value",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: OWNER_FILTER,
    label: "Owner",
    type: filterTypes.SELECT,
    options: "users",
    optionValue: "displayName",
  },
  {
    name: QUEUE_FILTER,
    label: "Queue",
    type: filterTypes.SELECT,
    options: "alertQueue",
  },
  {
    name: TAGS_FILTER,
    label: "Tags",
    type: filterTypes.CHIPS,
    options: "nodeTag",
  },
  {
    name: THREAT_ACTOR_FILTER,
    label: "Threat Actor",
    type: filterTypes.SELECT,
    options: "nodeThreat",
  },
  {
    name: THREATS_FILTER,
    label: "Threats",
    type: filterTypes.CHIPS,
    options: "nodeThreatActor",
  },
  {
    name: TOOL_FILTER,
    label: "Tool",
    type: filterTypes.SELECT,
    options: "tool",
  },
  {
    name: TOOL_INSTANCE_FILTER,
    label: "Tool Instance",
    type: filterTypes.SELECT,
    options: "toolInstance",
  },
  {
    name: TYPE_FILTER,
    label: "Type",
    type: filterTypes.SELECT,
    options: "alertType",
  },
] as const;

export const alertRangeFilters = {
  eventTime: {
    start: EVENT_TIME_AFTER_FILTER,
    end: EVENT_TIME_BEFORE_FILTER,
  },
  insertTime: {
    start: INSERT_TIME_AFTER_FILTER,
    end: INSERT_TIME_BEFORE_FILTER,
  },
  dispositionedTime: {
    start: DISPOSITIONED_AFTER_FILTER,
    end: DISPOSITIONED_BEFORE_FILTER,
  },
};
