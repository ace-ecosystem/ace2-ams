import ViewAlert from "../../../../../src/pages/Alerts/ViewAlert.vue";
import { flushPromises, shallowMount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { useAlertStore } from "@/stores/alert";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import myNock from "@unit/services/api/nock";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";

import {
  mockAlert,
  mockAlertReadDateStrings,
} from "../../../../mocks/alert";
import nock from "nock";

function factory(options?: TestingOptions) {
  myNock.get("/alert/uuid1").reply(200, mockAlert);
  const router = createRouterMock({
    initialLocation: "/alert/uuid1",
  });

  injectRouterMock(router);
  getRouter().setParams({ alertID: "uuid1" });

  const wrapper: VueWrapper<any> = shallowMount(ViewAlert, {
    global: {
      plugins: [createTestingPinia(options)],
    },
  });

  return {
    wrapper,
  };
}

describe("ViewAlert.vue", () => {
  afterAll(async () => {
    nock.cleanAll();
  });

  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("reloads open alert on reloadPage", async () => {
    const { wrapper } = factory();

    const alertStore = useAlertStore();
    await wrapper.vm.reloadPage();
    expect(alertStore.read).toHaveBeenCalledTimes(2);
  });
  it("reloads open alert when alertStore requestReload is set to true", async () => {
    factory();
    const alertStore = useAlertStore();
    alertStore.requestReload = true;
    await flushPromises();
    expect(alertStore.read).toHaveBeenCalledTimes(2);
  });
  it("selects open alert and fetches given alertID on initPage", async () => {
    const { wrapper } = factory({ stubActions: false });

    myNock.get("/alert/uuid1").reply(200, mockAlert);
    const selectedAlertStore = useSelectedAlertStore();
    const alertStore = useAlertStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedAlertStore.selected).toEqual(["uuid1"]);
    expect(alertStore.openAlert).toEqual(mockAlertReadDateStrings);
  });
  it("unselects all selected alerts when umounted", async () => {
    const { wrapper } = factory({ stubActions: false });

    myNock.get("/alert/uuid1").reply(200, mockAlert);
    const selectedAlertStore = useSelectedAlertStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedAlertStore.selected).toEqual(["uuid1"]);
    wrapper.unmount();
    expect(selectedAlertStore.selected).toEqual([]);
  });
});
