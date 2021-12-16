import TheHeader from "@/components/UserInterface/TheHeader.vue";
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import Button from "primevue/button";
import router from "@/router";

describe("TheHeader.vue", () => {
  const wrapper = mount(TheHeader, {
    global: {
      plugins: [router, createTestingPinia()],
    },
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("renders all buttons", () => {
    expect(wrapper.findAllComponents(Button).length).toBe(7);
  });
});
