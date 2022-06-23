import { describe, it, beforeEach, expect } from "vitest";
import { useFilterStore, isEmpty } from "@/stores/filter";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

const store = useFilterStore();

describe("filters helpers", () => {
  it("will correctly identify if a given variable is empty / falsy on isEmpty", () => {
    expect(isEmpty({})).toStrictEqual(true);
    expect(isEmpty({ test: "test" })).toStrictEqual(false);
    expect(isEmpty([])).toStrictEqual(true);
    expect(isEmpty(["test"])).toStrictEqual(false);
    expect(isEmpty(false)).toStrictEqual(true);
    expect(isEmpty(true)).toStrictEqual(false);
    expect(isEmpty("")).toStrictEqual(true);
    expect(isEmpty("test")).toStrictEqual(false);
    expect(isEmpty(new Date())).toStrictEqual(false);
  });
});

describe("filters Actions", () => {
  beforeEach(() => {
    store.$reset();
    localStorage.removeItem("aceFilters");
  });

  it("will set the given objectTypes filter object to the given filter object argument upon the bulkSetFilters action", () => {
    expect(localStorage.getItem("aceFilters")).toEqual(null);

    store.bulkSetFilters({
      objectType: "alerts",
      filters: { testFilterName: ["testFilterValue"] },
    });

    const expectedState = {
      alerts: {
        testFilterName: ["testFilterValue"],
      },
      events: {},
    };

    expect(store.$state).toEqual(expectedState);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState),
    );
  });

  it("will skip falsy/empty given filterValues upon the bulkSetFilters action", () => {
    store.bulkSetFilters({
      objectType: "alerts",
      filters: {
        testFilterName: [""],
        testFilterName2: [[]],
        testFilterName3: [null],
        testFilterName4: ["testFilterValue"],
      },
    });

    expect(store.$state).toEqual({
      alerts: {
        testFilterName4: ["testFilterValue"],
      },
      events: {},
    });
  });

  it("will add a new property and specified to a given filter object upon the setFilter action", () => {
    expect(localStorage.getItem("aceFilters")).toStrictEqual(null);

    // Adding a filter from empty
    store.setFilter({
      objectType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
    });

    const expectedState = {
      alerts: {
        testFilterName: ["testFilterValue"],
      },
      events: {},
    };

    expect(store.$state).toEqual(expectedState);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState),
    );

    // Adding a filter from a non-empty list
    store.setFilter({
      objectType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue2",
    });

    const expectedState2 = {
      alerts: {
        testFilterName: ["testFilterValue", "testFilterValue2"],
      },
      events: {},
    };

    expect(store.$state).toEqual(expectedState2);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState2),
    );

    // Adding a duplicate filter should not change the list
    // Adding a filter from a non-empty list
    store.setFilter({
      objectType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue2",
    });

    expect(store.$state).toEqual(expectedState2);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState2),
    );
  });

  it("will not alter a given property for a given filter object upon the setFilter action if given filterValue falsy/empty ", () => {
    store.setFilter({
      objectType: "alerts",
      filterName: "testFilterName",
      filterValue: [],
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    store.setFilter({
      objectType: "alerts",
      filterName: "testFilterName",
      filterValue: "",
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });
  });

  it("will delete a given value given filter type object upon the unsetFilterValue action", () => {
    store.$state = { alerts: { name: ["test", "test2"] }, events: {} };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({ alerts: { name: ["test", "test2"] }, events: {} }),
    );

    expect(store.alerts).toEqual({ name: ["test", "test2"] });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: { name: ["test", "test2"] }, events: {} }),
    );

    store.unsetFilterValue({
      objectType: "alerts",
      filterName: "name",
      filterValue: "test",
    });

    expect(store.$state).toEqual({
      alerts: { name: ["test2"] },
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: { name: ["test2"] }, events: {} }),
    );

    // If there are no values left, the filter will be deleted
    store.unsetFilterValue({
      objectType: "alerts",
      filterName: "name",
      filterValue: "test2",
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: {}, events: {} }),
    );
  });

  it("will delete a given property for a given filter object upon the unsetFilter action", () => {
    store.$state = { alerts: { name: ["test"] }, events: {} };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({ alerts: { name: ["test"] }, events: {} }),
    );

    expect(store.alerts).toEqual({ name: ["test"] });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: { name: ["test"] }, events: {} }),
    );

    store.unsetFilter({
      objectType: "alerts",
      filterName: "name",
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: {}, events: {} }),
    );
  });

  it("will delete all properties from a given filter object upon the clearAll action", () => {
    store.$state = {
      alerts: { name: ["test"], description: ["test"] },
      events: {},
    };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: { name: ["test"], description: ["test"] },
        events: {},
      }),
    );

    expect(store.alerts).toEqual({ name: ["test"], description: ["test"] });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: ["test"], description: ["test"] },
        events: {},
      }),
    );

    store.clearAll({
      objectType: "alerts",
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: {}, events: {} }),
    );
  });
});
