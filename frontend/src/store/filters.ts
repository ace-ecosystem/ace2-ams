import {
  alertFilterParams,
  alertFilterNames,
  alertFilterValues,
} from "@/models/alert";
import { CommitFunction } from "@/store/index";

const store = {
  namespaced: true,
  state: {
    alerts: {},
  },
  getters: {
    alerts: (state: { alerts: alertFilterParams }): alertFilterParams =>
      state.alerts,
  },
  mutations: {
    SET_FILTER: (
      state: { alerts: alertFilterParams },
      payload: {
        filterType: "alerts";
        filterName: alertFilterNames;
        filterValue: alertFilterValues;
      },
    ): alertFilterValues =>
      (state[payload.filterType][payload.filterName] = payload.filterValue),
    UNSET_FILTER: (
      state: { alerts: alertFilterParams },
      payload: { filterType: "alerts"; filterName: alertFilterNames },
    ): boolean => delete state[payload.filterType][payload.filterName],
    CLEAR_ALL: (
      state: { alerts: alertFilterParams },
      payload: { filterType: "alerts" },
    ): alertFilterParams => (state[payload.filterType] = {}),
  },
  actions: {
    setFilter: (
      { commit }: CommitFunction,
      payload: {
        filterType: "alerts";
        filterName: string;
        filterValue: string;
      },
    ): void => commit("SET_FILTER", payload),
    unsetFilter: (
      { commit }: CommitFunction,
      payload: { filterType: "alerts"; filterName: string },
    ): void => commit("UNSET_FILTER", payload),
    clearAllFilters: (
      { commit }: CommitFunction,
      payload: { filterType: "alerts" },
    ): void => commit("CLEAR_ALL", payload),
  },
};

export default store;
