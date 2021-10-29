import { Commit, createStore } from "vuex";

import makeGenericModule from "@/store/generic";
import alertQueue from "@/services/api/alertQueue";
import alertType from "@/services/api/alertType";
import observableType from "@/services/api/observableType";
import auth from "@/store/auth";
import alerts from "@/store/alerts";
import modals from "@/store/modals";
import nodeDirective from "@/services/api/nodeDirective";
import selectedAlerts from "@/store/selectedAlerts";
import users from "@/services/api/users";

export interface CommitFunction {
  commit: Commit;
}

const store = createStore({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    auth,
    alerts,
    modals,
    selectedAlerts,
  },
});

store.registerModule("alertQueue", makeGenericModule(alertQueue));
store.registerModule("alertType", makeGenericModule(alertType));
store.registerModule("nodeDirective", makeGenericModule(nodeDirective));
store.registerModule("observableType", makeGenericModule(observableType));
store.registerModule("users", makeGenericModule(users));

export default store;
