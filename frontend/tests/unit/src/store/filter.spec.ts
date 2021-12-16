import { createTestingPinia } from "@pinia/testing";
import { useFilterStore } from "@/stores/filter";

createTestingPinia();

const store = useFilterStore();

describe("filters Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will set the given filterTypes filter object to the given filter object argument upon the bulkSetFilters action", () => {
    expect(store.alerts).toStrictEqual({});

    store.bulkSetFilters({
      filterType: "alerts",
      filters: { testFilterName: "testFilterValue" },
    });

    expect(store.$state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });

  it("will add a new property and specified to a given filter object upon the setFilter action", () => {
    expect(store.alerts).toStrictEqual({});

    store.setFilter({
      filterType: "alerts",
      filterName: "testFilterName",
      filterValue: "testFilterValue",
    });

    expect(store.$state).toEqual({
      alerts: {
        testFilterName: "testFilterValue",
      },
    });
  });

  it("will delete a given proprty for a given filter object upon the unsetFilter action", () => {
    store.$state = { alerts: { name: "test" } };

    expect(store.alerts).toStrictEqual({ name: "test" });

    store.unsetFilter({
      filterType: "alerts",
      filterName: "name",
    });

    expect(store.$state).toEqual({
      alerts: {},
    });
  });

  it("will delete all properties from a given filter object upon the clearAll action", () => {
    store.$state = { alerts: { name: "test", description: "test" } };

    expect(store.alerts).toStrictEqual({ name: "test", description: "test" });

    store.clearAll({
      filterType: "alerts",
    });

    expect(store.$state).toEqual({
      alerts: {},
    });
  });
});
