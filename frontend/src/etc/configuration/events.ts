import { propertyOption, columnOption } from "@/models/base";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  nodeCommentProperty,
  queueProperty,
} from "@/etc/constants/base";
import {
  eventPropertyTypes,
  eventAlertTimeProperty,
  eventContainTimeProperty,
  eventCreatedAfterProperty,
  eventCreatedBeforeProperty,
  eventDispositionProperty,
  eventDispositionTimeProperty,
  eventEventTimeProperty,
  eventOwnershipTimeProperty,
  eventPreventionToolsProperty,
  eventRemediationProperty,
  eventRemediationTimeProperty,
  eventRiskLevelProperty,
  eventSourceProperty,
  eventStatusProperty,
  eventTypeProperty,
  eventVectorsProperty,
} from "@/etc/constants/events";

export const eventFilters: readonly propertyOption[] = [
  eventDispositionProperty,
  nameProperty,
  observableProperty,
  eventCreatedAfterProperty,
  eventCreatedBeforeProperty,
  observableTypesProperty,
  observableProperty,
  observableValueProperty,
  ownerProperty,
  eventPreventionToolsProperty,
  queueProperty,
  eventRiskLevelProperty,
  eventSourceProperty,
  eventStatusProperty,
  nodeTagsProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  eventTypeProperty,
  eventVectorsProperty,
] as const;

export const eventEditableProperties: readonly propertyOption[] = [
  nameProperty,
  ownerProperty,
  nodeCommentProperty,
  eventRemediationProperty,
  eventPreventionToolsProperty,
  eventRiskLevelProperty,
  eventStatusProperty,
  nodeThreatActorProperty,
  nodeThreatsProperty,
  eventTypeProperty,
  eventVectorsProperty,
  eventEventTimeProperty,
  eventAlertTimeProperty,
  eventOwnershipTimeProperty,
  eventDispositionTimeProperty,
  eventContainTimeProperty,
  eventRemediationTimeProperty,
];
export const eventRangeFilters = {
  "Created Time": {
    start: eventPropertyTypes.CREATED_AFTER_PROPERTY,
    end: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
  },
};

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
    { field: "threats", header: "Threats", sortable: false, default: true },
    { field: "type", header: "Type", sortable: true, default: false },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: true,
    },
    // dispo?
    {
      field: "preventionTools",
      header: "Prevention Tools",
      sortable: false,
      default: true,
    },
    {
      field: "remediations",
      header: "Remediation",
      sortable: true,
      default: true,
    },
    { field: "status", header: "Status", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: true },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
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
    {
      field: "threatActors",
      header: "Threat Actors",
      sortable: false,
      default: false,
    },
    { field: "threats", header: "Threats", sortable: false, default: false },
    { field: "type", header: "Type", sortable: true, default: true },
    {
      field: "riskLevel",
      header: "Risk Level",
      sortable: true,
      default: false,
    },
    // dispo?
    {
      field: "preventionTools",
      header: "Prevention Tools",
      sortable: false,
      default: false,
    },
    {
      field: "remediations",
      header: "Remediation",
      sortable: true,
      default: true,
    },
    { field: "status", header: "Status", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: false },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
  ],
};
