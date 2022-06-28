import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { observableTreeRead, observableInAlertRead } from "@/models/observable";
import ObservableEventStatusGroup from "@/components/Observables/ObservableEventStatusGroup.vue";
import { observableInAlertReadFactory } from "../../../../mocks/observable";
import router from "@/router/index";

interface ObservableEventStatusGroupProps {
  observable: observableTreeRead | observableInAlertRead;
  rerouteToManageEvents: boolean;
}

function factory(props: ObservableEventStatusGroupProps) {
  mount(ObservableEventStatusGroup, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            eventStatusStore: {
              items: [
                genericObjectReadFactory({ value: "OPEN" }),
                genericObjectReadFactory({ value: "CLOSED" }),
                genericObjectReadFactory({ value: "OTHER" }),
              ],
            },
          },
        }),
        router,
      ],
      provide: {
        config: testConfiguration,
      },
    },
    propsData: props,
  });
}

describe("ObservableEventStatusGroup", () => {
  it("renders no tags when there are no matching event entries", () => {
    const observable = observableInAlertReadFactory({
      matchingEvents: [],
    });
    factory({ observable: observable, rerouteToManageEvents: false });
    cy.get("[data-cy='event-status-tag']").should("not.exist");
  });

  it("renders one tag when there is only one matching event entry", () => {
    const observable = observableInAlertReadFactory({
      matchingEvents: [{ count: 1, status: "OPEN" }],
    });
    factory({ observable: observable, rerouteToManageEvents: false });
    cy.get("[data-cy='event-status-tag']").should("have.length", 1);
    cy.contains("OPEN").should("be.visible");
    cy.contains("(1)").should("be.visible");
  });

  it("renders all respective tags when there are multiple matching event entries", () => {
    const observable = observableInAlertReadFactory({
      matchingEvents: [
        { count: 2, status: "OPEN" },
        { count: 3, status: "CLOSED" },
        { count: 4, status: "OTHER" },
      ],
    });
    factory({ observable: observable, rerouteToManageEvents: false });
    cy.get("[data-cy='event-status-tag']").should("have.length", 3);
    cy.contains("OPEN").should("be.visible");
    cy.contains("(2)").should("be.visible");

    cy.contains("CLOSED").should("be.visible");
    cy.contains("(3)").should("be.visible");

    cy.contains("OTHER").should("be.visible");
    cy.contains("(4)").should("be.visible");
  });

  it("sets filters as expected when click on a status", () => {
    const observable = observableInAlertReadFactory({
      matchingEvents: [
        { count: 2, status: "OPEN" },
        { count: 2, status: "CLOSED" },
        { count: 4, status: "OTHER" },
      ],
    });

    factory({ observable: observable, rerouteToManageEvents: false });
    cy.contains("OPEN").click();
    cy.get("@stub-7").should("have.been.calledWith", {
      objectType: "events",
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      objectType: "events",
      filterName: "status",
      filterValue: genericObjectReadFactory({ value: "OPEN" }),
      isIncluded: true,
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      objectType: "events",
      filterName: "observable",
      filterValue: {
        category: observable.type,
        value: observable.value,
      },
      isIncluded: true,
    });
  });
});
