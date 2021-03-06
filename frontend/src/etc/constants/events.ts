import { eventRemediationRead } from "@/models/eventRemediation";
import { propertyOption } from "@/models/base";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { eventVectorRead } from "@/models/eventVector";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { useEventSeverityStore } from "@/stores/eventSeverity";
import { useEventSourceStore } from "@/stores/eventSource";
import { useEventStatusStore } from "@/stores/eventStatus";
import { useEventTypeStore } from "@/stores/eventType";
import { useEventVectorStore } from "@/stores/eventVector";

import {
  nameProperty,
  tagsProperty,
  threatActorProperty,
  threatsProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  queueProperty,
} from "./common";
import { inputTypes } from "./base";

// ** Events ** //

// NOTE: If alerts and events share a property name (like how they both originally had the "type" property),
// care must be taken... The event type field is queueable, whereas the alert type field is not. This will
// cause issues in the "formatObjectFiltersForAPI" function when you have properties that share a name but
// one is queueable and the other not. The fix for this is to rename the fields. So now there is the "alertType"
// property and the "eventType" property.

export const eventPropertyTypes: Record<string, string> = {
  CREATED_AFTER_PROPERTY: "createdAfter",
  CREATED_BEFORE_PROPERTY: "createdBefore",
  CONTAIN_TIME_PROPERTY: "containTime",
  EVENT_TIME_PROPERTY: "eventTime",
  EVENT_TYPE_PROPERTY: "eventType",
  ALERT_TIME_PROPERTY: "alertTime",
  OWNERSHIP_TIME_PROPERTY: "ownershipTime",
  DISPOSITION_TIME_PROPERTY: "dispositionTime",
  REMEDIATION_TIME_PROPERTY: "remediationTime",
  DISPOSITION_PROPERTY: "disposition",
  PREVENTION_TOOLS_PROPERTY: "preventionTools",
  REMEDIATIONS_PROPERTY: "remediations",
  SEVERITY_PROPERTY: "severity",
  SOURCE_PROPERTY: "source",
  STATUS_PROPERTY: "status",
  VECTORS_PROPERTY: "vectors",
};
export const eventEventTimeProperty: propertyOption = {
  name: eventPropertyTypes.EVENT_TIME_PROPERTY,
  label: "Event Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventAlertTimeProperty: propertyOption = {
  name: eventPropertyTypes.ALERT_TIME_PROPERTY,
  label: "Alert Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventOwnershipTimeProperty: propertyOption = {
  name: eventPropertyTypes.OWNERSHIP_TIME_PROPERTY,
  label: "Ownership Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventDispositionTimeProperty: propertyOption = {
  name: eventPropertyTypes.DISPOSITION_TIME_PROPERTY,
  label: "Disposition Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventContainTimeProperty: propertyOption = {
  name: eventPropertyTypes.CONTAIN_TIME_PROPERTY,
  label: "Contain Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventRemediationTimeProperty: propertyOption = {
  name: eventPropertyTypes.REMEDIATION_TIME_PROPERTY,
  label: "Remediation Time (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventRemediationProperty: propertyOption = {
  name: eventPropertyTypes.REMEDIATIONS_PROPERTY,
  label: "Remediation",
  type: inputTypes.MULTISELECT,
  store: useEventRemediationStore,
  queueDependent: true,
  stringRepr: (value: eventRemediationRead[]): string => {
    return value
      .map(function (elem) {
        return elem.value;
      })
      .join();
  },
  parseStringRepr: (valueString: string): string[] => {
    return valueString.split(",");
  },
};
export const eventPreventionToolsProperty: propertyOption = {
  name: eventPropertyTypes.PREVENTION_TOOLS_PROPERTY,
  label: "Prevention Tools",
  type: inputTypes.MULTISELECT,
  store: useEventPreventionToolStore,
  queueDependent: true,

  stringRepr: (value: eventPreventionToolRead[]) => {
    return value
      .map(function (elem) {
        return elem.value;
      })
      .join();
  },
  parseStringRepr: (valueString: string) => {
    return valueString.split(",");
  },
};
export const eventSeverityProperty: propertyOption = {
  name: eventPropertyTypes.SEVERITY_PROPERTY,
  label: "Severity",
  type: inputTypes.SELECT,
  store: useEventSeverityStore,
  queueDependent: true,

  optionProperty: "value",
  valueProperty: "value",
};
export const eventStatusProperty: propertyOption = {
  name: eventPropertyTypes.STATUS_PROPERTY,
  label: "Status",
  type: inputTypes.SELECT,
  store: useEventStatusStore,
  queueDependent: true,

  optionProperty: "value",
  valueProperty: "value",
};
export const eventTypeProperty: propertyOption = {
  name: eventPropertyTypes.EVENT_TYPE_PROPERTY,
  label: "Type",
  type: inputTypes.SELECT,
  store: useEventTypeStore,
  queueDependent: true,

  optionProperty: "value",
  valueProperty: "value",
};
export const eventVectorsProperty: propertyOption = {
  name: eventPropertyTypes.VECTORS_PROPERTY,
  label: "Vectors",
  type: inputTypes.MULTISELECT,
  store: useEventVectorStore,
  queueDependent: true,

  stringRepr: (value: eventVectorRead[]) => {
    return value
      .map(function (elem) {
        return elem.value;
      })
      .join();
  },
  parseStringRepr: (valueString: string) => {
    return valueString.split(",");
  },
};
export const eventCreatedAfterProperty: propertyOption = {
  name: eventPropertyTypes.CREATED_AFTER_PROPERTY,
  label: "Created After (UTC)",
  type: inputTypes.DATE,
  stringRepr: (value: Date) => {
    return value.toISOString().replace("Z", "");
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const eventCreatedBeforeProperty: propertyOption = {
  name: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
  label: "Created Before (UTC)",
  type: inputTypes.DATE,
  stringRepr: (value: Date) => {
    return value.toISOString().replace("Z", "");
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const eventDispositionProperty: propertyOption = {
  name: eventPropertyTypes.DISPOSITION_PROPERTY,
  label: "Disposition",
  type: inputTypes.SELECT,
  store: useAlertDispositionStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const eventSourceProperty: propertyOption = {
  name: eventPropertyTypes.SOURCE_PROPERTY,
  label: "Source",
  type: inputTypes.SELECT,
  store: useEventSourceStore,
  queueDependent: true,
  optionProperty: "value",
  valueProperty: "value",
};

export const validEventFilters: propertyOption[] = [
  eventDispositionProperty,
  nameProperty,
  observableProperty,
  eventCreatedAfterProperty,
  eventCreatedBeforeProperty,
  observableTypesProperty,
  observableProperty,
  observableValueProperty,
  ownerProperty,
  eventPreventionToolsProperty,
  queueProperty,
  eventSeverityProperty,
  eventSourceProperty,
  eventStatusProperty,
  tagsProperty,
  threatActorProperty,
  threatsProperty,
  eventTypeProperty,
  eventVectorsProperty,
];
