import { eventRemediationRead } from "../../models/eventRemediation";
import { filterOption } from "@/models/base";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { eventVectorRead } from "@/models/eventVector";
import { nodeThreatRead } from "@/models/nodeThreat";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { observableTypeRead } from "@/models/observableType";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventQueueStore } from "@/stores/eventQueue";
import { useEventRemediationStore } from "@/stores/eventRemediation";
import { useEventRiskLevelStore } from "@/stores/eventRiskLevel";
import { useEventSourceStore } from "@/stores/eventSource";
import { useEventStatusStore } from "@/stores/eventStatus";
import { useEventTypeStore } from "@/stores/eventType";
import { useEventVectorStore } from "@/stores/eventVector";
import { useNodeTagStore } from "@/stores/nodeTag";
import { useNodeThreatStore } from "@/stores/nodeThreat";
import { useNodeThreatActorStore } from "@/stores/nodeThreatActor";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
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
  NAME_PROPERTY: "name",
  OBSERVABLE_TYPES_PROPERTY: "observableTypes",
  OBSERVABLE_VALUE_PROPERTY: "observableValue",
  OWNER_PROPERTY: "owner",
  COMMENTS_PROPERTY: "comments",
  PREVENTION_TOOLS_PROPERTY: "preventionTools",
  QUEUE_PROPERTY: "queue",
  REMEDIATIONS_PROPERTY: "remediations",
  RISK_LEVEL_PROPERTY: "riskLevel",
  SOURCE_PROPERTY: "source",
  STATUS_PROPERTY: "status",
  TAGS_PROPERTY: "tags",
  THREAT_ACTORS_PROPERTY: "threatActors",
  THREATS_PROPERTY: "threats",
  TYPE_PROPERTY: "type",
  VECTORS_PROPERTY: "vectors",
};
const eventEventTimeProperty = {
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
const eventAlertTimeProperty = {
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
const eventOwnershipTimeProperty = {
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
const eventDispositionTimeProperty = {
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
const eventContainTimeProperty = {
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
const eventRemediationTimeProperty = {
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
const eventRemediationProperty = {
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
const eventNameProperty: filterOption = {
  name: eventPropertyTypes.NAME_PROPERTY,
  label: "Name",
  type: inputTypes.INPUT_TEXT,
};
const eventOwnerProperty: filterOption = {
  name: eventPropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};
const eventCommentProperty: filterOption = {
  name: eventPropertyTypes.COMMENTS_PROPERTY,
  label: "Comment",
  type: inputTypes.INPUT_TEXT,
};
const eventPreventionToolsProperty: filterOption = {
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
const eventRiskLevelProperty: filterOption = {
  name: eventPropertyTypes.RISK_LEVEL_PROPERTY,
  label: "Risk Level",
  type: inputTypes.SELECT,
  store: useEventRiskLevelStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventStatusProperty: filterOption = {
  name: eventPropertyTypes.STATUS_PROPERTY,
  label: "Status",
  type: inputTypes.SELECT,
  store: useEventStatusStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventThreatActorsProperty: filterOption = {
  name: eventPropertyTypes.THREAT_ACTORS_PROPERTY,
  label: "Threat Actors",
  type: inputTypes.MULTISELECT,
  store: useNodeThreatActorStore,
  stringRepr: (value: nodeThreatActorRead[]) => {
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
const eventThreatsProperty: filterOption = {
  name: eventPropertyTypes.THREATS_PROPERTY,
  label: "Threats",
  type: inputTypes.MULTISELECT,
  store: useNodeThreatStore,
  stringRepr: (value: nodeThreatRead[]) => {
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
const eventTypeProperty: filterOption = {
  name: eventPropertyTypes.TYPE_PROPERTY,
  label: "Type",
  type: inputTypes.SELECT,
  store: useEventTypeStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventVectorsProperty: filterOption = {
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

export const eventEditableProperties: readonly filterOption[] = [
  eventNameProperty,
  eventOwnerProperty,
  eventCommentProperty,
  eventRemediationProperty,
  eventPreventionToolsProperty,
  eventRiskLevelProperty,
  eventStatusProperty,
  eventThreatActorsProperty,
  eventThreatsProperty,
  eventTypeProperty,
  eventVectorsProperty,
  eventEventTimeProperty,
  eventAlertTimeProperty,
  eventOwnershipTimeProperty,
  eventDispositionTimeProperty,
  eventContainTimeProperty,
  eventRemediationTimeProperty,
];

export const eventFilters: readonly filterOption[] = [
  {
    name: eventPropertyTypes.CREATED_AFTER_PROPERTY,
    label: "Created After",
    type: inputTypes.DATE,
    stringRepr: (value: Date) => {
      return value.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
    label: "Created Before",
    type: inputTypes.DATE,
    stringRepr: (value: Date) => {
      return value.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: eventPropertyTypes.DISPOSITION_PROPERTY,
    label: "Disposition",
    type: inputTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventNameProperty,
  {
    name: eventPropertyTypes.OBSERVABLE_PROPERTY,
    label: "Observable",
    type: inputTypes.CATEGORIZED_VALUE,
    store: useObservableTypeStore,
    stringRepr: (value: { category: observableTypeRead; value: string }) => {
      return `${value.category.value}|${value.value}`;
    },
    parseStringRepr: (valueString: string) => {
      const [category, value] = valueString.split("|");
      return { category: category, value: value };
    },
  },
  {
    name: eventPropertyTypes.OBSERVABLE_TYPES_PROPERTY,
    label: "Observable Types",
    type: inputTypes.MULTISELECT,
    store: useObservableTypeStore,
    stringRepr: (value: observableTypeRead[]) => {
      return value
        .map(function (elem) {
          return elem.value;
        })
        .join();
    },
    parseStringRepr: (valueString: string) => {
      return valueString.split(",");
    },
  },
  {
    name: eventPropertyTypes.OBSERVABLE_VALUE_PROPERTY,
    label: "Observable Value",
    type: inputTypes.INPUT_TEXT,
  },
  eventOwnerProperty,
  eventPreventionToolsProperty,
  {
    name: eventPropertyTypes.QUEUE_PROPERTY,
    label: "Queue",
    type: inputTypes.SELECT,
    store: useEventQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventRiskLevelProperty,
  {
    name: eventPropertyTypes.SOURCE_PROPERTY,
    label: "Source",
    type: inputTypes.SELECT,
    store: useEventSourceStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventStatusProperty,
  {
    name: eventPropertyTypes.TAGS_PROPERTY,
    label: "Tags",
    type: inputTypes.CHIPS,
    store: useNodeTagStore,
    stringRepr: (value: string[]) => {
      return value
        .map(function (elem) {
          return elem;
        })
        .join();
    },
    parseStringRepr: (valueString: string) => {
      return valueString.split(",");
    },
  },
  eventThreatActorsProperty,
  eventThreatsProperty,
  eventTypeProperty,
  eventVectorsProperty,
] as const;

export const eventRangeFilters = {
  "Created Time": {
    start: eventPropertyTypes.CREATED_AFTER_PROPERTY,
    end: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
  },
};
