import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";

import NewObservableForm from "@/components/Observables/NewObservableForm.vue";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { metadataObjectReadFactory } from "@mocks/metadata";

const testObservableTypeA = "file";
const testObservableTypeB = "ipv4";
const testDirective = "testDirective";

function factory() {
  mount(NewObservableForm, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            metadataDirectiveStore: {
              items: [metadataObjectReadFactory({ value: testDirective })],
            },
            observableTypeStore: {
              items: [
                genericObjectReadFactory({ value: testObservableTypeA }),
                genericObjectReadFactory({ value: testObservableTypeB }),
              ],
            },
          },
        }),
      ],
      provide: {
        config: testConfiguration,
      },
    },
    propsData: { modelValue: [] },
  });
}

describe("NewObservableForm", () => {
  it("renders initial observable correctly", () => {
    factory();
    // Make sure all the observable labels are there
    cy.findByText("Time (UTC)").should("be.visible");
    cy.findByText("Type").should("be.visible");
    cy.findByText("Value").should("be.visible");
    cy.findByText("Directives").should("be.visible");
    // Check all the initial inputs
    cy.get("[name=observable-time]")
      .invoke("attr", "placeholder")
      .should("contain", "No time selected");
    cy.get("[name=observable-type]").should("have.text", "file");
    cy.get("[name=observable-file-upload]").should("be.visible");
    cy.get("[name=observable-directives]").should(
      "have.text",
      "No directives selected",
    );
  });
  it("successfully renders additional and removed observables", () => {
    factory();
    // Add an observable
    cy.get("#add-observable").click();
    // Check that there's two of everything now
    cy.get("[name=observable-time]").should("have.length", 2);
    cy.get("[name=observable-type]").should("have.length", 2);
    cy.get("[name=observable-file-upload]").should("have.length", 2);

    // Delete one
    cy.get("[name=delete-observable]").eq(0).click();
    // Check that there's one of each observable input again
    cy.get("[name=observable-directives]").should("have.length", 1);
    cy.get("[name=observable-time]").should("have.length", 1);
    cy.get("[name=observable-type]").should("have.length", 1);
    cy.get("[name=observable-file-upload]").should("have.length", 1);
    cy.get("[name=observable-directives]").should("have.length", 1);
  });
  it("correctly renders observable input based on type", () => {
    factory();
    // When observable type is 'file', file input should be there
    cy.get("[name=observable-type]").should("have.text", "file");
    cy.get("[name=observable-value]").should("be.visible");
    cy.get("[name=observable-file-upload]").should("be.visible");

    // Switch to 'ipv4' input type
    cy.get("[name=observable-type]").click();
    cy.get(".p-dropdown-items").should("be.visible");
    cy.get('[aria-label="ipv4"]').click();
    cy.get(".p-dropdown-items").should("not.exist");

    // Should be input box
    cy.get("[name=observable-type]").should("have.text", "ipv4");
    cy.get("[name=observable-value] input").should("be.visible");
    cy.get("[name=observable-file-upload]").should("not.exist");

    // Switch back to 'file,' should be the file input again
    cy.get("[name=observable-type]").click();
    cy.get(".p-dropdown-items").should("be.visible");
    cy.get('[aria-label="file"]').click();
    cy.get(".p-dropdown-items").should("not.exist");
    cy.get("[name=observable-type]").should("have.text", "file");
    cy.get("[name=observable-value]").should("be.visible");
    cy.get("[name=observable-file-upload]").should("be.visible");
  });
  it("correctly toggles multi-add observable input", () => {
    factory();
    // Switch to 'ipv4' input type
    cy.get("[name=observable-type]").click();
    cy.get('[aria-label="ipv4"]').click();
    cy.get("[name=observable-value] input").should("be.visible");

    // Switch to 'multi' mode
    cy.get("[name=observable-value] button").click();
    cy.get("[name=observable-value] input").should("not.exist");
    cy.get("[name=observable-value] textarea")
      .should("be.visible")
      .invoke("attr", "placeholder")
      .should("contain", "Enter a comma or newline-delimited list of values");

    // Switch back
    cy.get("[name=observable-value] button").click();
    cy.get("[name=observable-value] input").should("be.visible");
    cy.get("[name=observable-value] textarea").should("not.exist");
  });
});
