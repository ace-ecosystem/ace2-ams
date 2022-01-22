describe("/login", () => {
  beforeEach(() => {
    cy.visit("/login");
  });

  it("greets with 'Welcome Back :)'", () => {
    cy.contains("div", "Welcome Back :)");
  });

  it("requires username", () => {
    cy.get("#password").type("analyst");
    cy.get("#submit").should("be.visible").should("be.disabled");
  });

  it("requires password", () => {
    cy.get("#username").type("analyst");
    cy.get("#submit").should("be.visible").should("be.disabled");
  });

  it("requires valid username and password (clicking submit button)", () => {
    cy.get("#error").should("not.exist");
    cy.get("#username").type("asdf");
    cy.get("#password").type("asdf");
    cy.get("#submit").should("not.be.disabled").click();
    cy.get("#error")
      .should("be.visible")
      .contains("Invalid username or password");
    cy.get("#submit").should("be.disabled");
  });

  it("navigates to /manage_alerts on successful login (pressing enter)", () => {
    cy.get("#username").type("analyst");
    cy.get("#password").type("analyst{enter}");
    cy.url().should("contain", "/manage_alerts");
    cy.getCookie("access_token").should("exist");
    cy.getCookie("refresh_token").should("exist");
    cy.getCookies().should("have.length", 2);
  });
});
