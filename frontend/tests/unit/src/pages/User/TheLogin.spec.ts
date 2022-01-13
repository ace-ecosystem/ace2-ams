import TheLogin from "@/pages/User/TheLogin.vue";
import { shallowMount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { createRouterMock, injectRouterMock } from "vue-router-mock";

describe("TheLogin.vue", () => {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper = shallowMount(TheLogin, {
    global: {
      plugins: [createTestingPinia()],
    },
  });
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
