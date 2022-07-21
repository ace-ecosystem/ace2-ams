// ** Base ** //

import { propertyOption } from "@/models/base";
import { threatRead } from "@/models/threat";
import { observableTypeRead } from "@/models/observableType";
import { useMetadataTagStore } from "@/stores/metadataTag";
import { useThreatStore } from "@/stores/threat";
import { useThreatActorStore } from "@/stores/threatActor";
import { useObservableTypeStore } from "@/stores/observableType";
import { useUserStore } from "@/stores/user";
import { useQueueStore } from "@/stores/queue";
import { inputTypes } from "./base";

// Property types common between various resources or object types
export const commonPropertyTypes: Record<string, string> = {
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

export const nameProperty: propertyOption = {
  name: commonPropertyTypes.NAME_PROPERTY,
  label: "Name",
  type: inputTypes.INPUT_TEXT,
};

export const commentProperty: propertyOption = {
  name: commonPropertyTypes.COMMENTS_PROPERTY,
  label: "Comment",
  type: inputTypes.INPUT_TEXT,
};

export const observableProperty: propertyOption = {
  name: commonPropertyTypes.OBSERVABLE_PROPERTY,
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

export const observableTypesProperty: propertyOption = {
  name: commonPropertyTypes.OBSERVABLE_TYPES_PROPERTY,
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
export const observableValueProperty: propertyOption = {
  name: commonPropertyTypes.OBSERVABLE_VALUE_PROPERTY,
  label: "Observable Value",
  type: inputTypes.INPUT_TEXT,
};

export const ownerProperty: propertyOption = {
  name: commonPropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
  nullOptions: {
    nullOption: { displayName: "None", username: "none" },
    nullableFilter: true,
    nullableEdit: false,
  },
};

export const threatActorProperty: propertyOption = {
  name: commonPropertyTypes.THREAT_ACTOR_PROPERTY,
  label: "Threat Actor",
  type: inputTypes.SELECT,
  store: useThreatActorStore,
  queueDependent: true,

  optionProperty: "value",
  valueProperty: "value",
};
export const threatsProperty: propertyOption = {
  name: commonPropertyTypes.THREATS_PROPERTY,
  label: "Threats",
  type: inputTypes.MULTISELECT,
  store: useThreatStore,
  queueDependent: true,

  stringRepr: (filter: threatRead[]) => {
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
export const tagsProperty: propertyOption = {
  name: commonPropertyTypes.TAGS_PROPERTY,
  label: "Tags",
  type: inputTypes.CHIPS,
  store: useMetadataTagStore,
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

export const queueProperty: propertyOption = {
  name: commonPropertyTypes.QUEUE_PROPERTY,
  label: "Queue",
  type: inputTypes.SELECT,
  store: useQueueStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const WHITE = "#FFFFFF";
export const RED = "#FF0000";
export const BLUE = "#00BFFF";
export const GREEN = "#32CD32";
export const ORANGE = "#FF8C00";
