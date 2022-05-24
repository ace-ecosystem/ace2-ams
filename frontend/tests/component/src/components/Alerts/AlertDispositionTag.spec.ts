import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import AlertDispositionTag from "@/components/Alerts/AlertDispositionTag.vue";

interface AlertDispositionTagProps {
  disposition: string;
}

const blue = "rgb(0, 191, 255)";
const white = "rgb(255, 255, 255)";
const black = "rgb(0, 0, 0)";

function factory(props: AlertDispositionTagProps) {
  mount(AlertDispositionTag, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: {
        config: testConfiguration,
      },
    },
    propsData: props,
  });
}

describe("AlertDispositionTag", () => {
  it("renders correctly when metadata config exists", () => {
    factory({ disposition: "TEST" });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);
  });
  it("renders correctly when metadata config does not exist", () => {
    factory({ disposition: "unknown" });
    cy.contains("unknown")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", white)
      .should("have.css", "color", black);
  });
});
