import { Commit, createStore } from "vuex";

import alerts from "@/store/alerts";
import filters from "@/store/filters";
import modals from "@/store/modals";
import selectedAlerts from "@/store/selectedAlerts";

export interface CommitFunction {
  commit: Commit;
}

const store = createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    alerts,
    filters,
    modals,
    selectedAlerts,
  },
});

export default store;
