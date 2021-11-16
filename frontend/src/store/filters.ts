import { CommitFunction } from "@/store/index";

const store = {
  namespaced: true,
  state: {
    disposition: null,
    dispositionUser: null,
    dispositionedAfter: null,
    dispositionedBefore: null,
    eventUuid: null,
    eventTimeAfter: null,
    eventTimeBefore: null,
    insertTimeAfter: null,
    insertTimeBefore: null,
    name: null,
    observable: null,
    observableTypes: null,
    observableValue: null,
    owner: null,
    queue: null,
    tags: null,
    threatActor: null,
    threats: null,
    tool: null,
    toolInstance: null,
    type: null,
  },
  getters: {
    allFilters: (state: Record<string, any>) => state,
    setFilters: (state: Record<string, any>) =>
      Object.fromEntries(
        Object.entries(state).filter(([key, value]) => value != null),
      ),
    unsetFilters: (state: Record<string, any>) =>
      Object.fromEntries(
        Object.entries(state).filter(([key, value]) => value == null),
      ),
  },
  mutations: {
    SET_FILTER: (
      state: Record<string, any>,
      payload: { filterType: string; filterValue: string },
    ) => (state[payload.filterType] = payload.filterValue),
    UNSET_FILTER: (
      state: Record<string, any>,
      payload: { filterType: string },
    ) => (state[payload.filterType] = null),
  },
  actions: {
    setFilter: (
      { commit }: CommitFunction,
      payload: { filterType: string; filterValue: string },
    ) => commit("SET_FILTER", payload),
    unsetFilter: (
      { commit }: CommitFunction,
      payload: { filterType: string },
    ) => commit("UNSET_FILTER", payload),
  },
};

export default store;
