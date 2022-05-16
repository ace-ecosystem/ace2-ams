import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import ObservableInput from "@/components/Observables/ObservableInput.vue";

interface ObservableInputProps {
  observableValue: undefined | string;
  multiAdd: boolean;
  type: string;
  invalid: boolean;
}

function factory(props: ObservableInputProps) {
  return mount(ObservableInput, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("ObservableInput", () => {
  it("renders with FileUpload component if given prop 'type' == 'file and prop 'multiAdd' == false'", () => {
    factory({
      observableValue: undefined,
      multiAdd: false,
      type: "file",
      invalid: false,
    });
    cy.contains("Choose").should("be.visible");
    cy.contains("Enter a value").should("not.exist");
    cy.contains("Enter a comma or newline-delimited list of values").should(
      "not.exist",
    );
  });
  it("renders with FileUpload component if given prop 'type' == 'file and prop 'multiAdd' == true'", () => {
    factory({
      observableValue: undefined,
      multiAdd: true,
      type: "file",
      invalid: false,
    });
    cy.contains("Choose").should("be.visible");
    cy.contains("Enter a value").should("not.exist");
    cy.contains("Enter a comma or newline-delimited list of values").should(
      "not.exist",
    );
  });
  it("renders with TextArea component if given prop 'type' !== 'file' and prop 'multiAdd' == true", () => {
    factory({
      observableValue: undefined,
      multiAdd: true,
      type: "ipv4",
      invalid: false,
    });
    cy.findByPlaceholderText(
      "Enter a comma or newline-delimited list of values",
    ).should("be.visible");
    cy.contains("Enter a value").should("not.exist");
    cy.contains("Choose").should("not.exist");
  });
  it("displays expected placeholder for InputText if given prop 'type' !== 'file' and prop 'multiAdd' == false and observable metadata does not exist", () => {
    factory({
      observableValue: undefined,
      multiAdd: false,
      type: "unknown",
      invalid: false,
    });
    cy.findByPlaceholderText("Enter a value").should("be.visible");
    cy.contains("Choose").should("not.exist");
    cy.contains("Enter a comma or newline-delimited list of values").should(
      "not.exist",
    );
  });
  it("displays expected placeholder if given prop 'type' !== 'file' and prop 'multiAdd' == false and observable metadata exists", () => {
    factory({
      observableValue: undefined,
      multiAdd: false,
      type: "ipv4",
      invalid: false,
    });
    cy.findByPlaceholderText("ex. 1.2.3.4").should("be.visible");
    cy.contains("Choose").should("not.exist");
    cy.contains("Enter a comma or newline-delimited list of values").should(
      "not.exist",
    );
  });
  it("displays validation error when expected if given prop 'type' !== 'file' and prop 'multiAdd' == false and observable metadata exists", () => {
    factory({
      observableValue: undefined,
      multiAdd: false,
      type: "ipv4",
      invalid: false,
    });
    cy.contains("ipv4 is malformed").should("not.exist");
    cy.findByPlaceholderText("ex. 1.2.3.4").type("1234");
    cy.contains("ipv4 is malformed").should("be.visible");
    cy.findByDisplayValue("1234").clear().type("1.2.3.4");
    cy.contains("ipv4 is malformed").should("not.exist");
  });
});
