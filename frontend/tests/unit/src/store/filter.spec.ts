import { createTestingPinia } from "@pinia/testing";
import { useFilterStore, isEmpty } from "@/stores/filter";

createTestingPinia();

const store = useFilterStore();

describe("filters helpers", () => {
  it("will correctly identify if a given variable is empty / falsy on isEmpty", () => {
    expect(isEmpty({})).toBeTruthy();
    expect(isEmpty({ test: "test" })).toBeFalsy();
    expect(isEmpty([])).toBeTruthy();
    expect(isEmpty(["test"])).toBeFalsy();
    expect(isEmpty(false)).toBeTruthy();
    expect(isEmpty(true)).toBeFalsy();
    expect(isEmpty("")).toBeTruthy();
    expect(isEmpty("test")).toBeFalsy();
    expect(isEmpty(new Date())).toBeFalsy();
  });
});

describe("filters Actions", () => {
  beforeEach(() => {
    store.$reset();
    localStorage.removeItem("aceFilters");
  });

  it("will set the given filterTypes filter object to the given filter object argument upon the bulkSetFilters action", () => {
    expect(store.alerts).toStrictEqual({});
    expect(localStorage.getItem("aceFilters")).toStrictEqual(null);

    store.bulkSetFilters({
      filterType: "alerts",
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
    expect(store.alerts).toStrictEqual({});

    store.bulkSetFilters({
      filterType: "alerts",
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
    expect(store.alerts).toStrictEqual({});
    expect(localStorage.getItem("aceFilters")).toStrictEqual(null);

    store.setFilter({
      filterType: "alerts",
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
    expect(store.alerts).toStrictEqual({});

    store.setFilter({
      filterType: "alerts",
      filterName: "testFilterName",
      filterValue: [],
    });

    expect(store.$state).toEqual({
      alerts: {},
      events: {},
    });

    store.setFilter({
      filterType: "alerts",
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

    expect(store.alerts).toStrictEqual({ name: "test" });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({ alerts: { name: "test" }, events: {} }),
    );

    store.unsetFilter({
      filterType: "alerts",
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

    expect(store.alerts).toStrictEqual({ name: "test", description: "test" });
    expect(localStorage.getItem("aceFilters")).toStrictEqual(
      JSON.stringify({
        alerts: { name: "test", description: "test" },
        events: {},
      }),
    );

    store.clearAll({
      filterType: "alerts",
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
