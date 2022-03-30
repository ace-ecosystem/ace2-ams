import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTableExpansion from "@/components/Alerts/AlertTableExpansion.vue";

import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { observableRead } from "@/models/observable";
import { observableReadFactory } from "@mocks/observable";
import router from "@/router/index";

interface AlertTableExpansionProps {
  observables: observableRead[] | null;
}

const defaultProps: AlertTableExpansionProps = {
  observables: null,
};

function factory(
  args = {
    props: defaultProps,
  },
) {
  return mount(AlertTableExpansion, {
    global: {
      plugins: [createCustomCypressPinia(), PrimeVue, router],
      provide: { nodeType: "alerts" },
    },
    propsData: args.props,
  });
}

describe("AlertTableExpansion", () => {
  it("renders with observables prop set to null (loading state)", () => {
    factory();
    cy.get("ul").should("be.visible");
    cy.get('[data-cy="loading-observable"]').should("have.length", 4);
  });
  it("renders with observables prop set to empty", () => {
    factory({ props: { observables: [] } });
    cy.get("ul").should("not.exist");
    cy.contains("No observables exist for this alert.");
  });
  it("renders with observables containing observables with tags", () => {
    factory({
      props: {
        observables: [
          observableReadFactory(),
          observableReadFactory({
            value: "TestObservable2",
            tags: [genericObjectReadFactory({ value: "testTag" })],
          }),
        ],
      },
    });
    // Check that the observables (and any tags) showed up
    cy.get("li").contains("testObservableType : TestObservable");
    cy.get("li").contains("testObservableType : TestObservable2");
    cy.get("li").eq(1).contains("testTag");
  });
  it("renders with observables containing observables with tags", () => {
    const observable = observableReadFactory();
    factory({
      props: {
        observables: [observable],
      },
    });
    cy.contains("testObservableType : TestObservable").click();
    cy.get("@stub-1").should("have.been.calledWith", {
      nodeType: "alerts",
      filters: {
        observable: { category: observable.type, value: observable.value },
      },
    });
  });
});
