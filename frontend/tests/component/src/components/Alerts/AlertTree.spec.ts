// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTree from "@/components/Alerts/AlertTree.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import router from "@/router/index";
import { observableTreeRead } from "@/models/observable";
import { analysisTreeRead } from "@/models/analysis";
import { observableTreeReadFactory } from "@mocks/observable";
import {
  analysisModuleTypeNodeTreeReadFactory,
  analysisTreeReadFactory,
} from "@mocks/analysis";
import { genericObjectReadFactory } from "@mocks/genericObject";

const childObservable = observableTreeReadFactory({
  value: "Child Observable",
  firstAppearance: true,
  nodeMetadata: { display: { type: "custom type", value: "custom value" } },
});
const childAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeNodeTreeReadFactory({
    value: "Child Analysis",
  }),
});
const parentObservable = observableTreeReadFactory({
  value: "Parent Observable",
  children: [childAnalysis],
  tags: [genericObjectReadFactory({ value: "testTag" })],
});
const parentAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeNodeTreeReadFactory({
    value: "Parent Analysis",
  }),
  children: [childObservable],
  firstAppearance: true,
});
interface AlertTreeProps {
  items: (analysisTreeRead | observableTreeRead)[];
  alertId: string;
}

const defaultProps: AlertTreeProps = {
  items: [],
  alertId: "test",
};

function factory(
  args = {
    props: defaultProps,
  },
) {
  return mount(AlertTree, {
    global: {
      plugins: [createCustomCypressPinia(), PrimeVue, router],
      provide: { nodeType: "alerts" },
    },
    propsData: args.props,
  });
}

describe("AlertTree", () => {
  it("renders when there are no given items", () => {
    factory();
  });
  it("correctly renders list items that include children", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    // 3 Visible to start
    cy.get("li").should("have.length", 3);

    // Check icons and values
    cy.get("li").eq(0).get(".pi-chevron-right");
    cy.get("li")
      .eq(0)
      .should("contain.text", "Parent Observable")
      .get(".pi-chevron-right");

    cy.get("li").eq(1).get(".pi-chevron-down");
    cy.get("li")
      .eq(1)
      .should("contain.text", "Parent Analysis")
      .get(".pi-chevron-right");

    cy.get("li").eq(2).get(".pi-minus");
    cy.get("li")
      .eq(2)
      .should("contain.text", "testObservableType")
      .get(".pi-chevron-right");
  });
  it("renders an observables tags if available", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    cy.get("li").eq(0).contains("testTag");
  });
  it("displays an observables value using node metadata if available", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    cy.get("li")
      .eq(2)
      .should("contain.text", "custom type (testObservableType): custom value")
      .get(".pi-chevron-right");
  });
  it("toggles showing child nodes (analysis or observables) when toggle clicked", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    // Click first toggle
    cy.get(".pi-chevron-right").click();
    // Check newest
    cy.get("li")
      .eq(1)
      .should("contain.text", "Child Analysis")
      .get(".pi-minus");

    // Click toggle again
    cy.get(".pi-chevron-down").eq(0).click();
    // Should be 3 again
    cy.get("li").should("have.length", 3);
    cy.contains("Child Analysis").should("not.exist");
  });
  it("renders analysis list items with a link to that analysis's specifc page", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    cy.contains("Parent Analysis")
      .invoke("attr", "href")
      .should("contain", "/alert/test/testUuid");
  });
  it("sets the alert filters to the an observable's type and value when clicked", () => {
    factory({
      props: { items: [parentObservable, parentAnalysis], alertId: "test" },
    });
    cy.contains("Parent Observable").click();
    cy.get("@stub-1").should("have.been.calledWith", {
      nodeType: "alerts",
      filters: {
        observable: {
          category: parentObservable.type,
          value: parentObservable.value,
        },
      },
    });
  });
});
