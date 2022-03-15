import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { TestingOptions } from "@pinia/testing";

import myNock from "@unit/services/api/nock";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "@unit/helpers";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheAlertsTable, {
    global: {
      plugins: [createCustomPinia(options), PrimeVue],
    },
  });

  return { wrapper };
}

// DATA/CREATION
describe("TheAlertsTable data/creation", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("initializes data as expected", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.columns).toStrictEqual([
      {
        field: "dispositionTime",
        header: "Dispositioned Time",
        default: false,
        sortable: true,
      },
      {
        field: "insertTime",
        header: "Insert Time",
        default: false,
        sortable: true,
      },
      {
        field: "eventTime",
        header: "Event Time",
        default: true,
        sortable: true,
      },
      { field: "name", header: "Name", default: true, sortable: true },
      { field: "owner", header: "Owner", default: true, sortable: true },
      {
        field: "disposition",
        header: "Disposition",
        default: true,
        sortable: true,
      },
      {
        field: "dispositionUser",
        header: "Dispositioned By",
        default: false,
        sortable: true,
      },
      { field: "queue", header: "Queue", default: false, sortable: true },
      { field: "type", header: "Type", default: false, sortable: true },
    ]);
    expect(wrapper.vm.alertObservables).toEqual({});
  });
});

describe("TheAlertsTable methods", () => {
  it("correctly fetches, sorts, and returns observables on getObservables", async () => {
    myNock.post("/node/tree/observable", '["uuid1"]').reply(200, [
      { type: { value: "type_B" }, value: "value_B", tags: [] },
      { type: { value: "type_C" }, value: "value_C", tags: [] },
      { type: { value: "type_B" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_C", tags: [] },
    ]);

    const { wrapper } = factory();

    const result = await wrapper.vm.getObservables("uuid1");
    expect(result).toEqual([
      { type: { value: "type_A" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_C", tags: [] },
      { type: { value: "type_B" }, value: "value_A", tags: [] },
      { type: { value: "type_B" }, value: "value_B", tags: [] },
      { type: { value: "type_C" }, value: "value_C", tags: [] },
    ]);
  });

  it("fetches observables and caches in alertObservables for a given alert on onRowExpand", async () => {
    myNock.post("/node/tree/observable", '["uuid1"]').reply(200, [
      { type: { value: "type_B" }, value: "value_B", tags: [] },
      { type: { value: "type_C" }, value: "value_C", tags: [] },
      { type: { value: "type_B" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_A", tags: [] },
      { type: { value: "type_A" }, value: "value_C", tags: [] },
    ]);
    const { wrapper } = factory();
    await wrapper.vm.onRowExpand({ data: { uuid: "uuid1" } });
    expect(wrapper.vm.alertObservables).toEqual({
      uuid1: [
        { type: { value: "type_A" }, value: "value_A", tags: [] },
        { type: { value: "type_A" }, value: "value_C", tags: [] },
        { type: { value: "type_B" }, value: "value_A", tags: [] },
        { type: { value: "type_B" }, value: "value_B", tags: [] },
        { type: { value: "type_C" }, value: "value_C", tags: [] },
      ],
    });
  });

  it("deletes a given uuid from alertObservables on onRowCollapse", () => {
    const { wrapper } = factory();
    wrapper.vm.alertObservables = { uuid1: [], uuid2: [], uuid3: [] };
    wrapper.vm.onRowCollapse({ data: { uuid: "uuid2" } });
    expect(wrapper.vm.alertObservables).toEqual({ uuid1: [], uuid3: [] });
  });
});
