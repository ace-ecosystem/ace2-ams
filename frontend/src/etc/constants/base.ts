// ** Base ** //

import { propertyOption } from "@/models/base";
import { nodeThreatRead } from "@/models/nodeThreat";
import { observableTypeRead } from "@/models/observableType";
import { useNodeTagStore } from "@/stores/nodeTag";
import { useNodeThreatStore } from "@/stores/nodeThreat";
import { useNodeThreatActorStore } from "@/stores/nodeThreatActor";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { useQueueStore } from "@/stores/queue";

export const inputTypes = {
  MULTISELECT: "multiselect",
  CHIPS: "chips",
  SELECT: "select",
  DATE: "date",
  INPUT_TEXT: "inputText",
  CATEGORIZED_VALUE: "categorizedValue",
};

// Property types common between node types
export const nodePropertyTypes: Record<string, string> = {
  NAME_PROPERTY: "name",
  OBSERVABLE_PROPERTY: "observable",
  OBSERVABLE_TYPES_PROPERTY: "observableTypes",
  OBSERVABLE_VALUE_PROPERTY: "observableValue",
  OWNER_PROPERTY: "owner",
  QUEUE_PROPERTY: "queue",
  COMMENTS_PROPERTY: "comments",
  TAGS_PROPERTY: "tags",
  THREAT_ACTOR_PROPERTY: "threatActors",
  THREATS_PROPERTY: "threats",
};

export const nodeNameProperty: propertyOption = {
  name: nodePropertyTypes.NAME_PROPERTY,
  label: "Name",
  type: inputTypes.INPUT_TEXT,
};

export const nodeCommentProperty: propertyOption = {
  name: nodePropertyTypes.COMMENTS_PROPERTY,
  label: "Comment",
  type: inputTypes.INPUT_TEXT,
};

export const nodeObservableProperty: propertyOption = {
  name: nodePropertyTypes.OBSERVABLE_PROPERTY,
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
};

export const nodeObservableTypesProperty: propertyOption = {
  name: nodePropertyTypes.OBSERVABLE_TYPES_PROPERTY,
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
};
export const nodeObservableValueProperty: propertyOption = {
  name: nodePropertyTypes.OBSERVABLE_VALUE_PROPERTY,
  label: "Observable Value",
  type: inputTypes.INPUT_TEXT,
};

export const nodeOwnerProperty: propertyOption = {
  name: nodePropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};

export const nodeThreatActorProperty: propertyOption = {
  name: nodePropertyTypes.THREAT_ACTOR_PROPERTY,
  label: "Threat Actor",
  type: inputTypes.SELECT,
  store: useNodeThreatActorStore,
  optionProperty: "value",
  valueProperty: "value",
};
export const nodeThreatsProperty: propertyOption = {
  name: nodePropertyTypes.THREATS_PROPERTY,
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
};
export const nodeTagsProperty: propertyOption = {
  name: nodePropertyTypes.TAGS_PROPERTY,
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
};

export const nodeQueueProperty: propertyOption = {
  name: nodePropertyTypes.QUEUE_PROPERTY,
  label: "Queue",
  type: inputTypes.SELECT,
  store: useQueueStore,
  optionProperty: "value",
  valueProperty: "value",
};