import TheLogin from "@/pages/User/TheLogin.vue";
import { shallowMount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";

describe("TheLogin.vue", () => {
  const wrapper = shallowMount(TheLogin, {
    global: {
      plugins: [createTestingPinia()],
    },
  });
  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });
});
