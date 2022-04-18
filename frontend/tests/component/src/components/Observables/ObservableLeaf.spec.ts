import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import ObservableLeaf from "@/components/Observables/ObservableLeaf.vue";
import router from "@/router/index";
import { observableTreeRead } from "../../../../../src/models/observable";
import { observableTreeReadFactory } from "../../../../mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

const defaultProps: { observable: observableTreeRead } = {
  observable: observableTreeReadFactory(),
};

const parentObservable = observableTreeReadFactory({
  value: "Parent Observable",
  children: [],
  tags: [genericObjectReadFactory({ value: "testTag" })],
});

const childObservable = observableTreeReadFactory({
  value: "Child Observable",
  firstAppearance: true,
  nodeMetadata: { display: { type: "custom type", value: "custom value" } },
});

function factory(args = { props: defaultProps }) {
  mount(ObservableLeaf, {
    global: {
      plugins: [PrimeVue, createCustomCypressPinia(), router],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: args.props,
  });
}

describe("ObservableLeaf", () => {
  it("renders", () => {
    factory();
  });
  it("renders an observables tags if available", () => {
    factory({
      props: { observable: parentObservable },
    });
    cy.get("span").contains("testTag");
  });
  it("displays an observables value using node metadata if available", () => {
    factory({
      props: { observable: childObservable },
    });
    cy.get("span").should(
      "contain.text",
      "custom type (testObservableType): custom value",
    );
  });
  it("sets the alert filters to the an observable's type and value when clicked", () => {
    factory({
      props: { observable: parentObservable },
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
