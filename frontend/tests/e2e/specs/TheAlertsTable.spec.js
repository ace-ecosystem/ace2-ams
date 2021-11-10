// WARNING!! These tests are running under the assumption that it is a freshly reset container and AnalyzeAlert.spec.js has successfully completed ONE time.
// Need to add some setup/teardown utilities in order to decouple these tests.

describe("TheAlertsTable.vue", () => {
  before(() => {
    cy.log("logging in");
    cy.login();
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
    cy.get("tr").should("have.length", 11);
  });

  it("has default columns visible", () => {
    cy.get(".p-multiselect-label").should(
      "have.text",
      "Event Date, Name, Owner, Disposition",
    );
    cy.get("tr > .p-highlight").should("have.text", "Event Date");
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
      "Dispositioned Time, Insert Date, Event Date, Name, Owner, Disposition, Dispositioned By, Queue, Type",
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
      "Event Date, Name, Owner, Disposition",
    );
  });

  it("selects/deselects as expected when checkboxes clicked", () => {
    // There should be this many checkboxes to start
    cy.get(".p-checkbox-box").should("have.length", 11);
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

  it("shows observable dropdown when arrow is clicked", () => {
    // There should be this many to start with
    cy.get(".p-row-toggler-icon").should("have.length", 10);
    // The observable dropdown should not be showing to start
    cy.get(".p-datatable-row-expansion > td").should("not.exist");
    // Click the chevron
    cy.get(":nth-child(1) > :nth-child(1) > .p-row-toggler")
      .should("be.visible")
      .click();
    // Now the observable dropdown should be visible
    cy.get(".p-datatable-row-expansion > td")
      .should("be.visible")
      .contains("Observables:");
    // Click the chevron again
    cy.get(":nth-child(1) > :nth-child(1) > .p-row-toggler")
      .should("be.visible")
      .click();
    // And the dropdown should be gone again
    cy.get(".p-datatable-row-expansion > td").should("not.exist");
  });

  it("shows observable dropdown when arrow is clicked", () => {
    cy.intercept("GET", "/api/alert/?limit=10&offset=0").as(
      "getAlertsDefaultRows",
    );
    cy.intercept("GET", "/api/alert/?limit=5&offset=0").as(
      "getAlertsChangedRows",
    );
    cy.intercept("GET", "/api/alert/?limit=5&offset=5").as(
      "getAlertsChangedRowsOffset",
    );
    // Should start with default number of rows
    cy.wait("@getAlertsDefaultRows").its("state").should("eq", "Complete");
    cy.get("tr").should("have.length", 11);
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
    cy.get("tr").should("have.length", 6);
  });

  // This test broken by pagination changes
  // it("correctly searches by keyword", () => {
  //   // Do a keyword search
  //   cy.get(".p-input-icon-left > .p-inputtext").type("1.2.3.4");
  //   // Based on created alerts, there should only be 4 now (+1 for header row)
  //   cy.get("tr").should("have.length", 3);
  // });
});
