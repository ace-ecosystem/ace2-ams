import NodeTag from "../../../../../src/components/Node/NodeTag.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import router from "@/router";

import { useFilterStore } from "@/stores/filter";

const tagStub = { value: "my_tag" };

describe("TheHeader.vue", () => {
  let wrapper: VueWrapper<any>;
  beforeEach(() => {
    wrapper = mount(NodeTag, {
      props: {
        tag: tagStub,
      },
      global: {
        stubs: ["router-link"],
        provide: {
          plugins: [router, createTestingPinia()],
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
