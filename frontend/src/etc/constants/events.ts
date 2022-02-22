import { columnOption } from "./../../models/base";
import { eventRemediationRead } from "../../models/eventRemediation";
import { propertyOption } from "@/models/base";
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
const eventEventTimeProperty: propertyOption = {
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
const eventAlertTimeProperty: propertyOption = {
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
const eventOwnershipTimeProperty: propertyOption = {
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
const eventDispositionTimeProperty: propertyOption = {
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
const eventContainTimeProperty: propertyOption = {
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
const eventRemediationTimeProperty: propertyOption = {
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
const eventRemediationProperty: propertyOption = {
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
const eventNameProperty: propertyOption = {
  name: eventPropertyTypes.NAME_PROPERTY,
  label: "Name",
  type: inputTypes.INPUT_TEXT,
};
const eventOwnerProperty: propertyOption = {
  name: eventPropertyTypes.OWNER_PROPERTY,
  label: "Owner",
  type: inputTypes.SELECT,
  store: useUserStore,
  optionProperty: "displayName",
  valueProperty: "username",
};
const eventCommentProperty: propertyOption = {
  name: eventPropertyTypes.COMMENTS_PROPERTY,
  label: "Comment",
  type: inputTypes.INPUT_TEXT,
};
const eventPreventionToolsProperty: propertyOption = {
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
const eventRiskLevelProperty: propertyOption = {
  name: eventPropertyTypes.RISK_LEVEL_PROPERTY,
  label: "Risk Level",
  type: inputTypes.SELECT,
  store: useEventRiskLevelStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventStatusProperty: propertyOption = {
  name: eventPropertyTypes.STATUS_PROPERTY,
  label: "Status",
  type: inputTypes.SELECT,
  store: useEventStatusStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventThreatActorsProperty: propertyOption = {
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
const eventThreatsProperty: propertyOption = {
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
const eventTypeProperty: propertyOption = {
  name: eventPropertyTypes.TYPE_PROPERTY,
  label: "Type",
  type: inputTypes.SELECT,
  store: useEventTypeStore,
  optionProperty: "value",
  valueProperty: "value",
};
const eventVectorsProperty: propertyOption = {
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

export const eventEditableProperties: readonly propertyOption[] = [
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

export const eventFilters: readonly propertyOption[] = [
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

export const eventQueueOptions = ["default", "secondary_queue"];

export const eventQueueColumnMappings: Record<string, columnOption[]> = {
  default: [
    {
      field: "edit",
      header: "",
      sortable: false,
      required: true,
    },
    { field: "createdTime", header: "Created", sortable: true, default: true },
    { field: "name", header: "Name", sortable: true, default: true },
    {
      field: "threatActors",
      header: "Threat Actors",
      sortable: false,
      default: false,
    },
    { field: "type", header: "Type", sortable: true, default: true },
    {
      field: "remediations",
      header: "Remediation",
      sortable: true,
      default: true,
    },
    { field: "threats", header: "Threats", sortable: false, default: false },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: true,
    },
    {
      field: "preventionTools",
      header: "Prevention Tools",
      sortable: false,
      default: false,
    },
    { field: "status", header: "Status", sortable: true, default: false },
    { field: "owner", header: "Owner", sortable: true, default: true },
    { field: "vectors", header: "Vectors", sortable: false, default: true },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: false,
    },
  ],
  secondary_queue: [
    {
      field: "edit",
      header: "",
      sortable: false,
      required: true,
    },
    { field: "createdTime", header: "Created", sortable: true, default: true },
    { field: "name", header: "Name", sortable: true, default: true },
    { field: "type", header: "Type", sortable: true, default: true },
    {
      field: "remediations",
      header: "Remediation",
      sortable: true,
      default: true,
    },
    { field: "status", header: "Status", sortable: true, default: false },
    { field: "owner", header: "Owner", sortable: true, default: false },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
    {
      field: "threatActors",
      header: "Threat Actors",
      sortable: false,
      default: false,
    },
    { field: "threats", header: "Threats", sortable: false, default: false },
    {
      field: "preventionTools",
      header: "Prevention Tools",
      sortable: false,
      default: false,
    },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: false,
    },
  ],
};
