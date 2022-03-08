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

  it("View Event page renders", () => {
    cy.get('[data-cy="event-details-menu"]').should("be.visible");
    cy.get('[aria-haspopup="true"]').eq(0).should("have.text", "Actions");
    cy.get('[aria-haspopup="true"]').eq(1).should("have.text", "Information");
    cy.get('[aria-haspopup="true"]').eq(2).should("have.text", "Analysis");
    cy.get('[data-cy="event-details-card"]').should("be.visible");
    cy.get('[data-cy="event-details-header"]').should("be.visible");
    cy.get('[data-cy="event-title"]').should("have.text", "Test Event");
    cy.get('[data-cy="event-details-link"]').should("be.visible");
    cy.get('[data-cy="event-details-content"]').should("be.visible");
    cy.get("#event-section-title").should("contain.text", "Event Summary");
  });

  it("Switches the component / details section when selected from dropdown", () => {
    // Click on the Analysis dropdown
    cy.get('[aria-haspopup="true"]').eq(2).click();
    // Select first available analysis type
    cy.get("span").contains("a_type0 Analysis").click();
    // Check that basic analysis showed up
    cy.get('[data-cy="event-details-content"]')
      .contains("Basic Analysis")
      .should("be.visible");
    cy.get('[data-cy="event-details-content"]')
      .contains("a_type0 Analysis")
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

  // Have to log out and manually leave event page
  // BC when database resets it will try to get the old event with old uuid
  // And will cause an error
  afterEach(() => {
    cy.logout();
    cy.visit("/login");
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
    cy.intercept("POST", "/api/node/tag/").as("addTag");

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
    cy.intercept("GET", "/api/event/risk_level/?offset=0").as("eventRiskLevel");
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
      "@eventRiskLevel",
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

  it("renders main elements correctly", () => {
    cy.get("#event-summary-timeline").should("be.visible");
    cy.get("#event-summary-table").should("be.visible");
    cy.get("#event-section-title").should("contain.text", "Event Summary");
  });
  it("renders timeline correctly", () => {
    cy.get("#event-summary-timeline").should("be.visible");
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(0)
      .should("have.text", "Event");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(0)
      .should("contains.text", nowString);
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(1)
      .should("have.text", "Alert");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(1)
      .should("contains.text", nowString);
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(2)
      .should("have.text", "Ownership");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(2)
      .should("have.text", "TBD");
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(3)
      .should("have.text", "Disposition");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(3)
      .should("have.text", "TBD");
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(4)
      .should("have.text", "Contain");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(4)
      .should("have.text", "TBD");
    cy.get('[data-cy="event-summary-timeline-label"]')
      .eq(5)
      .should("have.text", "Remediation");
    cy.get('[data-cy="event-summary-timeline-datetime"]')
      .eq(5)
      .should("have.text", "TBD");
  });
  it("renders table correctly", () => {
    cy.get("#event-summary-table").should("be.visible");
    cy.get('[data-cy="table-column-select"]').should("be.visible");
    cy.get(".p-multiselect-label").should(
      "contain.text",
      "Created, Name, Threats, Risk Level, Status, Owner",
    );
    cy.get('[data-cy="reset-table-button"]').should("be.visible");
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
      .should("have.text", "Risk Level");
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
  it("allows user to change and reset columns in details table", () => {
    // Open columns selector and select a new column
    cy.get(".p-multiselect-label").click();
    cy.get('[aria-label="Threat Actors"]').click();
    cy.get(".p-menubar").click(); // Click away from column selector
    cy.get(".p-multiselect-label").should(
      "contain.text",
      "Created, Name, Threat Actors, Threats, Risk Level, Status, Owner",
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
      .should("have.text", "Risk Level");
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
      .should("have.text", "Risk Level");
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
