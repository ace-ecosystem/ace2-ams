import FilterModal from "@/components/Modals/FilterModal.vue";
import { mount } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";

import { useFilterStore } from "@/stores/filter";
import { useModalStore } from "@/stores/modal";
import { alertFilterParams } from "@/models/alert";
import { createCustomPinia } from "@unit/helpers";

function factory(args: {
  filters?: { nodeType: "alerts"; filters: alertFilterParams };
  options?: TestingOptions;
}) {
  const testingPinia = createCustomPinia(args.options);
  const filterStore = useFilterStore();
  const modalStore = useModalStore();

  if (args.filters) {
    filterStore.bulkSetFilters(args.filters);
  }

  const wrapper = mount(FilterModal, {
    attachTo: document.body,
    global: {
      plugins: [testingPinia],
      provide: {
        nodeType: "alerts",
      },
    },
    props: { name: "FilterModal" },
  });

  return { wrapper, filterStore, modalStore };
}

describe("FilterModal setup", () => {
  it("renders", () => {
    const { wrapper } = factory({});

    expect(wrapper.exists()).toBe(true);
  });

  it("sets up data correctly", () => {
    const { wrapper } = factory({});

    expect(wrapper.vm.formFilters).toEqual([]);
  });

  it("executes loadFormFilters when the modal is mounted so preexisting filters are shown in the form", () => {
    const { wrapper } = factory({
      filters: {
        nodeType: "alerts",
        filters: { name: "hello world" },
      },
      options: { stubActions: false },
    });

    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({
      name: "hello world",
    });
    expect(wrapper.vm.submitFilters).toEqual({ name: "hello world" });
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: "name",
        filterValue: "hello world",
      },
    ]);
  });
});

describe("FilterModal computed properties", () => {
  it("contains expected computed data when no filters are set", () => {
    const { wrapper } = factory({});

    expect(wrapper.vm.submitFilters).toEqual({});
    expect(wrapper.vm.name).toEqual("FilterModal");
  });

  it("contains expected computed data when there are filters are set", () => {
    const { wrapper } = factory({ options: { stubActions: false } });

    wrapper.vm.filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: { name: "hello world" },
    });
    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({
      name: "hello world",
    });

    // if filters had been set, loadFormFilters would have been ran, so simulate that here before checking submitFilters
    wrapper.vm.loadFormFilters();
    expect(wrapper.vm.submitFilters).toEqual({ name: "hello world" });
  });
});

describe("FilterModal watchers", () => {
  it("executes loadFormFilters when filters change", async () => {
    const { wrapper } = factory({ options: { stubActions: false } });

    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({});
    expect(wrapper.vm.formFilters).toEqual([]);

    wrapper.vm.filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: { name: "hello world" },
    });

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({
      name: "hello world",
    });
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: "name",
        filterValue: "hello world",
      },
    ]);
  });
});

describe("FilterModal methods", () => {
  it("executes submit as expected when there are new filters", () => {
    const { wrapper } = factory({ options: { stubActions: false } });

    // Test submitting new filters
    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({});
    expect(wrapper.vm.formFilters).toEqual([]);
    wrapper.vm.formFilters = [
      {
        filterName: "name",
        filterValue: "hello world",
      },
    ];
    wrapper.vm.submit();
    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({
      name: "hello world",
    });
  });
  it("executes submit as expected when there no filters (cleared)", () => {
    const { wrapper } = factory({ options: { stubActions: false } });

    wrapper.vm.formFilters = [];
    wrapper.vm.submit();
    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({});
  });
  it("executes deleteFormFilter as expected", () => {
    const { wrapper } = factory({});

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
    const { wrapper } = factory({});

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
    const { wrapper } = factory({});

    expect(wrapper.vm.formFilters).toEqual([]);
    wrapper.vm.addNewFilter();
    expect(wrapper.vm.formFilters).toEqual([
      {
        filterName: null,
        filterValue: null,
      },
    ]);
  });
  it("executes loadFormFilters as expected", async () => {
    const { wrapper } = factory({ options: { stubActions: false } });

    expect(wrapper.vm.filterStore.$state[wrapper.vm.nodeType]).toEqual({});
    expect(wrapper.vm.formFilters).toEqual([]);

    wrapper.vm.filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: { name: "hello world", owner: "test analyst" },
    });

    wrapper.vm.loadFormFilters();
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
    const { wrapper } = factory({ options: { stubActions: false } });

    wrapper.vm.filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: { name: "hello world", owner: "test analyst" },
    });

    wrapper.vm.modalStore.open("FilterModal");
    expect(wrapper.vm.modalStore.openModals).toEqual(["FilterModal"]);

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
    expect(wrapper.vm.modalStore.openModals).toEqual([]);
    expect(wrapper.vm.formFilters).toEqual([
      { filterName: "name", filterValue: "hello world" },
      { filterName: "owner", filterValue: "test analyst" },
    ]);
  });
});
