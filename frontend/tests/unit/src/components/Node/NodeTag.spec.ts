import NodeTag from "../../../../../src/components/Node/NodeTag.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

const tagStub = { value: "my_tag" };

describe("NodeTag.vue", () => {
  const router = createRouterMock();

  let wrapper: VueWrapper<any>;
  beforeEach(() => {
    injectRouterMock(router);

    wrapper = mount(NodeTag, {
      props: {
        tag: tagStub,
      },
      global: {
        plugins: [createTestingPinia({ stubActions: false })],
        provide: {
          filterType: "alerts",
        },
      },
    });
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("receives props  as expected", () => {
    expect(wrapper.vm.props).toEqual({ tag: tagStub });
  });
});
