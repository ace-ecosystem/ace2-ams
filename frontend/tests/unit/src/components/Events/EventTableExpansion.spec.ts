import EventTableExpansion from "@/components/Events/EventTableExpansion.vue";
import { flushPromises, mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

import { useFilterStore } from "@/stores/filter";
import myNock from "@unit/services/api/nock";
import nock from "nock";
import { mockAlertPage } from "../../../../mocks/alert";

function factory(options: TestingOptions = {}) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(EventTableExpansion, {
    global: {
      plugins: [createTestingPinia(options)],
      provide: { nodeType: "events" },
    },
    props: {
      uuid: "uuid1",
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

describe("EventTableExpansion", () => {
  myNock
    .get("/alert/?event_uuid=uuid1&sort=event_time|asc&offset=0")
    .reply(200, mockAlertPage)
    .persist();

  afterAll(async () => {
    await flushPromises();
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("correctly fetches alerts and sets alert summaries on getAlerts", async () => {
    const { wrapper } = factory();

    await wrapper.vm.getAlerts("uuid1");

    expect(wrapper.vm.alerts.length).toStrictEqual(2);
    expect(wrapper.vm.alerts[0].disposition).toStrictEqual("OPEN");
    expect(wrapper.vm.alerts[1].name).toStrictEqual("Manual Alert 1");
  });
});
