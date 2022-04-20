import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import TheAlertsTable from "@/components/Alerts/TheAlertsTable.vue";
import router from "@/router/index";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertRead } from "@/models/alert";
import { alertReadFactory } from "@mocks/alert";
import { NodeTree } from "@/services/api/nodeTree";
import { observableReadFactory } from "@mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";

interface alertTableStoreState {
  visibleQueriedItems: alertRead[];
  totalItems: number;
  sortField: string | null;
  sortOrder: string | null;
  pageSize: number;
  requestReload: boolean;
  stateFiltersLoaded: boolean;
  routeFiltersLoaded: boolean;
}

const initialStateDefault: alertTableStoreState = {
  visibleQueriedItems: [],
  totalItems: 0,
  sortField: "eventTime",
  sortOrder: "desc",
  pageSize: 10,
  requestReload: false,
  stateFiltersLoaded: false,
  routeFiltersLoaded: false,
};

function factory(initialState: alertTableStoreState) {
  return mount(TheAlertsTable, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: { alertTableStore: initialState },
        }),
        router,
      ],
      provide: {
        nodeType: "alerts",
      },
    },
  });
}

describe("TheAlertsTable", () => {
  it("renders when alert table is empty", () => {
    factory(initialStateDefault);
  });
  it("renders when alert table store has alerts", () => {
    const defaultColumnHeaders = [
      "",
      "",
      "Event Time",
      "Name",
      "Owner",
      "Disposition",
    ];
    const defaultColumnValues = [
      "",
      "",
      "3/24/2022, 12:00:00 AM",
      "Test Alert",
      "None",
      "OPEN",
    ];

    factory({
      ...initialStateDefault,
      visibleQueriedItems: [alertReadFactory()],
      totalItems: 1,
    });
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", defaultColumnHeaders[index]);
      });
    cy.get("tr")
      .eq(1)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", defaultColumnValues[index]);
      });
  });
  it("attempts to fetch and show observables when alert dropdown is clicked", () => {
    // Make sure that observables are sorted as expected
    // Alphabetically by type, and then alphatbetically by value within type
    const testObservables = [
      observableReadFactory({ value: "Z-Value" }),
      observableReadFactory({ value: "A-Value" }),
      observableReadFactory({
        type: genericObjectReadFactory({ value: "A-Type" }),
      }),
    ];

    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(["testAlertUuid"], "observable")
      .as("getObservables")
      .resolves(testObservables);
    factory({
      ...initialStateDefault,
      visibleQueriedItems: [alertReadFactory()],
      totalItems: 1,
    });
    cy.get(".p-row-toggler").click();
    cy.get("[data-cy=row-expansion]").should("be.visible");
    cy.get("li").eq(0).should("contain.text", "A-Type");
    cy.get("li").eq(1).should("contain.text", "A-Value");
    cy.get("li").eq(2).should("contain.text", "Z-Value");
    cy.get(".p-row-toggler").click();
    cy.get("[data-cy=row-expansion]").should("not.exist");
  });
});
