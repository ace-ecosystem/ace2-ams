import { propertyOption, columnOption } from "@/models/base";
import {
  nameProperty,
  observableProperty,
  observableTypesProperty,
  observableValueProperty,
  ownerProperty,
  tagsProperty,
  threatActorProperty,
  threatsProperty,
  commentProperty,
  queueProperty,
} from "@/etc/constants/common";
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
  eventSeverityProperty,
  eventSourceProperty,
  eventStatusProperty,
  eventTypeProperty,
  eventVectorsProperty,
} from "@/etc/constants/events";

import EventSummaryVue from "@/components/Events/EventSummary.vue";
import EventAlertsTableVue from "@/components/Events/EventAlertsTable.vue";
import EventURLSummaryVue from "@/components/Events/EventURLSummary.vue";
import EventURLDomainSummaryVue from "@/components/Events/EventURLDomainSummary.vue";
import EventObservableSummaryVue from "@/components/Events/EventObservableSummary.vue";
import EventDetectionsSummaryVue from "@/components/Events/EventDetectionsSummary.vue";

export const eventFilters: Record<string, readonly propertyOption[]> = {
  external: [
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
    eventSeverityProperty,
    eventSourceProperty,
    eventStatusProperty,
    tagsProperty,
    threatActorProperty,
    threatsProperty,
    eventTypeProperty,
    eventVectorsProperty,
  ],
  internal: [
    eventDispositionProperty,
    nameProperty,
    observableProperty,
    eventCreatedAfterProperty,
    eventCreatedBeforeProperty,
    observableTypesProperty,
    observableProperty,
    observableValueProperty,
    ownerProperty,
    queueProperty,
    eventSourceProperty,
    eventStatusProperty,
    tagsProperty,
    threatsProperty,
    eventTypeProperty,
  ],
} as const;

export const eventEditableProperties: Record<string, propertyOption[]> = {
  external: [
    nameProperty,
    ownerProperty,
    commentProperty,
    eventRemediationProperty,
    eventPreventionToolsProperty,
    eventSeverityProperty,
    eventStatusProperty,
    threatActorProperty,
    threatsProperty,
    eventTypeProperty,
    eventVectorsProperty,
    eventEventTimeProperty,
    eventAlertTimeProperty,
    eventOwnershipTimeProperty,
    eventDispositionTimeProperty,
    eventContainTimeProperty,
    eventRemediationTimeProperty,
  ],
  intel: [
    nameProperty,
    ownerProperty,
    commentProperty,
    eventRemediationProperty,
    eventPreventionToolsProperty,
    eventSeverityProperty,
    eventStatusProperty,
    threatActorProperty,
    threatsProperty,
    eventTypeProperty,
    eventVectorsProperty,
    eventEventTimeProperty,
    eventAlertTimeProperty,
    eventOwnershipTimeProperty,
    eventDispositionTimeProperty,
    eventContainTimeProperty,
    eventRemediationTimeProperty,
  ],
  internal: [
    nameProperty,
    ownerProperty,
    commentProperty,
    eventRemediationProperty,
    eventStatusProperty,
    threatsProperty,
    eventTypeProperty,
    eventEventTimeProperty,
    eventAlertTimeProperty,
    eventOwnershipTimeProperty,
    eventDispositionTimeProperty,
    eventContainTimeProperty,
    eventRemediationTimeProperty,
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
    {
      field: "createdTime",
      header: "Created (UTC)",
      sortable: true,
      default: true,
    },
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
  internal: [
    {
      field: "edit",
      header: "",
      sortable: false,
      required: true,
    },
    {
      field: "createdTime",
      header: "Created (UTC)",
      sortable: true,
      default: true,
    },
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
      default: true,
    },
    { field: "status", header: "Status", sortable: true, default: true },
    { field: "owner", header: "Owner", sortable: true, default: false },
    { field: "vectors", header: "Vectors", sortable: false, default: false },
  ],
  intel: [
    {
      field: "edit",
      header: "",
      sortable: false,
      required: true,
    },
    {
      field: "createdTime",
      header: "Created (UTC)",
      sortable: true,
      default: true,
    },
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
