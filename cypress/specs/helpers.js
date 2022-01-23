export function visitUrl(url) {
  // Persist the cookies for the duration of the test
  Cypress.Cookies.preserveOnce("access_token", "refresh_token");

  // Intercept the auth refresh call
  cy.intercept("GET", "/api/auth/refresh").as("authRefresh");

  // Intercept all of the populateCommonStores API calls
  cy.intercept("GET", "/api/alert/disposition/?offset=0").as(
    "alertDisposition"
  );
  cy.intercept("GET", "/api/alert/queue/?offset=0").as("alertQueue");
  cy.intercept("GET", "/api/alert/tool/?offset=0").as("alertTool");
  cy.intercept("GET", "/api/alert/tool/instance/?offset=0").as(
    "alertToolInstance"
  );
  cy.intercept("GET", "/api/alert/type/?offset=0").as("alertType");
  cy.intercept("GET", "/api/event/prevention_tool/?offset=0").as(
    "eventPreventionTool"
  );
  cy.intercept("GET", "/api/event/queue/?offset=0").as("eventQueue");
  cy.intercept("GET", "/api/event/risk_level/?offset=0").as("eventRiskLevel");
  cy.intercept("GET", "/api/event/status/?offset=0").as("eventStatus");
  cy.intercept("GET", "/api/event/type/?offset=0").as("eventType");
  cy.intercept("GET", "/api/event/vector/?offset=0").as("eventVector");
  cy.intercept("GET", "/api/node/directive/?offset=0").as("nodeDirective");
  cy.intercept("GET", "/api/observable/type/?offset=0").as("observableType");
  cy.intercept("GET", "/api/user/?offset=0").as("user");

  // Visit the intended URL
  cy.visit(url);

  // Wait for all of the intercepted calls to complete
  cy.wait([
    "@authRefresh",
    "@alertDisposition",
    "@alertQueue",
    "@alertTool",
    "@alertToolInstance",
    "@alertType",
    "@eventPreventionTool",
    "@eventQueue",
    "@eventRiskLevel",
    "@eventStatus",
    "@eventType",
    "@eventVector",
    "@nodeDirective",
    "@observableType",
    "@user",
  ]).then((interceptions) => {
    for (let i = 0; i < interceptions.length; i++) {
      cy.wrap(interceptions[i]).its("state").should("eq", "Complete");
    }
  });
}
