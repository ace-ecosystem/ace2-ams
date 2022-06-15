import { mount } from "@cypress/vue";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";
import EventSummary from "@/components/Events/EventSummary.vue";
import router from "@/router/index";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { eventReadFactory } from "@mocks/events";
import { genericObjectReadFactory } from "@mocks/genericObject";

const props = {
  eventUuid: "uuid",
};

const manualTime = new Date(Date.UTC(2022, 2, 29, 12, 0, 0, 0));
const autoTime = new Date(Date.UTC(2022, 2, 30, 12, 0, 0, 0));

function factory(initialState = {}) {
  return mount(EventSummary, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({ initialState: initialState }),
        router,
      ],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("EventSummary", () => {
  const openEventDefaults = eventReadFactory({
    queue: genericObjectReadFactory({ value: "external" }),
  });
  const openEventManual = eventReadFactory({
    eventTime: manualTime,
    alertTime: manualTime,
    ownershipTime: manualTime,
    dispositionTime: manualTime,
    containTime: manualTime,
    remediationTime: manualTime,
    queue: genericObjectReadFactory({ value: "external" }),
  });
  const openEventAuto = eventReadFactory({
    autoEventTime: autoTime,
    autoAlertTime: autoTime,
    autoOwnershipTime: autoTime,
    autoDispositionTime: autoTime,
    queue: genericObjectReadFactory({ value: "external" }),
  });

  const expectedDefaultColHeaders = [
    "Created",
    "Name",
    "Threats",
    "Severity",
    "Status",
    "Owner",
  ];

  it("renders when there is no open event available", () => {
    factory();
    cy.contains("Event data not found.");
  });

  it("renders table when there is an open event available", () => {
    factory({ eventStore: { open: openEventDefaults, requestReload: false } });

    cy.get("#event-summary-timeline").should("be.visible");
    cy.findByRole("table").should("be.visible");

    cy.get("tr").should("have.length", 2);
    cy.get("tr")
      .eq(1)
      .children()
      .each(($el, index) => {
        cy.wrap($el).should("contain.text", expectedDefaultColHeaders[index]);
      });
  });

  it("renders correctly updates and resets columns on user input", () => {
    const expandedColHeaders = [...expectedDefaultColHeaders, "Queue"];

    factory({ eventStore: { open: openEventDefaults, requestReload: false } });

    // Select additional column
    cy.contains("Created, Name, Threats, Severity, Status, Owner").click();
    cy.get('[aria-label="Queue"]').click();
    cy.get(".p-multiselect-close").click();

    // Check new column headers
    cy.get("tr")
      .eq(1)
      .children()
      .each(($el, index) => {
        cy.wrap($el).should("contain.text", expandedColHeaders[index]);
      });

    // Reset
    cy.get('[data-cy="reset-table-button"]').click();

    // Check again
    cy.get("tr")
      .eq(1)
      .children()
      .each(($el, index) => {
        cy.wrap($el).should("contain.text", expectedDefaultColHeaders[index]);
      });
  });

  const eventsParameters = [
    [openEventDefaults, "TBD", "default"],
    [openEventManual, manualTime, "manual"],
    [openEventAuto, autoTime, "auto"],
  ];

  eventsParameters.forEach(($event) => {
    const [event, expectedTime, eventTimeType] = $event;

    it(`renders timeline correctly when there is an open event available with all ${eventTimeType} values`, () => {
      factory({ eventStore: { open: event, requestReload: false } });

      cy.get('[data-cy="event-summary-timeline-label"]').should(
        "have.length",
        6,
      );
      cy.get('[data-cy="event-summary-timeline-datetime"]').should(
        "have.length",
        6,
      );

      if (eventTimeType === "default") {
        cy.get('[data-cy="event-summary-timeline-datetime"]').each(($el) => {
          cy.wrap($el).should("contain.text", "TBD");
        });
      } else if (eventTimeType === "manual") {
        cy.get('[data-cy="event-summary-timeline-datetime"]').each(($el) => {
          cy.wrap($el).should(
            "contain.text",
            expectedTime.toLocaleString("en-US", { timeZone: "UTC" }),
          );
        });
      } else if (eventTimeType === "auto") {
        cy.get('[data-cy="event-summary-timeline-datetime"]').each(
          ($el, index) => {
            if (index < 4) {
              cy.wrap($el).should(
                "contain.text",
                expectedTime.toLocaleString("en-US", { timeZone: "UTC" }),
              );
            } else {
              cy.wrap($el).should("contain.text", "TBD");
            }
          },
        );
      }
    });
  });
});
