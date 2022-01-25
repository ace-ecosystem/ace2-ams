import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheAlertsTable, {
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
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
      },
      { field: "insertTime", header: "Insert Time", default: false },
      { field: "eventTime", header: "Event Time", default: true },
      { field: "name", header: "Name", default: true },
      { field: "owner", header: "Owner", default: true },
      { field: "disposition", header: "Disposition", default: true },
      { field: "dispositionUser", header: "Dispositioned By", default: false },
      { field: "queue", header: "Queue", default: false },
      { field: "type", header: "Type", default: false },
    ]);
  });
});
