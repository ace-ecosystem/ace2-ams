import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import ObservableLeaf from "@/components/Observables/ObservableLeaf.vue";
import router from "@/router/index";
import { observableTreeRead } from "../../../../../src/models/observable";
import { observableTreeReadFactory } from "../../../../mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { testConfiguration } from "@/etc/configuration/test";

interface ObservableLeafProps {
  observable: observableTreeRead;
  showCopyToClipboard?: boolean;
  showActionsMenu?: boolean;
  showTags?: boolean;
}

const defaultProps: ObservableLeafProps = {
  observable: observableTreeReadFactory(),
};

function factory(
  args: { props: ObservableLeafProps } = { props: defaultProps },
) {
  mount(ObservableLeaf, {
    global: {
      plugins: [PrimeVue, createCustomCypressPinia(), router],
      provide: {
        config: testConfiguration,
        nodeType: "alerts",
      },
    },
    propsData: args.props,
  });
}

describe("ObservableLeaf", () => {
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

  it("renders correctly with all optional props set to false", () => {
    factory({
      props: {
        observable: observableTreeReadFactory(),
        showCopyToClipboard: false,
        showActionsMenu: false,
        showTags: false,
      },
    });
  });
  it("renders correctly with default props", () => {
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
