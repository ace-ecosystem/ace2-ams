import { propertyOption, columnOption } from "@/models/base";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  ownerProperty,
  nodeTagsProperty,
  nodeThreatsProperty,
  nodeCommentProperty,
  queueProperty,
} from "@/etc/constants/base";
import {
  eventPropertyTypes,
  eventCreatedAfterProperty,
  eventCreatedBeforeProperty,
  eventEventTimeProperty,
  eventRemediationProperty,
  eventStatusProperty,
} from "@/etc/constants/events";

export const eventFilters: Record<string, readonly propertyOption[]> = {
  external: [
    nameProperty,
    eventCreatedAfterProperty,
    eventCreatedBeforeProperty,
    observableProperty,
    observableTypesProperty,
    ownerProperty,
    queueProperty, // Required, do not delete
    nodeTagsProperty,
    eventStatusProperty, // Required, do not delete
  ],
  internal: [
    nameProperty,
    eventCreatedAfterProperty,
    eventCreatedBeforeProperty,
    observableProperty,
    observableTypesProperty,
    queueProperty, // Required, do not delete
    eventStatusProperty, // Required, do not delete
  ],
} as const;

export const eventEditableProperties: readonly propertyOption[] = [
  nameProperty,
  ownerProperty,
  nodeCommentProperty,
  eventRemediationProperty,
  nodeThreatsProperty,
  eventEventTimeProperty,
];
export const eventRangeFilters = {
  "Created Time": {
    start: eventPropertyTypes.CREATED_AFTER_PROPERTY,
    end: eventPropertyTypes.CREATED_BEFORE_PROPERTY,
  },
};

export const eventQueueColumnMappings: Record<string, columnOption[]> = {
  external: [
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
      sortable: false,
      default: true,
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
      default: false,
    },
    { field: "status", header: "Status", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: true },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
    { field: "queue", header: "Queue", sortable: true, default: false },
  ],
  internal: [
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
      default: false,
    },
    { field: "status", header: "Status", sortable: true, default: false },
    { field: "owner", header: "Owner", sortable: true, default: false },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
    { field: "queue", header: "Queue", sortable: true, default: false },
  ],
  intel: [
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
      sortable: false,
      default: true,
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
      default: false,
    },
    { field: "status", header: "Status", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: true },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
    { field: "queue", header: "Queue", sortable: true, default: false },
  ],
};
