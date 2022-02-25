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
  queueProperty,
  ownerProperty,
} from "@/etc/constants/base";

export const alertFilters: readonly propertyOption[] = [
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
] as const;

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
