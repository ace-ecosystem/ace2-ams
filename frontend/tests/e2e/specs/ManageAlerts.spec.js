import { visitUrl } from "./helpers";

describe("Manage Alerts - No Database Changes", () => {
  // These tests do not affect the database, so only need to reset the database once.
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test alert to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_alerts",
      body: {
        template: "small.json",
        count: 1,
      },
    });
  });

  beforeEach(() => {
    // Intercept the API call that loads the default alert table view
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("getAlertsDefaultRows");

    visitUrl({
      url: "/manage_alerts",
      extraIntercepts: ["@getAlertsDefaultRows"],
    });
  });

  describe("Date Ranges", () => {
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
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).click();
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
      cy.get("[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext")
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
      cy.get(
        "[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext",
      ).click();
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
      cy.get("[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext")
        .click()
        .clear()
        .type("03/02/2021 13:00");
      // Alerts should reload

      cy.wait("@getAlerts").its("state").should("eq", "Complete");
    });

    it("will set a range (before and after filters) and update input boxes and reload alerts when a range is selected", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*&event_time_before=*",
      ).as("getAlerts");

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
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      //  Click the 'Today' range button
      cy.get(".p-flex-column > :nth-child(1) > .p-button", {
        timeout: 10000,
      }).click();
      // Make sure the ranges were correctly set
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", todayStartString);
      cy.get(
        "[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext",
      ).should("have.value", todayEndString);

      cy.wait("@getAlerts").its("state").should("eq", "Complete");
    });

    it("will clear a time filter when its 'delete' button is clicked", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*&event_time_before=*",
      ).as("getAlerts");

      // Set the date range to 'today' using the date options dropdown
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      cy.get(".p-flex-column > :nth-child(1) > .p-button", {
        timeout: 10000,
      }).click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the 'start' input delete button
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_before=*",
      ).as("getAlerts");
      cy.get(":nth-child(2) > .p-inputgroup > .p-button").click();
      // Should now be empty
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the 'end' input delete button
      cy.get(":nth-child(4) > .p-inputgroup > .p-button").click();
      // Should now be empty
      cy.get(
        "[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });

    it("will clear both time filters when either the filter 'Clear' or 'Reset' buttons are clicked", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*&event_time_before=*",
      ).as("getAlerts");

      // Set the date range to 'today' using the date options dropdown
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      cy.get(".p-flex-column > :nth-child(1) > .p-button", {
        timeout: 10000,
      }).click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the 'clear' button
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(3) > .p-menuitem-link").click();
      // Both inputs should now be empty
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.get(
        "[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");

      // Set the date range to 'today' using the date options dropdown (again)
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*&event_time_before=*",
      ).as("getAlerts");
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      cy.get(".p-flex-column > :nth-child(1) > .p-button", {
        timeout: 10000,
      }).click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the 'reset' button
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*&event_time_before=*",
      ).as("getAlerts");
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(2) > .p-menuitem-link").click();
      // Both inputs should now be empty
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.get(
        "[data-cy=date-range-picker-end] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
      cy.wait("@getAlerts").its("state").should("eq", "Complete");
    });

    it("will use the set time filter will be used for requests ", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&insert_time_after=2021-03-02T*",
      ).as("getAlerts");

      // Set the date range filter type to be "Insert Time"
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
        timeout: 10000,
      }).click();
      cy.get('[aria-label="Insert Time (UTC)"]').click();

      // Manually type the given time
      cy.get("[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext")
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
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&event_time_after=*",
      ).as("getAlerts");

      // Manually type the given time
      cy.get("[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext")
        .click()
        .clear()
        .type("03/02/2021 13:00");
      // Just verifying that right time was entered
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "03/02/2021 13:00");
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Change the date range filter type to "Insert Time"
      cy.get('[data-cy="date-range-picker-options-button"]').click();
      cy.get(".p-overlaypanel-content").should("be.visible");
      cy.get(":nth-child(1) > .p-dropdown > .p-dropdown-trigger", {
        timeout: 10000,
      }).click();
      cy.get('[aria-label="Insert Time (UTC)"]').click();

      // Request to get alerts with no filters (aka a reset) should be made
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");

      // And the input should be cleared
      cy.get(
        "[data-cy=date-range-picker-start] > .p-inputgroup > .p-inputtext",
      ).should("have.value", "");
    });
  });

  describe("Filter Actions", () => {
    it("will open the filter modal when the 'Edit Filter' button is clicked", () => {
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
      cy.get(".p-dialog-header").should("be.visible");
    });

    it("will add / remove / clear form filters when respective buttons are clicked", () => {
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.get("[data-cy='property-input-delete']").last().click();
      cy.get(".flex ").children().should("have.length", 3);

      // Clear all of them
      cy.get(".p-dialog-footer > :nth-child(1)").click();
      cy.get(".flex").children().should("have.length", 0);
    });

    it("will change the input box depending on the selected filter", () => {
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
      cy.get(".p-dialog-footer > :nth-child(2)").click();
      cy.get(".col > .field > .p-dropdown").should("be.visible");

      cy.get(
        ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get(".p-dropdown-items-wrapper").should("be.visible");
      cy.get("[aria-label='Event Time After (UTC)']").click();
      cy.get(".p-dropdown-items-wrapper").should("not.exist");
      cy.get("div.inputfield > .p-inputgroup > .p-inputtext")
        .invoke("attr", "placeholder")
        .should("contain", "Enter a date!");

      cy.get(
        ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get(".p-dropdown-items-wrapper").should("be.visible");
      cy.get("[aria-label='Name']").click();
      cy.get(".p-dropdown-items-wrapper").should("not.exist");
      cy.get(".field > .p-inputtext").should("be.visible");

      cy.get(
        ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get(".p-dropdown-items-wrapper").should("be.visible");
      cy.get("[aria-label='Observable']").click({ force: true });
      cy.get(".p-dropdown-items-wrapper").should("not.exist");
      cy.get(".col > :nth-child(1) > :nth-child(1) > .p-dropdown").should(
        "be.visible",
      );
      cy.get(":nth-child(2) > .p-inputtext").should("be.visible");

      cy.get(
        ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get(".p-dropdown-items-wrapper").should("be.visible");
      cy.get("[aria-label='Observable Types']").click();
      cy.get(".p-dropdown-items-wrapper").should("not.exist");
      cy.get(".field > .p-multiselect > .p-multiselect-label-container").should(
        "be.visible",
      );

      cy.get(
        ".formgrid > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get(".p-dropdown-items-wrapper").should("be.visible");
      cy.get("[aria-label='Tags']").click();
      cy.get(".p-dropdown-items-wrapper").should("not.exist");
      cy.get(".p-chips-input-token").should("be.visible");
    });

    it("will clear unsubmitted form filters when the Edit Filter modal is exited or cancelled", () => {
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
      cy.get(".p-dialog-footer > :nth-child(2)").click();

      // Cancel
      cy.get(".p-dialog-footer > :nth-child(3)").click();
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
      cy.get(".flex").children().should("have.length", 0);

      // Exit
      cy.get(".p-dialog-footer > :nth-child(2)").click();
      cy.get(".p-dialog-header-icon").click();
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&name=hello+world",
      ).as("getAlerts");

      // Open the modal
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Reopen the modal
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();

      // Verify the form data
      cy.get(".flex").children().should("have.length", 1);
      cy.get(":nth-child(1) > .p-dropdown").eq(1).should("have.text", "Name");
      cy.get(".inputfield").should("have.value", "hello world");

      // Exit modal for end of test
      cy.get(".p-dialog-header-close-icon").click();
    });

    it("will load any currently set filters from localStorage and add them in the form", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&name=hello+world",
      ).as("getAlerts");

      // Open the modal
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Refresh the page
      cy.reload();

      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&name=hello+world",
      ).as("getAlerts");
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Reopen the modal
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();

      // Verify the form data
      cy.get(".flex").children().should("have.length", 1);
      cy.get(":nth-child(1) > .p-dropdown").eq(1).should("have.text", "Name");
      cy.get(".inputfield").should("have.value", "hello world");
      // Exit modal for end of test
      cy.get(".p-dialog-header-close-icon").click();
    });

    it("will add new filters through the quick add menu", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&disposition=IGNORE",
      ).as("getAlerts");

      // Open Quick Add menu
      cy.get(".p-splitbutton-defaultbutton > .p-button-label").click();
      // Add the default
      cy.get(".p-overlaypanel-content > .p-button").click();
      // Check text
      cy.get(".filter-name-text").should("have.text", "Disposition:");
      cy.get(".link-text").should("have.text", "IGNORE");
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Open Quick Add menu again
      cy.get(".p-splitbutton-defaultbutton > .p-button-label").click();
      // Select "observable" type filter from the dropdown
      cy.get(".col-fixed > .p-dropdown > .p-dropdown-trigger").click();
      cy.get("[aria-label='Observable']").click();
      // Select 'ipv4' type
      cy.get(
        ".col > :nth-child(1) > :nth-child(1) > .p-dropdown > .p-dropdown-trigger",
      ).click();
      cy.get("li[aria-label='ipv4']").click();
      // Type in observable value and submit
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&disposition=IGNORE&observable=ipv4%7C127.0.0.1",
      ).as("getAlerts");
      cy.get(".field > .p-inputtext").click();
      cy.get(":nth-child(2) > .p-inputtext").type("127.0.0.1");
      cy.get(".p-overlaypanel-content > .p-button").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Check value
      cy.get(".filter-name-text").last().should("have.text", "Observable:");
      cy.get(".link-text").last().should("have.text", "ipv4|127.0.0.1");
    });
  });

  describe("URL Param Filters", () => {
    // Can't test at the moment, no way to check clipboard data in insecure context
    // Tried using clipboardy package, but Cypress throws a fit when importing ES6 modules
    it.skip("will generate and copy a link of currently applied filters when link button clicked", () => {
      // Start by setting a filter

      // Open the filter modal
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
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
      cy.get(".field > .p-inputtext").type("Small Alert");

      // Submit
      cy.get(".p-dialog-footer > :nth-child(4)").click();

      // Click link button
      cy.get(
        ".p-button.p-button-icon-only.p-component.p-splitbutton-menubutton",
      ).click();
      cy.get("li:nth-of-type(4) > a[role='menuitem']").click();

      // Check clipboard data
      // ???
    });

    it("will load filters from URL and reroute to /manage_alerts if URL params are provided", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&name=Small+Alert&owner=bob",
      ).as("getAlerts");

      visitUrl({ url: "/manage_alerts?name=Small+Alert&owner=bob" });

      // Check current URL
      cy.url().should("contain", "/manage_alerts");
      cy.url().should("not.contain", "?name=Small+Alert&owner=bob");

      // Open the filter modal & check filters are applied
      cy.get(".p-splitbutton-menubutton").click();
      cy.get(".p-menuitem:nth-child(1) > .p-menuitem-link").click();
      cy.get(".p-dialog-header").should("be.visible");
      cy.get(
        ":nth-child(1) > :nth-child(1) > .p-dropdown > .p-dropdown-label",
      ).should("have.text", "Name");
      cy.get(".field > .p-inputtext").should("have.value", "Small Alert");
      cy.get(
        ".flex > :nth-child(2) > :nth-child(1) > .p-dropdown > .p-dropdown-label",
      ).should("have.text", "Owner");
      cy.get(".col > .field > .p-dropdown > .p-dropdown-label").should(
        "have.text",
        "Analyst Bob",
      );
      cy.get(".p-dialog-header-icon").click();
    });
  });

  describe("Filter Chips", () => {
    it("will display a set filter as chip in chips toolbar", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=c2",
      ).as("getAlerts");

      // Find the TestTag tag and click to set filter
      cy.get("[data-cy=tags]").contains("c2").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Check that the filter chip is visible and has right text
      cy.get(".p-chip").should("exist");
      cy.get(".filter-name-text").should("have.text", "Tags:");
      cy.get(".link-text").should("have.text", "c2");
    });

    it("will delete a filter and remove chip when it's value in the filter chip is clicked", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=c2",
      ).as("getAlerts");

      // Find the c2 tag and click to set filter
      cy.get("[data-cy=tags]").contains("c2").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the filter value
      cy.get(".p-chip > .link-text").click();
      cy.get(".p-chip").should("not.exist");
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });

    it("will delete a filter and remove chip when the close icon in the filter chip is clicked", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=c2",
      ).as("getAlerts");

      // Find the c2 tag and click to set filter
      cy.get("[data-cy=tags]").contains("c2").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Click the close icon
      cy.get(".p-chip > .pi-times-circle").click();
      cy.get(".transparent-toolbar").should("not.exist");
      cy.get(".p-chip").should("not.exist");
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });

    it("will update filters when a given filter is edited through its filter chip", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&disposition=IGNORE",
      ).as("getAlerts");

      // Set the filter using the quick add default
      cy.get(".p-splitbutton-defaultbutton").click();
      cy.get(".pi-check").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&disposition=UNKNOWN",
      ).as("getAlerts");

      // Open the filter edit menu
      cy.get(".pi-pencil").click();
      // Select a different disposition and submit
      cy.get(".field > .p-dropdown > .p-dropdown-trigger").click();
      cy.get(".p-dropdown-item:nth-child(5)").click();
      cy.get("button[name='update-filter']").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Verify that the filter changed
      cy.get(".filter-name-text").should("have.text", "Disposition:");
      cy.get(".link-text").should("have.text", "UNKNOWN");
    });
  });
});

describe("Manage Alerts - Single Alert Tests", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test alert to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_alerts",
      body: {
        template: "small.json",
        count: 1,
      },
    });
  });

  beforeEach(() => {
    // Intercept the API call that loads the default alert table view
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("getAlertsDefaultRows");

    visitUrl({
      url: "/manage_alerts",
      extraIntercepts: ["@getAlertsDefaultRows"],
    });
  });

  describe("Comments", () => {
    it("will add a given comment to an alert via the comment modal", () => {
      cy.intercept("POST", "/api/node/comment/").as("addComment");

      // Get first visible alert checkbox
      cy.get(".p-checkbox-box").eq(1).click();
      // Open the comment modal
      cy.get("[data-cy=comment-button]").click();

      cy.get(".p-dialog-content").should("be.visible");
      // Set Comment
      cy.get(".p-inputtextarea").click().type("Test comment");
      // Enter & close modal
      cy.get(".p-dialog-footer > :nth-child(2)").click();
      cy.get(".p-dialog-content").should("not.exist");
      // Check for comment after adding
      cy.get(".comment")
        .first()
        .should("contain.text", "(Analyst) Test comment");
      cy.wait("@addComment").its("state").should("eq", "Complete");
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });
  });

  describe("Tags", () => {
    it("will add given tags to an alert via the tag modal", () => {
      cy.intercept("GET", "/api/tag/?offset=0").as("getNodeTags");
      cy.intercept("POST", "/api/tag").as("addTags");
      cy.intercept("PATCH", "/api/alert/").as("updateAlert");

      // Get first visible alert checkbox
      cy.get(".p-checkbox-box").eq(1).click();
      // Open the tag modal
      cy.get("[data-cy=tag-button]").click();

      cy.get(".p-dialog-content").should("be.visible");
      cy.wait("@getNodeTags").its("state").should("eq", "Complete");
      // Type a tag
      cy.get(".p-chips > .p-inputtext").click().type("TestTag").type("{enter}");
      // Select a tag from the dropdown
      cy.get(".p-fluid > .p-dropdown > .p-dropdown-label").click();
      cy.get('[aria-label="scan_me"]').click();
      // Enter & close modal
      cy.get(".p-dialog-footer > :nth-child(2)").click();
      cy.get(".p-dialog-content").should("not.exist");
      cy.wait("@addTags").its("state").should("eq", "Complete");
      cy.wait("@updateAlert").its("state").should("eq", "Complete");
      // Check for the tags after adding
      cy.get("[data-cy='tags']")
        .eq(0)
        .within(() => {
          cy.get(".p-tag").contains("TestTag").should("have.text", "TestTag");
          cy.get(".p-tag").contains("scan_me").should("have.text", "scan_me");
        });
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });

    it("will filter by a given tag when clicked", () => {
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=c2",
      ).as("getAlerts");

      // Find the c2 tag and click
      cy.get("[data-cy=tags]").contains("c2").click();
      cy.wait("@getAlerts").its("state").should("eq", "Complete");

      // Check which alerts are visible (should be 2, 1 header + 1 alert that has the c2 tag)
      cy.get(".p-checkbox-box").should("have.length", 2);

      // Verify it is the correct alert and the filtered tag is there
      cy.get(".p-datatable-tbody > tr > :nth-child(4) > div").should(
        "contain.text",
        "Small Alert",
      );
      cy.get("[data-cy=tags]").contains("c2").should("exist");
    });
  });

  describe("Take Ownership", () => {
    it("will set the owner via the take ownership button", () => {
      cy.intercept("PATCH", "/api/alert/").as("updateAlert");

      // Check first visible alert current owner, should be "Analyst Bob" (from the test alert that was inserted)
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(5) > div").should(
        "have.text",
        "Analyst Bob",
      );
      // Get first visible alert checkbox
      cy.get(" .p-checkbox-box").eq(1).click();
      // Click Take Ownership button
      cy.get("[data-cy=take-ownership-button]").click();

      cy.wait("@updateAlert").its("state").should("eq", "Complete");
      // Check owner name after taking ownership
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(5) > div").should(
        "have.text",
        "Analyst",
      );
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });
  });

  describe("Assign Ownership", () => {
    it("will set the owner via the assign modal", () => {
      cy.intercept("PATCH", "/api/alert/").as("updateAlert");

      // Check first visible alert current owner, should not be Analyst Alice
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(5) > div").should(
        "not.have.text",
        "Analyst Alice",
      );
      // Get first visible alert checkbox
      cy.get(" .p-checkbox-box").eq(1).click();
      // Open assign owner modal
      cy.get("[data-cy=assign-button]").click();
      cy.get(".p-dialog-content").should("be.visible");
      // Select Analyst Alice from the dropdown
      cy.get(".p-field > .p-dropdown > .p-dropdown-trigger").click();
      cy.get("li[aria-label='Analyst Alice']").click();
      // Submit and close modal
      cy.get(".p-dialog-footer > :nth-child(2)").click();
      cy.get(".p-dialog-content").should("not.exist");
      cy.wait("@updateAlert").its("state").should("eq", "Complete");
      // Check owner name after assigning
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(5) > div").should(
        "have.text",
        "Analyst Alice",
      );
      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });
  });

  describe("Disposition", () => {
    it("will set the disposition and disposition comment via disposition modal", () => {
      cy.intercept("PATCH", "/api/alert/").as("updateAlert");
      cy.intercept("POST", "/api/node/comment/").as("addComment");

      // Check first visible alert current disposition, should be "OPEN"
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(6) > div").should(
        "have.text",
        "OPEN",
      );
      // Get first visible alert checkbox
      cy.get(" .p-checkbox-box").eq(1).click();
      // Open disposition modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get(".p-dialog-content").should("be.visible");
      // Select disposition option
      cy.get('[aria-label="FALSE_POSITIVE"]').click();
      // Add disposition comment
      cy.get(".p-inputtextarea").click().type("Test disposition comment");
      // Submit and close
      cy.get(".p-dialog-footer > .p-button").click();
      cy.get(".p-dialog-content").should("not.exist");
      cy.wait("@addComment").its("state").should("eq", "Complete");
      cy.wait("@updateAlert").its("state").should("eq", "Complete");
      // Check disposition
      cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(6) > div").should(
        "have.text",
        "FALSE_POSITIVE",
      );
      // Check for disposition comment
      cy.get(".comment")
        .first()
        .should("contain.text", "(Analyst) Test disposition comment");

      cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    });
  });
});

describe("Manage Alerts - Save to Event", () => {
  describe("No Database Changes", () => {
    before(() => {
      cy.resetDatabase();
      cy.login();

      // Add a test alert to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_alerts",
        body: {
          template: "small.json",
          count: 1,
        },
      });

      // Add an OPEN test event to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_event",
        body: {
          alert_template: "small.json",
          alert_count: 1,
          name: "Test Open Event",
          status: "OPEN",
        },
      });

      // Add a CLOSED test event to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_event",
        body: {
          alert_template: "small.json",
          alert_count: 1,
          name: "Test Closed Event",
          status: "CLOSED",
        },
      });
    });

    beforeEach(() => {
      // Intercept the API call that loads the default alert table view
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
      ).as("getAlertsDefaultRows");

      visitUrl({
        url: "/manage_alerts",
        extraIntercepts: ["@getAlertsDefaultRows"],
      });

      cy.get(".p-checkbox").first().click();
    });

    it("will correctly load the 'NEW' tab in the Save to Event modal", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");

      // Open disposition modal, select disposition, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-dialog-footer > .p-button-raised").click();

      cy.wait("@getOpenEvents").its("state").should("eq", "Complete");
      cy.wait("@getClosedEvents").its("state").should("eq", "Complete");

      // Go to New Event tab
      cy.get(":nth-child(1) > .p-tabview-nav-link > .p-tabview-title").click();
      cy.get("[data-cy=new-event-name]")
        .should("be.visible")
        .should("contain.text", "");
      cy.get("[data-cy=new-event-name]")
        .should("be.visible")
        .should("be.empty");
    });

    it("will close the save to event modal when back button clicked", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");

      // Open disposition modal, select disposition, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-dialog-footer > .p-button-raised").click();

      cy.wait("@getOpenEvents").its("state").should("eq", "Complete");
      cy.wait("@getClosedEvents").its("state").should("eq", "Complete");

      // Click back button
      cy.get("[data-cy=save-to-event-back-button]").click();
      cy.get("[data-cy=save-to-event-modal]").should("not.exist");
    });

    it("will close the save to event modal when close button clicked", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");

      // Open disposition modal, select disposition, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-dialog-footer > .p-button-raised").click();

      cy.wait("@getOpenEvents").its("state").should("eq", "Complete");
      cy.wait("@getClosedEvents").its("state").should("eq", "Complete");

      // Click close button
      cy.get(".p-dialog-header-icon").eq(1).click();
      cy.get("[data-cy=save-to-event-modal]").should("not.exist");
    });

    it("will correctly load each dynamic tab in the Save to Event modal", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");

      // Open disposition modal, select disposition, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-dialog-footer > .p-button-raised").click();

      cy.wait("@getOpenEvents").its("state").should("eq", "Complete");
      cy.wait("@getClosedEvents").its("state").should("eq", "Complete");

      // First check the initial 'OPEN' tab
      cy.get("[data-cy=event-options]").should("be.visible");
      cy.get("[data-cy=save-to-event-modal] .p-listbox-item")
        .eq(0)
        .should("be.visible")
        .should("contain.text", "Test Open Event");
      cy.get("[data-cy=save-to-event-modal] .p-listbox-item")
        .eq(1)
        .should("not.be.visible");
      // Then check 'CLOSED' tab
      cy.get(".p-tabview-title").last().click();
      cy.get("[data-cy=event-options]").should("be.visible");
      cy.get("[data-cy=save-to-event-modal] .p-listbox-item")
        .eq(1)
        .should("be.visible")
        .should("contain.text", "Test Closed Event");
      cy.get("[data-cy=save-to-event-modal] .p-listbox-item")
        .eq(0)
        .should("not.be.visible");
    });
  });

  describe("Database Changes", () => {
    beforeEach(() => {
      cy.resetDatabase();
      cy.login();

      // Add a test alert to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_alerts",
        body: {
          template: "small.json",
          count: 1,
        },
      });

      // Add an OPEN test event to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_event",
        body: {
          alert_template: "small.json",
          alert_count: 1,
          name: "Test Open Event",
          status: "OPEN",
        },
      });

      // Add a CLOSED test event to the database
      cy.request({
        method: "POST",
        url: "/api/test/add_event",
        body: {
          alert_template: "small.json",
          alert_count: 1,
          name: "Test Closed Event",
          status: "CLOSED",
        },
      });

      // Intercept the API call that loads the default alert table view
      cy.intercept(
        "GET",
        "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
      ).as("getAlertsDefaultRows");

      visitUrl({
        url: "/manage_alerts",
        extraIntercepts: ["@getAlertsDefaultRows"],
      });
    });

    it("will successfully save to an existing event with a disposition comment", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");
      cy.intercept("PATCH", "/api/alert/").as("updateAlerts");
      cy.intercept("POST", "/api/node/comment").as("addComment");

      //  Select all alerts
      cy.get(
        ".p-column-header-content > .p-checkbox > .p-checkbox-box",
      ).click();

      // Open disposition modal, select disposition, add disposition comment, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-inputtextarea").click().type("disposition comment");
      cy.get(".p-dialog-footer > .p-button-raised").click();

      // Select "Test Open Event"
      cy.get("[data-cy=save-to-event-modal] .p-listbox-item").eq(0).click();

      cy.get("[data-cy=save-to-event-submit-button]").click();

      // Update alerts event uuid
      cy.wait("@updateAlerts").its("state").should("eq", "Complete");
      // Update alerts disposition
      cy.wait("@updateAlerts").its("state").should("eq", "Complete");
      // Add disposition comment
      cy.wait("@addComment").its("state").should("eq", "Complete");

      cy.get("[data-cy=save-to-event-modal]").should("not.exist");

      // Check first alert disposition
      cy.get(".p-datatable-tbody > tr > :nth-child(6) > div").should(
        "contain.text",
        "APPROVED_BUSINESS",
      );
      // Check alert comment
      cy.get(".p-datatable-tbody > tr > :nth-child(4) .p-mr-2").should(
        "contain.text",
        "(Analyst) disposition comment",
      );
    });

    it("will successfully create a new event with a disposition/event comment", () => {
      cy.intercept(
        "GET",
        "/api/event/?status=OPEN&sort=created_time%7Casc&offset=0",
      ).as("getOpenEvents");
      cy.intercept(
        "GET",
        "/api/event/?status=CLOSED&sort=created_time%7Casc&offset=0",
      ).as("getClosedEvents");
      cy.intercept("PATCH", "/api/alert/").as("updateAlerts");
      cy.intercept("POST", "/api/event/").as("createEvent");
      cy.intercept("POST", "/api/node/comment").as("addComment");

      //  Select all alerts
      cy.get(
        ".p-column-header-content > .p-checkbox > .p-checkbox-box",
      ).click();

      // Open disposition modal, select disposition, add disposition comment, and open save to event modal
      cy.get("[data-cy=disposition-button]").click();
      cy.get('[aria-label="APPROVED_BUSINESS"]').click();
      cy.get(".p-inputtextarea").click().type("disposition comment");
      cy.get(".p-dialog-footer > .p-button-raised").click();

      cy.wait("@getOpenEvents").its("state").should("eq", "Complete");
      cy.wait("@getClosedEvents").its("state").should("eq", "Complete");

      // Select new event
      cy.get(":nth-child(1) > .p-tabview-nav-link").click();
      cy.get("[data-cy=new-event-name]").click().type("Test new event");
      cy.get("[data-cy=new-event-comment]").click().type("new event comment");

      cy.get("[data-cy=save-to-event-submit-button]").click();

      // Create new event
      cy.wait("@createEvent").its("state").should("eq", "Complete");
      // Update alerts event uuid
      cy.wait("@updateAlerts").its("state").should("eq", "Complete");
      // Update alerts disposition
      cy.wait("@updateAlerts").its("state").should("eq", "Complete");
      // Add disposition comment
      cy.wait("@addComment").its("state").should("eq", "Complete");

      cy.get("[data-cy=save-to-event-modal]").should("not.exist");

      // Check first alert disposition
      cy.get(".p-datatable-tbody > tr > :nth-child(6) > div").should(
        "contain.text",
        "APPROVED_BUSINESS",
      );

      // Check alert comments
      cy.get(".p-datatable-tbody > tr > :nth-child(4) .p-mr-2").should(
        "contain.text",
        "(Analyst) disposition comment",
      );

      // Check the event comment (need to visit the Manage Events page)
      cy.intercept(
        "GET",
        "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
      ).as("getEvents");

      visitUrl({
        url: "/manage_events",
        extraIntercepts: ["@getEvents"],
      });

      cy.get(
        ".p-datatable-tbody > :nth-child(1) > :nth-child(5) .p-mr-2",
      ).should("contain.text", "(Analyst) new event comment");
    });
  });
});
