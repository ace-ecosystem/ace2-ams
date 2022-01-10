import NodeTag from "../../../../../src/components/Node/NodeTag.vue";
import { mount } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

const tagStub = { value: "my_tag" };

function factory(piniaOptions?: TestingOptions, filterType = "alerts") {
  const router = createRouterMock({
    initialLocation: "/alert/uuid1",
  });
  injectRouterMock(router);

  const wrapper = mount(NodeTag, {
    props: {
      tag: tagStub,
    },
    global: {
      plugins: [createTestingPinia(piniaOptions)],
      provide: {
        filterType: filterType,
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
  it("will route to manage_alerts with tag query on filterByTags if filterType is 'alerts'", async () => {
    const { wrapper, router } = factory();
    wrapper.vm.filterByTags();
    expect(router.currentRoute.value.fullPath).toEqual(
      "/manage_alerts?tags=my_tag",
    );
  });
  it("will not route anywhere on filterByTags if filterType is unsupported", async () => {
    const { wrapper, router } = factory(undefined, "unsupported");
    wrapper.vm.filterByTags();
    expect(router.currentRoute.value.fullPath).toEqual("/alert/uuid1");
  });
});
