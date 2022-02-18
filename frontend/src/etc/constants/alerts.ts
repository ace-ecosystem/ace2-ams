import { filterOption } from "@/models/base";
import { nodeThreatRead } from "@/models/nodeThreat";
import { observableTypeRead } from "@/models/observableType";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertQueueStore } from "@/stores/alertQueue";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
import { useNodeTagStore } from "@/stores/nodeTag";
import { useNodeThreatStore } from "@/stores/nodeThreat";
import { useNodeThreatActorStore } from "@/stores/nodeThreatActor";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { inputTypes } from "./base";

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
    type: inputTypes.SELECT,
    store: useAlertDispositionStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.DISPOSITION_USER_FILTER,
    label: "Dispositioned By",
    type: inputTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertPropertyTypes.DISPOSITIONED_AFTER_FILTER,
    label: "Dispositioned After",
    type: inputTypes.DATE,
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
    type: inputTypes.DATE,
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
    type: inputTypes.DATE,
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
    type: inputTypes.DATE,
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
    type: inputTypes.DATE,
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
    type: inputTypes.DATE,
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
    type: inputTypes.INPUT_TEXT,
  },
  {
    name: alertPropertyTypes.OBSERVABLE_FILTER,
    label: "Observable",
    type: inputTypes.CATEGORIZED_VALUE,
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
    type: inputTypes.MULTISELECT,
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
    type: inputTypes.INPUT_TEXT,
  },
  {
    name: alertPropertyTypes.OWNER_FILTER,
    label: "Owner",
    type: inputTypes.SELECT,
    store: useUserStore,
    optionProperty: "displayName",
    valueProperty: "username",
  },
  {
    name: alertPropertyTypes.QUEUE_FILTER,
    label: "Queue",
    type: inputTypes.SELECT,
    store: useAlertQueueStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TAGS_FILTER,
    label: "Tags",
    type: inputTypes.CHIPS,
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
    type: inputTypes.SELECT,
    store: useNodeThreatActorStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.THREATS_FILTER,
    label: "Threats",
    type: inputTypes.MULTISELECT,
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
    type: inputTypes.SELECT,
    store: useAlertToolStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TOOL_INSTANCE_FILTER,
    label: "Tool Instance",
    type: inputTypes.SELECT,
    store: useAlertToolInstanceStore,
    optionProperty: "value",
    valueProperty: "value",
  },
  {
    name: alertPropertyTypes.TYPE_FILTER,
    label: "Type",
    type: inputTypes.SELECT,
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
