import { propertyOption } from "@/models/base";
import {
  alertPropertyTypes,
  alertDispositionProperty,
  alertDispositionedAfterProperty,
  alertDispositionedBeforeProperty,
  alertDispositionUserProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  alertToolInstanceProperty,
  alertToolProperty,
  alertTypeProperty,
} from "@/etc/constants/alerts";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  tagsProperty as tagsProperty,
  threatActorProperty,
  threatsProperty,
  queueProperty,
  BLUE,
  GREEN,
  ORANGE,
  RED,
} from "@/etc/constants/common";

const defaultAlertFilters = [
  alertDispositionProperty,
  alertDispositionUserProperty,
  alertDispositionedAfterProperty,
  alertDispositionedBeforeProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  nameProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  queueProperty,
  tagsProperty,
  threatActorProperty,
  threatsProperty,
  alertToolProperty,
  alertToolInstanceProperty,
  alertTypeProperty,
];

export const alertFilters: Record<string, readonly propertyOption[]> = {
  external: defaultAlertFilters,
  intel: defaultAlertFilters,
  internal: defaultAlertFilters,
} as const;

export const alertRangeFilters = {
  "Event Time (UTC)": {
    start: alertPropertyTypes.EVENT_TIME_AFTER_PROPERTY,
    end: alertPropertyTypes.EVENT_TIME_BEFORE_PROPERTY,
  },
  "Insert Time (UTC)": {
    start: alertPropertyTypes.INSERT_TIME_AFTER_PROPERTY,
    end: alertPropertyTypes.INSERT_TIME_BEFORE_PROPERTY,
  },
  "Disposition Time (UTC)": {
    start: alertPropertyTypes.DISPOSITIONED_AFTER_PROPERTY,
    end: alertPropertyTypes.DISPOSITIONED_BEFORE_PROPERTY,
  },
};

export const FALSE_POSITIVE_DISPOSITION_STRING = "FALSE_POSITIVE";
export const IGNORE_DISPOSITION_STRING = "IGNORE";

export const alertIconTypeMapping = {};

export const alertDispositionMetadata: Record<string, string> = {
  false_positive: GREEN,
  authorized: GREEN,
  unknown: BLUE,
  reviewed: BLUE,
  grayware: BLUE,
  policy_violation: ORANGE,
  reconnaissance: ORANGE,
  weaponization: RED,
  delivery: RED,
  exploitation: RED,
  installation: RED,
  command_and_control: RED,
  data_control: RED,
  exfil: RED,
  damage: RED,
};

// Used to set the cutoff for which dispositions allow you to save an alert to an event
export const minimumSaveToEventDisposition = "APPROVED_BUSINESS";

export const alertDetailsComponents: Record<string, unknown> = {};
