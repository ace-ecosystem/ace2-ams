import FilterChipContainer from "@/components/Filters/FilterChipContainer.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { useFilterStore } from "@/stores/filter";
import { useModalStore } from "@/stores/modal";
import { createCustomPinia } from "@unit/helpers";

describe("FilterChipContainer.vue", () => {
  function factory(options?: TestingOptions) {
    const wrapper: VueWrapper<any> = shallowMount(FilterChipContainer, {
      global: {
        plugins: [createCustomPinia(options)],
        provide: {
          nodeType: "alerts",
        },
      },
    });

    const filterStore = useFilterStore();
    const modalStore = useModalStore();

    return { wrapper, filterStore, modalStore };
  }

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("correctly receives injected data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.nodeType).toEqual("alerts");
  });
  it("correctly computes setFilters", () => {
    const { wrapper, filterStore } = factory();

    expect(wrapper.vm.setFilters).toEqual([]);
    filterStore.alerts = {
      testFilter1: { value: "test" },
      testFilter2: { value: "test2" },
    };
    expect(wrapper.vm.setFilters).toEqual(["testFilter1", "testFilter2"]);
  });
  it("correctly returns value for given filterName on filterValue", () => {
    const { wrapper, filterStore } = factory();
    filterStore.alerts = {
      testFilter1: { value: "test" },
      testFilter2: { value: "test2" },
    };

    expect(wrapper.vm.filterValue("testFilter1")).toEqual({ value: "test" });
    expect(wrapper.vm.filterValue("unknown")).toBeUndefined();
  });
});
