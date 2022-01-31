import ViewAnalysis from "../../../../../src/pages/Alerts/ViewAnalysis.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { useAlertStore } from "@/stores/alert";
import myNock from "@unit/services/api/nock";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";
import {
  mockAlert,
  mockAnalysisRead,
  mockAlertReadDateStrings,
} from "../../../../mocks/alert";
import nock from "nock";

describe("ViewAnalysis.vue", () => {
  myNock.get("/alert/uuid1").reply(200, mockAlert).persist();
  myNock.get("/analysis/uuid2").reply(200, mockAnalysisRead).persist();

  const router = createRouterMock({
    initialLocation: "/alert/uuid1/uuid2",
  });

  const pinia = createTestingPinia({ stubActions: false });

  injectRouterMock(router);
  getRouter().setParams({ alertID: "uuid1", analysisID: "uuid2" });

  const wrapper: VueWrapper<any> = mount(ViewAnalysis, {
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

  it("fetches alert and analysis using route params on initPage", async () => {
    const alertStore = useAlertStore();
    await wrapper.vm.initPage("uuid2", "uuid1");
    expect(wrapper.vm.analysis).toEqual(mockAnalysisRead);
    expect(alertStore.openAlert).toEqual(mockAlertReadDateStrings);
  });
  it("correctly computes alertName", async () => {
    await wrapper.vm.initPage("uuid2", "uuid1");
    expect(wrapper.vm.alertName).toEqual("Small Alert");
  });
  it("correctly computes analysisName", async () => {
    await wrapper.vm.initPage("uuid2", "uuid1");
    expect(wrapper.vm.analysisName).toEqual("File Analysis");
  });
  it("correctly computes analysisDetails", async () => {
    await wrapper.vm.initPage("uuid2", "uuid1");
    expect(wrapper.vm.analysisDetails).toEqual(mockAnalysisRead.details);
  });
});
