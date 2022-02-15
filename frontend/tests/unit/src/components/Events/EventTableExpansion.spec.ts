import EventTableExpansion from "@/components/Events/EventTableExpansion.vue";
import { flushPromises, mount, VueWrapper } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

import { useFilterStore } from "@/stores/filter";
import nock from "nock";
import { mockAlertPage } from "../../../../mocks/alert";
import { createCustomPinia } from "@unit/helpers";

function factory(
  options: TestingOptions = {},
  alerts: unknown = mockAlertPage.items,
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(EventTableExpansion, {
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "events" },
    },
    props: {
      alerts: alerts,
    },
  });

  const filterStore = useFilterStore();

  return { wrapper, filterStore };
}

describe("EventTableExpansion", () => {
  afterAll(async () => {
    await flushPromises();
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("correctly computes isLoading as true when alerts prop is null", () => {
    const { wrapper } = factory({}, null);
    expect(wrapper.vm.isLoading).toBeTruthy();
  });

  it("correctly computes isLoading as true when alerts prop is not null", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.isLoading).toBeFalsy();
  });
});
