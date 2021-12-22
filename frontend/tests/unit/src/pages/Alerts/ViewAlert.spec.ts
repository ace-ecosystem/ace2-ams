import ViewAlert from "../../../../../src/pages/Alerts/ViewAlert.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { useAlertStore } from "@/stores/alert";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import myNock from "@unit/services/api/nock";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";

import {
  mockAlertTree,
  mockAlertRead,
  mockAlertReadDateStringsFirstAppearances,
  mockAlertTreeFirstAppearances,
} from "../../../../mockData/alert";
import nock from "nock";

describe("ViewAlert.vue", () => {
  myNock.get("/alert/uuid1").reply(200, mockAlertRead).persist();
  const router = createRouterMock({
    initialLocation: "/alert/uuid1",
  });

  const pinia = createTestingPinia({ stubActions: false });

  injectRouterMock(router);
  getRouter().setParams({ alertID: "uuid1" });

  const wrapper: VueWrapper<any> = mount(ViewAlert, {
    global: {
      plugins: [pinia],
    },
  });

  afterAll(async () => {
    nock.cleanAll();
  });

  it("renders", async () => {
    expect(wrapper.exists()).toBe(true);
  });
  it("selects open alert and fetches given alertID on initPage", async () => {
    const selectedAlertStore = useSelectedAlertStore();
    const alertStore = useAlertStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedAlertStore.selected).toEqual(["uuid1"]);
    expect(alertStore.openAlert).toEqual(
      mockAlertReadDateStringsFirstAppearances,
    );
  });
  it("unselects all selected alerts when umounted", async () => {
    const selectedAlertStore = useSelectedAlertStore();
    await wrapper.vm.initPage("uuid1");
    expect(selectedAlertStore.selected).toEqual(["uuid1"]);
    wrapper.unmount();
    expect(selectedAlertStore.selected).toEqual([]);
  });
});
