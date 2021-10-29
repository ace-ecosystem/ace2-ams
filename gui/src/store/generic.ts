// Taken from: https://markus.oberlehner.net/blog/generic-content-vuex-modules/

// Many of our API calls serve solely to get a list of data types from the backend to display in the GUI
// To reduce the number of nearly identical vuex stores, we can use this base vuex module
// Note that only the getAll action is implemented at the moment
// As the need arises for more actions/state complexity, that can be added to this module

export default function makeGenericModule(service: any = {}): {
  namespaced: boolean;
  state: { items: any[] };
  getters: {
    allItems: (state: any, getters: any) => any;
  };
  mutations: { addItems: (state: any, items: any[]) => void };
  actions: { getAll: ({ commit }: { commit: any }) => Promise<void> };
} {
  return {
    namespaced: true,
    state: {
      items: [],
    },

    getters: {
      allItems: (state) => {
        return state.items;
      },
    },

    mutations: {
      addItems: (state, items) => {
        state.items = items;
      },
    },

    actions: {
      getAll: async ({ commit }) => {
        // It is not strictly necessary to pass a service,
        // but if none was passed, no data can be loaded.
        if (!service) throw new Error("No service specified!");

        return await service
          .getAll()
          .then((items: any[]) => {
            commit("addItems", items);
          })
          .catch((error: Error) => {
            throw error;
          });
      },
    },
  };
}
