import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import * as helpers from "@/etc/helpers";
import { useFilterStore } from "@/stores/filter";
import { useModalStore } from "@/stores/modal";
import { createCustomPinia } from "@unit/helpers";
import { testConfiguration } from "@/etc/configuration/test/index";
import { vi } from "vitest";
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { userReadFactory } from "../../../../mocks/user";

describe("TheFilterToolbar.vue", () => {
  function factory(options?: TestingOptions) {
    const wrapper: VueWrapper<any> = shallowMount(TheFilterToolbar, {
      global: {
        plugins: [
          createCustomPinia({
            ...options,
            initialState: {
              authStore: {
                user: userReadFactory({
                  defaultAlertQueue: genericObjectReadFactory({
                    value: "external",
                  }),
                  defaultEventQueue: genericObjectReadFactory({
                    value: "external",
                  }),
                }),
              },
            },
          }),
        ],
        provide: {
          nodeType: "alerts",
          config: testConfiguration,
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
    it("correctly computes current queue based on node type", () => {
    const { wrapper } = factory({stubActions: false});

    expect(wrapper.vm.queue).toEqual("external");

    wrapper.vm.currentUserSettingsStore.queues.alerts =
      genericObjectReadFactory({
        value: "internal",
      });
    expect(wrapper.vm.queue).toEqual("internal");
  });
  it("correctly opens EditFilterModal modal on openFilterModal", () => {
    const { wrapper, modalStore } = factory({ stubActions: false });
    wrapper.vm.openFilterModal();

    expect(modalStore.openModals).toContain("EditFilterModal");
  });
  it("correctly receives injected data", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.nodeType).toEqual("alerts");
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
      nodeType: "alerts",
    });

    wrapper.vm.reset();
    expect(filterStore.clearAll).toHaveBeenLastCalledWith({
      nodeType: "alerts",
    });

    expect(filterStore.clearAll).toHaveBeenCalledTimes(2);
  });
  it("correctly generates link to filtered view based on currently set filters", () => {
    const { wrapper } = factory({ stubActions: false });

    let link = wrapper.vm.generateLink();
    expect(link).toEqual("http://localhost:3000/manage_alerts");

    wrapper.vm.filterStore.bulkSetFilters({
      nodeType: "alerts",
      filters: { name: "hello world", owner: { username: "test_analyst" } },
    });

    link = wrapper.vm.generateLink();
    expect(link).toEqual(
      "http://localhost:3000/manage_alerts?name=hello+world&owner=test_analyst",
    );
  });
  it("calls copyToClipboard with generated link when copyLink is called", () => {
    const spy = vi
      .spyOn(helpers, "copyToClipboard")
      .mockImplementationOnce(() => null);
    const { wrapper } = factory({ stubActions: false });

    wrapper.vm.copyLink();
    expect(spy).toHaveBeenCalledWith("http://localhost:3000/manage_alerts");
  });
  it("correctly sets up filterModel on mount", () => {
    const { wrapper } = factory();

    expect(wrapper.vm.filterModel).toEqual({
      propertyType: null,
      propertyValue: null,
    });
  });
  it("correctly adds a filter to store  and resets filterModel on addFilter", () => {
    const { wrapper, filterStore } = factory({ stubActions: false });
    wrapper.vm.filterModel = {
      propertyType: "test",
      propertyValue: "name",
    };

    wrapper.vm.addFilter();
    expect(filterStore.alerts).toEqual({ test: "name" });

    expect(wrapper.vm.filterModel).toEqual({
      propertyType: null,
      propertyValue: null,
    });
  });
});
