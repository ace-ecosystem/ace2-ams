describe("ManageAlerts.vue", () => {
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
    cy.visit("/manage_alerts");
    cy.url().should("contain", "/manage_alerts");
  });

  it("renders", () => {
    cy.get(".p-menubar").should("be.visible");
    cy.get("#AlertActionToolbar").should("be.visible");
    cy.get("#FilterToolbar").should("be.visible");
    cy.get("#AlertsTable").should("be.visible");
  });

  it("will reload alerts table with 'after' filter applied when 'start' input changed by using date picker", () => {
    cy.intercept("GET", "/api/alert/?limit=10&offset=0&event_time_after=*").as(
      "getAlert",
    );
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").click();
    cy.get(".vc-popover-content").should("be.visible");
    cy.get(".in-month > .vc-day-content").first().click({ force: true });
    cy.wait("@getAlert").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'after' filter applied when 'start' input changed by typing", () => {
    cy.intercept(
      "GET",
      "/api/alert/?limit=10&offset=0&event_time_after=2021-03-02T*",
    ).as("getAlert");
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    cy.wait("@getAlert").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'before' filter applied when 'end' input changed by using date picker", () => {
    cy.intercept("GET", "/api/alert/?limit=10&offset=0&event_time_before=*").as(
      "getAlert",
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").click();
    cy.get(".vc-popover-content").should("be.visible");
    cy.get(".in-month > .vc-day-content").first().click({ force: true });
    cy.wait("@getAlert").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'before' filter applied when 'end' input changed by typing", () => {
    cy.intercept(
      "GET",
      "/api/alert/?limit=10&offset=0&event_time_before=2021-03-02T*",
    ).as("getAlert");
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    cy.wait("@getAlert").its("state").should("eq", "Complete");
  });

  it("will set a range (before and after filters) and update input boxes and reload alerts when a range is selected", () => {
    const today = new Date();
    const todayString = `${
      today.getMonth() + 1
    }/${today.getDate()}/${today.getFullYear()}`;
    const todayStartString = `${todayString} 00:00`;
    const todayEndString = `${todayString} 23:59`;
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      todayStartString,
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      todayEndString,
    );
  });
  it("will clear a time filter when its 'delete' button is clicked", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();
    cy.get(":nth-child(2) > .p-inputgroup > .p-button").click();
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-button").click();
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
  });
  it("will clear both time filters when either the filter 'Clear' or 'Reset' buttons are clicked", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();
    cy.get("#FilterToolbar > .p-toolbar-group-right > :nth-child(1)").click();
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );

    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();
    cy.get("#FilterToolbar > .p-toolbar-group-right > :nth-child(2)").click();
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
  });
  it("will use the set time filter will be used for requests ", () => {
    cy.intercept(
      "GET",
      "/api/alert/?limit=10&offset=0&insert_time_after=2021-03-02T*",
    ).as("getAlert");
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
      timeout: 10000,
    }).click();
    cy.get('[aria-label="Insert Time"]').click();

    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    cy.wait("@getAlert", {
      timeout: 10000,
    })
      .its("state")
      .should("eq", "Complete");
  });
  it("will clear the set filters when default time filter changed, and set time filter will be used for requests ", () => {
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "03/02/2021 13:00",
    );
    cy.intercept("GET", "/api/alert/?limit=10&offset=0").as(
      "getAlertNoFilters",
    );
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
      timeout: 10000,
    }).click();
    cy.get('[aria-label="Insert Time"]').click();
    cy.wait("@getAlertNoFilters").its("state").should("eq", "Complete");
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
  });
});
