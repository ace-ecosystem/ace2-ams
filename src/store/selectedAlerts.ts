// Store to track which alerts are currently selected
// Can be used in 'alert actions' modals (or elsewhere) to determine what alerts to apply actions on
import { CommitFunction } from "@/store/index";
import { UUID } from "@/models/base";

const store = {
  namespaced: true,
  state: {
    selected: Array<UUID>(),
  },
  getters: {
    selected: (state: { selected: UUID[] }) => state.selected,
    anySelected: (state: { selected: UUID[] }) => state.selected.length > 0,
    multipleSelected: (state: { selected: UUID[] }) =>
      state.selected.length > 1,
  },
  mutations: {
    SELECT: (state: { selected: UUID[] }, payload: UUID) =>
      state.selected.push(payload),
    UNSELECT: (state: { selected: UUID[] }, payload: UUID) =>
      (state.selected = state.selected.filter((e) => e !== payload)),
    SELECTALL: (state: { selected: UUID[] }, payload: UUID[]) =>
      (state.selected = payload),
    UNSELECTALL: (state: { selected: UUID[] }) => (state.selected = []),
  },
  actions: {
    select: ({ commit }: CommitFunction, payload: UUID) =>
      commit("SELECT", payload),
    unselect: ({ commit }: CommitFunction, payload: UUID) =>
      commit("UNSELECT", payload),
    selectAll: ({ commit }: CommitFunction, payload: UUID[]) =>
      commit("SELECTALL", payload),
    unselectAll: ({ commit }: CommitFunction) => commit("UNSELECTALL"),
  },
};

export default store;
