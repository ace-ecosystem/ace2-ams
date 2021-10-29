import Vuex from "vuex";

import auth from "@/store/auth";
const getters = auth.getters;

class State {
  isLoggedIn = false;
}

describe("auth Getters", () => {
  it("will return isLoggedIn state when not logged in", () => {
    // Manually set the sessionStorage value
    sessionStorage.removeItem("authenticated");

    const state = new State();
    const store = new Vuex.Store({ state, getters });

    expect(store.getters["isLoggedIn"]).toStrictEqual(false);
  });

  it("will return isLoggedIn state when logged in", () => {
    // Manually set the sessionStorage value
    sessionStorage.setItem("authenticated", "yes");

    const state = new State();
    const store = new Vuex.Store({ state, getters });

    expect(store.getters["isLoggedIn"]).toStrictEqual(true);
  });
});
