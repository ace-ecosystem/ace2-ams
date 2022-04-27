import { defineStore } from "pinia";
import { UUID } from "@/models/base";
import { Event } from "@/services/api/event";
import { eventFilterParams, eventRead, eventSummary } from "@/models/event";
import { camelToSnakeCase } from "@/etc/helpers";
import { useSelectedEventStore } from "./selectedEvent";

export function parseEventSummary(event: eventRead): eventSummary {
  return {
    comments: event.comments,
    createdTime: new Date(event.creationTime),
    // disposition: event.disposition,  // Need to edit the API so that it adds disposition into the Event response
    name: event.name,
    owner: event.owner ? event.owner.displayName : "None",
    preventionTools: event.preventionTools.map((x) => x.value),
    riskLevel: event.riskLevel ? event.riskLevel.value : "None",
    status: event.status ? event.status.value : "None",
    tags: event.tags,
    threatActors: event.threatActors.map((x) => x.value),
    threats: event.threats.map((x) => x.value),
    type: event.type ? event.type.value : "None",
    uuid: event.uuid,
    vectors: event.vectors.map((x) => x.value),
    queue: event.queue ? event.queue.value : "None",
    remediations: event.remediations.map((x) => x.value),
  };
}

export const useEventTableStore = defineStore({
  id: "eventTableStore",

  state: () => ({
    // all events returned from the current page using the current filters
    visibleQueriedItems: [] as eventRead[],

    // total number of events from all pages
    totalItems: 0,

    // whether the event table should be reloaded
    requestReload: false,

    // current sort field
    sortField: "createdTime" as string | null,

    // current sort oder
    sortOrder: "desc" as string | null,

    // current page size
    pageSize: 10,

    // whether event filters have been loaded from saved state
    stateFiltersLoaded: false,

    // whether event filters have been loaded from route query
    routeFiltersLoaded: false,
  }),

  getters: {
    allFiltersLoaded(): boolean {
      return this.stateFiltersLoaded && this.routeFiltersLoaded;
    },

    visibleQueriedItemSummaries(): eventSummary[] {
      return this.visibleQueriedItems.map((x) => parseEventSummary(x));
    },

    visibleQueriedItemsUuids(): UUID[] {
      return this.visibleQueriedItems.map((x) => x.uuid);
    },

    visibleQueriedSelectedItems(): eventRead[] {
      const selectedStore = useSelectedEventStore();
      return this.visibleQueriedItems.filter((x) =>
        selectedStore.selected.includes(x.uuid),
      );
    },

    visibleQueriedItemById: (state) => {
      return (eventUuid: UUID) =>
        state.visibleQueriedItems.find((event) => event.uuid === eventUuid);
    },

    sortFilter: (state) => {
      if (state.sortField && state.sortOrder) {
        return `${camelToSnakeCase(state.sortField)}|${state.sortOrder}`;
      }
      return null;
    },
  },

  actions: {
    async readPage(params: eventFilterParams) {
      await Event.readPage(params)
        .then((page) => {
          this.visibleQueriedItems = page.items;
          this.totalItems = page.total;
        })
        .catch((error) => {
          throw error;
        });
    },
    resetSort() {
      this.sortField = "createdTime";
      this.sortOrder = "desc";
    },
  },
});
