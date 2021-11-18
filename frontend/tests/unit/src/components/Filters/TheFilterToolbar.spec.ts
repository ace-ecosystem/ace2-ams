import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import { shallowMount, VueWrapper } from "@vue/test-utils";
import { createStore } from "vuex";

describe("TheFilterToolbar.vue", () => {
  let actions: { clearAllFilters: jest.Mock<any, any> },
    store,
    wrapper: VueWrapper<any>;

  beforeEach(() => {
    actions = {
      clearAllFilters: jest.fn(),
    };
    store = createStore({
      modules: {
        filters: {
          namespaced: true,
          actions: actions,
        },
      },
    });

    wrapper = shallowMount(TheFilterToolbar, {
      global: {
        plugins: [store],
        provide: {
          filterType: "alerts",
        },
      },
    });
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
  it("correctly receives injected data", () => {
    expect(wrapper.vm.filterType).toEqual("alerts");
  });
  it("correctly maps vuex action", () => {
    wrapper.vm.clearAllFilters();
    expect(actions.clearAllFilters).toHaveBeenCalled();
  });
  it("calls clearAllFilters on clear and reset", () => {
    wrapper.vm.clear();
    wrapper.vm.reset();
    expect(actions.clearAllFilters).toBeCalledTimes(2);

    // Checks that correct arguments were sent
    expect(actions.clearAllFilters.mock.calls[0][1]).toEqual({
      filterType: "alerts",
    });
    expect(actions.clearAllFilters.mock.calls[1][1]).toEqual({
      filterType: "alerts",
    });
  });
});
