import { propertyOption, columnOption } from "@/models/base";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  ownerProperty,
  tagsProperty,
  nodeThreatsProperty,
  nodeCommentProperty,
  queueProperty,
} from "@/etc/constants/common";
import {
  eventPropertyTypes,
  eventCreatedAfterProperty,
  eventCreatedBeforeProperty,
  eventEventTimeProperty,
  eventRemediationProperty,
  eventStatusProperty,
  eventPreventionToolsProperty,
} from "@/etc/constants/events";

import EventSummaryVue from "@/components/Events/EventSummary.vue";
import EventAlertsTableVue from "@/components/Events/EventAlertsTable.vue";
import EventURLSummaryVue from "@/components/Events/EventURLSummary.vue";
import EventURLDomainSummaryVue from "@/components/Events/EventURLDomainSummary.vue";
import EventObservableSummaryVue from "@/components/Events/EventObservableSummary.vue";
import EventDetectionsSummaryVue from "@/components/Events/EventDetectionsSummary.vue";

export const eventFilters: Record<string, readonly propertyOption[]> = {
  external: [
    nameProperty,
    eventCreatedAfterProperty,
    eventCreatedBeforeProperty,
    observableProperty,
    observableTypesProperty,
    ownerProperty,
    queueProperty, // Required, do not delete
    tagsProperty,
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

export const eventEditableProperties: Record<string, propertyOption[]> = {
  external: [
    nameProperty,
    ownerProperty,
    nodeCommentProperty,
    eventPreventionToolsProperty,
    eventRemediationProperty,
    nodeThreatsProperty,
    eventEventTimeProperty,
  ],
  intel: [
    nameProperty,
    ownerProperty,
    nodeCommentProperty,
    eventPreventionToolsProperty,
    eventRemediationProperty,
    nodeThreatsProperty,
    eventEventTimeProperty,
  ],
  internal: [
    nameProperty,
    ownerProperty,
    nodeCommentProperty,
    eventRemediationProperty,
    nodeThreatsProperty,
    eventEventTimeProperty,
  ],
};

export const eventRangeFilters = {
  "Created Time (UTC)": {
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
      field: "severity",
      header: "Severity",
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
      field: "severity",
      header: "Severity",
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
      field: "severity",
      header: "Severity",
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

export const faqueue = {
  lowHits: 1,
  mediumHits: 500,
};

export const defaultEventDetailsSections = {
  "Event Summary": EventSummaryVue,
  "Alert Summary": EventAlertsTableVue,
  "Detection Summary": EventDetectionsSummaryVue,
  "URL Summary": EventURLSummaryVue,
  "URL Domain Summary": EventURLDomainSummaryVue,
  "Observable Summary": EventObservableSummaryVue,
};

export const closedEventStatus = "CLOSED";
