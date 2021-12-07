import {
  alertFilterParams,
  alertFilterValues,
  alertFilterNameTypes,
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
    BULK_SET_FILTERS: (
      state: { alerts: alertFilterParams },
      payload: {
        filterType: "alerts";
        filters: alertFilterParams;
      },
    ): alertFilterParams => (state[payload.filterType] = payload.filters),
    SET_FILTER: (
      state: { alerts: alertFilterParams },
      payload: {
        filterType: "alerts";
        filterName: alertFilterNameTypes;
        filterValue: alertFilterValues;
      },
    ): alertFilterValues =>
      (state[payload.filterType][payload.filterName] = payload.filterValue),
    UNSET_FILTER: (
      state: { alerts: alertFilterParams },
      payload: { filterType: "alerts"; filterName: alertFilterNameTypes },
    ): boolean => delete state[payload.filterType][payload.filterName],
    CLEAR_ALL: (
      state: { alerts: alertFilterParams },
      payload: { filterType: "alerts" },
    ): alertFilterParams => (state[payload.filterType] = {}),
  },
  actions: {
    bulkSetFilters: (
      { commit }: CommitFunction,
      payload: {
        filterType: "alerts";
        filters: alertFilterParams;
      },
    ): void => commit("BULK_SET_FILTERS", payload),
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
    clearAll: (
      { commit }: CommitFunction,
      payload: { filterType: "alerts" },
    ): void => commit("CLEAR_ALL", payload),
  },
};

export default store;
