import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";

import TheEventsTable from "@/components/Events/TheEventsTable.vue";
import router from "@/router/index";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { eventRead } from "@/models/event";
import { eventReadFactory } from "@mocks/events";
import NodeQueueSelectorVue from "@/components/Node/NodeQueueSelector.vue";
import { nodeThreatRead } from "@/models/nodeThreat";

interface eventTableStoreState {
  visibleQueriedItems: eventRead[];
  totalItems: number;
  sortField: string | null;
  sortOrder: string | null;
  pageSize: number;
  requestReload: boolean;
  stateFiltersLoaded: boolean;
  routeFiltersLoaded: boolean;
}

const initialStateDefault: eventTableStoreState = {
  visibleQueriedItems: [],
  totalItems: 0,
  sortField: "eventTime",
  sortOrder: "desc",
  pageSize: 10,
  requestReload: false,
  stateFiltersLoaded: false,
  routeFiltersLoaded: false,
};

function factory(initialState: eventTableStoreState) {
  mount(TheEventsTable, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            eventTableStore: initialState,
            currentUserSettingsStore: {
              queues: {
                alerts: null,
                events: genericObjectReadFactory({ value: "external" }),
              },
            },
          },
        }),
        router,
      ],
      provide: {
        nodeType: "events",
        config: testConfiguration,
      },
    },
  });

  cy.findByRole("table");
  cy.vue().then((wrapper) => {
    expect(wrapper.findComponent(NodeQueueSelectorVue)).to.exist;
  });
}

describe("TheEventsTable", () => {
  it("renders when there are no events to show", () => {
    factory(initialStateDefault);
    const defaultColumnHeaders = [
      "",
      "",
      "",
      "Created",
      "Name",
      "Threats",
      "Risk Level",
      "Status",
      "Owner",
    ];
    cy.get("tr").should("have.length", 2);
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", defaultColumnHeaders[index]);
      });
  });
  it("renders when events table store has events to show", () => {
    const defaultColumnHeaders = [
      "",
      "",
      "",
      "Created",
      "Name",
      "Threats",
      "Risk Level",
      "Status",
      "Owner",
    ];
    const defaultColumnValues = [
      "",
      "",
      "",
      "1/1/2020, 12:00:00 AM",
      "Test Event",
      "ThreatA, ThreatB",
      "low",
      "None",
      "None",
    ];

    const threats: nodeThreatRead[] = [
      { ...genericObjectReadFactory({ value: "ThreatA" }), types: [] },
      { ...genericObjectReadFactory({ value: "ThreatB" }), types: [] },
    ];

    factory({
      ...initialStateDefault,
      visibleQueriedItems: [
        eventReadFactory({
          threats: threats,
          riskLevel: genericObjectReadFactory({ value: "low" }),
        }),
        eventReadFactory({ value: "Test Event 2", uuid: "uuid2" }),
      ],
      totalItems: 1,
    });
    cy.get("tr").should("have.length", 3);
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
        if (index === 0) {
          cy.wrap($li).get(".p-row-toggler-icon").should("be.visible");
        } else if (index === 1) {
          cy.wrap($li).findByRole("checkbox").should("be.visible");
        } else if (index === 2) {
          cy.wrap($li)
            .get('[data-cy="edit-event-button"]')
            .should("be.visible");
        } else {
          cy.wrap($li).should("contain.text", defaultColumnValues[index]);
        }
      });
  });
  it("updates columns and reloads table when preferred event queue changes", () => {
    factory(initialStateDefault);
    const internalQueue = genericObjectReadFactory({ value: "internal" });
    cy.vue().then((wrapper) => {
      // Table should not change if preferred alert queue changes
      wrapper.vm.currentUserSettingsStore.queues.alerts = internalQueue;
      const defaultColumnHeaders = [
        "",
        "",
        "",
        "Created",
        "Name",
        "Threats",
        "Risk Level",
        "Status",
        "Owner",
      ];
      cy.get("tr").should("have.length", 2);
      cy.get("tr")
        .eq(0)
        .children()
        .each(($li, index) => {
          cy.wrap($li).should("have.text", defaultColumnHeaders[index]);
        });
    });
    cy.vue().then((wrapper) => {
      // Table SHOULD update if preferred event queue changes
      wrapper.vm.currentUserSettingsStore.queues.events = internalQueue;
      const updatedColumnHeaders = ["", "", "", "Created", "Name", "Type"];
      cy.get("tr").should("have.length", 2);
      cy.get("tr")
        .eq(0)
        .children()
        .each(($li, index) => {
          cy.wrap($li).should("have.text", updatedColumnHeaders[index]);
        });
    });
  });
});
