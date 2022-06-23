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
      filters: {
        testFilterName: {
          included: ["testFilterValue"],
          notIncluded: ["testFilterValue2"],
        },
      },
    });

    const expectedState = {
      alerts: {
        testFilterName: {
          included: ["testFilterValue"],
          notIncluded: ["testFilterValue2"],
        },
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
        testFilterName: { included: [""], notIncluded: [""] },
        testFilterName2: { included: [[]], notIncluded: [[]] },
        testFilterName3: { included: [null], notIncluded: [null] },
        testFilterName4: {
          included: ["testFilterValue"],
          notIncluded: ["testFilterValue2"],
        },
      },
    });

    expect(store.$state).toEqual({
      alerts: {
        testFilterName4: {
          included: ["testFilterValue"],
          notIncluded: ["testFilterValue2"],
        },
      },
      events: {},
    });
  });

  it("will add a new property and specified to a given filter object upon the setFilter action", () => {
    expect(localStorage.getItem("aceFilters")).toStrictEqual(null);

    // Adding a filter from empty
    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
      isIncluded: true,
    });

    const expectedState = {
      alerts: {
        testFilterName: { included: ["testFilterValue"], notIncluded: [] },
      },
      events: {},
    };

    expect(store.$state).toEqual(expectedState);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState),
    );

    // Adding a filter from a non-empty list
    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue2",
      isIncluded: true,
    });

    const expectedState2 = {
      alerts: {
        testFilterName: {
          included: ["testFilterValue", "testFilterValue2"],
          notIncluded: [],
        },
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
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue2",
      isIncluded: true,
    });

    expect(store.$state).toEqual(expectedState2);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState2),
    );

    const expectedState3 = {
      alerts: {
        testFilterName: {
          included: ["testFilterValue", "testFilterValue2"],
          notIncluded: ["testFilterValue"],
        },
      },
      events: {},
    };

    // Adding a filter to the notIncluded list
    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
      isIncluded: false,
    });

    expect(store.$state).toEqual(expectedState3);
    expect(localStorage.getItem("aceFilters")).toEqual(
      JSON.stringify(expectedState3),
    );
  });

  it("will not alter a given property for a given filter object upon the setFilter action if given filterValue falsy/empty ", () => {
    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: [],
      isIncluded: true,
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    store.setFilter({
      nodeType: "alerts",
      filterName: "testFilterName",
      filterValue: "",
      isIncluded: true,
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });
  });

  it("will delete a given value given filter type object upon the unsetFilterValue action", () => {
    store.$state = {
      alerts: { name: { included: ["test", "test2"], notIncluded: ["test"] } },
      events: {},
    };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: {
          name: { included: ["test", "test2"], notIncluded: ["test"] },
        },
        events: {},
      }),
    );

    expect(store.alerts).toEqual({
      name: { included: ["test", "test2"], notIncluded: ["test"] },
    });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: {
          name: { included: ["test", "test2"], notIncluded: ["test"] },
        },
        events: {},
      }),
    );

    store.unsetFilterValue({
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test",
      isIncluded: true,
    });

    expect(store.$state).toEqual({
      alerts: { name: { included: ["test2"], notIncluded: ["test"] } },
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: { included: ["test2"], notIncluded: ["test"] } },
        events: {},
      }),
    );

    store.unsetFilterValue({
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test",
      isIncluded: false,
    });

    expect(store.$state).toEqual({
      alerts: { name: { included: ["test2"], notIncluded: [] } },
      events: {},
    });

    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: { included: ["test2"], notIncluded: [] } },
        events: {},
      }),
    );

    // If there are no values left, the filter will be deleted
    store.unsetFilterValue({
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test2",
      isIncluded: true,
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
    store.$state = {
      alerts: { name: { included: ["test"], notIncluded: [] } },
      events: {},
    };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: { name: { included: ["test"], notIncluded: [] } },
        events: {},
      }),
    );

    expect(store.alerts).toEqual({
      name: { included: ["test"], notIncluded: [] },
    });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: { included: ["test"], notIncluded: [] } },
        events: {},
      }),
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
      alerts: {
        name: { included: ["test"], notIncluded: [] },
        description: { included: ["test"], notIncluded: [] },
      },
      events: {},
    };
    localStorage.setItem(
      "aceFilters",
      JSON.stringify({
        alerts: {
          name: { included: ["test"], notIncluded: [] },
          description: { included: ["test"], notIncluded: [] },
        },
        events: {},
      }),
    );

    expect(store.alerts).toEqual({
      name: { included: ["test"], notIncluded: [] },
      description: { included: ["test"], notIncluded: [] },
    });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: {
          name: { included: ["test"], notIncluded: [] },
          description: { included: ["test"], notIncluded: [] },
        },
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
