import TheEventsTable from "@/components/Events/TheEventsTable.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import myNock from "@unit/services/api/nock";

import { createRouterMock, injectRouterMock } from "vue-router-mock";

import { mockAlertPage } from "../../../../mocks/alert";
import { parseAlertSummary } from "@/etc/helpers";

function factory(options?: TestingOptions) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(TheEventsTable, {
    global: {
      plugins: [createTestingPinia(options), PrimeVue],
    },
  });

  return { wrapper };
}

// DATA/CREATION
describe("TheEventsTable data/creation", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("initializes data as expected", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.columns).toStrictEqual([
      {
        field: "createdTime",
        header: "Created",
        sortable: true,
        default: true,
      },
      { field: "name", header: "Name", sortable: true, default: true },
      { field: "owner", header: "Owner", sortable: true, default: true },
      { field: "status", header: "Status", sortable: true, default: false },
      { field: "type", header: "Type", sortable: true, default: true },
      { field: "vectors", header: "Vectors", sortable: false, default: true },
      {
        field: "threatActors",
        header: "Threat Actors",
        sortable: false,
        default: false,
      },
      { field: "threats", header: "Threats", sortable: false, default: false },
      {
        field: "preventionTools",
        header: "Prevention Tools",
        sortable: false,
        default: false,
      },
      {
        field: "riskLevel",
        header: "Risk Level",
        sortable: true,
        default: false,
      },
    ]);
  });
});

// METHODS
describe("TheEventsTable methods", () => {
  myNock
    .get("/alert/?event_uuid=uuid1&sort=event_time|asc&offset=0")
    .reply(200, mockAlertPage)
    .persist();

  it("correctly fetches alerts and sets alert summaries on getAlerts", async () => {
    const { wrapper } = factory();

    const result = await wrapper.vm.getAlerts("uuid1");

    expect(result.length).toStrictEqual(2);
    expect(result[0].disposition).toStrictEqual("OPEN");
    expect(result[1].name).toStrictEqual("Manual Alert 1");
  });

  it("correctly sets the alerts for a given eventUuid in eventAlerts on onRowExpand", async () => {
    const { wrapper } = factory();

    await wrapper.vm.onRowExpand({ data: { uuid: "uuid1" } });

    const expected = mockAlertPage.items.map((x) => parseAlertSummary(x));
    expect(wrapper.vm.eventAlerts).toStrictEqual({ uuid1: expected });
  });

  it("correctly deletes a given eventUuid from eventAlerts on onRowCollapse", () => {
    const { wrapper } = factory();

    wrapper.vm.eventAlerts = { uuid1: [], uuid2: [], uuid3: [] };

    wrapper.vm.onRowCollapse({ data: { uuid: "uuid2" } });

    expect(wrapper.vm.eventAlerts).toStrictEqual({ uuid1: [], uuid3: [] });
  });
});
