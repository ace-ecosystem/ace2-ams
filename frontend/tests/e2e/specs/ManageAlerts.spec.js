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
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*",
    ).as("getAlerts");
    // Click the first available day in the date picker for 'start' input
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").click();
    cy.get(".vc-popover-content").should("be.visible");
    cy.get(".in-month > .vc-day-content").first().click({ force: true });
    // Alerts should reload
    cy.wait("@getAlerts").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'after' filter applied when 'start' input changed by typing", () => {
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=2021-03-02T*",
    ).as("getAlerts");
    // Type the date into the 'start' input
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    // Alerts should reload
    cy.wait("@getAlerts").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'before' filter applied when 'end' input changed by using date picker", () => {
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_before=*",
    ).as("getAlerts");
    // Click the first available day in the date picker for 'end' input
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").click();
    cy.get(".vc-popover-content").should("be.visible");
    cy.get(".in-month > .vc-day-content").first().click({ force: true });
    cy.wait("@getAlerts").its("state").should("eq", "Complete");
  });

  it("will reload alerts table with 'before' filter applied when 'end' input changed by typing", () => {
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_before=2021-03-02T*",
    ).as("getAlerts");
    // Type the date into the 'end' input
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    // Alerts should reload

    cy.wait("@getAlerts").its("state").should("eq", "Complete");
  });

  it("will set a range (before and after filters) and update input boxes and reload alerts when a range is selected", () => {
    // Calculate the expected start and end strings for the 'today' range
    const today = new Date();
    const todayString = today.toLocaleDateString("en-US", {
      year: "numeric",
      month: "2-digit",
      day: "2-digit",
    });
    const todayStartString = `${todayString} 00:00`;
    const todayEndString = `${todayString} 23:59`;
    // Click on the date options button
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    //  Click the 'Today' range button
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();
    // Make sure the ranges were correctly set
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
    // Set the date range to 'today' using the date options dropdown
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();

    // Click the 'start' input delete button
    cy.get(":nth-child(2) > .p-inputgroup > .p-button").click();
    // Should now be empty
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );

    // Click the 'end' input delete button
    cy.get(":nth-child(4) > .p-inputgroup > .p-button").click();
    // Should now be empty
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
  });
  it("will clear both time filters when either the filter 'Clear' or 'Reset' buttons are clicked", () => {
    // Set the date range to 'today' using the date options dropdown
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();

    // Click the 'clear' button
    cy.get("#FilterToolbar > .p-toolbar-group-right > :nth-child(1)").click();
    // Both inputs should now be empty
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
    cy.get(":nth-child(4) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );

    // Set the date range to 'today' using the date options dropdown (again)
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(".p-flex-column > :nth-child(1) > .p-button", {
      timeout: 10000,
    }).click();

    // Click the 'reset' button
    cy.get("#FilterToolbar > .p-toolbar-group-right > :nth-child(2)").click();
    // Both inputs should now be empty
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
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&insert_time_after=2021-03-02T*",
    ).as("getAlerts");

    // Set the date range filter type to be "Insert Time"
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
      timeout: 10000,
    }).click();
    cy.get('[aria-label="Insert Time"]').click();

    // Manually type the given time
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");

    // Check that the right request is made
    cy.wait("@getAlerts", {
      timeout: 10000,
    })
      .its("state")
      .should("eq", "Complete");
  });
  it("will clear the set filters when default time filter changed", () => {
    // Manually type the given time
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext")
      .click()
      .clear()
      .type("03/02/2021 13:00");
    // Just verifying that right  time was entered
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "03/02/2021 13:00",
    );

    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("getAlertsNoFilters");
    // Change the date range filter type to "Insert Time"
    cy.get("#FilterToolbar > .p-toolbar-group-left > :nth-child(1)").click();
    cy.get(".p-overlaypanel-content").should("be.visible");
    cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
      timeout: 10000,
    }).click();
    cy.get('[aria-label="Insert Time"]').click();

    // Request to get alerts with no filters (aka a reset) should be made
    cy.wait("@getAlertsNoFilters").its("state").should("eq", "Complete");

    // And the input should be cleared
    cy.get(":nth-child(2) > .p-inputgroup > .p-inputtext").should(
      "have.value",
      "",
    );
  });

  it("will open the filter modal when the 'Edit Filter' button is clicked", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-header").should("be.visible");
  });

  it("will add / remove / clear form filters when respective buttons are clicked", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-header").should("be.visible");

    // Add a single filter
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".formgrid").should("be.visible");

    // Add some more
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".flex ").children().should("have.length", 4);

    // Delete one
    cy.get(":nth-child(2) > :nth-child(3) > .p-button").click();
    cy.get(".flex ").children().should("have.length", 3);

    // Clear all of them
    cy.get(".p-dialog-footer > :nth-child(1)").click();
    cy.get(".flex").children().should("have.length", 0);
  });

  it("will change the input box depending on the selected filter", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".col > .field > .p-dropdown").should("be.visible");

    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Dispositioned After']").click();
    cy.get(".p-dropdown-items-wrapper").should("not.exist");
    cy.get("div.inputfield > .p-inputgroup > .p-inputtext")
      .invoke("attr", "placeholder")
      .should("contain", "Enter a date!");

    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Name']").click();
    cy.get(".field > .p-inputtext").should("be.visible");

    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Observable']").click();
    cy.get(".col > :nth-child(1) > :nth-child(1) > .p-dropdown").should(
      "be.visible",
    );
    cy.get(":nth-child(2) > .p-inputtext").should("be.visible");

    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Observable Types']").click();
    cy.get(".field > .p-multiselect > .p-multiselect-label-container").should(
      "be.visible",
    );

    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Tags']").click();
    cy.get(".p-chips-input-token").should("be.visible");
  });

  it("will clear unsubmitted form filters when the Edit Filter modal is exited or cancelled", () => {
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();

    // Cancel
    cy.get(".p-dialog-footer > :nth-child(3)").click();
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".flex").children().should("have.length", 0);

    // Exit
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".p-dialog-header-icon").click();
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".flex").children().should("have.length", 0);

    // Exit modal for end of test
    cy.get(".p-dialog-header-close-icon").click();
  });

  it("will make a request to update filters when a new filter is set", () => {
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&name=hello+world",
    ).as("getAlertWithFilters");

    // Open the modal
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".col > .field > .p-dropdown").should("be.visible");

    // Select name filter
    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Name']").click();
    cy.get(".field > .p-inputtext").should("be.visible");

    // Add a filter value
    cy.get(".field > .p-inputtext").type("hello world");

    // Submit
    cy.get(".p-dialog-footer > :nth-child(4)").click();
    cy.wait("@getAlertWithFilters").its("state").should("eq", "Complete");
  });

  it("will load any currently set filters in the form", () => {
    // Open the modal
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();
    cy.get(".p-dialog-footer > :nth-child(2)").click();
    cy.get(".col > .field > .p-dropdown").should("be.visible");

    // Select name filter
    cy.get(
      ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
    ).click();
    cy.get(".p-dropdown-items-wrapper").should("be.visible");
    cy.get("[aria-label='Name']").click();
    cy.get(".field > .p-inputtext").should("be.visible");

    // Add a filter value
    cy.get(".field > .p-inputtext").type("hello world");

    // Submit
    cy.get(".p-dialog-footer > :nth-child(4)").click();

    // Reopen the modal
    cy.get("#FilterToolbar > .p-toolbar-group-left > .p-m-1").click();

    // Verify the form data
    cy.get(".flex").children().should("have.length", 1);
    cy.get(":nth-child(1) > .p-dropdown").should("have.text", "Name");
    cy.get(".inputfield").should("have.value", "hello world");

    // Exit modal for end of test
    cy.get(".p-dialog-header-close-icon").click();
  });
});
