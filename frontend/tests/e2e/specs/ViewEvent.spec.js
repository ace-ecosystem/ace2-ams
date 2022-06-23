import { visitUrl } from "./helpers";

describe("ViewEvent.vue", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });

  it("Switches the component / details section when selected from dropdown", () => {
    // Click on the Analysis dropdown
    cy.get('[aria-haspopup="true"]').eq(2).click();
    // Select first available analysis type
    cy.get("span").contains("Email Analysis").click();
    // Check that rge analysis showed up
    cy.get('[data-cy="event-details-content"]')
      .contains("Email Analysis")
      .should("be.visible");
    // Switch back to the event summary section and check content
    cy.get('[aria-haspopup="true"]').eq(1).click();
    cy.get("span").contains("Event Summary").click();
    cy.get("#event-section-title").should("contain.text", "Event Summary");
  });
});

describe("ViewEvent.vue actions", () => {
  beforeEach(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });

  // Have to  manually leave event page
  // BC when database resets it will try to get the old event with old uuid
  // And will cause an error
  afterEach(() => {
    visitUrl({
      url: "/manage_alerts",
    });
  });

  it("Correctly adds comment via comment modal and reloads page", () => {
    cy.intercept("POST", "/api/node/comment/").as("addComment");

    // Click on the Actions dropdown
    cy.get('[aria-haspopup="true"]').eq(0).click();
    cy.get("span").contains("Comment").click();
    // Add test data and submit
    cy.get(".p-inputtextarea").click().type("Test comment");
    cy.get(".p-dialog-footer > Button").last().click();
    cy.wait("@addComment").its("state").should("eq", "Complete");
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });
  it("Correctly takes ownership via take ownership item and reloads page", () => {
    cy.intercept("PATCH", "/api/event/").as("updateEvent");

    // Click on the Actions dropdown
    cy.get('[aria-haspopup="true"]').eq(0).click();
    cy.get("span").contains("Take Ownership").click();
    cy.wait("@updateEvent").its("state").should("eq", "Complete");
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });
  it("Correctly assigns owner via assign modal and reloads page", () => {
    cy.intercept("PATCH", "/api/event/").as("updateEvent");

    // Click on the Actions dropdown
    cy.get('[aria-haspopup="true"]').eq(0).click();
    cy.get("span").contains("Assign").click();
    cy.get(".p-dropdown-trigger").click();
    cy.get('[aria-label="Analyst Alice"]').click();
    cy.get(".p-dialog-footer > Button").last().click();
    cy.wait("@updateEvent").its("state").should("eq", "Complete");
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });
  it("Correctly adds tags via add tags modal and reloads page", () => {
    cy.intercept("PATCH", "/api/event/").as("updateEvent");
    cy.intercept("POST", "/api/metadata/tag/").as("addTag");

    // Click on the Actions dropdown
    cy.get('[aria-haspopup="true"]').eq(0).click();
    cy.get("span").contains("Add Tags").click();
    cy.get(".p-chips > .p-inputtext").click().type("TestTag").type("{enter}");
    cy.get(".p-dialog-footer > Button").last().click();
    cy.wait("@addTag").its("state").should("eq", "Complete");
    cy.wait("@updateEvent").its("state").should("eq", "Complete");
    cy.wait("@getEvent").its("state").should("eq", "Complete");
    cy.get(".p-tag").should("be.visible");
    cy.get(".p-tag > .tag").should("have.text", "TestTag");
  });
  it("Correctly edits event via edit event modal and reloads page", () => {
    cy.intercept("PATCH", "/api/event/").as("updateEvent");
    cy.intercept("GET", "/api/event/prevention_tool/?offset=0").as(
      "eventPreventionTool",
    );
    cy.intercept("GET", "/api/event/remediation/?offset=0").as(
      "eventRemediation",
    );
    cy.intercept("GET", "/api/event/severity/?offset=0").as("eventSeverity");
    cy.intercept("GET", "/api/event/status/?offset=0").as("eventStatus");
    cy.intercept("GET", "/api/event/type/?offset=0").as("eventType");
    cy.intercept("GET", "/api/event/vector/?offset=0").as("eventVector");
    cy.intercept("GET", "/api/node/threat_actor/?offset=0").as(
      "nodeThreatActor",
    );
    cy.intercept("GET", "/api/node/threat/?offset=0").as("nodeThreat");
    cy.intercept("GET", "/api/node/threat/type/?offset=0").as("nodeThreatType");
    cy.intercept("GET", "/api/user/?offset=0").as("user");
    cy.intercept("GET", "/api/event/*").as("event");

    // Wait for all of the intercepted calls to complete
    const intercepts = [
      "@eventPreventionTool",
      "@eventRemediation",
      "@eventSeverity",
      "@eventStatus",
      "@eventType",
      "@eventVector",
      "@nodeThreatActor",
      "@nodeThreat",
      "@nodeThreatType",
      "@user",
    ];

    // Click on the Actions dropdown
    cy.get('[aria-haspopup="true"]').eq(0).click();
    cy.get("span").contains("Edit Event").click();

    cy.wait(intercepts).then((interceptions) => {
      for (let i = 0; i < interceptions.length; i++) {
        cy.wrap(interceptions[i]).its("state").should("eq", "Complete");
      }
    });
    cy.get('[data-cy="event-name-field"] [data-cy="property-input-value"]')
      .click()
      .clear()
      .type("New Name");
    cy.get('[data-cy="save-edit-event-button"]').click();
    cy.wait("@updateEvent").its("state").should("eq", "Complete");
    cy.wait("@getEvent").its("state").should("eq", "Complete");
    cy.get('[data-cy="event-title"]').should("have.text", "New Name");
  });
});

describe("Event Summary Details", () => {
  let now;
  let nowString;

  before(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");

    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");

    now = new Date();
    nowString = now.toLocaleString("en-US", { timeZone: "UTC" }).slice(0, -9);
    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "small_template.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");
  });

  it("allows user to change and reset columns in details table", () => {
    // Open columns selector and select a new column
    cy.get(".p-multiselect-label").click();
    cy.get('[aria-label="Threat Actors"]').click();
    cy.get(".p-menubar").click(); // Click away from column selector
    cy.get(".p-multiselect-label").should(
      "contain.text",
      "Created, Name, Threat Actors, Threats, Severity, Status, Owner",
    );
    cy.get(".p-column-header-content > .p-column-title")
      .eq(0)
      .should("have.text", "Created");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(0)
      .should("contain.text", nowString);
    cy.get(".p-column-header-content > .p-column-title")
      .eq(1)
      .should("have.text", "Name");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(1)
      .should("have.text", "Test Event");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(2)
      .should("have.text", "Threat Actors");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(2)
      .should("contain.text", "None");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(3)
      .should("have.text", "Threats");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(3)
      .should("contain.text", "None");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(4)
      .should("have.text", "Severity");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(4)
      .should("have.text", "None");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(5)
      .should("have.text", "Status");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(5)
      .should("have.text", "OPEN");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(6)
      .should("have.text", "Owner");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(6)
      .should("have.text", "None");

    // Reset the columns and check they're back to the default
    cy.get('[data-cy="reset-table-button"]').click();
    cy.get(".p-column-header-content > .p-column-title")
      .eq(0)
      .should("have.text", "Created");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(0)
      .should("contain.text", nowString);
    cy.get(".p-column-header-content > .p-column-title")
      .eq(1)
      .should("have.text", "Name");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(1)
      .should("have.text", "Test Event");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(2)
      .should("have.text", "Threats");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(2)
      .should("contain.text", "None");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(3)
      .should("have.text", "Severity");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(3)
      .should("have.text", "None");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(4)
      .should("have.text", "Status");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(4)
      .should("have.text", "OPEN");
    cy.get(".p-column-header-content > .p-column-title")
      .eq(5)
      .should("have.text", "Owner");
    cy.get(".p-datatable-tbody > tr >  > :nth-child(2)")
      .eq(5)
      .should("have.text", "None");
  });
});

describe("URL Summary Details", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("POST", "/api/alert/observables").as("getObservables");

    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "smallWithUrls.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");

    // Switch to alert summary view
    cy.get('[aria-haspopup="true"]').eq(1).click();
    // Select first available analysis type
    cy.get("span").contains("URL Summary").click();

    cy.wait("@getObservables").its("state").should("eq", "Complete");
  });

  it("selects and highlights last clicked url observable", () => {
    // None highlighted to start
    cy.get(".p-listbox-item").eq(0).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(1).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(2).should("not.have.class", "p-highlight");

    // Click the first
    cy.get(".p-listbox-item").eq(0).click();
    cy.get(".p-listbox-item").eq(0).should("have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(1).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(2).should("not.have.class", "p-highlight");

    // Click the second
    cy.get(".p-listbox-item").eq(1).click();
    cy.get(".p-listbox-item").eq(0).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(1).should("have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(2).should("not.have.class", "p-highlight");

    // Click the third
    cy.get(".p-listbox-item").eq(2).click();
    cy.get(".p-listbox-item").eq(0).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(1).should("not.have.class", "p-highlight");
    cy.get(".p-listbox-item").eq(2).should("have.class", "p-highlight");
  });
});

describe("Observable Summary Details - Affect State", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("GET", "/api/event/*/summary/observable").as(
      "getObservableSummary",
    );

    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "smallWithUrls.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");

    // Switch to alert summary view
    cy.get('[aria-haspopup="true"]').eq(1).click();
    // Select first available analysis type
    cy.get("span").contains("Observable Summary").click();

    cy.wait("@getObservableSummary").its("state").should("eq", "Complete");
  });

  it("correctly updates observables for detection status when 'Save Detection Status' button clicked", () => {
    cy.intercept("PATCH", "/api/observable/*").as("updateObservable");
    // Select the first two observables and de-select the third (already checked)
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(0).click();
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(1).click();
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(2).click();

    // Click the save button
    cy.get("#save-detection-status-button").click();

    // 3 calls for each of the changed observables
    cy.wait("@updateObservable").its("state").should("eq", "Complete");
    cy.wait("@updateObservable").its("state").should("eq", "Complete");
    cy.wait("@updateObservable").its("state").should("eq", "Complete");

    // Call to update the table
    cy.wait("@getObservableSummary").its("state").should("eq", "Complete");

    // Check classes
    cy.get("tr").eq(0).should("not.have.class", "p-highlight");
    cy.get("tr").eq(1).should("not.have.class", "p-highlight");
    cy.get("tr").eq(2).should("have.class", "p-highlight");
    cy.get("tr").eq(3).should("have.class", "p-highlight");
    cy.get("tr").eq(4).should("not.have.class", "p-highlight");
    cy.get("tr").eq(5).should("not.have.class", "p-highlight");
    cy.get("tr").eq(6).should("not.have.class", "p-highlight");
    cy.get("tr").eq(7).should("not.have.class", "p-highlight");
    cy.get("tr").eq(8).should("not.have.class", "p-highlight");
    cy.get("tr").eq(9).should("not.have.class", "p-highlight");

    cy.get("tr").eq(0).should("not.have.class", "low-hits");
    cy.get("tr").eq(1).should("not.have.class", "low-hits");
    cy.get("tr").eq(2).should("not.have.class", "low-hits");
    cy.get("tr").eq(3).should("not.have.class", "low-hits");
    cy.get("tr").eq(4).should("not.have.class", "low-hits");
    cy.get("tr").eq(5).should("not.have.class", "low-hits");
    cy.get("tr").eq(6).should("have.class", "low-hits");
    cy.get("tr").eq(7).should("not.have.class", "low-hits");
    cy.get("tr").eq(8).should("have.class", "low-hits");
    cy.get("tr").eq(9).should("not.have.class", "low-hits");

    // Check checkboxes
    cy.get(".p-datatable-thead .p-checkbox .p-checkbox-box").should(
      "not.be.visible",
    ); // header checkbox should not be visible
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(0)
      .should("have.attr", "aria-checked", "true");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(1)
      .should("have.attr", "aria-checked", "true");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(2)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(3)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(4)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(5)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(6)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(7)
      .should("have.attr", "aria-checked", "false");
  });
});

describe("Observable Summary Details - Don't Affect State", () => {
  before(() => {
    cy.resetDatabase();
    cy.login();

    // Intercept the API call that loads the event data
    cy.intercept("GET", "/api/event/*").as("getEvent");
    cy.intercept(
      "GET",
      "/api/event/?sort=created_time%7Cdesc&limit=10&offset=0",
    ).as("getEventsDefaultRows");
    cy.intercept("GET", "/api/event/*/summary/observable").as(
      "getObservableSummary",
    );

    // Add the test event to the database
    cy.request({
      method: "POST",
      url: "/api/test/add_event",
      body: {
        alert_template: "smallWithUrls.json",
        alert_count: 1,
        name: "Test Event",
      },
    });

    visitUrl({
      url: "/manage_events",
      extraIntercepts: ["@getEventsDefaultRows"],
    });
    cy.get('[data-cy="eventName"] > a').click();
    cy.wait("@getEvent").its("state").should("eq", "Complete");

    // Switch to alert summary view
    cy.get('[aria-haspopup="true"]').eq(1).click();
    // Select first available analysis type
    cy.get("span").contains("Observable Summary").click();

    cy.wait("@getObservableSummary").its("state").should("eq", "Complete");
  });

  afterEach(() => {
    cy.get("#reset-selected-observables-button").click();
  });

  it("correctly selects observables with low hits when 'Select low hits' button clicked ", () => {
    cy.get("#select-low-hits-button").click();

    // Check classes
    cy.get("tr").eq(0).should("not.have.class", "p-highlight");
    cy.get("tr").eq(1).should("not.have.class", "p-highlight");
    cy.get("tr").eq(2).should("not.have.class", "p-highlight");
    cy.get("tr").eq(3).should("not.have.class", "p-highlight");
    cy.get("tr").eq(4).should("have.class", "p-highlight"); // This row will stay selected/highlighted
    cy.get("tr").eq(5).should("not.have.class", "p-highlight");
    cy.get("tr").eq(6).should("have.class", "p-highlight"); // Will have the highlighted class now that it is selected
    cy.get("tr").eq(7).should("not.have.class", "p-highlight");
    cy.get("tr").eq(8).should("have.class", "p-highlight"); // Will have the highlighted class now that it is selected
    cy.get("tr").eq(9).should("not.have.class", "p-highlight");

    cy.get("tr").eq(0).should("not.have.class", "low-hits");
    cy.get("tr").eq(1).should("not.have.class", "low-hits");
    cy.get("tr").eq(2).should("not.have.class", "low-hits");
    cy.get("tr").eq(3).should("not.have.class", "low-hits");
    cy.get("tr").eq(4).should("not.have.class", "low-hits");
    cy.get("tr").eq(5).should("not.have.class", "low-hits");
    cy.get("tr").eq(6).should("have.class", "low-hits");
    cy.get("tr").eq(7).should("not.have.class", "low-hits");
    cy.get("tr").eq(8).should("have.class", "low-hits");
    cy.get("tr").eq(9).should("not.have.class", "low-hits");

    // Check checkboxes
    cy.get(".p-datatable-thead .p-checkbox .p-checkbox-box").should(
      "not.be.visible",
    ); // header checkbox should not be visible
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(0)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(1)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(2)
      .should("have.attr", "aria-checked", "true"); // This observable is enabled and will stay checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(3)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(4)
      .should("have.attr", "aria-checked", "true");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(5)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(6)
      .should("have.attr", "aria-checked", "true"); // This observable will now be checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(7)
      .should("have.attr", "aria-checked", "false");

    // Reset newly selected checkbox
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(5).click();
  });

  it("correctly resets selected observables when 'Reset' button clicked", () => {
    // Click a couple of other rows
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(1).click();
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box").eq(5).click();

    // Check classes
    cy.get("tr").eq(0).should("not.have.class", "p-highlight");
    cy.get("tr").eq(1).should("not.have.class", "p-highlight");
    cy.get("tr").eq(2).should("not.have.class", "p-highlight");
    cy.get("tr").eq(3).should("have.class", "p-highlight"); // Will have the highlighted class now that it is selected
    cy.get("tr").eq(4).should("have.class", "p-highlight"); // This row will stay selected/highlighted
    cy.get("tr").eq(5).should("not.have.class", "p-highlight");
    cy.get("tr").eq(6).should("not.have.class", "p-highlight");
    cy.get("tr").eq(7).should("have.class", "p-highlight"); // Will have the highlighted class now that it is selected
    cy.get("tr").eq(8).should("not.have.class", "p-highlight");
    cy.get("tr").eq(9).should("not.have.class", "p-highlight");

    cy.get("tr").eq(0).should("not.have.class", "low-hits");
    cy.get("tr").eq(1).should("not.have.class", "low-hits");
    cy.get("tr").eq(2).should("not.have.class", "low-hits");
    cy.get("tr").eq(3).should("not.have.class", "low-hits");
    cy.get("tr").eq(4).should("not.have.class", "low-hits");
    cy.get("tr").eq(5).should("not.have.class", "low-hits");
    cy.get("tr").eq(6).should("have.class", "low-hits");
    cy.get("tr").eq(7).should("not.have.class", "low-hits");
    cy.get("tr").eq(8).should("have.class", "low-hits");
    cy.get("tr").eq(9).should("not.have.class", "low-hits");

    // Check checkboxes
    cy.get(".p-datatable-thead .p-checkbox .p-checkbox-box").should(
      "not.be.visible",
    ); // header checkbox should not be visible
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(0)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(1)
      .should("have.attr", "aria-checked", "true"); // This observable will now be checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(2)
      .should("have.attr", "aria-checked", "true"); // This observable is enabled and will stay checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(3)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(4)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(5)
      .should("have.attr", "aria-checked", "true"); // This observable will now be checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(6)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(7)
      .should("have.attr", "aria-checked", "false");

    cy.get("#reset-selected-observables-button").click();

    // Check again, should be back to default
    cy.get("tr").eq(0).should("not.have.class", "p-highlight");
    cy.get("tr").eq(1).should("not.have.class", "p-highlight");
    cy.get("tr").eq(2).should("not.have.class", "p-highlight");
    cy.get("tr").eq(3).should("not.have.class", "p-highlight");
    cy.get("tr").eq(4).should("have.class", "p-highlight");
    cy.get("tr").eq(5).should("not.have.class", "p-highlight");
    cy.get("tr").eq(6).should("not.have.class", "p-highlight");
    cy.get("tr").eq(7).should("not.have.class", "p-highlight");
    cy.get("tr").eq(8).should("not.have.class", "p-highlight");
    cy.get("tr").eq(9).should("not.have.class", "p-highlight");

    cy.get("tr").eq(0).should("not.have.class", "low-hits");
    cy.get("tr").eq(1).should("not.have.class", "low-hits");
    cy.get("tr").eq(2).should("not.have.class", "low-hits");
    cy.get("tr").eq(3).should("not.have.class", "low-hits");
    cy.get("tr").eq(4).should("not.have.class", "low-hits");
    cy.get("tr").eq(5).should("not.have.class", "low-hits");
    cy.get("tr").eq(6).should("have.class", "low-hits");
    cy.get("tr").eq(7).should("not.have.class", "low-hits");
    cy.get("tr").eq(8).should("have.class", "low-hits");
    cy.get("tr").eq(9).should("not.have.class", "low-hits");

    // Check checkboxes
    cy.get(".p-datatable-thead .p-checkbox .p-checkbox-box").should(
      "not.be.visible",
    ); // header checkbox should not be visible
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(0)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(1)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(2)
      .should("have.attr", "aria-checked", "true"); // This observable is enabled and should be pre-checked
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(3)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(4)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(5)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(6)
      .should("have.attr", "aria-checked", "false");
    cy.get(".p-selection-column > .p-checkbox > .p-checkbox-box")
      .eq(7)
      .should("have.attr", "aria-checked", "false");
  });

  it("correctly hides and shows rows with high FAQueue Hits when toggle button clicked", () => {
    cy.get("#toggle-max-hits-button").should("have.text", "Hide Max Hits");
    cy.get("#toggle-max-hits-button > .pi").should(
      "have.class",
      "pi-eye-slash",
    );
    cy.get("#toggle-max-hits-button").click();
    // Should only be 9 rows now, 1 will have been hidden
    cy.get("tr").should("have.length", 9);
    cy.get("#toggle-max-hits-button").should("have.text", "Show Max Hits");
    cy.get("#toggle-max-hits-button > .pi").should("have.class", "pi-eye");
    cy.get('[data-cy="faqueue-hits-count"]')
      .contains("1000")
      .should("not.exist");
    cy.get(".p-datatable-tbody > > :nth-child(3)")
      .contains("ipv4")
      .should("not.exist");
    cy.get(".p-datatable-tbody > > :nth-child(4)")
      .contains("127.0.0.1")
      .should("not.exist");
    cy.get("#toggle-max-hits-button").click();
    cy.get("tr").should("have.length", 10);
    cy.get("#toggle-max-hits-button").should("have.text", "Hide Max Hits");
    cy.get("#toggle-max-hits-button > .pi").should(
      "have.class",
      "pi-eye-slash",
    );
    cy.get('[data-cy="faqueue-hits-count"]')
      .contains("1000")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(3)")
      .contains("ipv4")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(4)")
      .contains("127.0.0.1")
      .should("be.visible");
  });

  it("correctly filters by observable type when selected", () => {
    cy.get('[data-cy="observable-type-filter-multiselect"]').click();
    cy.get('[aria-label="email_address"]').click();
    // Should only be 3 rows now, 2 headers and 1 email_address observable
    cy.get("tr").should("have.length", 3);
    cy.get('[data-cy="faqueue-hits-count"]').contains("5").should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(3)")
      .contains("email_address")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(4)")
      .contains("badguy@evil.com")
      .should("be.visible");
    // Click to add another observable type filter and remove the old, this one will have no results
    cy.get('[aria-label="email_address"]').click();
    cy.get('[aria-label="file"]').click();
    cy.get("tr").should("have.length", 3);
    cy.get("td").contains("No observables found.").should("be.visible");
    // Click the remove filter button, all rows should be visible again
    cy.get(".p-column-filter-clear-button").eq(2).click();
    cy.get("tr").should("have.length", 10);
  });

  it("correctly filters by observable value when typing", () => {
    cy.get('[data-cy="observable-value-filter-input"]').click().type("He");
    // Should only be 3 rows now, 2 headers and 3 "H" observable
    cy.get("tr").should("have.length", 3);
    cy.get('[data-cy="faqueue-hits-count"]')
      .contains("100")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(3)")
      .contains("email_subject")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(4)")
      .contains("Hello")
      .should("be.visible");
    // Click the remove filter button, all rows should be visible again
    cy.get(".p-column-filter-clear-button").eq(3).click();
    cy.get("tr").should("have.length", 10);
  });

  it("correctly sorts by observable value when typing", () => {
    cy.get('[data-cy="observable-value-filter-input"]').click().type("He");
    // Should only be 3 rows now, 2 headers and 3 "H" observable
    cy.get("tr").should("have.length", 3);
    cy.get('[data-cy="faqueue-hits-count"]')
      .contains("100")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(3)")
      .contains("email_subject")
      .should("be.visible");
    cy.get(".p-datatable-tbody > > :nth-child(4)")
      .contains("Hello")
      .should("be.visible");
    // Click the remove filter button, all rows should be visible again
    cy.get(".p-column-filter-clear-button").eq(3).click();
    cy.get("tr").should("have.length", 10);
  });
});
