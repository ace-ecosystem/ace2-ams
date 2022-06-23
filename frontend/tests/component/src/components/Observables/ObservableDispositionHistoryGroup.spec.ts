import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { observableTreeRead, observableInAlertRead } from "@/models/observable";
import ObservableDispositionHistoryGroup from "@/components/Observables/ObservableDispositionHistoryGroup.vue";
import { observableInAlertReadFactory } from "../../../../mocks/observable";
import router from "@/router/index";

interface ObservableDispositionHistoryGroupProps {
  observable: observableTreeRead | observableInAlertRead;
  rerouteToManageAlerts: boolean;
}

function factory(props: ObservableDispositionHistoryGroupProps) {
  mount(ObservableDispositionHistoryGroup, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            alertDispositionStore: {
              items: [
                genericObjectReadFactory({ value: "UNKNOWN" }),
                genericObjectReadFactory({ value: "FALSE_POSITIVE" }),
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

describe("ObservableDispositionHistoryGroup", () => {
  it("renders no tags when there are no disposition history entries", () => {
    const observable = observableInAlertReadFactory({
      dispositionHistory: [],
    });
    factory({ observable: observable, rerouteToManageAlerts: false });
    cy.get("[data-cy='disposition-tag']").should("not.exist");
  });
  it("renders one tag when there is only one disposition history entry", () => {
    const observable = observableInAlertReadFactory({
      dispositionHistory: [
        { count: 1, disposition: "testDisposition", percent: 100 },
      ],
    });
    factory({ observable: observable, rerouteToManageAlerts: false });
    cy.get("[data-cy='disposition-tag']").should("have.length", 1);
    cy.contains("testDisposition").should("be.visible");
    cy.contains("100%").should("be.visible");
    cy.contains("(1)").should("be.visible");
  });
  it("renders all respective tags when there is multiple disposition history entries", () => {
    const observable = observableInAlertReadFactory({
      dispositionHistory: [
        { count: 2, disposition: "UNKNOWN", percent: 25 },
        { count: 2, disposition: "OPEN", percent: 25 },
        { count: 4, disposition: "FALSE_POSITIVE", percent: 50 },
      ],
    });
    factory({ observable: observable, rerouteToManageAlerts: false });
    cy.get("[data-cy='disposition-tag']").should("have.length", 3);
    cy.contains("UNKNOWN").should("be.visible");
    cy.contains("OPEN").should("be.visible");
    cy.contains("25%").should("be.visible");
    cy.contains("(2)").should("be.visible");

    cy.contains("FALSE_POSITIVE").should("be.visible");
    cy.contains("50%").should("be.visible");
    cy.contains("(4)").should("be.visible");
  });
  it("sets filters as expected when on click of 'OPEN' disposition", () => {
    const observable = observableInAlertReadFactory({
      dispositionHistory: [
        { count: 2, disposition: "UNKNOWN", percent: 25 },
        { count: 2, disposition: "OPEN", percent: 25 },
        { count: 4, disposition: "FALSE_POSITIVE", percent: 50 },
      ],
    });
    factory({ observable: observable, rerouteToManageAlerts: false });
    cy.contains("OPEN").click();
    cy.get("@stub-7").should("have.been.calledWith", {
      nodeType: "alerts",
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "disposition",
      filterValue: { value: "None" },
      isIncluded: true,
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "observable",
      filterValue: {
        category: observable.type,
        value: observable.value,
      },
      isIncluded: true,
    });
  });
  it("sets filters as expected on click of non-'OPEN' disposition", () => {
    const observable = observableInAlertReadFactory({
      dispositionHistory: [
        { count: 2, disposition: "UNKNOWN", percent: 25 },
        { count: 2, disposition: "OPEN", percent: 25 },
        { count: 4, disposition: "FALSE_POSITIVE", percent: 50 },
      ],
    });
    factory({ observable: observable, rerouteToManageAlerts: false });
    cy.contains("UNKNOWN").click();
    cy.get("@stub-7").should("have.been.calledWith", {
      nodeType: "alerts",
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "disposition",
      filterValue: genericObjectReadFactory({ value: "UNKNOWN" }),
      isIncluded: true,
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "observable",
      filterValue: {
        category: observable.type,
        value: observable.value,
      },
      isIncluded: true,
    });
  });
});
