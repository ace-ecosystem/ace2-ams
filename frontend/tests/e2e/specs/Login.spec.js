// https://docs.cypress.io/api/introduction/api.html

describe("TheLogin.vue", () => {
  before(() => {
    cy.log("logging in");
    cy.login();
  });

  after(() => {
    cy.log("logging out");
    cy.logout();
  });

  beforeEach(() => {
    Cypress.Cookies.preserveOnce("access_token", "refresh_token");
  });

  it("Visits Login Page", () => {
    cy.log("going to login page after already logging in");
    cy.visit("/login");
    cy.url().should("contain", "/manage");
  });
});
