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
    cy.login();
  });

  after(() => {
    cy.logout();
  });

  beforeEach(() => {
    visitUrl({ url: "/analyze" });
  });

  it("Analyze page renders", () => {
    cy.get("#alert-form").should("be.visible");
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

  it("Changes the observable input box based on observable type", () => {
    // Check that initial observable is a file observable & doesn't have a multi-input button
    cy.get("div[name='observable-value']")
      .find("[type='file']")
      .should("exist");
    cy.get("div[name='observable-value']").find("button").should("not.exist");
    cy.get("div[name='observable-value']").find("textarea").should("not.exist");
    // Check dropdown options and select 'ipv4'
    cy.get("div[name='observable-type']").click();
    cy.get("div[name='observable-input']")
      .get(".p-dropdown-item", { timeout: 5_000 })
      .should("have.length", 9)
      .contains("ipv4")
      .click();
    // Check that input switched to text input
    cy.get("div[name='observable-value']")
      .find("[type='text']")
      .should("exist");
    // Find and click the multi-input button and check that input changes to text area
    cy.get("div[name='observable-value']").find("button").click();
    cy.get("div[name='observable-value']")
      .find("[type='text']")
      .should("not.exist");
    cy.get("div[name='observable-value']").find("textarea").should("exist");
    // Find and click multi-input again and check that input switches back to text input
    cy.get("div[name='observable-value']").find("button").click();
    cy.get("div[name='observable-value']")
      .find("[type='text']")
      .should("exist");
    cy.get("div[name='observable-value']").find("textarea").should("not.exist");
    // Switch back to file observable type and check that input switches back to file input
    cy.get("div[name='observable-type']").click();
    cy.get("div[name='observable-input']")
      .get(".p-dropdown-item", { timeout: 5_000 })
      .contains("file")
      .click();
    cy.get("div[name='observable-value']")
      .find("[type='file']")
      .should("exist");
    cy.get("div[name='observable-value']").find("button").should("not.exist");
  });

  it("submits alert/observable data to API and routes user to new alert page after submission", () => {
    cy.intercept("POST", "/api/alert").as("createAlert");
    cy.intercept("GET", "/api/alert/*").as("getAlert");
    addMultipleObservables();
    cy.get(".p-splitbutton-defaultbutton").click();
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
    cy.get(".p-splitbutton-defaultbutton").click();
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.get(".p-message-wrapper").should("exist");
    cy.url().should("include", "/analyze");
  });

  it("submits alert/observable data to API for ea. observable when multi-alert option is clicked, and then routes to last created alert", () => {
    cy.intercept("POST", "/api/alert").as("createAlert");
    cy.intercept("GET", "/api/alert/*").as("getAlert");
    addMultipleObservables();
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").click();

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
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").click();
    cy.wait("@createAlert").its("state").should("eq", "Complete");
    cy.get(".p-message-wrapper").should("exist");
    cy.url().should("include", "/analyze");
  });
});
