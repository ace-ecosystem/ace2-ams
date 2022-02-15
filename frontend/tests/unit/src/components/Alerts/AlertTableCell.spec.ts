import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { alertSummary } from "@/models/alert";
import { nodeCommentRead } from "@/models/nodeComment";
import { userRead } from "@/models/user";
import { createCustomPinia } from "@unit/helpers";

const mockUser: userRead = {
  defaultAlertQueue: { description: null, uuid: "1", value: "default" },
  defaultEventQueue: { description: null, uuid: "1", value: "default" },
  displayName: "Test Analyst",
  email: "analyst@test.com",
  enabled: true,
  roles: [],
  timezone: "UTC",
  training: false,
  username: "test analyst",
  uuid: "1",
};

const mockComment: nodeCommentRead = {
  insertTime: new Date(),
  nodeUuid: "uuid1",
  user: mockUser,
  uuid: "uuid1",
  value: "Test comment",
};

const mockAlertReadASummary: alertSummary = {
  childTags: [
    {
      description: null,
      value: "recipient",
      uuid: "c5d3321d-883c-4772-b511-489273e13fde",
    },
    {
      description: null,
      value: "from_address",
      uuid: "f9081b70-c2bf-4a7d-ba90-a675e8a929d2",
    },
    {
      description: null,
      value: "contacted_host",
      uuid: "3c1ca637-48d1-4d47-aeee-0962bc32d96d",
    },
    {
      description: null,
      value: "c2",
      uuid: "a0b2d514-c544-4a8f-a059-b6151b9f1dd6",
    },
  ],
  comments: [mockComment],
  description: "",
  disposition: "OPEN",
  dispositionTime: null,
  dispositionUser: "Analyst",
  eventUuid: "None",
  eventTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  insertTime: new Date("2021-12-18T00:59:43.570343+00:00"),
  name: "Small Alert",
  owner: "Analyst",
  queue: "test_queue",
  tags: [],
  tool: "test_tool",
  toolInstance: "test_tool_instance",
  type: "test_type",
  uuid: "uuid1",
};

function factory(
  piniaOptions?: TestingOptions,
  data: alertSummary = mockAlertReadASummary,
  field = "name",
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(AlertTableCell, {
    global: {
      plugins: [createCustomPinia(piniaOptions), PrimeVue],
    },
    props: {
      data: data,
      field: field,
    },
  });

  return { wrapper };
}

describe("AlertTableCell", () => {
  it("renders", async () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("correctly formats a given date object into string", () => {
    const { wrapper } = factory();
    let result = wrapper.vm.formatDateTime(null);
    expect(result).toEqual("None");
    result = wrapper.vm.formatDateTime(new Date("2022-01-24"));
    expect(result).toEqual("1/24/2022, 12:00:00 AM");
  });
});
