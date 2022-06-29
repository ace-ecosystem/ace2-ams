import { visitUrl } from "./helpers";

describe("ManageEvents.vue table functionality", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small.json",
        alert_count: 1,
        name: "Test Event",
      },
    });
  });

  beforeEach(() => {
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRowsExternalQueue");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRowsExternalQueue"],
    });
  });

  it("will show columns selected in select dropdown", () => {
    //   Select all the columns
    cy.get('[data-cy="table-column-select"]').click();
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    // Check columns in table
    cy.get('[data-cy="table-column-select"]').should(
      "have.text",
      "Created, Name, Threat Actors, Threats, Type, Severity, Prevention Tools, Remediation, Status, Owner, Vectors, Queue",
    );
    cy.get(".p-column-title").eq(0).should("have.text", "Created");
    cy.get(".p-column-title").eq(1).should("have.text", "Name");
    cy.get(".p-column-title").eq(2).should("have.text", "Threat Actors");
    cy.get(".p-column-title").eq(3).should("have.text", "Threats");
    cy.get(".p-column-title").eq(4).should("have.text", "Type");
    cy.get(".p-column-title").eq(5).should("have.text", "Severity");
    cy.get(".p-column-title").eq(6).should("have.text", "Prevention Tools");
    cy.get(".p-column-title").eq(7).should("have.text", "Remediation");
    cy.get(".p-column-title").eq(8).should("have.text", "Status");
    cy.get(".p-column-title").eq(9).should("have.text", "Owner");
    cy.get(".p-column-title").eq(10).should("have.text", "Vectors");
    cy.get(".p-column-title").eq(11).should("have.text", "Queue");

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

  it("will refetch events when page size is changed", () => {
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
    ).as("getEventsDefaultRowsExternalQueue");
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
    cy.wait("@getEventsDefaultRowsExternalQueue")
      .its("state")
      .should("eq", "Complete");

    // Check columns
    // Check default columns in column select
    cy.get('[data-cy="table-column-select"]').should(
      "have.text",
      "Created, Name, Threats, Severity, Status, Owner",
    );
    // Check columns in table
    cy.get(".p-column-title").eq(0).should("have.text", "Created");
    cy.get(".p-column-title").eq(1).should("have.text", "Name");
    cy.get(".p-column-title").eq(2).should("have.text", "Threats");
    cy.get(".p-column-title").eq(3).should("have.text", "Severity");
    cy.get(".p-column-title").eq(4).should("have.text", "Status");
    cy.get(".p-column-title").eq(5).should("have.text", "Owner");

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
    cy.resetDatabase();
    cy.login();

    // Add a test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small.json",
        alert_count: 1,
        name: "Test Event",
      },
    });
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
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'name' filter type
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-type"]').should("have.text", "Name");
    cy.get('[data-cy="property-input-value"]').should("be.empty");
    cy.get('[data-cy="property-input-value"]').click().type("Test");
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
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Edit the filter
    cy.get('[data-cy="filter-chip-edit-button"]').click();
    cy.get('[data-cy="filter-chip-edit-panel"]').should("be.visible");
    cy.get('[data-cy="property-input-value"]').click().clear().type("NewValue");
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
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Click the value to remove
    cy.get('[data-cy="filter-chip-content"]').click();
    cy.get(".p-chip").should("not.exist");
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");

    // Add filter
    cy.get('[data-cy="edit-filter-button"]').click();
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // Click the delete button to remove
    cy.contains("Name:").click();
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
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();
    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Check that the currently set filter shows up
    cy.get('[data-cy="property-input-type"]').should("have.text", "Name");
    cy.get('[data-cy="property-input-value"]').should("have.value", "Test");
    // Remove the filter and submit
    cy.get("[data-cy=property-input-delete]").click();
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

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&status=OPEN&queue=external",
    ).as("getEventsResetFilters");

    // SETUP -- adding a filter
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(0).click();

    // Click to add a filter
    cy.get(".p-dialog-footer > button").eq(1).click();

    // Add the filter
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();

    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Click reset button
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(1).click();
    cy.wait("@getEventsResetFilters").its("state").should("eq", "Complete");
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
    cy.get('[data-cy="property-input-type"]').click();
    cy.get("[aria-label='Name']").click();
    cy.get('[data-cy="property-input-value"]').click().type("Test");
    cy.get(".p-dialog-footer > button").eq(3).click();

    cy.wait("@getEventsNameFilter").its("state").should("eq", "Complete");

    // REMOVING
    // Click clear button
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(".p-menuitem-link").eq(2).click();
    cy.wait("@getEventsDefault").its("state").should("eq", "Complete");
  });
});

describe("ManageEvents.vue Actions", () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

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
    cy.intercept("POST", "/api/event/comment/").as("createComment");

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

  it("will assign event owner to current user when take ownership button is clicked", () => {
    cy.intercept("PATCH", "/api/event/").as("takeOwnership");

    // Select an event and take ownership
    cy.get(".p-selection-column > .p-checkbox ").click();
    cy.get('[data-cy="take-ownership-button"]').click();
    cy.wait("@takeOwnership").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check owner
    cy.get(".p-datatable-tbody > tr > :nth-child(9) > div").should(
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
    cy.get(".p-datatable-tbody > tr > :nth-child(9) > div").should(
      "have.text",
      "Analyst Alice",
    );
  });
  it("will submit and show any event tags when tags are created via tag action", () => {
    cy.intercept("GET", "/api/metadata/tag/?offset=0").as("getTags");
    cy.intercept("POST", "/api/metadata/tag/").as("createTag");
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

describe("ManageEvents.vue Filter Queues", () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small.json",
        alert_count: 1,
        name: "Test Event",
      },
    });
    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRowsExternalQueue");

    visitUrl({
      url: "/manage_events?queue=external",
      extraIntercepts: ["@getEventsDefaultRowsExternalQueue"],
    });
  });
  it("will display queue's correct options filters in quick add filter panel", () => {
    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // There should be 9 options
    cy.get(".p-dropdown-item").should("have.length", 9);
    // Click out of the quick add panel
    cy.get("#FilterToolbar > .p-toolbar").click();

    // Switch the queue
    cy.get('[data-cy="event-queue-selector"]').click();
    cy.get('[aria-label="internal"]').click();
    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // There should be 7 options
    cy.get(".p-dropdown-item").should("have.length", 7);
    // Click out of the quick add panel
    cy.get("#FilterToolbar > .p-toolbar").click();
  });
  it("will display queue's correct values for given filter filters in quick add filter panel", () => {
    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Check that correct options are available
    cy.get('[aria-label="OPEN"]').should("exist");
    cy.get('[aria-label="IGNORE"]').should("exist");
    cy.get('[aria-label="CLOSED"]').should("exist");
    // Click out of the quick add panel
    cy.get("#FilterToolbar > .p-toolbar").click();

    // Switch the queue
    cy.get('[data-cy="event-queue-selector"]').click();
    cy.get('[aria-label="internal"]').click();
    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Check that correct options are available
    cy.get('[aria-label="CLOSED"]').should("exist");
    cy.get('[aria-label="IGNORE"]').should("exist");
    cy.get('[aria-label="some internal value"]').should("exist");
  });
  it("will display queue's correct values for given filter in filter chip edit panel", () => {
    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Select a value and add the filter
    cy.get('[aria-label="OPEN"]').click();
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();

    // Open the filter chip quick edit panel
    cy.get('[data-cy="filter-chip-edit-button"]').eq(1).click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Check that correct options are available
    cy.get('[aria-label="CLOSED"]').should("exist");
    cy.get('[aria-label="IGNORE"]').should("exist");
    cy.get('[aria-label="OPEN"]').should("exist");
    // Switch the queue
    cy.get('[data-cy="event-queue-selector"]').click();
    cy.get('[aria-label="internal"]').click();

    // Open quick add filter panel
    cy.get('[data-cy="edit-filter-button"]').click();
    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Check that correct options are available
    cy.get('[aria-label="CLOSED"]').should("exist");
    cy.get('[aria-label="IGNORE"]').should("exist");
    cy.get('[aria-label="some internal value"]').should("exist");
  });

  it("will display queue's correct options filters in filter modal", () => {
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(":nth-child(1) > .p-menuitem-link").click();

    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // There should be 9 options
    cy.get(".p-dropdown-item").should("have.length", 9);

    // Switch the queue using the in-dialog selectorcy.get(
    cy.get(
      '.p-dialog-content > [data-cy="event-queue-selector"] > .p-float-label > #queue-dropdown > .p-dropdown-label',
    ).click();
    cy.get('[aria-label="internal"]').click();

    // Open list of options
    cy.get('[data-cy="property-input-type"]').first().click();
    // There should be 7 options
    cy.get(".p-dropdown-item").should("have.length", 7);
  });
  it("will display queue's correct values for given filter filters in filter modal", () => {
    // Open edit filter modal
    cy.get(".p-splitbutton > .p-button-icon-only").click();
    cy.get(":nth-child(1) > .p-menuitem-link").click();

    // Open list of options
    cy.get('[data-cy="property-input-type"]').click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label').click();
    // Select a value and add the filter
    cy.get('[aria-label="OPEN"]').click();

    // Switch the queue using the in-dialog selector
    cy.get(
      '.p-dialog-content > [data-cy="event-queue-selector"] > .p-float-label > #queue-dropdown > .p-dropdown-label',
    ).click();
    cy.get('[aria-label="internal"]').click();

    // Open list of options
    cy.get('[data-cy="property-input-type"]').first().click();
    // Select the 'status' type filter
    cy.get('[aria-label="Status"]').click();
    // Open the filter value options
    cy.get('[data-cy="property-input-value"] > .p-dropdown-label')
      .first()
      .click();
    // Check that correct options are available
    cy.get('[aria-label="CLOSED"]').should("exist");
    cy.get('[aria-label="IGNORE"]').should("exist");
    cy.get('[aria-label="some internal value"]').should("exist");
  });
});
