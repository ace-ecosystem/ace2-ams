import {
  alertFilterParams,
  alertFilterTypes,
  alertFilterValues,
} from "@/models/alert";
import { CommitFunction } from "@/store/index";

const store = {
  namespaced: true,
  state: {
    filters: {},
  },
  getters: {
    filters: (state: { filters: alertFilterParams }): alertFilterParams =>
      state.filters,
  },
  mutations: {
    SET_FILTER: (
      state: { filters: alertFilterParams },
      payload: {
        filterType: alertFilterTypes;
        filterValue: alertFilterValues;
      },
    ): alertFilterValues =>
      (state.filters[payload.filterType] = payload.filterValue),
    UNSET_FILTER: (
      state: { filters: alertFilterParams },
      payload: { filterType: alertFilterTypes },
    ): boolean => delete state.filters[payload.filterType],
  },
  actions: {
    setFilter: (
      { commit }: CommitFunction,
      payload: { filterType: string; filterValue: string },
    ): void => commit("SET_FILTER", payload),
    unsetFilter: (
      { commit }: CommitFunction,
      payload: { filterType: string },
    ): void => commit("UNSET_FILTER", payload),
  },
};

export default store;
