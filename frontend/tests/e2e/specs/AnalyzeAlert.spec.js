import { visitUrl } from "./helpers";

const addMultipleObservables = () => {
  // Add first (single) observable
  cy.get("div[name='observable-type']").click();
  cy.get("div[name='observable-input']")
    .get(".p-dropdown-item", { timeout: 5_000 })
    .contains("ipv4")
    .click();
  cy.get("div[name='observable-value']").find("input").type("1.2.3.4");

  // Add second (multi-input, comma-separated) observable
  cy.get("#add-observable").click();
  cy.get("div[name='observable-type']").last().click();
  cy.get("div[name='observable-input']")
    .get(".p-dropdown-item", { timeout: 5_000 })
    .contains("ipv4")
    .click();
  cy.get("div[name='observable-value']").find("button").last().click();
  cy.get("div[name='observable-value']")
    .find("textarea")
    .type("5.6.7.8,8.7.6.5");

  // Add third (multi-input, newline-separated) observable
  cy.get("#add-observable").click();
  cy.get("div[name='observable-type']").last().click();
  cy.get("div[name='observable-input']")
    .get(".p-dropdown-item", { timeout: 5_000 })
    .contains("ipv4")
    .click();
  cy.get("div[name='observable-value']").find("button").last().click();
  cy.get("div[name='observable-value']")
    .find("textarea")
    .last()
    .type("0.0.0.0\n4.3.2.1");
};

describe("AnalyzeAlert.vue", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();
  });

  beforeEach(() => {
    visitUrl({ url: "/analyze" });
  });

  it("Add observable button adds another row", () => {
    cy.get("div[name='observable-input']").should("have.length", 1);
    cy.get("#add-observable").click();
    cy.get("div[name='observable-input']").should("have.length", 2);
  });

  it("Delete observable button works", () => {
    cy.get("button[name='delete-observable']").should("have.length", 1);
    cy.get("button[name='delete-observable']").click();
    cy.get("div[name='observable-input']").should("have.length", 0);
  });

  it("submits alert/observable data to API and routes user to new alert page after submission", () => {
    cy.intercept("POST", "/api/alert").as("createAlert");
    cy.intercept("GET", "/api/alert/*").as("getAlert");
    addMultipleObservables();
    cy.contains("Submit Alert").click();
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");
    cy.url().should("include", "/alert/");
  });

  it("submits alert/observable data to API and shows error if alert creation fails", () => {
    addMultipleObservables();
    cy.intercept("POST", "/api/alert/", {
      statusCode: 500,
      body: "Server error",
    }).as("createAlert");
    cy.contains("Submit Alert").click();
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.get(".p-message-wrapper").should("exist");
    cy.url().should("include", "/analyze");
  });

  it("submits alert/observable data to API for ea. observable when multi-alert option is clicked, and then routes to last created alert", () => {
    cy.intercept("POST", "/api/alert").as("createAlert");
    cy.intercept("GET", "/api/alert/*").as("getAlert");
    addMultipleObservables();
    cy.contains("Submit Multiple Alerts").click();

    // 5 alerts and 5 respsective observables should be created
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");

    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");

    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");

    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");

    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.wait("@getAlert").its("state").should("eq", "Complete");

    // Last alert will have an extra GET request to display it
    cy.wait("@getAlert").its("state").should("eq", "Complete");
    cy.url().should("include", "/alert/");
  });

  it("submits alert data to API and shows error message if alert creation fails when multi-alert create option is clicked", () => {
    addMultipleObservables();
    cy.intercept("POST", "/api/alert/", {
      statusCode: 500,
      body: "Server error",
    }).as("createAlert");
    cy.contains("Submit Alert").click();
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.get(".p-message-wrapper").should("exist");
    cy.url().should("include", "/analyze");
  });
});
