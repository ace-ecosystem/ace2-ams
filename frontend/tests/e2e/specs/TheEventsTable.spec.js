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
      timeout: 60000,
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

  it("resets selected columns when reset button clicked", () => {
    // Open selected columns multiselect
    cy.get(".p-multiselect-label").click();
    // Select all available columns
    cy.get(".p-multiselect-header > .p-checkbox > .p-checkbox-box").click();
    // Test that all of the selected columns are there
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threat Actors, Threats, Type, Severity, Prevention Tools, Remediation, Status, Owner, Vectors, Queue",
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
      "Created, Name, Threats, Severity, Status, Owner",
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
    cy.waitFor('[data-cy="event-alerts-table"] > .p-datatable-header');
    // Find and click the first tag in list
    cy.get("[data-cy='tags']").eq(1).contains("tag0").click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    cy.waitFor('[data-cy="event-alerts-table"] > .p-datatable-header');
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
    cy.get("[data-cy='event-alerts-table']")
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
    cy.get("[data-cy='event-alerts-table']")
      .eq(0)
      .within(() => {
        cy.get("tr").should("have.length", 6);
      });

    // Click to next page and more alerts should be loaded (again no API call)
    cy.get(".p-paginator-pages > :nth-child(2)").click();

    // One row for header, one row for alert
    cy.get("[data-cy='event-alerts-table']")
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
      timeout: 50000,
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
    cy.get("[data-cy='event-alerts-table']")
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
    cy.get("[data-cy='event-alerts-table']")
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
      extraIntercepts: ["@getEventsDefaultRows"],
    });
  });

  it("will auto-set the event queue filter and event table columns based on the auth'd users preferredEventQueue", () => {
    // Queue selector should have right value
    cy.get("#queue-dropdown > .p-dropdown-label").should(
      "have.text",
      "external",
    );
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Severity, Status, Owner",
    );

    // log out and log back in as 'alice', whose default event queue is 'internal'
    cy.logout();
    cy.login("alice");
    // go to manage events
    visitUrl({
      url: "/manage_events",
    });
    // Queue selector should have right value
    cy.get("#queue-dropdown > .p-dropdown-label").should(
      "have.text",
      "internal",
    );
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should("have.text", "Created, Name, Type");
  });
  it("will update the event queue filter and event table columns when preferred event queue is changed", () => {
    // Queue selector should have right value
    cy.get("#queue-dropdown > .p-dropdown-label").should(
      "have.text",
      "external",
    );
    // Correct columns should be showing
    // Open queue selector and check options
    cy.get("#queue-dropdown > .p-dropdown-label").click();
    cy.get(".p-dropdown-items").should("be.visible");
    cy.get('[aria-label="external"]').should("be.visible");
    cy.get('[aria-label="internal"]').should("be.visible");
    cy.get('[aria-label="intel"]').should("be.visible");

    // Switch to internal queue and check data
    cy.get('[aria-label="internal"]').click();
    cy.wait("@getEventsInternalQueueFilter")
      .its("state")
      .should("eq", "Complete");
    // Queue selector should have right value
    cy.get("#queue-dropdown > .p-dropdown-label").should(
      "have.text",
      "internal",
    );
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should("have.text", "Created, Name, Type");

    // Switch back to external queue
    cy.get("#queue-dropdown > .p-dropdown-label").click();
    cy.get('[aria-label="external"]').click();
    cy.wait("@getEventsExternalQueueFilter")
      .its("state")
      .should("eq", "Complete");
    // External queue filter should be there (check filter chip)
    cy.get(".p-chip .filter-name-text").should("have.text", "Queue:");
    cy.get('[data-cy="filter-chip-content"]').should("have.text", "external");
    // Queue selector should have right value
    cy.get("#queue-dropdown > .p-dropdown-label").should(
      "have.text",
      "external",
    );
    // Correct columns should be showing
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Created, Name, Threats, Severity, Status, Owner",
    );
  });
});
