import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import TheEventDetailsMenuBar from "@/components/Events/TheEventDetailsMenuBar.vue";
import router from "@/router/index";

import { testConfiguration } from "@/etc/configuration/test/index";
import { eventRead } from "@/models/event";
import { eventReadFactory } from "@mocks/events";
import { userReadFactory } from "@mocks/user";

const props = {
  eventUuid: "uuid",
};

function factory(event: eventRead = eventReadFactory()) {
  return mount(TheEventDetailsMenuBar, {
    global: {
      provide: {
        nodeType: "events",
        availableEditFields: testConfiguration.events.eventEditableProperties,
        analysisModuleComponents:
          testConfiguration.analysis.analysisModuleComponents,
        closedEventStatus: testConfiguration.events.closedEventStatus,
      },
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
            eventStore: {
              open: event,
              requestReload: false,
            },
            selectedEventStore: {
              selected: ["uuid"],
            },
          },
        }),
        router,
      ],
    },
    propsData: props,
  });
}

describe("TheEventDetailsMenuBar", () => {
  it("renders defaults correctly (no analysis available)", () => {
    factory();
    cy.findByRole("menubar")
      .should("be.visible")
      .children()
      .should("have.length", 3);

    const actionsLinks = [
      "Comment",
      "Take Ownership",
      "Assign",
      "Add Tags",
      "Edit Event",
      "Close Event",
    ];

    cy.findByRole("menubar")
      .children()
      .eq(0)
      .children()
      .eq(0)
      .should("have.text", "Actions")
      .click();
    actionsLinks.forEach((link) => {
      cy.contains(link).should("be.visible");
    });
    cy.contains("Actions").click(); // Close menu panel

    const informationLinks = [
      "Event Summary",
      "Alert Summary",
      "Detection Summary",
      "URL Summary",
      "URL Domain Summary",
      "Observable Summary",
    ];

    cy.findByRole("menubar")
      .children()
      .eq(1)
      .children()
      .eq(0)
      .should("have.text", "Information")
      .click();
    informationLinks.forEach((link) => {
      cy.contains(link).should("be.visible");
    });
    cy.contains("Information").click(); // Close menu panel

    cy.findByRole("menubar")
      .children()
      .eq(2)
      .children()
      .eq(0)
      .should("have.text", "Analysis");

    cy.findByRole("menubar")
      .children()
      .eq(2)
      .children()
      .eq(1)
      .children()
      .should("have.length", 1)
      .should("have.text", "Analysis Details");
  });
  it("correctly attempts to open respective 'action' modals", () => {
    factory();
    // Comment
    cy.contains("Actions").click();
    cy.contains("Comment").click();
    cy.get("@stub-5").should("have.been.calledWith", "CommentModal");
    // Assign
    cy.contains("Actions").click();
    cy.contains("Assign").click();
    cy.get("@stub-5").should("have.been.calledWith", "AssignModal");
    // Edit
    cy.contains("Actions").click();
    cy.contains("Edit Event").click();
    cy.get("@stub-5").should("have.been.calledWith", "EditEventModal-uuid");
    // Tag
    cy.contains("Actions").click();
    cy.contains("Add Tags").click();
    cy.get("@stub-5").should("have.been.calledWith", "TagModal");
  });
  it("makes a request to update event with current user as owner when 'Take Ownership' menu link clicked", () => {
    factory();
    cy.contains("Actions").click();
    cy.contains("Take Ownership").click();
    cy.get("@stub-3").should("have.been.calledWith", [
      {
        uuid: "uuid",
        owner: "analyst",
        historyUsername: "analyst",
      },
    ]);
  });
  it("makes a request to update event with configured closed status when 'Close Event' menu link clicked", () => {
    factory();
    cy.contains("Actions").click();
    cy.contains("Close Event").click();
    cy.get("@stub-3").should("have.been.calledWith", [
      {
        uuid: "uuid",
        status: "CLOSED",
        historyUsername: "analyst",
      },
    ]);
  });
  it("correctly renders analysis links", () => {
    const eventWithAnalysis = eventReadFactory({
      analysisTypes: [
        "User Analysis",
        "Sandbox Analysis - Cuckoo",
        "Sandbox Analysis - Falcon",
        "Unknown Analysis",
      ],
    });

    factory(eventWithAnalysis);
    cy.contains("Analysis")
      .click()
      .parent()
      .children()
      .eq(1)
      .should("be.visible");

    cy.contains("Analysis")
      .parent()
      .children()
      .eq(1)
      .children()
      .findAllByRole("menuitem")
      .should("have.length", 2);

    cy.contains("Analysis")
      .parent()
      .children()
      .eq(1)
      .children()
      .findAllByRole("menuitem")
      .eq(0)
      .should("have.text", "User Analysis");

    cy.contains("Analysis")
      .parent()
      .children()
      .eq(1)
      .children()
      .findAllByRole("menuitem")
      .eq(1)
      .should("have.text", "Sandbox Analysis");
  });
  it("correctly emits sectionClicked with section name when menu item link is clicked", () => {
    factory();
    cy.contains("Information").click();
    cy.contains("Event Summary")
      .click()
      .then(() => {
        expect(Cypress.vueWrapper.emitted("sectionClicked")).eqls([
          ["Event Summary"],
        ]);
      });
  });
});
