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
  cy.intercept("POST", "/api/auth").as("auth");

  cy.visit("/login");
  cy.get("div[name='loginForm']").should("be.visible");
  cy.get("#username").should("be.visible").type("analyst");
  cy.get("#password").should("be.visible").type("analyst");
  cy.get("#submit").should("be.visible").click();
  cy.url().should("contain", "/manage");

  cy.wait("@auth").then((xhr) => {
    cy.log(xhr.request.headers);
    cy.log(xhr.request.body);
    cy.task("log", xhr.request.headers);
    cy.task("log", xhr.request.body);

    cy.log(xhr.response.headers);
    cy.log(xhr.response.statusMessage);
    cy.log(xhr.response.body);
    cy.task("log", xhr.response.headers);
    cy.task("log", xhr.response.statusMessage);
    cy.task("log", xhr.response.body);
  });

  cy.getCookie("access_token").should("exist");
  cy.getCookie("refresh_token").should("exist");
  cy.getCookies().should("have.length", 2);

  // cy.intercept("/api/auth", (req) => {
  //   req.continue((res) => {
  //     headers = res.headers;
  //     body = res.body;
  //   });
  // });

  // cy.log(headers);
  // cy.log(body);
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
