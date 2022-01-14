import App from "@/App.vue";
import { mount } from "@vue/test-utils";
import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

import { useAuthStore } from "@/stores/auth";
import { useFilterStore } from "@/stores/filter";

function factory(args: {
  authenticated?: boolean;
  filters?: Record<string, unknown>;
  options?: TestingOptions;
}) {
  const testingPinia = createTestingPinia(args.options);
  const authStore = useAuthStore();
  const filterStore = useFilterStore();

  const router = createRouterMock();
  injectRouterMock(router);

  // If we want to simulate the user already being authenticated, set the user in the authStore
  if (args.authenticated) {
    authStore.$state.user = {
      defaultAlertQueue: {
        uuid: "alertQueue1",
        description: null,
        value: "alertQueue",
      },
      defaultEventQueue: {
        uuid: "eventQueue1",
        description: null,
        value: "eventQueue",
      },
      displayName: "analyst",
      email: "analyst@analyst.com",
      enabled: true,
      roles: [{ uuid: "role1", description: null, value: "role1" }],
      timezone: "UTC",
      training: false,
      username: "analyst",
      uuid: "1",
    };
  }

  // If filters were given, place them in localStorage
  if (args.filters) {
    localStorage.setItem("aceFilters", JSON.stringify(args.filters));
  }

  const wrapper = mount(App, {
    attachTo: document.body,
    global: {
      plugins: [testingPinia],
    },
  });

  return { wrapper, authStore, filterStore };
}

describe("App setup", () => {
  it("renders", () => {
    const { wrapper } = factory({});

    expect(wrapper.exists()).toBe(true);
  });

  it("hydrates the filter store from localStorage if the user is authenticated", () => {
    const { filterStore } = factory({
      authenticated: true,
      filters: { alerts: { tags: ["tag1"] } },
    });

    expect(filterStore.$state).toEqual({ alerts: { tags: ["tag1"] } });
  });

  it("will not hydrate the filter store from localStorage if the user is not authenticated", () => {
    const { filterStore } = factory({
      authenticated: false,
      filters: { alerts: { tags: ["tag1"] } },
    });

    expect(filterStore.$state).toEqual({ alerts: {} });
  });
});
