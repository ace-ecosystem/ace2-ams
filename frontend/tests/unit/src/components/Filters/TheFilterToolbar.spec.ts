import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import * as helpers from "@/etc/helpers";
import { useFilterStore } from "@/stores/filter";
import { useModalStore } from "@/stores/modal";

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

    const filterStore = useFilterStore();
    const modalStore = useModalStore();

    return { wrapper, filterStore, modalStore };
  }

  it("renders", () => {
    const { wrapper } = factory();

    expect(wrapper.exists()).toBe(true);
  });
  it("correctly opens given modal when modal open called", () => {
    const { wrapper, modalStore } = factory({ stubActions: false });
    wrapper.vm.open("EditFilterModal");

    expect(modalStore.openModals).toContain("EditFilterModal");
  });
  it("correctly receives injected data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.filterType).toEqual("alerts");
  });
  it("correctly computes whether given filterType filters are empty", () => {
    const { wrapper, filterStore } = factory();

    filterStore.alerts = {test: "test_value"}
    expect(wrapper.vm.filtersAreEmpty).toBeFalsy();
    filterStore.alerts = {}
    expect(wrapper.vm.filtersAreEmpty).toBeTruthy();
  });
  it("correctly calls Pinia action", () => {
    const { wrapper, filterStore } = factory();

    wrapper.vm.clear();
    expect(filterStore.clearAll).toHaveBeenCalled();
  });
  it("calls clearAll Pinia action on clear and reset", () => {
    const { wrapper, filterStore } = factory();

    wrapper.vm.clear();
    expect(filterStore.clearAll).toHaveBeenLastCalledWith({
      filterType: "alerts",
    });

    wrapper.vm.reset();
    expect(filterStore.clearAll).toHaveBeenLastCalledWith({
      filterType: "alerts",
    });

    expect(filterStore.clearAll).toHaveBeenCalledTimes(2);
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
