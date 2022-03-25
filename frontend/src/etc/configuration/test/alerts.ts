import { propertyOption } from "@/models/base";
import {
  alertPropertyTypes,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  alertDispositionProperty,
} from "@/etc/constants/alerts";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  nodeTagsProperty,
  nodeThreatsProperty,
  queueProperty,
  ownerProperty,
} from "@/etc/constants/common";

const defaultAlertFilters = [
  alertDispositionProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  nameProperty,
  observableProperty,
  observableTypesProperty,
  ownerProperty,
  queueProperty,
  nodeTagsProperty,
  nodeThreatsProperty,
];

export const alertFilters: Record<string, readonly propertyOption[]> = {
  external: defaultAlertFilters,
  intel: defaultAlertFilters,
  internal: defaultAlertFilters,
} as const;

export const alertRangeFilters = {
  "Event Time": {
    start: alertPropertyTypes.EVENT_TIME_AFTER_PROPERTY,
    end: alertPropertyTypes.EVENT_TIME_BEFORE_PROPERTY,
  },
  "Insert Time": {
    start: alertPropertyTypes.INSERT_TIME_AFTER_PROPERTY,
    end: alertPropertyTypes.INSERT_TIME_BEFORE_PROPERTY,
  },
};
