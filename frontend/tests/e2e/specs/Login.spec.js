// https://docs.cypress.io/api/introduction/api.html

describe("TheLogin.vue", () => {
  it("Visits Login Page", () => {
    cy.visit("/login");
    cy.get('div[name="loginForm"]').should("be.visible");
  });
});
