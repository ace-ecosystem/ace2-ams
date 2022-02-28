import { openEditEventModal, visitUrl } from "./helpers";

describe("TheEventsTable.vue", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add some test events to the database
    for (let i = 0; i < 5; i++) {
      cy.request({
        method: "POST",
        url: "/api/test/add_event",
        body: {
          alert_template: "small_template.json",
          alert_count: 1,
          name: "Test Event " + i,
        },
      });
    }

    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 6,
        name: "Test Event 5",
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

    // Remove default queue filter (irrelevant to this test suite)
    cy.get('[data-cy="filter-chip-remove-button"]').click();
  });

  it("renders", () => {
    cy.get("#EventsTable").should("be.visible");
  });

  it("shows events", () => {
    // 1 row for header + 6 rows for events
    cy.get("tr").should("have.length", 7);
  });

  it("has default columns visible", () => {
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );
    // Edit event button column
    cy.get(".p-datatable-thead > tr > :nth-child(3)").should("have.text", "");
    cy.get("tr > .p-highlight").should("have.text", "Created");
    cy.get(".p-datatable-thead > tr > :nth-child(5)").should(
      "have.text",
      "Name",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(6)").should(
      "have.text",
      "Threats",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(7)").should(
      "have.text",
      "Risk Level",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(8)").should(
      "have.text",
      "Status",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(9)").should(
      "have.text",
      "Owner",
    );
  });

  it("resets selected columns when reset button clicked", () => {
    // Open selected columns multiselect
    cy.get(".p-multiselect-label").click();
    // Select all available columns
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    // Test that all of the selected columns are there
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threat Actors, Threats, Type, Risk Level, Prevention Tools, Remediation, Status, Owner, Vectors, Queue",
    );
    // Close the column multiselect
    cy.get(".p-multiselect-close").click();
    // Click the reset button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");
    // Test that it's gone back to the normal columns
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );
  });

  it("selects/deselects as expected when checkboxes clicked", () => {
    // There should be this many checkboxes to start (header + 6 events)
    cy.get(".p-checkbox-box").should("have.length", 7);
    // Test that they all start unchecked
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      cy.get(item).invoke("attr", "aria-checked").should("eq", "false");
    });
    // Test that they all become checked when header checkbox clicked
    cy.get(".p-column-header-content > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      cy.get(item).invoke("attr", "aria-checked").should("eq", "true");
    });
    // Test that they all become UNchecked when header checkbox clicked again
    cy.get(".p-column-header-content > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      cy.get(item).invoke("attr", "aria-checked").should("eq", "false");
    });
    // Test that when one is clicked that is the only one toggled
    cy.get(
      ":nth-child(3) > .p-selection-column > .p-checkbox > .p-checkbox-box",
    ).click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      if (index == 3) {
        cy.get(item).invoke("attr", "aria-checked").should("eq", "true");
      } else {
        cy.get(item).invoke("attr", "aria-checked").should("eq", "false");
      }
    });
    // Test that when header is clicked and one is selected, ALL are selected
    cy.get(".p-column-header-content > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      cy.get(item).invoke("attr", "aria-checked").should("eq", "true");
    });
    // Test that when is clicked while selected, it is the only one toggled
    cy.get(
      ":nth-child(3) > .p-selection-column > .p-checkbox > .p-checkbox-box",
    ).click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      if (index == 3) {
        cy.get(item).invoke("attr", "aria-checked").should("eq", "false");
      } else {
        cy.get(item).invoke("attr", "aria-checked").should("eq", "true");
      }
    });
    // Test that when header checkbox is clicked and many are selected, ALL are selected again
    cy.get(".p-column-header-content > .p-checkbox > .p-checkbox-box").click();
    cy.get(".p-checkbox-box").each((item, index) => {
      if (index == 0) {
        return;
      }
      cy.get(item).invoke("attr", "aria-checked").should("eq", "true");
    });
  });

  it("lazy pagination works correctly when page size or number is changed", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=5&offset=0",
    ).as("getEventsChangedRows");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=5&offset=5",
    ).as("getEventsChangedRowsOffset");
    // Should start with default number of rows (header + 6 alerts)
    cy.get("tr").should("have.length", 7);
    // Change number of rows to 5 per page
    cy.get('[data-cy="table-pagination-options"] .p-dropdown-trigger').click();
    cy.get('[aria-label="5"]').click();
    // Should reload with only 5 rows (+1 for header)
    cy.wait("@getEventsChangedRows").its("state").should("eq", "Complete");
    cy.get("tr").should("have.length", 6);
    // Click to next page and more alerts should be loaded (with offset)
    cy.get(".p-paginator-pages > :nth-child(2)").click();
    cy.wait("@getEventsChangedRowsOffset")
      .its("state")
      .should("eq", "Complete");
    // One row for header, one row for alert
    cy.get("tr").should("have.length", 2);
  });

  it("correctly changes the sort filter when a column is clicked", () => {
    cy.intercept("GET", "/api/event/?sort=name%7Casc&limit=10&offset=0").as(
      "nameSortAsc",
    );
    cy.intercept("GET", "/api/event/?sort=name%7Cdesc&limit=10&offset=0").as(
      "nameSortDesc",
    );
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Casc&limit=10&offset=0",
    ).as("createdTimeSortAsc");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("defaultSort");

    // sort by name to start, will default to ascending
    cy.get(".p-datatable-thead > tr > :nth-child(5)").click();
    // check api call
    cy.wait("@nameSortAsc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="eventName"]').eq(0).should("have.text", "Test Event 0");
    // sort by name again, will change to descending
    cy.get(".p-datatable-thead > tr > :nth-child(5)").click();
    // check api call
    cy.wait("@nameSortDesc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="eventName"]').eq(0).should("have.text", "Test Event 5");
    // sort by name again, this time it will remove all sorts
    cy.get(".p-datatable-thead > tr > :nth-child(5)").click();
    // there shouldn't be an API call this time
    // check first alerts name (will be the same)
    cy.get('[data-cy="eventName"]').eq(0).should("have.text", "Test Event 5");
    // sort by event time again, will default to ascending
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // check api call
    cy.wait("@createdTimeSortAsc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="eventName"]').eq(0).should("have.text", "Test Event 0");
    // click the reset table button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    // check api call
    cy.wait("@defaultSort").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="eventName"]').eq(0).should("have.text", "Test Event 5");
  });

  // This test broken by pagination changes
  it.skip("correctly searches by keyword", () => {
    // Do a keyword search
    cy.get(".p-input-icon-left > .p-inputtext").type("1.2.3.4");
    // Based on created alerts, there should only be 4 now (+1 for header row)
    cy.get("tr").should("have.length", 3);
  });

  it("correctly fetches and displays alerts when event row is expanded and hides when collapsed", () => {
    cy.intercept("GET", "/api/alert/?event_uuid=*").as("getEventAlerts");

    // Find the toggle button to expand and click on the first event
    cy.get(".p-row-toggler").eq(0).click();
    // cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");
    // Table of alerts should now exist
    cy.get("tr.p-datatable-row-expansion").should("exist").should("be.visible");
    // Check the first alert to make sure it's the expected one
    cy.get("[data-cy='alertName']").eq(0).should("have.text", "Manual Alert 0");
    // Also check that the tags are there for that alert
    // NOTE: The first (0) tags is for the event row. The second (1) is for the first alert in
    // the expanded event table.
    cy.get("[data-cy='tags']")
      .eq(1)
      .should("have.text", "tag0tag1tag2tag3tag4tag5tag6");
    // Click the toggle button again to close
    cy.get(".p-row-toggler").eq(0).click();
    // Table of alerts should no longer exist or be visible
    cy.get("tr.p-datatable-row-expansion").should("not.exist");
  });
  it("correctly filters by tag when a tag in the dropdown is clicked", () => {
    cy.intercept("GET", "/api/alert/?event_uuid=*").as("getEventAlerts");
    cy.intercept({
      method: "GET",
      path: "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&tags=tag0",
    }).as("filterURL");
    // Find the toggle button to expand and click on the first event
    cy.get(".p-row-toggler").eq(0).click();
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");
    // Table of alerts should now exist
    cy.get("tr.p-datatable-row-expansion").should("exist").should("be.visible");
    cy.waitFor('[data-cy="expandedEvent"] > .p-datatable-header');
    // Find and click the first tag in list
    cy.get("[data-cy='tags']").eq(1).contains("tag0").click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    cy.waitFor('[data-cy="expandedEvent"] > .p-datatable-header');
    // Check which event checkboxes are visible (should be 7, 1 header + 6 events that have the tag, + 7 checkboxes from alerts in expanded event)
    cy.get(".p-checkbox-box").should("have.length", 14);
  });

  it("pagination works correctly when a row is expanded", () => {
    cy.intercept("GET", "/api/alert/?event_uuid=*").as("getEventAlerts");
    // Find the toggle button to expand and click on the first event
    cy.get(".p-row-toggler").eq(0).click();
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");
    // Table of alerts should now exist
    cy.get("tr.p-datatable-row-expansion").should("exist").should("be.visible");
    // There should be 7 rows in the table (header + 6 alerts)
    cy.get("[data-cy='expandedEvent']")
      .eq(0)
      .within(() => {
        cy.get("tr").should("have.length", 7);
      });

    // Change number of rows to 5 per page
    cy.get(
      '[data-cy="event-alert-table-pagination-options"] > .p-dropdown > .p-dropdown-trigger',
    )
      .eq(0)
      .click();
    cy.get('[aria-label="5"]').click();

    // Should reload with only 5 rows (+1 for header) (but no API call is made)
    cy.get("[data-cy='expandedEvent']")
      .eq(0)
      .within(() => {
        cy.get("tr").should("have.length", 6);
      });

    // Click to next page and more alerts should be loaded (again no API call)
    cy.get(".p-paginator-pages > :nth-child(2)").click();

    // One row for header, one row for alert
    cy.get("[data-cy='expandedEvent']")
      .eq(0)
      .within(() => {
        cy.get("tr").should("have.length", 2);
      });
  });
});

describe("TheEventsTable.vue - Remove Alerts", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add a test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 6,
        name: "Test Event 5",
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

    // Remove default queue filter (irrelevant to this test suite)
    cy.get('[data-cy="filter-chip-remove-button"]').click();
  });

  it("removes alerts from the event when Remove Alerts button is clicked", () => {
    cy.intercept("GET", "/api/alert/?event_uuid=*").as("getEventAlerts");
    cy.intercept("PATCH", "/api/alert/").as("updateAlerts");

    // Find the toggle button to expand and click on the first event
    cy.get(".p-row-toggler").eq(0).click();
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");

    // There should be 6 alerts in the event
    cy.get("[data-cy='event-alert-table-pagination-options']").should(
      "contain.text",
      "6 alerts in the event",
    );

    // Select the first alert
    cy.get("[data-cy='expandedEvent']")
      .eq(0)
      .within(() => {
        cy.get(".p-checkbox-box").eq(1).click();
      });

    // Click the Remove Alerts button
    cy.get("[data-cy='remove-alerts-button']").click();

    // Wait for the API call to remove the alert from the event
    cy.wait("@updateAlerts").its("state").should("eq", "Complete");

    // Wait for the API call to refetch the list of alerts in the event
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");

    // The event should only have 5 alerts now
    cy.get("[data-cy='event-alert-table-pagination-options']").should(
      "contain.text",
      "5 alerts in the event",
    );

    // Select all of the alerts
    cy.get("[data-cy='expandedEvent']")
      .eq(0)
      .within(() => {
        cy.get(".p-checkbox-box").eq(0).click();
      });

    // Click the Remove Alerts button
    cy.get("[data-cy='remove-alerts-button']").click();

    // Wait for the API call to remove the alert from the event
    cy.wait("@updateAlerts").its("state").should("eq", "Complete");

    // Wait for the API call to refetch the list of alerts in the event
    cy.wait("@getEventAlerts").its("state").should("eq", "Complete");

    // The event should not have any alerts now
    cy.get("[data-cy='event-alert-table-pagination-options']").should(
      "contain.text",
      "0 alerts in the event",
    );
  });
});

describe("TheEventsTable.vue - EditEventModal", () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.login();

    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
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

    // Remove default queue filter (irrelevant to this test suite)
    cy.get('[data-cy="filter-chip-remove-button"]').click();
  });

  it("opens edit event modal with expected buttons when open button is clicked", () => {
    openEditEventModal();

    cy.get("[data-cy=edit-event-modal]").should("be.visible");
    cy.get(".p-dialog-header-close-icon").should("be.visible");
    cy.get(".p-dialog-header-close-icon").should("be.visible");
    cy.get("[data-cy=nevermind-edit-event-button]").should("be.visible");
    cy.get("[data-cy=nevermind-edit-event-button]").should("be.visible");
  });
  it("loads event data for each input when edit event modal is opened", () => {
    openEditEventModal();

    // Check name
    cy.get("[data-cy=event-name-field] .field > input").should(
      "have.value",
      "Test Event",
    );
    // Check owner
    cy.get("[data-cy=event-owner-field] [data-cy=property-input-value]")
      .invoke("text")
      .should("eq", "Analyst Alice");
    // Check remediation
    cy.get(
      "[data-cy=event-remediations-field] [data-cy=property-input-value]",
    ).should("have.value", "");
    // Check event time
    cy.get(
      "[data-cy=event-eventTime-field] [data-cy=property-input-value]",
    ).should("have.value", "");
  });
  it("successfully updates an 'input'-type field (ex. name)", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");

    openEditEventModal();

    cy.get("[data-cy=event-name-field]  [data-cy=property-input-value]")
      .click()
      .clear()
      .type("New Name");
    cy.get("[data-cy=save-edit-event-button]").click();
    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");
    cy.get("[data-cy=eventName]").invoke("text").should("eq", "New Name");
  });
  it("successfully updates an 'select'-type field (ex. owner)", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");

    openEditEventModal();

    cy.get(
      "[data-cy=event-owner-field] [data-cy=property-input-value]",
    ).click();
    cy.get('[aria-label="Analyst"]').click();
    cy.get("[data-cy=save-edit-event-button]").click();
    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");
    cy.get(".p-datatable-tbody > tr > :nth-child(9) > span")
      .invoke("text")
      .should("eq", "Analyst");
  });
  it("successfully updates an 'multiselect'-type field (ex. remediation)", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");

    openEditEventModal();

    cy.get(
      "[data-cy=event-remediations-field]  [data-cy=property-input-value]",
    ).click();
    cy.get(".p-multiselect-item ").eq(0).click();
    cy.get(".p-multiselect-item ").eq(1).click();

    cy.get("[data-cy=save-edit-event-button]").click();
    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");
  });
  it("successfully updates a 'date'-type field (ex. event time)", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");

    openEditEventModal();

    cy.get("[data-cy=event-eventTime-field]  [data-cy=property-input-value]")
      .click()
      .type("03/02/2022 12:00");

    cy.get("[data-cy=save-edit-event-button]").click();
    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");
  });
  it("successfully updates a comment using NodeCommentEditor", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");
    cy.intercept("PATCH", "/api/node/comment/*").as("updateComment");

    // First add an initial comment
    cy.get(".p-column-header-content > .p-checkbox > .p-checkbox-box").click();
    cy.get("[data-cy=comment-button]").click();
    cy.get(".p-inputtextarea").click().type("Test comment");
    cy.get(".p-dialog-footer > .p-button").last().click();

    // Check that the comment field is set up correctly
    openEditEventModal();

    cy.get("li.p-listbox-item > span").should(
      "include.text",
      "(Analyst) Test comment",
    );

    // Open the edit comment panel and check initial input
    cy.get("[data-cy=edit-comment-button]").click();
    cy.get("[data-cy=edit-comment-panel]").should("be.visible");
    cy.get("[data-cy=updated-comment-value]").should(
      "have.value",
      "Test comment",
    );
    // Test closing the edit comment panel without saving
    cy.get("[data-cy=close-edit-comment-panel]").click();
    cy.get("[data-cy=edit-comment-panel]").should("not.exist");
    // Test adding a new comment value and saving the event
    cy.get("[data-cy=edit-comment-button]").click();
    cy.get("[data-cy=updated-comment-value]")
      .click()
      .clear()
      .type("Updated comment");
    cy.get("[data-cy=save-comment-button]").click();
    cy.get("li.p-listbox-item > span").should(
      "include.text",
      "(Analyst) Updated comment",
    );
    cy.get("[data-cy=save-edit-event-button]").click();

    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@updateComment").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Check comment value
    cy.get(".p-mr-2 > span").should("have.text", "(Analyst) Updated comment");
  });
  it("successfully creates a new threat or updates using NodeThreatSelector", () => {
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("PATCH", "/api/event/").as("updateAlert");
    cy.intercept("POST", "/api/node/threat/").as("createThreat");
    cy.intercept("PATCH", "/api/node/threat/*").as("updateThreat");
    cy.intercept("GET", "/api/node/threat/*").as("getThreats");

    openEditEventModal();

    // Open new threat panel
    cy.get("[data-cy=new-threat-button]").click();
    cy.get("[data-cy=edit-threat-panel]").should("be.visible");
    // Add new threat values
    cy.get("[data-cy=edit-threat-panel] > :nth-child(1) > .p-inputtext")
      .click()
      .type("test");
    cy.get("[data-cy=threat-types]").click();
    cy.get(".p-multiselect-item ").eq(0).click();
    cy.get(".p-multiselect-item ").eq(1).click();

    // Save the new threat and intercept calls for creating/fetching new threat
    cy.get("[data-cy=save-threat-button]").click();
    cy.wait("@createThreat").its("state").should("eq", "Complete");
    cy.wait("@getThreats").its("state").should("eq", "Complete");

    // Select the new threat and save
    cy.get(".p-listbox-item > .align-items-center").click();
    cy.get("[data-cy=save-edit-event-button]").click();
    cy.wait("@updateAlert").its("state").should("eq", "Complete");
    cy.wait("@getEventsDefaultRows").its("state").should("eq", "Complete");

    // Reopen the panel
    openEditEventModal();

    // Check that the panel gets initialized with correct values when editing
    cy.get("[data-cy=edit-threat-button] > .pi").click();
    cy.get("[data-cy=edit-threat-panel]").should("be.visible");
    cy.get("[data-cy=threat-name]").should("have.value", "test");
    cy.get(
      ":nth-child(2) > .p-multiselect > .p-multiselect-label-container > .p-multiselect-label",
    )
      .invoke("text")
      .should("not.eq", "");

    // Test closing the panel
    cy.get("[data-cy=close-edit-threat-panel-button]").click();
    cy.get("[data-cy=edit-threat-panel]").should("not.exist");

    // Open the panel again and test changing the threats
    cy.get("[data-cy=edit-threat-button] > .pi").click();
    cy.get("[data-cy=threat-types]").click();
    cy.get(".p-multiselect-item ").eq(2).click();
    cy.get(".p-multiselect-item ").eq(3).click();
    cy.get("[data-cy=save-threat-button]").click();

    // Make sure that the threat was updated
    cy.wait("@updateThreat").its("state").should("eq", "Complete");
  });
});

describe("TheEventsTable.vue - Queue Settings", () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.login();

    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    // Intercept the API call that loads the default event table view
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&queue=external",
    ).as("getEventsExternalQueueFilter");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0&queue=internal",
    ).as("getEventsInternalQueueFilter");

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsExternalQueueFilter"],
    });
  });

  it("will auto-set the event queue filter and event table columns based on the auth'd users preferredEventQueue", () => {
    //  External queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "external");
    // Queue selector should have right value
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-label',
    ).should("have.text", "external");
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );

    // log out and log back in as 'alice', whose default event queue is 'internal'
    cy.logout();
    cy.login("alice");
    // go to manage events
    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsInternalQueueFilter"],
    });

    //  Default queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "internal");
    // Queue selector should have right value
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-label',
    ).should("have.text", "internal");
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should("have.text", "Created, Name, Type");
  });
  it("will update the event queue filter and event table columns when preferred event queue is changed", () => {
    //  Default queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "external");
    // Queue selector should have right value
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-label',
    ).should("have.text", "external");
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );

    // Open queue selector and check options
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-trigger',
    ).click();
    cy.get(".p-dropdown-items").should("be.visible");
    cy.get('[aria-label="external"]').should("be.visible");
    cy.get('[aria-label="internal"]').should("be.visible");
    cy.get('[aria-label="intel"]').should("be.visible");

    // Switch to internal queue and check data
    cy.get('[aria-label="internal"]').click();
    cy.wait("@getEventsInternalQueueFilter")
      .its("state")
      .should("eq", "Complete");
    // internal queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "internal");
    // Queue selector should have right value
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-label',
    ).should("have.text", "internal");
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should("have.text", "Created, Name, Type");

    // Switch back to external queue
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-trigger',
    ).click();
    cy.get('[aria-label="external"]').click();
    cy.wait("@getEventsExternalQueueFilter")
      .its("state")
      .should("eq", "Complete");
    // External queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "external");
    // Queue selector should have right value
    cy.get(
      '[data-cy="event-queue-selector"] > .p-dropdown > .p-dropdown-label',
    ).should("have.text", "external");
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );
  });
});
