import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";
import { flushPromises, mount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";

import { useFilterStore } from "@/stores/filter";
import myNock from "@unit/services/api/nock";
import nock from "nock";
import { createCustomPinia } from "@unit/helpers";

function factory(options?: TestingOptions) {
  const wrapper: VueWrapper<any> = mount(AlertTableExpansion, {
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "alerts" },
    },
    props: {
      uuid: "uuid1",
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

describe("AlertTableExpansion", () => {
  myNock
    .post("/node/tree/observable", '["uuid1"]')
    .reply(200, [
      { type: { value: "type_B" }, value: "value_B", tags: [] },
      { type: { value: "type_C" }, value: "value_C", tags: [] },
      { type: { value: "type_B" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_C", tags: [] },
    ])
    .persist();

  afterAll(async () => {
    await flushPromises();
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("correctly fetches, sets, and sorts observables on getObservables", async () => {
    const { wrapper } = factory();

    await wrapper.vm.getObservables("uuid1");

    expect(wrapper.vm.observables).toEqual([
      { type: { value: "type_A" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_C", tags: [] },
      { type: { value: "type_B" }, value: "value_A", tags: [] },

      { type: { value: "type_B" }, value: "value_B", tags: [] },
      { type: { value: "type_C" }, value: "value_C", tags: [] },
    ]);
  });

  it("correctly formats a given observable object into string", async () => {
    const { wrapper } = factory();
    const result = wrapper.vm.formatObservable({
      type: { value: "type_B" },
      value: "value_B",
      tags: [],
    });
    expect(result).toEqual("type_B : value_B");
  });

  it("correctly sets an observable filter on filterByObservable", async () => {
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
