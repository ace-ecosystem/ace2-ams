// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";

import TheNodeTable from "@/components/Node/TheNodeTable.vue";

const props = {
    columns: [{ field: "name", header: "Name", sortable: true, default: true }],
};

describe("TheNodeTable", () => {
  it("renders", () => {
    mount(TheNodeTable, {
      global: {
        plugins: [PrimeVue, createPinia()],
        provide: {nodeType: "alerts"}
      },
      propsData: props,
    });
  });
});
