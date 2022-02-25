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
  nodeNameProperty,
  nodeObservableProperty,
  nodeObservableTypesProperty,
  nodeTagsProperty,
  nodeQueueProperty,
  nodeOwnerProperty,
} from "@/etc/constants/base";

export const alertFilters: readonly propertyOption[] = [
  alertDispositionProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  nodeNameProperty,
  nodeObservableProperty,
  nodeObservableTypesProperty,
  nodeOwnerProperty,
  nodeQueueProperty,
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
