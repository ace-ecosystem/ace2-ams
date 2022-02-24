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
  nodeNameProperty,
  nodeObservableProperty,
  nodeObservableTypesProperty,
  nodeObservableValueProperty,
  nodeOwnerProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  nodeQueueProperty,
} from "../constants/base";

export const alertFilters: readonly propertyOption[] = [
  alertDispositionProperty,
  alertDispositionUserProperty,
  alertDispositionedAfterProperty,
  alertDispositionedBeforeProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  nodeNameProperty,
  nodeObservableProperty,
  nodeObservableTypesProperty,
  nodeObservableValueProperty,
  nodeOwnerProperty,
  nodeQueueProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  alertToolProperty,
  alertToolInstanceProperty,
  alertTypeProperty,
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
  "Disposition Time": {
    start: alertPropertyTypes.DISPOSITIONED_AFTER_PROPERTY,
    end: alertPropertyTypes.DISPOSITIONED_BEFORE_PROPERTY,
  },
};
