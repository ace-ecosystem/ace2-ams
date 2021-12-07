import Vuex from "vuex";
import filters from "@/store/filters";
const actions = filters.actions;
const mutations = filters.mutations;
const getters = filters.getters;

describe("filters Getters", () => {
  it("will return empty object for 'alerts' getter if no alerts filters are set", () => {
    const state = { alerts: {} };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["alerts"]).toStrictEqual({});
  });
  it("will return object of set 'alerts' filters if any are set", () => {
    const state = { alerts: { name: "test" } };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["alerts"]).toStrictEqual({ name: "test" });
  });
});

describe("filters Mutations", () => {
  it("will set the given filterTypes filter object to the given filter object argument upon the BULK_SET_FILTERS mutation", () => {
    const state = { alerts: {} };
    const store = new Vuex.Store({ state, mutations });

    store.commit("BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: { testFilterName: "testFilterValue" }
    });
    expect(state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });
  it("will add a new property and specified to a given filter object upon the SET_FILTER mutation", () => {
    const state = { alerts: {} };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SET_FILTER", {
      filterType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
    });
    expect(state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });
  it("will delete a given proprty for a given filter object upon the UNSET_FILTER mutation", () => {
    const state = { alerts: { name: "test" } };
    const store = new Vuex.Store({ state, mutations });

    store.commit("UNSET_FILTER", {
      filterType: "alerts",
      filterName: "name",
    });
    expect(state).toEqual({
      alerts: {},
    });
  });
  it("will delete all properties from a given filter object upon the CLEAR_ALL mutation", () => {
    const state = { alerts: { name: "test", description: "test" } };
    const store = new Vuex.Store({ state, mutations });

    store.commit("CLEAR_ALL", {
      filterType: "alerts",
    });
    expect(state).toEqual({
      alerts: {},
    });
  });
});

describe("filters Actions", () => {
  it("will set the given filterTypes filter object to the given filter object argument upon the bulkSetFilters action", () => {
    const state = { alerts: {} };
    const store = new Vuex.Store({ state, mutations, actions });

    store.dispatch("bulkSetFilters", {
      filterType: "alerts",
      filters: { testFilterName: "testFilterValue" },
    });
    expect(state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });
  it("will add a new property and specified to a given filter object upon the setFilter action", () => {
    const state = { alerts: {} };
    const store = new Vuex.Store({ state, mutations, actions });

    store.dispatch("setFilter", {
      filterType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
    });
    expect(state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });
  it("will delete a given proprty for a given filter object upon the unsetFiilter action", () => {
    const state = { alerts: { name: "test" } };
    const store = new Vuex.Store({ state, mutations, actions });

    store.dispatch("unsetFilter", {
      filterType: "alerts",
      filterName: "name",
    });
    expect(state).toEqual({
      alerts: {},
    });
  });
  it("will delete all properties from a given filter object upon the clearAll action", () => {
    const state = { alerts: { name: "test", description: "test" } };
    const store = new Vuex.Store({ state, mutations, actions });

    store.dispatch("clearAll", {
      filterType: "alerts",
    });
    expect(state).toEqual({
      alerts: {},
    });
  });
});
