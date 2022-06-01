import { visitUrl } from "./helpers";

describe("TheAlertsTable.vue", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Add 6 test alerts to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_alerts",
      body: {
        template: "small_template.json",
        count: 6,
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

  it("renders", () => {
    cy.get("#AlertsTable").should("be.visible");
  });

  it("shows alerts", () => {
    // 1 row for header + 6 rows for alerts
    cy.get("tr").should("have.length", 7);
  });

  it("has default columns visible", () => {
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Event Time (UTC), Name, Owner, Disposition",
    );
    cy.get("tr > .p-highlight").should("have.text", "Event Time (UTC)");
    cy.get(".p-datatable-thead > tr > :nth-child(4)").should(
      "have.text",
      "Name",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(5)").should(
      "have.text",
      "Owner",
    );
    cy.get(".p-datatable-thead > tr > :nth-child(6)").should(
      "have.text",
      "Disposition",
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
      "Dispositioned Time (UTC), Insert Time (UTC), Event Time (UTC), Name, Owner, Disposition, Dispositioned By, Queue, Type",
    );
    // Close the column multiselect
    cy.get(".p-multiselect-close").click();
    // Click the reset button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    // Test that it's gone back to the normal columns
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Event Time (UTC), Name, Owner, Disposition",
    );
  });

  it("selects/deselects as expected when checkboxes clicked", () => {
    // There should be this many checkboxes to start (header + 6 alerts)
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
      "/api/alert/?sort=event_time%7Cdesc&limit=5&offset=0",
    ).as("getAlertsChangedRows");
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=5&offset=5",
    ).as("getAlertsChangedRowsOffset");
    // Should start with default number of rows (header + 6 alerts)
    cy.get("tr").should("have.length", 7);
    // Change number of rows to 5 per page
    cy.get(".p-dropdown-trigger").click();
    cy.get('[aria-label="5"]').click();
    // Should reload with only 5 rows (+1 for header)
    cy.wait("@getAlertsChangedRows").its("state").should("eq", "Complete");
    cy.get("tr").should("have.length", 6);
    // Click to next page and more alerts should be loaded (with offset)
    cy.get(".p-paginator-pages > :nth-child(2)").click();
    cy.wait("@getAlertsChangedRowsOffset")
      .its("state")
      .should("eq", "Complete");
    // One row for header, one row for alert
    cy.get("tr").should("have.length", 2);
  });

  it("correctly changes the sort filter when a column is clicked", () => {
    cy.intercept("GET", "/api/alert/?sort=name%7Casc&limit=10&offset=0").as(
      "nameSortAsc",
    );
    cy.intercept("GET", "/api/alert/?sort=name%7Cdesc&limit=10&offset=0").as(
      "nameSortDesc",
    );
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Casc&limit=10&offset=0",
    ).as("eventTimeSortAsc");
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("defaultSort");

    // sort by name to start, will default to ascending
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // check api call
    cy.wait("@nameSortAsc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Manual Alert 0");
    // sort by name again, will change to descending
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // check api call
    cy.wait("@nameSortDesc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Manual Alert 5");
    // sort by name again, this time it will remove all sorts
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // there shouldn't be an API call this time
    // check first alerts name (will be the same)
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Manual Alert 5");
    // sort by event time again, will default to ascending
    cy.get(".p-datatable-thead > tr > :nth-child(3)").click();
    // check api call
    cy.wait("@eventTimeSortAsc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Manual Alert 0");
    // click the reset table button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    // check api call
    cy.wait("@defaultSort").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Manual Alert 5");
  });

  // This test broken by pagination changes
  it.skip("correctly searches by keyword", () => {
    // Do a keyword search
    cy.get(".p-input-icon-left > .p-inputtext").type("1.2.3.4");
    // Based on created alerts, there should only be 4 now (+1 for header row)
    cy.get("tr").should("have.length", 3);
  });

  it("correctly fetches and displays observables when alert row is expanded and hides when collapsed", () => {
    cy.intercept("POST", "/api/alert/observables").as("getAlertObservables");

    // Find the toggle button to expand and click on the first alert
    cy.get(".p-row-toggler").eq(0).click();
    // cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    cy.wait("@getAlertObservables").its("state").should("eq", "Complete");
    // List of observables should now exist
    cy.get("td ul").should("exist").should("be.visible");
    // Check the first observable to make sure it's the expected one (aka sorting and formatting worked)
    cy.get(":nth-child(1) > .link-text").should(
      "have.text",
      "o_type0 : o_value0",
    );
    // Also check that the tags are there for that observable
    cy.get(":nth-child(1) > .tag > .p-tag")
      .should("contain.text", "tag0")
      .should("contain.text", "tag1")
      .should("contain.text", "tag2");
    // Click the toggle button again to close
    cy.get(".p-row-toggler").eq(0).click();
    // List of observables should no longer exist or be visible
    cy.get("td ul").should("not.exist");
  });
  it("correctly filters by observable when an observable in the dropdown is clicked", () => {
    cy.intercept("POST", "/api/alert/observables").as("getAlertObservables");
    cy.intercept({
      method: "GET",
      path: "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&observable=o_type0%7Co_value0",
    }).as("filterURL");
    // Find the toggle button to expand and click on the first alert
    cy.get(".p-row-toggler").eq(0).click();
    cy.wait("@getAlertObservables").its("state").should("eq", "Complete");
    // List of observables should now exist
    cy.get("td ul").should("exist").should("be.visible");
    // Find and click the first observable in list
    cy.get(":nth-child(1) > .link-text")
      .should("have.text", "o_type0 : o_value0")
      .click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    // Check which alerts checkboxes are visible (should be 7, 1 header + 6 alerts that have the observable)
    cy.get(".p-checkbox-box").should("have.length", 7);
  });
  it("correctly filters by tag when an observable tag in the dropdown is clicked", () => {
    cy.intercept("POST", "/api/alert/observables").as("getAlertObservables");
    cy.intercept({
      method: "GET",
      path: "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=tag0",
    }).as("filterURL");
    // Find the toggle button to expand and click on the first alert
    cy.get(".p-row-toggler").eq(0).click();
    cy.wait("@getAlertObservables").its("state").should("eq", "Complete");
    // List of observables should now exist
    cy.get("td ul").should("exist").should("be.visible");
    // Find and click the first observable tag in list
    cy.get(":nth-child(1) > .tag > .p-tag")
      .eq(1)
      .should("contain.text", "tag0")
      .click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    // Check which alerts checkboxes are visible (should be 7, 1 header + 6 alerts that have the observable)
    cy.get(".p-checkbox-box").should("have.length", 7);
  });
});
