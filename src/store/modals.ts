// Modal manager that handles opening/closing of modals
// Allows modal components to be (cleanly) called from buttons in parent component, as well as opening a modal from a modal
// Ex. Disposition > Save to Event
// Credit to: https://xon5.medium.com/a-vue-modal-manager-via-vuex-1ae530c8649

import { Commit } from "vuex";

export interface CommitFunction {
  commit: Commit;
}

const store = {
  namespaced: true,
  state: {
    open: [],
  },
  getters: {
    active: (state: { open: string | string[] }) =>
      state.open.length > 0 ? state.open[0] : null,
    allOpen: (state: { open: string[] }) => state.open,
  },
  mutations: {
    OPEN: (state: { open: string[] }, payload: string) =>
      state.open.unshift(payload),
    CLOSE: (state: { open: string[] }, payload: string) =>
      (state.open = state.open.filter((e) => e !== payload)),
  },
  actions: {
    open: ({ commit }: CommitFunction, payload: string) =>
      commit("OPEN", payload),
    close: ({ commit }: CommitFunction, payload: string) =>
      commit("CLOSE", payload),
  },
};

export default store;
