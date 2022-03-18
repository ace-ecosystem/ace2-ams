import { visitUrl } from "./helpers";

describe("ViewAnalysis.vue", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add the test alert to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_alerts",
      body: {
        template: "small.json",
        count: 1,
      },
    });
  });

  beforeEach(() => {
    // Intercept the API call that loads the alert data
    cy.intercept("GET", "/api/alert/02f8299b-2a24-400f-9751-7dd9164daf6a").as(
      "getAlert",
    );

    visitUrl({
      url: "/alert/02f8299b-2a24-400f-9751-7dd9164daf6a",
      extraIntercepts: ["@getAlert"],
    });

    // Open up the "Test Analysis" analysis details
    cy.get('[data-cy="Test Analysis"]').contains("Test Analysis").click();
  });

  it("View Analysis page renders", () => {
    cy.get("#view-analysis").should("be.visible");
  });

  it("Will display breadcrumbs back to alert and home", () => {
    // There should be 3 breadcrumbs
    cy.get(".p-menuitem-link").should("have.length", 3);

    // There should be a home breadcrumb
    cy.get(".p-breadcrumb-home > .p-menuitem-link").should("be.visible");

    // There should be a breadcrumb to the parent alert
    cy.get(".p-menuitem-link").contains('"Small Alert"').should("be.visible");

    // There should be a breadcrumb representing the current analysis
    cy.get(".p-menuitem-link").contains('"Test Analysis"').should("be.visible");
  });

  it("Will route to home (Manage Alerts) when home breadcrumb is clicked", () => {
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("getAlerts");

    cy.get(".p-breadcrumb-home > .p-menuitem-link").click();
    cy.wait("@getAlerts").its("state").should("eq", "Complete");
    cy.url().should("contain", "/manage_alerts");
  });

  it("Will route to parent alert when alert breadcrumb is clicked", () => {
    cy.get(".p-menuitem-link").contains('"Small Alert"').click();
    cy.wait("@getAlert").its("state").should("eq", "Complete");
    cy.url().should(
      "not.contain",
      "/alert/02f8299b-2a24-400f-9751-7dd9164daf6a/",
    );
    cy.url().should("contain", "/alert/02f8299b-2a24-400f-9751-7dd9164daf6a");
  });
  it("should not route anywhere when analysis breadcrumb is clicked", () => {
    cy.get(".p-menuitem-link").contains('"Test Analysis"').click();
    cy.url().should("contain", "/alert/02f8299b-2a24-400f-9751-7dd9164daf6a/");
  });
});
