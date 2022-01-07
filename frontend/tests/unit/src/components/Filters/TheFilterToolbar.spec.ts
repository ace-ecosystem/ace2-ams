import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import * as helpers from "@/etc/helpers";

import { useFilterStore } from "@/stores/filter";

describe("TheFilterToolbar.vue", () => {
  function factory(options?: TestingOptions) {
    const wrapper: VueWrapper<any> = shallowMount(TheFilterToolbar, {
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
  it("correctly generates link to filtered view based on currently set filters", () => {
    const { wrapper } = factory({ stubActions: false });

    let link = wrapper.vm.generateLink();
    expect(link).toEqual("http://localhost/manage_alerts");

    wrapper.vm.filterStore.bulkSetFilters({
      filterType: "alerts",
      filters: { name: "hello world", owner: { username: "test_analyst" } },
    });

    link = wrapper.vm.generateLink();
    expect(link).toEqual(
      "http://localhost/manage_alerts?name=hello+world&owner=test_analyst",
    );
  });
  it("calls copyToClipboard with generated link when copyLink is called", () => {
    const spy = jest
      .spyOn(helpers, "copyToClipboard")
      .mockImplementationOnce(() => null);
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.copyLink();
    expect(spy).toHaveBeenCalledWith("http://localhost/manage_alerts");
  });
});
