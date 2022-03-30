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

  it("will set the given nodeTypes filter object to the given filter object argument upon the bulkSetFilters action", () => {
    expect(localStorage.getItem("aceFilters")).toEqual(null);

    store.bulkSetFilters({
      nodeType: "alerts",
      filters: { testFilterName: "testFilterValue" },
    });

    const expectedState = {
      alerts: {
        testFilterName: "testFilterValue",
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
      nodeType: "alerts",
      filters: {
        testFilterName: "",
        testFilterName2: [],
        testFilterName3: null,
        testFilterName4: "testFilterValue",
      },
    });

    expect(store.$state).toEqual({
      alerts: {
        testFilterName4: "testFilterValue",
      },
      events: {},
    });
  });

  it("will add a new property and specified to a given filter object upon the setFilter action", () => {
    expect(localStorage.getItem("aceFilters")).toStrictEqual(null);

    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
    });

    const expectedState = {
      alerts: {
        testFilterName: "testFilterValue",
      },
      events: {},
    };

    expect(store.$state).toEqual(expectedState);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState),
    );
  });

  it("will not alter a given property for a given filter object upon the setFilter action if given filterValue falsy/empty ", () => {
    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: [],
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "",
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });
  });

  it("will delete a given property for a given filter object upon the unsetFilter action", () => {
    store.$state = { alerts: { name: "test" }, events: {} };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({ alerts: { name: "test" }, events: {} }),
    );

    expect(store.alerts).toEqual({ name: "test" });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: { name: "test" }, events: {} }),
    );

    store.unsetFilter({
      nodeType: "alerts",
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
      alerts: { name: "test", description: "test" },
      events: {},
    };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: { name: "test", description: "test" },
        events: {},
      }),
    );

    expect(store.alerts).toEqual({ name: "test", description: "test" });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: "test", description: "test" },
        events: {},
      }),
    );

    store.clearAll({
      nodeType: "alerts",
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
