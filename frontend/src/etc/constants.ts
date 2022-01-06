import { alertFilterNameTypes } from "@/models/alert";
import { filterOption } from "@/models/base";
import { alertDispositionRead } from "@/models/alertDisposition";
import { alertQueueRead } from "@/models/alertQueue";
import { alertToolRead } from "@/models/alertTool";
import { alertToolInstanceRead } from "@/models/alertToolInstance";
import { alertTypeRead } from "@/models/alertType";
import { nodeTagRead } from "@/models/nodeTag";
import { nodeThreatRead } from "@/models/nodeThreat";
import { nodeThreatActorRead } from "@/models/nodeThreatActor";
import { observableTypeRead } from "@/models/observableType";
import { userRead } from "@/models/user";

import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
import { useEventStore } from "@/stores/event";
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
    formatForAPI: (filter: alertDispositionRead) => {
      return filter.value;
    },
  },
  {
    name: alertFilterNames.DISPOSITION_USER_FILTER,
    label: "Dispositioned By",
    type: filterTypes.SELECT,
    store: useUserStore,
    optionLabel: "displayName",
    valueProperty: "username",
    formatForAPI: (filter: userRead) => {
      return filter.username;
    },
  },
  {
    name: alertFilterNames.DISPOSITIONED_AFTER_FILTER,
    label: "Dispositioned After",
    type: filterTypes.DATE,
  },
  {
    name: alertFilterNames.DISPOSITIONED_BEFORE_FILTER,
    label: "Dispositioned Before",
    type: filterTypes.DATE,
  },
  {
    name: alertFilterNames.EVENT_UUID_FILTER,
    label: "Event",
    type: filterTypes.SELECT,
    store: useEventStore,
  },
  {
    name: alertFilterNames.EVENT_TIME_AFTER_FILTER,
    label: "Event Time After",
    type: filterTypes.DATE,
    
  },
  {
    name: alertFilterNames.EVENT_TIME_BEFORE_FILTER,
    label: "Event Time Before",
    type: filterTypes.DATE,
  },
  {
    name: alertFilterNames.INSERT_TIME_AFTER_FILTER,
    label: "Insert Time After",
    type: filterTypes.DATE,
  },
  {
    name: alertFilterNames.INSERT_TIME_BEFORE_FILTER,
    label: "Insert Time Before",
    type: filterTypes.DATE,
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
    formatForAPI: (filter: { category: observableTypeRead; value: string }) => {
      return `${filter.category.value}|${filter.value}`;
    },
    formatForGUI: (filterString: string) => {
      const [category, value] = filterString.split("|");
      return { category: category, value: value };
    },
  },
  {
    name: alertFilterNames.OBSERVABLE_TYPES_FILTER,
    label: "Observable Types",
    type: filterTypes.MULTISELECT,
    store: useObservableTypeStore,
    formatForAPI: (filter: observableTypeRead[]) => {
      return filter
        .map(function (elem) {
          return elem.value;
        })
        .join();
    },
    formatForGUI: (filterString: string) => {
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
    optionLabel: "displayName",
    valueProperty: "username",
    formatForAPI: (filter: userRead) => {
      return filter.username;
    },
  },
  {
    name: alertFilterNames.QUEUE_FILTER,
    label: "Queue",
    type: filterTypes.SELECT,
    store: useAlertQueueStore,
    formatForAPI: (filter: alertQueueRead) => {
      return filter.value;
    },
  },
  {
    name: alertFilterNames.TAGS_FILTER,
    label: "Tags",
    type: filterTypes.CHIPS,
    store: useNodeTagStore,
    formatForAPI: (filter: nodeTagRead[]) => {
      return filter
        .map(function (elem) {
          return elem;
        })
        .join();
    },
    formatForGUI: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: alertFilterNames.THREAT_ACTOR_FILTER,
    label: "Threat Actor",
    type: filterTypes.SELECT,
    store: useNodeThreatActorStore,
    formatForAPI: (filter: nodeThreatActorRead) => {
      return filter.value;
    },
  },
  {
    name: alertFilterNames.THREATS_FILTER,
    label: "Threats",
    type: filterTypes.MULTISELECT,
    store: useNodeThreatStore,
    formatForAPI: (filter: nodeThreatRead[]) => {
      return filter
        .map(function (elem) {
          return elem.value;
        })
        .join();
    },
    formatForGUI: (filterString: string) => {
      return filterString.split(",");
    },
  },
  {
    name: alertFilterNames.TOOL_FILTER,
    label: "Tool",
    type: filterTypes.SELECT,
    store: useAlertToolStore,
    formatForAPI: (filter: alertToolRead) => {
      return filter.value;
    },
  },
  {
    name: alertFilterNames.TOOL_INSTANCE_FILTER,
    label: "Tool Instance",
    type: filterTypes.SELECT,
    store: useAlertToolInstanceStore,
    formatForAPI: (filter: alertToolInstanceRead) => {
      return filter.value;
    },
  },
  {
    name: alertFilterNames.TYPE_FILTER,
    label: "Type",
    type: filterTypes.SELECT,
    store: useAlertTypeStore,
    formatForAPI: (filter: alertTypeRead) => {
      return filter.value;
    },
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
