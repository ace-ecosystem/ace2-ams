describe("ManageAlerts.vue", () => {
  before(() => {
    cy.log("logging in");
    cy.login();
  });

  beforeEach(() => {
    Cypress.Cookies.preserveOnce("access_token", "refresh_token");
    cy.visit("/manage_alerts");
    cy.url().should("contain", "/manage_alerts");
  });

  it("renders", () => {
    cy.get(".p-menubar").should("be.visible");
    cy.get("#AlertActionToolbar").should("be.visible");
    cy.get("#FilterToolbar").should("be.visible");
    cy.get("#AlertsTable").should("be.visible");
  });
});
