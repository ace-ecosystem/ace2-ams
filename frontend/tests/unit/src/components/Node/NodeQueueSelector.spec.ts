import NodeQueueSelector from "../../../../../src/components/Node/NodeQueueSelector.vue";
import { mount } from "@vue/test-utils";
import { createCustomPinia } from "@unit/helpers";
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { userReadFactory } from "../../../../mocks/user";

function factory(nodeQueue) {
  const wrapper = mount(NodeQueueSelector, {
    props: {
      nodeQueue: nodeQueue,
    },
    global: {
      plugins: [
        createCustomPinia({
          stubActions: false,
          initialState: {
            authStore: {
              user: userReadFactory({
                defaultAlertQueue: genericObjectReadFactory({
                  value: "internal",
                }),
                defaultEventQueue: genericObjectReadFactory({
                  value: "external",
                }),
              }),
            },
          },
        }),
      ],
    },
  });

  return { wrapper };
}

describe("NodeComment.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it.each([
    ["alerts", "alerts"],
    ["events", "events"],
  ])("receives props as expected", (nodeQueue, expected) => {
    const { wrapper } = factory(nodeQueue);
    expect(wrapper.vm.props).toEqual({
      nodeQueue: expected,
    });
  });
  it.each([
    ["alerts", "internal"],
    ["events", "external"],
  ])(
    "correctly sets preferredQueue in setup using nodeQueue prop",
    (nodeQueue, expected) => {
      const { wrapper } = factory(nodeQueue);
      expect(wrapper.vm.preferredQueue).toEqual(
        genericObjectReadFactory({
          value: expected,
        }),
      );
    },
  );
  it.each([
    ["alerts", "external"],
    ["events", "internal"],
  ])(
    "correctly updates currentUserSettingsStore on updateUserSettings",
   (nodeQueue, expected) => {
      const { wrapper } = factory(nodeQueue);
      wrapper.vm.preferredQueue = genericObjectReadFactory({
        value: expected,
      });
      wrapper.vm.updateUserSettings();
      expect(wrapper.vm.currentUserSettingsStore.queues[nodeQueue]).toEqual(
        genericObjectReadFactory({
          value: expected,
        }),
      );
    },
  );
});
