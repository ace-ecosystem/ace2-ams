import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createCustomPinia } from "@unit/helpers";

import { useFilterStore } from "@/stores/filter";

function factory(
  options: TestingOptions = {},
  observables: unknown = [
    { type: { value: "type_A" }, value: "value_A", tags: [] },
    { type: { value: "type_A" }, value: "value_C", tags: [] },
    { type: { value: "type_B" }, value: "value_A", tags: [] },
    { type: { value: "type_B" }, value: "value_B", tags: [] },
    { type: { value: "type_C" }, value: "value_C", tags: [] },
  ],
) {
  const wrapper: VueWrapper<any> = mount(AlertTableExpansion, {
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "alerts" },
    },
    props: {
      observables: observables,
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

describe("AlertTableExpansion", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("correctly computes isLoading as true when observables prop is null", () => {
    const { wrapper } = factory({}, null);
    expect(wrapper.vm.isLoading).toBeTruthy();
  });

  it("correctly computes isLoading as true when observables prop is not null", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.isLoading).toBeFalsy();
  });

  it("correctly formats a given observable object into string", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.formatObservable({
      type: { value: "type_B" },
      value: "value_B",
      tags: [],
    });
    expect(result).toEqual("type_B : value_B");
  });

  it("correctly sets an observable filter on filterByObservable", () => {
    const { wrapper, filterStore } = factory({ stubActions: false });
    wrapper.vm.filterByObservable({
      type: { value: "type_B" },
      value: "value_B",
      tags: [],
    });
    expect(filterStore.alerts).toEqual({
      observable: { category: { value: "type_B" }, value: "value_B" },
    });
  });
});
