import { propertyOption } from "@/models/base";
import { nodeThreatRead } from "@/models/nodeThreat";
import { useAlertDispositionStore } from "@/stores/alertDisposition";
import { useAlertToolStore } from "@/stores/alertTool";
import { useAlertToolInstanceStore } from "@/stores/alertToolInstance";
import { useAlertTypeStore } from "@/stores/alertType";
import { useNodeTagStore } from "@/stores/nodeTag";
import { useNodeThreatStore } from "@/stores/nodeThreat";
import { useNodeThreatActorStore } from "@/stores/nodeThreatActor";
import { useUserStore } from "@/stores/user";
import {
  nameProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  queueProperty,
} from "./common";
import { inputTypes } from "./base";

// ** Alerts ** //

// NOTE: If alerts and events share a property name (like how they both originally had the "type" property),
// care must be taken... The event type field is queueable, whereas the alert type field is not. This will
// cause issues in the "formatNodeFiltersForAPI" function when you have properties that share a name but
// one is queueable and the other not. The fix for this is to rename the fields. So now there is the "alertType"
// property and the "eventType" property.

export const alertPropertyTypes: Record<string, string> = {
  ALERT_TYPE_PROPERTY: "alertType",
  DISPOSITION_PROPERTY: "disposition",
  DISPOSITION_USER_PROPERTY: "dispositionUser",
  DISPOSITIONED_AFTER_PROPERTY: "dispositionedAfter",
  DISPOSITIONED_BEFORE_PROPERTY: "dispositionedBefore",
  EVENT_UUID_PROPERTY: "eventUuid",
  EVENT_TIME_AFTER_PROPERTY: "eventTimeAfter",
  EVENT_TIME_BEFORE_PROPERTY: "eventTimeBefore",
  INSERT_TIME_AFTER_PROPERTY: "insertTimeAfter",
  INSERT_TIME_BEFORE_PROPERTY: "insertTimeBefore",
  QUEUE_PROPERTY: "queue",
  TOOL_PROPERTY: "tool",
  TOOL_INSTANCE_PROPERTY: "toolInstance",
};

export const alertDispositionProperty: propertyOption = {
  name: alertPropertyTypes.DISPOSITION_PROPERTY,
  label: "Disposition",
  type: inputTypes.SELECT,
  store: useAlertDispositionStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const alertDispositionUserProperty: propertyOption = {
  name: alertPropertyTypes.DISPOSITION_USER_PROPERTY,
  label: "Dispositioned By",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};

export const alertDispositionedAfterProperty: propertyOption = {
  name: alertPropertyTypes.DISPOSITIONED_AFTER_PROPERTY,
  label: "Dispositioned After (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const alertDispositionedBeforeProperty: propertyOption = {
  name: alertPropertyTypes.DISPOSITIONED_BEFORE_PROPERTY,
  label: "Dispositioned Before (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};
export const alertEventTimeAfterProperty: propertyOption = {
  name: alertPropertyTypes.EVENT_TIME_AFTER_PROPERTY,
  label: "Event Time After (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const alertEventTimeBeforeProperty: propertyOption = {
  name: alertPropertyTypes.EVENT_TIME_BEFORE_PROPERTY,
  label: "Event Time Before (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const alertInsertTimeBeforeProperty: propertyOption = {
  name: alertPropertyTypes.INSERT_TIME_BEFORE_PROPERTY,
  label: "Insert Time Before (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const alertInsertTimeAfterProperty: propertyOption = {
  name: alertPropertyTypes.INSERT_TIME_AFTER_PROPERTY,
  label: "Insert Time After (UTC)",
  type: inputTypes.DATE,
  stringRepr: (filter: Date) => {
    return filter.toISOString().slice(0, -5);
  },
  displayRepr: (filter: Date) => {
    const d = filter.toISOString().slice(0, -5);
    return `${d} (UTC)`;
  },
  parseStringRepr: (valueString: string) => {
    return new Date(valueString);
  },
};

export const alertOwnerProperty: propertyOption = {
  name: alertPropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};
export const alertTagsProperty: propertyOption = {
  name: alertPropertyTypes.TAGS_PROPERTY,
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
};

export const alertThreatActorProperty: propertyOption = {
  name: alertPropertyTypes.THREAT_ACTOR_PROPERTY,
  label: "Threat Actor",
  type: inputTypes.SELECT,
  store: useNodeThreatActorStore,
  optionProperty: "value",
  valueProperty: "value",
};
export const alertThreatsProperty: propertyOption = {
  name: alertPropertyTypes.THREATS_PROPERTY,
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

export const alertToolProperty: propertyOption = {
  name: alertPropertyTypes.TOOL_PROPERTY,
  label: "Tool",
  type: inputTypes.SELECT,
  store: useAlertToolStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const alertToolInstanceProperty: propertyOption = {
  name: alertPropertyTypes.TOOL_INSTANCE_PROPERTY,
  label: "Tool Instance",
  type: inputTypes.SELECT,
  store: useAlertToolInstanceStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const alertTypeProperty: propertyOption = {
  name: alertPropertyTypes.ALERT_TYPE_PROPERTY,
  label: "Type",
  type: inputTypes.SELECT,
  store: useAlertTypeStore,
  optionProperty: "value",
  valueProperty: "value",
};

export const validAlertFilters: propertyOption[] = [
  alertDispositionProperty,
  alertDispositionUserProperty,
  alertDispositionedAfterProperty,
  alertDispositionedBeforeProperty,
  alertEventTimeAfterProperty,
  alertEventTimeBeforeProperty,
  alertInsertTimeAfterProperty,
  alertInsertTimeBeforeProperty,
  nameProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  queueProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  alertToolProperty,
  alertToolInstanceProperty,
  alertTypeProperty,
];
