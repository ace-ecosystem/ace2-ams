import TheHeader from "@/components/UserInterface/TheHeader.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import Button from "primevue/button";
import router from "@/router";

describe("TheHeader.vue", () => {
  let wrapper: VueWrapper<any>;
  beforeEach(() => {
    wrapper = mount(TheHeader, {
      global: {
        plugins: [router],
      },
    });
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("renders all buttons", () => {
    expect(wrapper.findAllComponents(Button).length).toBe(7);
  });
});
