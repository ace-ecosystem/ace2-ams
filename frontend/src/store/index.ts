import { Commit, createStore } from "vuex";

import makeGenericModule from "@/store/generic";
import { AlertQueue } from "@/services/api/alertQueue";
import { AlertType } from "@/services/api/alertType";
import { ObservableType } from "@/services/api/observableType";
import auth from "@/store/auth";
import alerts from "@/store/alerts";
import filters from "@/store/filters";
import modals from "@/store/modals";
import { NodeDirective } from "@/services/api/nodeDirective";
import selectedAlerts from "@/store/selectedAlerts";
import { User } from "@/services/api/users";

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
    filters,
    modals,
    selectedAlerts,
  },
});

store.registerModule("alertQueue", makeGenericModule(AlertQueue));
store.registerModule("alertType", makeGenericModule(AlertType));
store.registerModule("nodeDirective", makeGenericModule(NodeDirective));
store.registerModule("observableType", makeGenericModule(ObservableType));
store.registerModule("users", makeGenericModule(User));

export default store;
