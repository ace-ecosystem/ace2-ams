import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import AlertDispositionTag from "@/components/Alerts/AlertDispositionTag.vue";

interface AlertDispositionTagProps {
  disposition: string;
  dispositionCount?: number;
  percent?: number;
}

const blue = "rgb(0, 191, 255)";
const white = "rgb(255, 255, 255)";
const black = "rgb(0, 0, 0)";
const solid = "solid";

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
      .should("have.css", "color", black)
      .should("have.css", "border-style", solid);
  });
  it("renders correctly if dispositionCount prop is provided", () => {
    factory({ disposition: "TEST", dispositionCount: 5 });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);

    cy.contains("(5)").should("be.visible");
  });
  it("renders correctly if percent prop is provided", () => {
    factory({ disposition: "TEST", percent: 50 });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);

    cy.contains("50%").should("be.visible");
  });
  it("renders correctly if dispositionCount and percent props are provided", () => {
    factory({ disposition: "TEST", dispositionCount: 5, percent: 50 });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);

    cy.contains("50%").should("be.visible");
    cy.contains("(5)").should("be.visible");
  });
});
