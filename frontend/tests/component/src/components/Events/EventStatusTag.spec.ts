import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import EventStatusTag from "@/components/Events/EventStatusTag.vue";

interface EventStatusTagProps {
  status: string;
  statusCount?: number;
}

const blue = "rgb(0, 191, 255)";
const white = "rgb(255, 255, 255)";
const black = "rgb(0, 0, 0)";
const solid = "solid";

function factory(props: EventStatusTagProps) {
  mount(EventStatusTag, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: {
        config: testConfiguration,
      },
    },
    propsData: props,
  });
}

describe("EventStatusTag", () => {
  it("renders correctly when metadata config exists", () => {
    factory({ status: "TEST" });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);
  });
  it("renders correctly when metadata config does not exist", () => {
    factory({ status: "unknown" });
    cy.contains("unknown")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", white)
      .should("have.css", "color", black)
      .should("have.css", "border-style", solid);
  });
  it("renders correctly if statusCount prop is provided", () => {
    factory({ status: "TEST", statusCount: 5 });
    cy.contains("TEST")
      .should("be.visible")
      .parent()
      .should("have.css", "background-color", blue)
      .should("have.css", "color", white);

    cy.contains("(5)").should("be.visible");
  });
});
