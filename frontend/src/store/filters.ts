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
  },
};

export default store;
