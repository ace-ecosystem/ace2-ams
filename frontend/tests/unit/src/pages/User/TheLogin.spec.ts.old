import TheLogin from "@/pages/User/TheLogin.vue";
import { shallowMount } from "@vue/test-utils";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { createCustomPinia } from "@unit/helpers";

describe("TheLogin.vue", () => {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper = shallowMount(TheLogin, {
    global: {
      plugins: [createCustomPinia()],
    },
  });
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
