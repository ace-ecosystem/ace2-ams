import { defineStore } from "pinia";
import { UUID } from "@/models/base";
import { Event } from "@/services/api/event";
import { eventFilterParams, eventRead, eventSummary } from "@/models/event";

export function parseEventSummary(event: eventRead): eventSummary {
  return {
    createdTime: event.creationTime,
    // disposition: event.disposition,  // Need to edit the API so that it adds disposition into the Event response
    name: event.name,
    owner: event.owner ? event.owner.displayName : "None",
    preventionTools: event.preventionTools.map((x) => x.value),
    riskLevel: event.riskLevel ? event.riskLevel.value : "None",
    status: event.status ? event.status.value : "None",
    threatActors: event.threatActors.map((x) => x.value),
    threats: event.threats.map((x) => x.value),
    type: event.type ? event.type.value : "None",
    uuid: event.uuid,
    vectors: event.vectors.map((x) => x.value),
  };
}

export const useEventTableStore = defineStore({
  id: "eventTableStore",

  state: () => ({
    // all events returned from the current page using the current filters
    visibleQueriedEvents: [] as eventRead[],

    // total number of events from all pages
    totalEvents: 0,

    // whether the event table should be reloaded
    requestReload: false,
  }),

  getters: {
    visibleQueriedEventSummaries(): eventSummary[] {
      return this.visibleQueriedEvents.map((x) => parseEventSummary(x));
    },

    visibleQueriedEventsUuids(): UUID[] {
      return this.visibleQueriedEvents.map((x) => x.uuid);
    },

    visibleQueriedEventById: (state) => {
      return (eventUuid: UUID) =>
        state.visibleQueriedEvents.find((event) => event.uuid === eventUuid);
    },
  },

  actions: {
    async readPage(params: eventFilterParams) {
      await Event.readPage(params)
        .then((page) => {
          this.visibleQueriedEvents = page.items;
          this.totalEvents = page.total;
        })
        .catch((error) => {
          throw error;
        });
    },
  },
});
