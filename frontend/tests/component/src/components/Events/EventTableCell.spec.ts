// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import EventTableCell from "@/components/Events/EventTableCell.vue";

import router from "@/router/index";

const props = {
  data: {
    name: "test",
    tags: [],
    childTags: [],
    comments: [],
    insert_time: "03/23/2022",
    uuid: "test",
  },
  field: "name",
};

describe("EventTableCell", () => {
  it("renders", () => {
    mount(EventTableCell, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
      },
      propsData: props,
    });
  });
});
