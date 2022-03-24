// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import EmailAnalysisHeadersBody from "@/components/Analysis/EmailAnalysisHeadersBody.vue";
import router from "@/router/index";

const props = {
  eventUuid: "uuid",
};

describe("EmailAnalysisHeadersBody", () => {
  it("renders", () => {
    mount(EmailAnalysisHeadersBody, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
      },
      propsData: props,
    });
  });
});
