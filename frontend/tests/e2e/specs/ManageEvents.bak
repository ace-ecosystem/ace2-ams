import { visitUrl } from "./helpers";

describe("ManageEvents.vue UI Elements", () => {
  before(() => {
    cy.visit("/login");
    cy.login();
  });

  beforeEach(() => {
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
  });

  it("renders page elments correctly", () => {
    cy.get(".p-menubar").should("be.visible");
    cy.get("#EventActionToolbar").should("be.visible");
    cy.get("#FilterToolbar").should("be.visible");
    cy.get("#EventsTable").should("be.visible");
  });

  it("renders action toolbar elements correctly", () => {
    cy.get('[data-cy="comment-button"]').should("be.visible");
    cy.get('[data-cy="take-ownership-button"]').should("be.visible");
    cy.get('[data-cy="assign-button"]').should("be.visible");
    cy.get('[data-cy="tag-button"]').should("be.visible");
  });
  it("renders filter toolbar elements correctly", () => {
    cy.get('[data-cy="edit-filter-button"]').should("be.visible");
    cy.get('[data-cy="date-range-picker-options-button"]').should("be.visible");
    cy.get('[data-cy="date-range-picker-end-input"]')
      .should("be.visible")
      .should("be.empty");
    cy.get('[data-cy="date-range-picker-end-input"]')
      .should("be.visible")
      .should("be.empty");
  });
  it("renders table elements correctly", () => {
    cy.get('[data-cy="table-column-select"]').should("be.visible");
    cy.get('[data-cy="table-keyword-search"]')
      .should("be.visible")
      .should("be.empty");
    cy.get('[data-cy="reset-table-button"]').should("be.visible");
    cy.get('[data-cy="export-table-button"]').should("be.visible");
    cy.get('[data-cy="table-pagination-options"]').should("be.visible");
  });
});

describe("ManageEvents.vue table functionality", () => {
  before(() => {
    cy.visit("/login");
    cy.login();
  });

  beforeEach(() => {
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
  });

  it("sets up table columns elements correctly", () => {
    // Check default columns in column select
    cy.get('[data-cy="table-column-select"]').should(
      "have.text",
      "Created, Name, Owner, Type, Vectors",
    );
    // Check columns in table
    cy.get(".p-column-title").eq(0).should("have.text", "Created");
    cy.get(".p-column-title").eq(1).should("have.text", "Name");
    cy.get(".p-column-title").eq(2).should("have.text", "Owner");
    cy.get(".p-column-title").eq(3).should("have.text", "Type");
    cy.get(".p-column-title").eq(4).should("have.text", "Vectors");

    // Check default sort column, 'Created' has the sort style applied
    cy.get(".pi-sort-amount-down").should("have.length", 1);
    cy.get(".p-sortable-column-icon")
      .eq(0)
      .should("have.class", "pi-sort-amount-down");
  });

  it("sets up keyword search element correctly", () => {
    cy.get('[data-cy="table-keyword-search"]').should("be.empty");
    cy.get('[data-cy="table-keyword-search"]')
      .invoke("attr", "placeholder")
      .should("contain", "Search in table");
  });

  it("will show columns selected in select dropdown", () => {
    //   Select all the columns
    cy.get('[data-cy="table-column-select"]').click();
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    // Check columns in table
    cy.get('[data-cy="table-column-select"]').should(
      "have.text",
      "Created, Name, Owner, Status, Type, Vectors, Threat Actors, Threats, Prevention Tools, Risk Level",
    );
    cy.get(".p-column-title").eq(0).should("have.text", "Created");
    cy.get(".p-column-title").eq(1).should("have.text", "Name");
    cy.get(".p-column-title").eq(2).should("have.text", "Owner");
    cy.get(".p-column-title").eq(3).should("have.text", "Status");
    cy.get(".p-column-title").eq(4).should("have.text", "Type");
    cy.get(".p-column-title").eq(5).should("have.text", "Vectors");
    cy.get(".p-column-title").eq(6).should("have.text", "Threat Actors");
    cy.get(".p-column-title").eq(7).should("have.text", "Threats");
    cy.get(".p-column-title").eq(8).should("have.text", "Prevention Tools");
    cy.get(".p-column-title").eq(9).should("have.text", "Risk Level");

    //   Clear all the columns
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-column-title").should("not.exist");

    // Close column select
    cy.get(".p-multiselect-close").click();
    cy.get(".p-multiselect-header").should("not.exist");
  });

  it("will change sort when a header column is clicked", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Casc&limit=10&offset=0",
    ).as("getEventsCreatedAscending");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDescending");

    // This will change to default (no call made)
    cy.get(".p-column-title").eq(0).click();
    cy.get(".pi-sort-amount-down").should("have.length", 0);

    // This will change to created ascending
    cy.get(".p-column-title").eq(0).click();
    cy.get(".pi-sort-amount-up-alt").should("have.length", 1);
    cy.get(".p-sortable-column-icon")
      .eq(0)
      .should("have.class", "pi-sort-amount-up-alt");
    cy.wait("@getEventsCreatedAscending").its("state").should("eq", "Complete");

    // Click once more to set back to default (descending)
    cy.get(".p-column-title").eq(0).click();
    cy.get(".pi-sort-amount-down").should("have.length", 1);
    cy.get(".p-sortable-column-icon")
      .eq(0)
      .should("have.class", "pi-sort-amount-down");
    cy.wait("@getEventsDescending").its("state").should("eq", "Complete");
  });

  it("will set up paginator correctly", () => {
    //   Check current page
    cy.get(".p-paginator-current").should("have.text", "Showing 1 to 1 of 1");
    cy.get(".p-paginator-page").should("have.text", "1");

    // Check default page size
    cy.get('[data-cy="table-pagination-options"] > .p-dropdown').should(
      "have.text",
      "10",
    );

    // Check page size options
    cy.get('[data-cy="table-pagination-options"] > .p-dropdown').click();
    cy.get(".p-dropdown-item").should("have.length", 4);
    cy.get(".p-dropdown-item").eq(0).should("have.text", "5");
    cy.get(".p-dropdown-item").eq(1).should("have.text", "10");
    cy.get(".p-dropdown-item").eq(2).should("have.text", "50");
    cy.get(".p-dropdown-item").eq(3).should("have.text", "100");
  });

  it("will refetch alerts when page size is changed", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=5&offset=0",
    ).as("getEventsSmallerPage");
    //   Check current page
    cy.get(".p-paginator-current").should("have.text", "Showing 1 to 1 of 1");
    cy.get(".p-paginator-page").should("have.text", "1");

    // Check default page size
    cy.get('[data-cy="table-pagination-options"] > .p-dropdown').should(
      "have.text",
      "10",
    );

    // Check page size options
    cy.get('[data-cy="table-pagination-options"] > .p-dropdown').click();
    cy.get(".p-dropdown-item").should("have.length", 4);
    cy.get(".p-dropdown-item").eq(0).click();
    cy.wait("@getEventsSmallerPage").its("state").should("eq", "Complete");

    // Check new page size
    cy.get('[data-cy="table-pagination-options"] > .p-dropdown').should(
      "have.text",
      "5",
    );
  });

  it("will reset selected columns, keyword search input, and column sort when reset table button is clicked", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Casc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("GET", "/api/event/?sort=name%7Casc&limit=10&offset=0").as(
      "getEventsNameAscending",
    );
    // SETUP
    //   Select all the columns
    cy.get('[data-cy="table-column-select"]').click();
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-multiselect-close").click();
    //   Change sort
    cy.get(".p-column-title").eq(1).click();
    cy.wait("@getEventsNameAscending").its("state").should("eq", "Complete");

    //   Type in keyword seach
    cy.get('[data-cy="table-keyword-search"]').click().type("Testing");

    // Click reset
    cy.get('[data-cy="reset-table-button"]').click();
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check columns
    // Check default columns in column select
    cy.get('[data-cy="table-column-select"]').should(
      "have.text",
      "Created, Name, Owner, Type, Vectors",
    );
    // Check columns in table
    cy.get(".p-column-title").eq(0).should("have.text", "Created");
    cy.get(".p-column-title").eq(1).should("have.text", "Name");
    cy.get(".p-column-title").eq(2).should("have.text", "Owner");
    cy.get(".p-column-title").eq(3).should("have.text", "Type");
    cy.get(".p-column-title").eq(4).should("have.text", "Vectors");

    // Check sort
    cy.get(".pi-sort-amount-down").should("have.length", 1);
    cy.get(".p-sortable-column-icon")
      .eq(0)
      .should("have.class", "pi-sort-amount-down");

    // Check keyword sort is empty
    cy.get('[data-cy="table-keyword-search"]')
      .should("be.visible")
      .should("be.empty");
  });
});

describe("ManageEvents.vue Filtering", () => {
  before(() => {
    cy.visit("/login");
    cy.login();
  });

  beforeEach(() => {
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
  });

  it("successfully adds a filter via the quick add filter", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");

    cy.get('[data-cy="edit-filter-button"]').click();
    cy.get('[data-cy="filter-input-type"]').click();
    // Select the 'name' filter type
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-type"]').should("have.text", "Name");
    cy.get('[data-cy="filter-input-value"]').should("be.empty");
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();

    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Check filter chip content
    cy.get(".filter-name-text").should("have.text", "Name:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "Test");
  });

  it("successfully updates a filter via the quick edit filter chip", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=NewValue",
    ).as("getEventsNameFilter2");

    // Add filter
    cy.get('[data-cy="edit-filter-button"]').click();
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Edit the filter
    cy.get('[data-cy="filter-chip-edit-button"]').click();
    cy.get('[data-cy="filter-chip-edit-panel"]').should("be.visible");
    cy.get('[data-cy="filter-input-value"]')
      .should("have.value", "Test")
      .click()
      .clear()
      .type("NewValue");
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.wait("@getEventsNameFilter2").its("state").should("eq", "Complete");

    // Check filter chip content
    cy.get(".filter-name-text").should("have.text", "Name:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "NewValue");
  });
  it("successfully removes a filter by clicking filter chip value or delete button", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsDefault");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");

    // Add filter
    cy.get('[data-cy="edit-filter-button"]').click();
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Click the value to remove
    cy.get('[data-cy="filter-chip-content"]').click();
    cy.get(".p-chip").should("not.exist");
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");

    // Add filter
    cy.get('[data-cy="edit-filter-button"]').click();
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Click the delete button to remove
    cy.get('[data-cy="filter-chip-remove-button"]').click();
    cy.get(".p-chip").should("not.exist");
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");
  });

  it("successfully adds and removes filter via the modal", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefault");

    // ADDING
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Click to add a filter
    cy.get(".p-dialog-footer > button").eq(1).click();

    // Add the filter
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Check that the currently set filter shows up
    cy.get('[data-cy="filter-input-type"]').should("have.text", "Name");
    cy.get('[data-cy="filter-input-value"]').should("have.value", "Test");
    // Remove the filter and submit
    cy.get('[data-cy="filter-input-delete"]').click();
    cy.get(".p-dialog-footer > button").eq(3).click();

    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");
  });

  it("successfully reset filters when reset filters clicked", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefault");

    // SETUP -- adding a filter
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Click to add a filter
    cy.get(".p-dialog-footer > button").eq(1).click();

    // Add the filter
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();

    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Click reset button
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(1).click();
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");
  });

  it("successfully clears filters when clear filters clicked", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&name=Test",
    ).as("getEventsNameFilter");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefault");

    // SETUP -- adding a filter
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Click to add a filter
    cy.get(".p-dialog-footer > button").eq(1).click();

    // Add the filter
    cy.get('[data-cy="filter-input-type"]').click();
    cy.get(".p-dropdown-item").eq(3).click();
    cy.get('[data-cy="filter-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();

    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Click clear button
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(2).click();
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");
  });

  it("successfully sets and clears the date range picker start", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&created_after=2020-01-01T00:00:00.000Z",
    ).as("getEventsCreatedAfterFilter");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefault");

    // Type in date and enter
    cy.get('[data-cy="date-range-picker-start-input"]')
      .click()
      .type("2020-01-01")
      .type("{enter}");
    // Click away from panel
    cy.get("#FilterToolbar > .p-toolbar").click();
    cy.wait("@getEventsCreatedAfterFilter")
      .its("state")
      .should("eq", "Complete");

    // Check filter val in chip
    cy.get(".filter-name-text").should("have.text", "Created After:");
    cy.get('[data-cy="filter-chip-content"]').should(
      "have.text",
      "2020-01-01T00:00:00.000Z",
    );

    // Clear the end date
    cy.get('[data-cy="date-range-picker-start-clear"]').click();
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");

    // Chip should be gone
    cy.get(".p-chip").should("not.exist");
  });
  it("successfully sets and clears the date range picker end", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&created_before=2020-01-01T00:00:00.000Z",
    ).as("getEventsCreatedBeforeFilter");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefault");

    // Type in date and enter
    cy.get('[data-cy="date-range-picker-end-input"]')
      .click()
      .type("2020-01-01")
      .type("{enter}");
    // Click away from panel
    cy.get("#FilterToolbar > .p-toolbar").click();
    cy.wait("@getEventsCreatedBeforeFilter")
      .its("state")
      .should("eq", "Complete");

    // Check filter val in chip
    cy.get(".filter-name-text").should("have.text", "Created Before:");
    cy.get('[data-cy="filter-chip-content"]').should(
      "have.text",
      "2020-01-01T00:00:00.000Z",
    );

    // Clear the end date
    cy.get('[data-cy="date-range-picker-end-clear"]').click();
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");

    // Chip should be gone
    cy.get(".p-chip").should("not.exist");
  });
});

describe("ManageEvents.vue Actions", () => {
  before(() => {
    cy.visit("/login");
    cy.login();
  });

  beforeEach(() => {
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
  });

  it("will not allow submission of a comment unless an event is selected and comment value is provided", () => {
    // Check comment submit button when no event is selected and no comment is provided
    cy.get('[data-cy="comment-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");
    cy.get(".p-dialog-header-icon").click();

    // Check comment submit button when an event is selected and no comment is provided
    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="comment-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");

    // Check comment submit button when an event is selected and comment is provided
    // (modal is still open already)
    cy.get(".p-inputtextarea").click().type("Test comment");
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.not.class", "p-disabled");
  });
  it("will not taking ownership of an event unless an event is selected", () => {
    // Check take ownership button when no event is selected
    cy.get('[data-cy="take-ownership-button"]').should(
      "have.class",
      "p-disabled",
    );

    // Check comment submit button when an event is selected and no comment is provided
    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="take-ownership-button"]').should(
      "have.not.class",
      "p-disabled",
    );
  });

  it("will not allow submission of an assigned owner unless an event is selected and owner is selected", () => {
    // Check assign submit button when no event is selected and no owner is selected
    cy.get('[data-cy="assign-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");
    cy.get(".p-dialog-header-icon").click();

    // Check assign submit button when an event is selected and no owner is selected
    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="assign-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");

    // Check assign submit button when an event is selected and owner is selected
    // (modal is still open already)
    cy.get(".p-field > .p-dropdown > .p-dropdown-label").click();
    cy.get(".p-dropdown-item").eq(0).click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.not.class", "p-disabled");
  });
  it("will not allow submission of a tag unless an event is selected and tag is provided", () => {
    // Check tag submit button when no event is selected and no tag is provided
    cy.get('[data-cy="tag-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");
    cy.get(".p-dialog-header-icon").click();

    // Check tag submit button when an event is selected and no tag is provided
    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="tag-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");

    // Check tag submit button when an event is selected and tag is provided
    // (modal is still open already)
    cy.get(".p-chips-input-token > input")
      .click()
      .type("TestTag")
      .type("{enter}");
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.not.class", "p-disabled");
  });
  it("will submit and show an event comment when comment is created via comment action", () => {
    cy.intercept("POST", "/api/node/comment/").as("createComment");

    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();

    // Add comment
    cy.get('[data-cy="comment-button"]').click();
    cy.get(".p-dialog-footer > button ")
      .eq(1)
      .should("have.class", "p-disabled");
    cy.get(".p-inputtextarea").click().type("Test comment");
    cy.get(".p-dialog-footer > button ").eq(1).click();
    cy.wait("@createComment").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check for comment displayed
    cy.get('[data-cy="comments"]').should(
      "have.text",
      "(Analyst) Test comment",
    );
  });

  it("assign event owner to current user when take ownership button is clicked", () => {
    cy.intercept("PATCH", "/api/event/").as("takeOwnership");

    // Select an event and take ownership
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="take-ownership-button"]').click();
    cy.wait("@takeOwnership").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check owner
    cy.get(".p-datatable-tbody > tr > :nth-child(4) > span").should(
      "have.text",
      "Analyst",
    );
  });
  it("will assign event owner to given user when owner is selected via assign action", () => {
    cy.intercept("PATCH", "/api/event/").as("assign");

    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();

    // Open modal and submit owner
    cy.get('[data-cy="assign-button"]').click();
    cy.get(".p-field > .p-dropdown > .p-dropdown-label").click();
    cy.get(".p-dropdown-item").eq(0).click();
    cy.get(".p-dialog-footer > button ").eq(1).click();
    cy.wait("@assign").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check owner
    cy.get(".p-datatable-tbody > tr > :nth-child(4) > span").should(
      "have.text",
      "Analyst Alice",
    );
  });
  it("will submit and show any event tags when tags are created via tag action", () => {
    cy.intercept("GET", "/api/node/tag/?offset=0").as("getTags");
    cy.intercept("POST", "/api/node/tag/").as("createTag");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    // Select an event
    cy.get(".p-selection-column > .p-checkbox ").click();

    // Open modal and add tags
    cy.get('[data-cy="tag-button"]').click();
    cy.wait("@getTags").its("state").should("eq", "Complete");

    cy.get(".p-chips-input-token > input")
      .click()
      .type("TestTag")
      .type("{enter}")
      .type("AnotherOne")
      .type("{enter}");
    cy.get(".p-dialog-footer > button ").eq(1).click();

    cy.wait("@createTag").its("state").should("eq", "Complete");
    cy.wait("@createTag").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check for tags
    cy.get(" .p-tag").eq(0).should("have.text", "TestTag");
    cy.get(" .p-tag").eq(1).should("have.text", "AnotherOne");
  });
});
