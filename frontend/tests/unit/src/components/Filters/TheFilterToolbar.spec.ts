import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import { shallowMount } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

import { useFilterStore } from "@/stores/filter";

describe("TheFilterToolbar.vue", () => {
  function factory(options?: TestingOptions) {
    const wrapper = shallowMount(TheFilterToolbar, {
      global: {
        plugins: [createTestingPinia(options)],
        provide: {
          filterType: "alerts",
        },
      },
    });

    const store = useFilterStore();

    return { wrapper, store };
  }

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("correctly receives injected data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.filterType).toEqual("alerts");
  });
  it("correctly calls Pinia action", () => {
    const { wrapper, store } = factory();

    wrapper.vm.clear();
    expect(store.clearAll).toHaveBeenCalled();
  });
  it("calls clearAll Pinia action on clear and reset", () => {
    const { wrapper, store } = factory();

    wrapper.vm.clear();
    expect(store.clearAll).toHaveBeenLastCalledWith({
      filterType: "alerts",
    });

    wrapper.vm.reset();
    expect(store.clearAll).toHaveBeenLastCalledWith({
      filterType: "alerts",
    });

    expect(store.clearAll).toHaveBeenCalledTimes(2);
  });
});
