// import { addUser } from "./helpers.js";

Cypress.Commands.add("login", (username = "analyst") => {
  cy.request({
    method: "POST",
    url: "/api/auth",
    form: true,
    body: {
      username: username,
      password: "analyst",
    },
  });
});

Cypress.Commands.add("logout", () => {
  cy.request({
    method: "GET",
    url: "/api/auth/logout",
  });
});

Cypress.Commands.add("resetDatabase", () => {
  try {
    cy.request({
      method: "POST",
      url: "/api/test/reset_database",
    });
  } catch {
    cy.wait(500);
    cy.request({
      method: "POST",
      url: "/api/test/reset_database",
    });
  }
});

Cypress.Commands.add("addFormObservable", () => {
  cy.get("#add-observable").click();
});
