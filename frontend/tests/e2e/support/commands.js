// import { addUser } from "./helpers.js";

Cypress.Commands.add("login", () => {
  cy.request({
    method: "POST",
    url: "/api/auth",
    form: true,
    body: {
      username: "analyst",
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
  cy.request({
    method: "POST",
    url: "/api/test/reset_database",
  });
});

Cypress.Commands.add("addFormObservable", () => {
  cy.get("#add-observable").click();
});
