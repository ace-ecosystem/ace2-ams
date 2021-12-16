import NodeTag from "../../../../../src/components/Node/NodeTag.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouterMock, getRouter, injectRouterMock } from "vue-router-mock";

import { useFilterStore } from "@/stores/filter";
import Chip from "primevue/chip";
import { RouterLink } from "vue-router";

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
        provide: {
          plugins: [createTestingPinia()],
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
