import NodeTag from "../../../../../src/components/Node/NodeTag.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

import { useFilterStore } from "@/stores/filter";

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

  it("receives props and injections as expected", () => {
    expect(wrapper.vm.props).toEqual({ tag: tagStub });
    expect(wrapper.vm.filterType).toEqual("alerts");
  });

  it("filterByTag updates 'tag' filter to prop filter", () => {
    const store = useFilterStore();
    wrapper.vm.filterByTag();
    expect(store.alerts).toEqual({ tags: tagStub });
  });
});
