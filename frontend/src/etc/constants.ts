import { eventRemediationRead } from "./../models/eventRemediation";
import { filterOption } from "@/models/base";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { eventVectorRead } from "@/models/eventVector";
import { nodeThreatRead } from "@/models/nodeThreat";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { observableTypeRead } from "@/models/observableType";

import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
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

// ** Base ** //

export const filterTypes = {
  MULTISELECT: "multiselect",
  CHIPS: "chips",
  SELECT: "select",
  DATE: "date",
  INPUT_TEXT: "inputText",
  CATEGORIZED_VALUE: "categorizedValue",
};

// ** Alerts ** //

export const alertPropertyTypes: Record<string, string> = {
  DISPOSITION_FILTER: "disposition",
  DISPOSITION_USER_FILTER: "dispositionUser",
  DISPOSITIONED_AFTER_FILTER: "dispositionedAfter",
  DISPOSITIONED_BEFORE_FILTER: "dispositionedBefore",
  EVENT_UUID_FILTER: "eventUuid",
  EVENT_TIME_AFTER_FILTER: "eventTimeAfter",
  EVENT_TIME_BEFORE_FILTER: "eventTimeBefore",
  INSERT_TIME_AFTER_FILTER: "insertTimeAfter",
  INSERT_TIME_BEFORE_FILTER: "insertTimeBefore",
  NAME_FILTER: "name",
  OBSERVABLE_FILTER: "observable",
  OBSERVABLE_TYPES_FILTER: "observableTypes",
  OBSERVABLE_VALUE_FILTER: "observableValue",
  OWNER_FILTER: "owner",
  QUEUE_FILTER: "queue",
  TAGS_FILTER: "tags",
  THREAT_ACTOR_FILTER: "threatActor",
  THREATS_FILTER: "threats",
  TOOL_FILTER: "tool",
  TOOL_INSTANCE_FILTER: "toolInstance",
  TYPE_FILTER: "type",
};

export const alertFilters: readonly filterOption[] = [
  {
    name: alertPropertyTypes.DISPOSITION_FILTER,
    label: "Disposition",
    type: filterTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.DISPOSITION_USER_FILTER,
    label: "Dispositioned By",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertPropertyTypes.DISPOSITIONED_AFTER_FILTER,
    label: "Dispositioned After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.DISPOSITIONED_BEFORE_FILTER,
    label: "Dispositioned Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.EVENT_TIME_AFTER_FILTER,
    label: "Event Time After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.EVENT_TIME_BEFORE_FILTER,
    label: "Event Time Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.INSERT_TIME_AFTER_FILTER,
    label: "Insert Time After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.INSERT_TIME_BEFORE_FILTER,
    label: "Insert Time Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (valueString: string) => {
      return new Date(valueString);
    },
  },
  {
    name: alertPropertyTypes.NAME_FILTER,
    label: "Name",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: alertPropertyTypes.OBSERVABLE_FILTER,
    label: "Observable",
    type: filterTypes.CATEGORIZED_VALUE,
    store: useObservableTypeStore,
    stringRepr: (filter: { category: observableTypeRead; value: string }) => {
      return `${filter.category.value}|${filter.value}`;
    },
    parseStringRepr: (valueString: string) => {
      const [category, value] = valueString.split("|");
      return { category: category, value: value };
    },
  },
  {
    name: alertPropertyTypes.OBSERVABLE_TYPES_FILTER,
    label: "Observable Types",
    type: filterTypes.MULTISELECT,
    store: useObservableTypeStore,
    stringRepr: (filter: observableTypeRead[]) => {
      return filter
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
    name: alertPropertyTypes.OBSERVABLE_VALUE_FILTER,
    label: "Observable Value",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: alertPropertyTypes.OWNER_FILTER,
    label: "Owner",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertPropertyTypes.QUEUE_FILTER,
    label: "Queue",
    type: filterTypes.SELECT,
    store: useAlertQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TAGS_FILTER,
    label: "Tags",
    type: filterTypes.CHIPS,
    store: useNodeTagStore,
    stringRepr: (filter: string[]) => {
      return filter
        .map(function (elem) {
          return elem;
        })
        .join();
    },
    parseStringRepr: (valueString: string) => {
      return valueString.split(",");
    },
  },
  {
    name: alertPropertyTypes.THREAT_ACTOR_FILTER,
    label: "Threat Actor",
    type: filterTypes.SELECT,
    store: useNodeThreatActorStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.THREATS_FILTER,
    label: "Threats",
    type: filterTypes.MULTISELECT,
    store: useNodeThreatStore,
    stringRepr: (filter: nodeThreatRead[]) => {
      return filter
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
    name: alertPropertyTypes.TOOL_FILTER,
    label: "Tool",
    type: filterTypes.SELECT,
    store: useAlertToolStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TOOL_INSTANCE_FILTER,
    label: "Tool Instance",
    type: filterTypes.SELECT,
    store: useAlertToolInstanceStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TYPE_FILTER,
    label: "Type",
    type: filterTypes.SELECT,
    store: useAlertTypeStore,
    optionProperty: "value",
    valueProperty: "value",
  },
] as const;

export const alertRangeFilters = {
  "Event Time": {
    start: alertPropertyTypes.EVENT_TIME_AFTER_FILTER,
    end: alertPropertyTypes.EVENT_TIME_BEFORE_FILTER,
  },
  "Insert Time": {
    start: alertPropertyTypes.INSERT_TIME_AFTER_FILTER,
    end: alertPropertyTypes.INSERT_TIME_BEFORE_FILTER,
  },
  "Disposition Time": {
    start: alertPropertyTypes.DISPOSITIONED_AFTER_FILTER,
    end: alertPropertyTypes.DISPOSITIONED_BEFORE_FILTER,
  },
};

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
  type: filterTypes.DATE,
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
  type: filterTypes.DATE,
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
  type: filterTypes.DATE,
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
  type: filterTypes.DATE,
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
  type: filterTypes.DATE,
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
  type: filterTypes.DATE,
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
  type: filterTypes.MULTISELECT,
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
  type: filterTypes.INPUT_TEXT,
};

const eventOwnerProperty: filterOption = {
  name: eventPropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: filterTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};

const eventPreventionToolsProperty: filterOption = {
  name: eventPropertyTypes.PREVENTION_TOOLS_PROPERTY,
  label: "Prevention Tools",
  type: filterTypes.MULTISELECT,
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
  type: filterTypes.SELECT,
  store: useEventRiskLevelStore,
  optionProperty: "value",
  valueProperty: "value",
};

const eventStatusProperty: filterOption = {
  name: eventPropertyTypes.STATUS_PROPERTY,
  label: "Status",
  type: filterTypes.SELECT,
  store: useEventStatusStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventThreatActorsProperty: filterOption = {
  name: eventPropertyTypes.THREAT_ACTORS_PROPERTY,
  label: "Threat Actors",
  type: filterTypes.MULTISELECT,
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
  type: filterTypes.MULTISELECT,
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
  type: filterTypes.SELECT,
  store: useEventTypeStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventVectorsProperty: filterOption = {
  name: eventPropertyTypes.VECTORS_PROPERTY,
  label: "Vectors",
  type: filterTypes.MULTISELECT,
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
    type: filterTypes.DATE,
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
    type: filterTypes.DATE,
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
    type: filterTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventNameProperty,
  {
    name: eventPropertyTypes.OBSERVABLE_PROPERTY,
    label: "Observable",
    type: filterTypes.CATEGORIZED_VALUE,
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
    type: filterTypes.MULTISELECT,
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
    type: filterTypes.INPUT_TEXT,
  },
  eventOwnerProperty,
  eventPreventionToolsProperty,
  {
    name: eventPropertyTypes.QUEUE_PROPERTY,
    label: "Queue",
    type: filterTypes.SELECT,
    store: useEventQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventRiskLevelProperty,
  {
    name: eventPropertyTypes.SOURCE_PROPERTY,
    label: "Source",
    type: filterTypes.SELECT,
    store: useEventSourceStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  eventStatusProperty,
  {
    name: eventPropertyTypes.TAGS_PROPERTY,
    label: "Tags",
    type: filterTypes.CHIPS,
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
