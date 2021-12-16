import ViewAlert from "../../../../../src/pages/Alerts/ViewAlert.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { getRouter, createRouterMock, injectRouterMock } from "vue-router-mock";
import { useAlertStore } from "@/stores/alert";
import { useSelectedAlertStore } from "@/stores/selectedAlert";
import { observableTreeRead } from "@/models/observable";
import { alertRead } from "@/models/alert";
import { analysisTreeRead } from "@/models/analysis";

const mockAlert: alertRead = {
  description: "Test Description",
  disposition: null,
  dispositionTime: null,
  dispositionUser: null,
  eventTime: new Date(),
  eventUuid: null,
  insertTime: new Date(),
  instructions: null,
  name: "Test Name",
  owner: null,
  queue: { description: null, uuid: "1", value: "test_alert_queue" },
  tool: null,
  toolInstance: null,
  type: { description: null, uuid: "1", value: "test_alert_type" },
  comments: [],
  directives: [],
  tags: [],
  threatActor: null,
  threats: [],
  uuid: "1234",
  version: "1",
};

const mockTree: (analysisTreeRead | observableTreeRead)[] = [];

describe("ViewAlert.vue", () => {
  const router = createRouterMock();
  let wrapper: VueWrapper<any>;
  beforeEach(() => {
    injectRouterMock(router);
    wrapper = mount(ViewAlert, {
      global: {
        provide: {
          plugins: [createTestingPinia()],
        },
      },
    });
    getRouter().setParams({ alertID: 1234 });
  });

  it("renders", () => {
      const alertStore = useAlertStore();

    alertStore.openAlert = { alert: mockAlert, tree: mockTree };
    expect(wrapper.exists()).toBe(true);
    console.log(wrapper);
    console.log(wrapper.vm);
    console.log(wrapper.vm.$route);
  });
});
