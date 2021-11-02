// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This is will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })

Cypress.Commands.add("login", () => {
  cy.visit("/login");
  const formData = new FormData();
  formData.append("username", "analyst");
  formData.append("password", "analyst");
  cy.request("POST", "/api/auth", formData);
});

Cypress.Commands.add("addFormObservable", () => {
  cy.get("#add-observable").click();
});

Cypress.Commands.add("toggleLastFormObservableMultiInput", () => {
  cy.get("div[name='observable-type']").last().click();
});

Cypress.Commands.add("switchLastFormObservableType", (type) => {
  cy.get("div[name='observable-type']").last().click();
  cy.get("div[name='observable-input']")
    .get(".p-dropdown-item", { timeout: 5_000 })
    .contains(type)
    .click();
});

// type should be 'input' or 'textarea'
Cypress.Commands.add("typeLastFormObservableValue", (type, typeText) => {
  cy.get("div[name='observable-value']").find(type).last().type(typeText);
});
