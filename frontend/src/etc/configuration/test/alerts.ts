import TestComponentVue from "@/components/test/TestComponent.vue";

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
  tagsProperty,
  threatsProperty,
  queueProperty,
  ownerProperty,
  BLUE,
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
  tagsProperty,
  threatsProperty,
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
};

export const FALSE_POSITIVE_DISPOSITION_STRING = "FALSE_POSITIVE";
export const IGNORE_DISPOSITION_STRING = "IGNORE";

// {alertType.value: iconFilename}
export const alertIconTypeMapping = {
  testType: "test.png",
};

export const alertDispositionMetadata: Record<string, string> = {
  test: BLUE,
};

// Used to set the cutoff for which dispositions allow you to save an alert to an event
export const minimumSaveToEventDisposition = "APPROVED_BUSINESS";

export const alertDetailsComponents: Record<string, unknown> = {
  "test type - a": TestComponentVue,
};
