import NodeTag from "@/components/Node/NodeTag.vue";
import { mount } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "@unit/helpers";

const tagStub = { value: "my_tag" };

function factory(piniaOptions?: TestingOptions, nodeType = "alerts") {
  const router = createRouterMock({
    initialLocation: "/alert/uuid1",
  });
  injectRouterMock(router);

  const wrapper = mount(NodeTag, {
    props: {
      tag: tagStub,
    },
    global: {
      plugins: [createCustomPinia(piniaOptions)],
      provide: {
        nodeType: nodeType,
      },
    },
  });

  return { wrapper, router };
}

describe("NodeTag.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("receives props  as expected", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.props).toEqual({ tag: tagStub });
  });
  it("will route to manage_alerts with tag query on filterByTags if nodeType is 'alerts'", async () => {
    const { wrapper, router } = factory();
    wrapper.vm.filterByTags();
    expect(router.currentRoute.value.fullPath).toEqual(
      "/manage_alerts?tags=my_tag",
    );
  });
  it("will not route anywhere on filterByTags if nodeType is unsupported", async () => {
    const { wrapper, router } = factory(undefined, "unsupported");
    wrapper.vm.filterByTags();
    expect(router.currentRoute.value.fullPath).toEqual("/alert/uuid1");
  });
});
