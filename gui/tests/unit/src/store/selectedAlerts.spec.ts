import Vuex from "vuex";
import selectedAlerts from "@/store/selectedAlerts";
const actions = selectedAlerts.actions;
const mutations = selectedAlerts.mutations;
const getters = selectedAlerts.getters;

describe("selectedAlerts Getters", () => {
  it("will return empty list of selected IDs when none selected", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["selected"]).toStrictEqual([]);
  });
  it("will return list of IDs currently selected", () => {
    const selected = ["id1", "id2"];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["selected"]).toStrictEqual(selected);
  });
  it("multipleSelected will return true when multiple alerts are selected", () => {
    const selected = ["id1", "id2"];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["multipleSelected"]).toBe(true);
  });
  it("will have anySelected return true when any alerts are selected", () => {
    const selected = ["id1", "id2"];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["anySelected"]).toBe(true);
  });
  it("will have anySelected return false when no alerts are selected", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["anySelected"]).toBe(false);
  });
  it("will have multipleSelected return true when multiple alerts are selected", () => {
    const selected = ["id1", "id2"];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["multipleSelected"]).toBe(true);
  });
  it("will have multipleSelected return false when one or less alerts are selected", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations, getters });

    expect(store.getters["multipleSelected"]).toBe(false);
  });
});

describe("selectedAlerts Mutations", () => {
  it("will add a given string to the selected list", () => {
    const state = selectedAlerts.state;
    const store = new Vuex.Store({ state, mutations });

    store.commit("SELECT", "id1");
    expect(state.selected.length).toBe(1);
  });
  it("will remove a given string from the selected list", () => {
    const state = { selected: ["id1"] };
    const store = new Vuex.Store({ state, mutations });

    store.commit("UNSELECT", "id1");
    expect(state.selected.length).toBe(0);
  });
  it("will not error if a nonexistent item is unselected", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations });

    store.commit("UNSELECT", "id1");
    expect(state.selected.length).toBe(0);
  });
  it("will add a list of strings to the selected list", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ state, mutations });

    store.commit("SELECTALL", ["id1", "id2", "id3"]);
    expect(state.selected.length).toBe(3);
    expect(state.selected[0]).toBe("id1");
    expect(state.selected[1]).toBe("id2");
    expect(state.selected[2]).toBe("id3");
  });
  it("will remove all from the selected list", () => {
    const state = { selected: ["id1", "id2", "id3"] };
    const store = new Vuex.Store({ state, mutations });

    store.commit("UNSELECTALL");
    expect(state.selected.length).toBe(0);
  });
});

describe("selectedAlerts Actions", () => {
  it("will add a given string to the selected list upon the select action", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ actions, getters, state, mutations });

    store.dispatch("select", "id1");
    expect(state.selected.length).toBe(1);
    expect(state.selected[0]).toBe("id1");
  });
  it("will remove a given string from the selected list upon the unselect action", () => {
    const state = { selected: ["id1"] };
    const store = new Vuex.Store({ actions, getters, state, mutations });

    store.dispatch("unselect", "id1");
    expect(state.selected.length).toBe(0);
  });
  it("will add a list of strings to the selected list upon the selected action", () => {
    const selected: string[] | undefined = [];
    const state = { selected: selected };
    const store = new Vuex.Store({ actions, getters, state, mutations });

    store.dispatch("selectAll", ["id1", "id2", "id3"]);
    expect(state.selected.length).toBe(3);
    expect(state.selected[0]).toBe("id1");
    expect(state.selected[1]).toBe("id2");
    expect(state.selected[2]).toBe("id3");
  });
  it("will remove all from the selected list upon the unselect action", () => {
    const state = { selected: ["id1", "id2", "id3"] };
    const store = new Vuex.Store({ actions, getters, state, mutations });

    store.dispatch("unselectAll");
    expect(state.selected.length).toBe(0);
  });
});
