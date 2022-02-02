import EventTableCell from "@/components/Events/EventTableCell.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import PrimeVue from "primevue/config";
import { TestingOptions } from "@pinia/testing";

import { createRouterMock, injectRouterMock } from "vue-router-mock";
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

function factory(
  piniaOptions?: TestingOptions,
  data = { name: "event" },
  field = "name",
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = shallowMount(EventTableCell, {
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

describe("EventTableCell", () => {
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
  it("correctly formats a given uuid object into the correct path", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.getEventLink("uuid1");
    expect(result).toEqual("/event/uuid1");
  });
  it("correctly joins an array of strings using joinStringArray", () => {
    const { wrapper } = factory();
    const result = wrapper.vm.joinStringArray(["stringA", "stringB"]);
    expect(result).toEqual("stringA, stringB");
  });
});
