import { alertFilterNameTypes } from "@/models/alert";
import { filterOption } from "@/models/base";
import { eventFilterNameTypes } from "@/models/event";
import { eventPreventionToolRead } from "@/models/eventPreventionTool";
import { nodeTagRead } from "@/models/nodeTag";
import { nodeThreatRead } from "@/models/nodeThreat";
import { observableTypeRead } from "@/models/observableType";

import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
import { useEventStore } from "@/stores/event";
import { useEventPreventionToolStore } from "@/stores/eventPreventionTool";
import { useEventQueueStore } from "@/stores/eventQueue";
import { useEventRiskLevelStore } from "@/stores/eventRiskLevel";
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

export const alertFilterNames: Record<string, alertFilterNameTypes> = {
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
    name: alertFilterNames.DISPOSITION_FILTER,
    label: "Disposition",
    type: filterTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertFilterNames.DISPOSITION_USER_FILTER,
    label: "Dispositioned By",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertFilterNames.DISPOSITIONED_AFTER_FILTER,
    label: "Dispositioned After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.DISPOSITIONED_BEFORE_FILTER,
    label: "Dispositioned Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.EVENT_UUID_FILTER,
    label: "Event",
    type: filterTypes.SELECT,
    store: useEventStore,
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.EVENT_TIME_AFTER_FILTER,
    label: "Event Time After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.EVENT_TIME_BEFORE_FILTER,
    label: "Event Time Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.INSERT_TIME_AFTER_FILTER,
    label: "Insert Time After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.INSERT_TIME_BEFORE_FILTER,
    label: "Insert Time Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: alertFilterNames.NAME_FILTER,
    label: "Name",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: alertFilterNames.OBSERVABLE_FILTER,
    label: "Observable",
    type: filterTypes.CATEGORIZED_VALUE,
    store: useObservableTypeStore,
    stringRepr: (filter: { category: observableTypeRead; value: string }) => {
      return `${filter.category.value}|${filter.value}`;
    },
    parseStringRepr: (filterString: string) => {
      const [category, value] = filterString.split("|");
      return { category: category, value: value };
    },
  },
  {
    name: alertFilterNames.OBSERVABLE_TYPES_FILTER,
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
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: alertFilterNames.OBSERVABLE_VALUE_FILTER,
    label: "Observable Value",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: alertFilterNames.OWNER_FILTER,
    label: "Owner",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertFilterNames.QUEUE_FILTER,
    label: "Queue",
    type: filterTypes.SELECT,
    store: useAlertQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertFilterNames.TAGS_FILTER,
    label: "Tags",
    type: filterTypes.CHIPS,
    store: useNodeTagStore,
    stringRepr: (filter: nodeTagRead[]) => {
      return filter
        .map(function (elem) {
          return elem;
        })
        .join();
    },
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: alertFilterNames.THREAT_ACTOR_FILTER,
    label: "Threat Actor",
    type: filterTypes.SELECT,
    store: useNodeThreatActorStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertFilterNames.THREATS_FILTER,
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
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: alertFilterNames.TOOL_FILTER,
    label: "Tool",
    type: filterTypes.SELECT,
    store: useAlertToolStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertFilterNames.TOOL_INSTANCE_FILTER,
    label: "Tool Instance",
    type: filterTypes.SELECT,
    store: useAlertToolInstanceStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertFilterNames.TYPE_FILTER,
    label: "Type",
    type: filterTypes.SELECT,
    store: useAlertTypeStore,
    optionProperty: "value",
    valueProperty: "value",
  },
] as const;

export const alertRangeFilters = {
  "Event Time": {
    start: alertFilterNames.EVENT_TIME_AFTER_FILTER,
    end: alertFilterNames.EVENT_TIME_BEFORE_FILTER,
  },
  "Insert Time": {
    start: alertFilterNames.INSERT_TIME_AFTER_FILTER,
    end: alertFilterNames.INSERT_TIME_BEFORE_FILTER,
  },
  "Disposition Time": {
    start: alertFilterNames.DISPOSITIONED_AFTER_FILTER,
    end: alertFilterNames.DISPOSITIONED_BEFORE_FILTER,
  },
};

// ** Events ** //

export const eventFilterNames: Record<string, eventFilterNameTypes> = {
  CREATED_AFTER_FILTER: "createdAfter",
  CREATED_BEFORE_FILTER: "createdBefore",
  DISPOSITION_FILTER: "disposition",
  OBSERVABLE_TYPES_FILTER: "observableTypes",
  OBSERVABLE_VALUE_FILTER: "observableValue",
  OWNER_FILTER: "owner",
  PREVENTION_TOOLS_FILTER: "preventionTools",
  QUEUE_FILTER: "queue",
  RISK_LEVEL_FILTER: "riskLevel",
  STATUS_FILTER: "status",
  TAGS_FILTER: "tags",
  THREAT_ACTOR_FILTER: "threatActor",
  THREATS_FILTER: "threats",
  TYPE_FILTER: "type",
  VECTOR_FILTER: "vector",
};

export const eventFilters: readonly filterOption[] = [
  {
    name: eventFilterNames.CREATED_AFTER_FILTER,
    label: "Created After",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: eventFilterNames.CREATED_BEFORE_FILTER,
    label: "Created Before",
    type: filterTypes.DATE,
    stringRepr: (filter: Date) => {
      return filter.toISOString();
    },
    parseStringRepr: (filterString: string) => {
      return new Date(filterString);
    },
  },
  {
    name: eventFilterNames.DISPOSITION_FILTER,
    label: "Disposition",
    type: filterTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.OBSERVABLE_FILTER,
    label: "Observable",
    type: filterTypes.CATEGORIZED_VALUE,
    store: useObservableTypeStore,
    stringRepr: (filter: { category: observableTypeRead; value: string }) => {
      return `${filter.category.value}|${filter.value}`;
    },
    parseStringRepr: (filterString: string) => {
      const [category, value] = filterString.split("|");
      return { category: category, value: value };
    },
  },
  {
    name: eventFilterNames.OBSERVABLE_TYPES_FILTER,
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
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: eventFilterNames.OBSERVABLE_VALUE_FILTER,
    label: "Observable Value",
    type: filterTypes.INPUT_TEXT,
  },
  {
    name: eventFilterNames.OWNER_FILTER,
    label: "Owner",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: eventFilterNames.PREVENTION_TOOLS_FILTER,
    label: "Prevention Tools",
    type: filterTypes.MULTISELECT,
    store: useEventPreventionToolStore,
    stringRepr: (filter: eventPreventionToolRead[]) => {
      return filter
        .map(function (elem) {
          return elem.value;
        })
        .join();
    },
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: eventFilterNames.QUEUE_FILTER,
    label: "Queue",
    type: filterTypes.SELECT,
    store: useEventQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.RISK_LEVEL_FILTER,
    label: "Risk Level",
    type: filterTypes.SELECT,
    store: useEventRiskLevelStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.STATUS_FILTER,
    label: "Status",
    type: filterTypes.SELECT,
    store: useEventStatusStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.TAGS_FILTER,
    label: "Tags",
    type: filterTypes.CHIPS,
    store: useNodeTagStore,
    stringRepr: (filter: nodeTagRead[]) => {
      return filter
        .map(function (elem) {
          return elem.value;
        })
        .join();
    },
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: eventFilterNames.THREAT_ACTOR_FILTER,
    label: "Threat Actor",
    type: filterTypes.SELECT,
    store: useNodeThreatActorStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.THREATS_FILTER,
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
    parseStringRepr: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: eventFilterNames.TYPE_FILTER,
    label: "Type",
    type: filterTypes.SELECT,
    store: useEventTypeStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: eventFilterNames.VECTOR_FILTER,
    label: "Vector",
    type: filterTypes.SELECT,
    store: useEventVectorStore,
    optionProperty: "value",
    valueProperty: "value",
  },
] as const;

export const eventRangeFilters = {
  "Created Time": {
    start: eventFilterNames.CREATED_AFTER_FILTER,
    end: eventFilterNames.CREATED_BEFORE_FILTER,
  },
};
