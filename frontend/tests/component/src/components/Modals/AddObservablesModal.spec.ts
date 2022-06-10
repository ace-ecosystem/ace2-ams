import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";

import AddObservablesModal from "@/components/Modals/AddObservablesModal.vue";
import NewObservableForm from "@/components/Observables/NewObservableForm.vue";

import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { userReadFactory } from "@mocks/user";
import { alertTreeReadFactory } from "@mocks/alert";
import { ObservableInstance } from "@/services/api/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";

const testObservableValueA = "1.2.3.4";
const testObservableValueB = "5.6.7.8";
const testObservableValueMultiA = "4.3.2.1,8.7.6.5";
const testObservableTypeA = "file";
const testObservableTypeB = "ipv4";
const testNodeDirective = "testNodeDirective";

function factory() {
  mount(AddObservablesModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            authStore: { user: userReadFactory() },
            alertStore: {
              open: alertTreeReadFactory(),
            },
            nodeDirectiveStore: {
              items: [genericObjectReadFactory({ value: testNodeDirective })],
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
    },
    provide: {
      config: testConfiguration,
    },
    propsData: {
      name: "AddObservablesModal",
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("AddObservablesModal");
    cy.get("[data-cy=AddObservablesModal]").should("be.visible");
    cy.findAllByText("Add Observable(s)").should("be.visible");
    cy.get("[data-cy='new-observable-form']").should("be.visible");
    cy.findAllByText("Actually, nevermind").should("be.visible");
    cy.findAllByText("Add!").should("be.visible");
  });
}
describe("AssignModal", () => {
  it("renders", () => {
    factory();
  });
  it("correctly makes a call to add multiple 'single'-type observables", () => {
    const stub = cy.stub(ObservableInstance, "create");
    stub
      .withArgs([
        {
          type: "ipv4",
          value: testObservableValueA,
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
          directives: [],
        },
        {
          type: "ipv4",
          value: testObservableValueB,
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
          directives: [],
        },
      ])
      .as("CreateObservables")
      .resolves();

    factory();

    // Add first observable
    cy.get("[name=observable-type]").click();
    cy.get('[aria-label="ipv4"]').click();
    cy.get("[name=observable-value] input").type(testObservableValueA);

    // Add second observable
    cy.get("#add-observable").click();
    cy.get("[name=observable-type]").eq(1).click();
    cy.get('[aria-label="ipv4"]').click();
    cy.get("[name=observable-value] input").eq(1).type(testObservableValueB);

    // Submit
    cy.contains("Add!").click();
    cy.get("@CreateObservables").should("have.been.called");

    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.emitted()).should(
        "have.property",
        "requestReload",
      );
    });
  });
  it("correctly makes a call to add observables with directives attached", () => {
    const stub = cy.stub(ObservableInstance, "create");
    stub
      .withArgs([
        {
          type: "ipv4",
          value: testObservableValueA,
          directives: ["testNodeDirective"],
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
        },
      ])
      .as("CreateObservables")
      .resolves();

    factory();

    // Add first observable
    cy.get("[name=observable-type]").click();
    cy.get('[aria-label="ipv4"]').click();
    cy.get("[name=observable-value] input").type(testObservableValueA);
    cy.contains("No directives selected").click();
    cy.contains("testNodeDirective").click();

    // Submit
    cy.contains("Add!").click();
    cy.get("@CreateObservables").should("have.been.called");

    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.emitted()).should(
        "have.property",
        "requestReload",
      );
    });
  });
  it("correctly makes a call to add 'multi-type' observables", () => {
    const stub = cy.stub(ObservableInstance, "create");
    stub
      .withArgs([
        {
          type: "ipv4",
          value: "4.3.2.1",
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
          directives: [],
        },
        {
          type: "ipv4",
          value: "8.7.6.5",
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
          directives: [],
        },
      ])
      .as("CreateObservables")
      .resolves();

    factory();

    // Add first observable
    cy.get("[name=observable-type]").click();
    cy.get('[aria-label="ipv4"]').click();

    // Switch to multi-type and enter input
    cy.get("[name=observable-value] button").click();
    cy.get("[name=observable-value] textarea").type(testObservableValueMultiA);

    // Submit
    cy.contains("Add!").click();

    cy.get("@CreateObservables").should("have.been.called");

    cy.get("body").then(() => {
      cy.wrap(Cypress.vueWrapper.emitted()).should(
        "have.property",
        "requestReload",
      );
    });
  });
  it("displays error if call to add observable fails", () => {
    const stub = cy.stub(ObservableInstance, "create");
    stub
      .withArgs([
        {
          type: "ipv4",
          value: testObservableValueA,
          historyUsername: "analyst",
          parentAnalysisUuid: "testRootAnalysisUuid",
          directives: [],
        },
      ])
      .as("CreateObservables")
      .rejects(new Error("Could not create observable"));

    factory();

    // Add first observable
    cy.get("[name=observable-type]").click();
    cy.get('[aria-label="ipv4"]').click();
    cy.get("[name=observable-value] input").type(testObservableValueA);

    // Submit
    cy.contains("Add!").click();
    cy.get("@CreateObservables").should("have.been.called");

    cy.contains("Could not create observable").should("be.visible");
  });
});
