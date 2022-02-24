import { eventRemediationRead } from "../../models/eventRemediation";
import { propertyOption } from "@/models/base";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { eventVectorRead } from "@/models/eventVector";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { useEventRiskLevelStore } from "@/stores/eventRiskLevel";
import { useEventSourceStore } from "@/stores/eventSource";
import { useEventStatusStore } from "@/stores/eventStatus";
import { useEventTypeStore } from "@/stores/eventType";
import { useEventVectorStore } from "@/stores/eventVector";

import { inputTypes } from "./base";

// ** Events ** //

export const eventPropertyTypes: Record<string, string> = {
  CREATED_AFTER_PROPERTY: "createdAfter",
  CREATED_BEFORE_PROPERTY: "createdBefore",
  CONTAIN_TIME_PROPERTY: "containTime",
  EVENT_TIME_PROPERTY: "eventTime",
  ALERT_TIME_PROPERTY: "alertTime",
  OWNERSHIP_TIME_PROPERTY: "ownershipTime",
  DISPOSITION_TIME_PROPERTY: "dispositionTime",
  REMEDIATION_TIME_PROPERTY: "remediationTime",
  DISPOSITION_PROPERTY_PROPERTY: "disposition",
  PREVENTION_TOOLS_PROPERTY: "preventionTools",
  REMEDIATIONS_PROPERTY: "remediations",
  RISK_LEVEL_PROPERTY: "riskLevel",
  SOURCE_PROPERTY: "source",
  STATUS_PROPERTY: "status",
  TYPE_PROPERTY: "type",
  VECTORS_PROPERTY: "vectors",
};
export const eventEventTimeProperty: propertyOption = {
  name: eventPropertyTypes.EVENT_TIME_PROPERTY,
  label: "Event TIme",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventAlertTimeProperty: propertyOption = {
  name: eventPropertyTypes.ALERT_TIME_PROPERTY,
  label: "Alert Time",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventOwnershipTimeProperty: propertyOption = {
  name: eventPropertyTypes.OWNERSHIP_TIME_PROPERTY,
  label: "Ownership Time",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventDispositionTimeProperty: propertyOption = {
  name: eventPropertyTypes.DISPOSITION_TIME_PROPERTY,
  label: "Disposition Time",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventContainTimeProperty: propertyOption = {
  name: eventPropertyTypes.CONTAIN_TIME_PROPERTY,
  label: "Contain Time",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string): Date => {
    return new Date(valueString);
  },
};
export const eventRemediationTimeProperty: propertyOption = {
  name: eventPropertyTypes.REMEDIATION_TIME_PROPERTY,
  label: "Remediation Time",
  type: inputTypes.DATE,
  stringRepr: (value: Date): string => {
    return value.toISOString();
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
export const eventRiskLevelProperty: propertyOption = {
  name: eventPropertyTypes.RISK_LEVEL_PROPERTY,
  label: "Risk Level",
  type: inputTypes.SELECT,
  store: useEventRiskLevelStore,
  optionProperty: "value",
  valueProperty: "value",
};
export const eventStatusProperty: propertyOption = {
  name: eventPropertyTypes.STATUS_PROPERTY,
  label: "Status",
  type: inputTypes.SELECT,
  store: useEventStatusStore,
  optionProperty: "value",
  valueProperty: "value",
};
export const eventTypeProperty: propertyOption = {
  name: eventPropertyTypes.TYPE_PROPERTY,
  label: "Type",
  type: inputTypes.SELECT,
  store: useEventTypeStore,
  optionProperty: "value",
  valueProperty: "value",
};
export const eventVectorsProperty: propertyOption = {
  name: eventPropertyTypes.VECTORS_PROPERTY,
  label: "Vectors",
  type: inputTypes.MULTISELECT,
  store: useEventVectorStore,
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
  label: "Created After",
  type: inputTypes.DATE,
  stringRepr: (value: Date) => {
    return value.toISOString();
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const eventCreatedBeforeProperty: propertyOption = {
  name: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
  label: "Created Before",
  type: inputTypes.DATE,
  stringRepr: (value: Date) => {
    return value.toISOString();
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
  optionProperty: "value",
  valueProperty: "value",
};
