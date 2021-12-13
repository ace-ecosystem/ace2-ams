import FilterModal from "@/components/Modals/FilterModal.vue";
import store from "@/store";
import { mount } from "@vue/test-utils";

describe("FilterModal setup", () => {
  const wrapper = mount(FilterModal, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
      },
    },
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly", () => {
    expect(wrapper.vm.formFilters).toEqual([]);
  });
});

describe("FilterModal computed properties", () => {
  const wrapper = mount(FilterModal, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
      },
    },
  });

  afterAll(() => {
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: {},
    });
  });

  it("contains expected computed data when no filters are set", () => {
    expect(wrapper.vm.currentlySetFilters).toEqual({});
    expect(wrapper.vm.submitFilters).toEqual({});
    expect(wrapper.vm.name).toEqual("EditFilterModal");
  });
  it("contains expected computed data when there are filters are set", () => {
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: { name: "hello world" },
    });
    expect(wrapper.vm.currentlySetFilters).toEqual({ name: "hello world" });

    // if filters had been set, resetFormFilters would have been ran, so simulate that here before checking submitFilters
    wrapper.vm.resetFormFilters();
    expect(wrapper.vm.submitFilters).toEqual({ name: "hello world" });
  });
});

describe("FilterModal watchers", () => {
  const wrapper = mount(FilterModal, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
      },
    },
  });

  afterAll(() => {
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: {},
    });
  });

  it("executes resetFormFilters when currentlySetFilters changes", async () => {
    expect(wrapper.vm.currentlySetFilters).toEqual({});
    expect(wrapper.vm.formFilters).toEqual([]);
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: { name: "hello world" },
    });
    await wrapper.vm.$nextTick();
    expect(wrapper.vm.currentlySetFilters).toEqual({ name: "hello world" });
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: "name",
        filterValue: "hello world",
      },
    ]);
  });
});

describe("FilterModal methods", () => {
  const wrapper = mount(FilterModal, {
    global: {
      plugins: [store],
      provide: {
        filterType: "alerts",
      },
    },
  });

  afterEach(() => {
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: {},
    });
    wrapper.vm.formFilters = [];
  });

  it("executes submit as expected", () => {
    expect(wrapper.vm.currentlySetFilters).toEqual({});
    expect(wrapper.vm.formFilters).toEqual([]);
    wrapper.vm.formFilters = [
      {
        filterName: "name",
        filterValue: "hello world",
      },
    ];
    wrapper.vm.submit();
    expect(wrapper.vm.currentlySetFilters).toEqual({ name: "hello world" });
  });
  it("executes deleteFormFilter as expected", () => {
    wrapper.vm.formFilters = [
      {
        filterName: "name",
        filterValue: "hello world",
      },
      {
        filterName: "name",
        filterValue: "hello world 2",
      },
      {
        filterName: "name",
        filterValue: "hello world 3",
      },
    ];
    wrapper.vm.deleteFormFilter(1);
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: "name",
        filterValue: "hello world",
      },
      {
        filterName: "name",
        filterValue: "hello world 3",
      },
    ]);
  });
  it("executes clear as expected", () => {
    wrapper.vm.formFilters = [
      {
        filterName: "name",
        filterValue: "hello world",
      },
      {
        filterName: "name",
        filterValue: "hello world 2",
      },
      {
        filterName: "name",
        filterValue: "hello world 3",
      },
    ];
    wrapper.vm.clear();
    expect(wrapper.vm.formFilters).toEqual([]);
  });
  it("executes addNewFilter as expected", () => {
    expect(wrapper.vm.formFilters).toEqual([]);
    wrapper.vm.addNewFilter();
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: null,
        filterValue: null,
      },
    ]);
  });
  it("executes resetFormFilters as expected", async () => {
    expect(wrapper.vm.currentlySetFilters).toEqual({});

    expect(wrapper.vm.formFilters).toEqual([]);
    store.commit("filters/BULK_SET_FILTERS", {
      filterType: "alerts",
      filters: { name: "hello world", owner: "test analyst" },
    });

    wrapper.vm.resetFormFilters();
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: "name",
        filterValue: "hello world",
      },
      {
        filterName: "owner",
        filterValue: "test analyst",
      },
    ]);
  });
  it("executes close as expected", () => {
    store.dispatch("modals/open", "EditFilterModal");
    wrapper.vm.formFilters = [
      {
        filterName: "name",
        filterValue: "hello world",
      },
      {
        filterName: "name",
        filterValue: "hello world 2",
      },
      {
        filterName: "name",
        filterValue: "hello world 3",
      },
    ];
    wrapper.vm.close();
    expect(store.getters["modals/allOpen"]).toEqual([]);
    expect(wrapper.vm.formFilters).toEqual([]);
  });
});
