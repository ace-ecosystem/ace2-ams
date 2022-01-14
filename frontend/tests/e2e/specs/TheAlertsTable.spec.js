// WARNING!! These tests are running under the assumption that it is a freshly reset container and AnalyzeAlert.spec.js has successfully completed ONE time.
// Need to add some setup/teardown utilities in order to decouple these tests.

describe("TheAlertsTable.vue", () => {
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
    cy.get("#AlertsTable").should("be.visible");
  });

  it("shows alerts", () => {
    cy.get("tr").should("have.length", 8);
  });

  it("has default columns visible", () => {
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Event Time, Name, Owner, Disposition",
    );
    cy.get("tr > .p-highlight").should("have.text", "Event Time");
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
      "Dispositioned Time, Insert Time, Event Time, Name, Owner, Disposition, Dispositioned By, Queue, Type",
    );
    // Close the column multiselect
    cy.get(".p-multiselect-close").click();
    // Click the reset button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    // Test that it's gone back to the normal columns
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Event Time, Name, Owner, Disposition",
    );
  });

  it("selects/deselects as expected when checkboxes clicked", () => {
    // There should be this many checkboxes to start
    cy.get(".p-checkbox-box").should("have.length", 8);
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
      "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0",
    ).as("getAlertsDefaultRows");
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=5&offset=0",
    ).as("getAlertsChangedRows");
    cy.intercept(
      "GET",
      "/api/alert/?sort=event_time%7Cdesc&limit=5&offset=5",
    ).as("getAlertsChangedRowsOffset");
    // Should start with default number of rows
    cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    cy.get("tr").should("have.length", 8);
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
    cy.get("tr").should("have.length", 3);
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
    cy.get(".p-datatable-tbody > :nth-child(1) > :nth-child(4)").should(
      "have.text",
      "Manual Alert",
    );
    // sort by name again, will change to descending
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // check api call
    cy.wait("@nameSortDesc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Small Alert");
    // sort by name again, this time it will remove all sorts
    cy.get(".p-datatable-thead > tr > :nth-child(4)").click();
    // there shouldn't be an API call this time
    // check first alerts name (will be the same)
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Small Alert");
    // sort by event time again, will default to ascending
    cy.get(".p-datatable-thead > tr > :nth-child(3)").click();
    // check api call
    cy.wait("@eventTimeSortAsc").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Small Alert");
    // click the reset table button
    cy.get(
      ".p-datatable-header > .p-toolbar > .p-toolbar-group-right > :nth-child(2)",
    ).click();
    // check api call
    cy.wait("@defaultSort").its("state").should("eq", "Complete");
    // check first alerts name
    cy.get('[data-cy="alertName"]').eq(0).should("have.text", "Small Alert");
  });

  // This test broken by pagination changes
  // it("correctly searches by keyword", () => {
  //   // Do a keyword search
  //   cy.get(".p-input-icon-left > .p-inputtext").type("1.2.3.4");
  //   // Based on created alerts, there should only be 4 now (+1 for header row)
  //   cy.get("tr").should("have.length", 3);
  // });

  it("correctly fetches and displays observables when alert row is expanded and hides when collapsed", () => {
    // Find the toggle button to expand and click (on the Small Alert alert)
    cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    // List of observables should now exist
    cy.get("td > ul").should("exist").should("be.visible");
    // Check the first observable to make sure it's the expected one (aka sorting and formatting worked)
    cy.get(":nth-child(1) > .link-text").should(
      "have.text",
      "email_address : badguy@evil.com",
    );
    // Also check that the tag is there for that observable
    cy.get('[data-cy=tags] > :nth-child(3) > .p-tag > .tag').should(
      "have.text",
      "from_address",
    );
    // Click the toggle button again to close
    cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    // List of observables should no longer exist or be visible
    cy.get("td > ul").should("not.exist");
  });
  it("correctly filters by observable when an observable in the dropdown is clicked", () => {
    cy.intercept({
      method: "GET",
      path: "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&observable=email_address%7Cbadguy%40evil.com",
    }).as("filterURL");
    // Find the toggle button to expand and click (on the Small Alert alert)
    cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    // List of observables should now exist
    cy.get("td > ul").should("exist").should("be.visible");
    // Find and click the first observable in list
    cy.get(":nth-child(1) > .link-text")
      .should("have.text", "email_address : badguy@evil.com")
      .click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    // Check which alerts checkboxes are visible (should be 2, 1 header + 1 alert that has the email_address observable)
    cy.get(".p-checkbox-box").should("have.length", 2);
  });
  it("correctly filters by tag when an observable tag in the dropdown is clicked", () => {
    cy.intercept({
      method: "GET",
      path: "/api/alert/?sort=event_time%7Cdesc&limit=10&offset=0&tags=from_address",
    }).as("filterURL");
    // Find the toggle button to expand and click (on the Small Alert alert)
    cy.get(":nth-child(7) > :nth-child(1) > .p-row-toggler").click();
    // List of observables should now exist
    cy.get("td > ul").should("exist").should("be.visible");
    // Find and click the first observable tag in list
    cy.get('[data-cy=tags] > :nth-child(3) > .p-tag > .tag')
      .should("have.text", "from_address")
      .click();
    // Wait for the filtered view to be requested
    cy.wait("@filterURL");
    // Check which alerts checkboxes are visible (should be only 1 for the header, and 1 alert with that tag)
    cy.get(".p-checkbox-box").should("have.length", 2);
  });
});
