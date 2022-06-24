export function visitUrl(options) {
  // Persist the cookies for the duration of the test
  Cypress.Cookies.preserveOnce("access_token", "refresh_token");

  // Intercept the auth refresh call
  cy.intercept("GET", "/api/auth/refresh").as("authRefresh");

  // Intercept the call that fetches the event
  // cy.intercept("GET", "/api/event/*").as("getEvent");

  // Intercept all of the populateCommonStores API calls
  cy.intercept("GET", "/api/alert/disposition/?offset=0").as(
    "alertDisposition",
  );
  cy.intercept("GET", "/api/alert/tool/?offset=0").as("alertTool");
  cy.intercept("GET", "/api/alert/tool/instance/?offset=0").as(
    "alertToolInstance",
  );
  cy.intercept("GET", "/api/alert/type/?offset=0").as("alertType");
  cy.intercept("GET", "/api/event/prevention_tool/?offset=0").as(
    "eventPreventionTool",
  );
  cy.intercept("GET", "/api/event/severity/?offset=0").as("eventSeverity");
  cy.intercept("GET", "/api/event/status/?offset=0").as("eventStatus");
  cy.intercept("GET", "/api/event/type/?offset=0").as("eventType");
  cy.intercept("GET", "/api/event/vector/?offset=0").as("eventVector");
  cy.intercept("GET", "/api/metadata/directive/?offset=0").as(
    "metadataDirective",
  );
  cy.intercept("GET", "/api/observable/type/?offset=0").as("observableType");
  cy.intercept("GET", "/api/queue/?offset=0").as("queue");
  cy.intercept("GET", "/api/user/?offset=0").as("user");

  // Visit the intended URL
  cy.visit(options.url);

  // Wait for all of the intercepted calls to complete
  const intercepts = [
    "@authRefresh",
    // "@getEvent",
    "@alertDisposition",
    "@alertTool",
    "@alertToolInstance",
    "@alertType",
    "@eventPreventionTool",
    "@eventSeverity",
    "@eventStatus",
    "@eventType",
    "@eventVector",
    "@metadataDirective",
    "@observableType",
    "@queue",
    "@user",
  ];

  // Also wait for any extra intercepts that were passed in
  if (options.extraIntercepts) {
    intercepts.push.apply(intercepts, options.extraIntercepts);
  }

  cy.wait(intercepts).then((interceptions) => {
    for (let i = 0; i < interceptions.length; i++) {
      cy.wrap(interceptions[i]).its("state").should("eq", "Complete");
    }
  });
}

export function openEditEventModal(eventNum = 0) {
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
  cy.intercept("GET", "/api/node/threat_actor/?offset=0").as("threatActor");
  cy.intercept("GET", "/api/node/threat/?offset=0").as("threat");
  cy.intercept("GET", "/api/node/threat/type/?offset=0").as("threatType");
  cy.intercept("GET", "/api/user/?offset=0").as("user");
  cy.intercept("GET", "/api/event/*").as("event");

  // Open the Edit Event modal
  cy.get("[data-cy=edit-event-button]").eq(eventNum).click();

  // Wait for all of the intercepted calls to complete
  const intercepts = [
    "@eventPreventionTool",
    "@eventRemediation",
    "@eventSeverity",
    "@eventStatus",
    "@eventType",
    "@eventVector",
    "@threatActor",
    "@threat",
    "@threatType",
    "@user",
  ];

  cy.wait(intercepts).then((interceptions) => {
    for (let i = 0; i < interceptions.length; i++) {
      cy.wrap(interceptions[i]).its("state").should("eq", "Complete");
    }
  });
}
