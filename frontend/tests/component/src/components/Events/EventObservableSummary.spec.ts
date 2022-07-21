import { mount } from "@cypress/vue";

import PrimeVue from "primevue/config";

import { testConfiguration } from "@/etc/configuration/test/index";
import EventObservableSummary from "@/components/Events/EventObservableSummary.vue";
import router from "@/router/index";
import { Event } from "@/services/api/event";
import { observableSummary } from "@/models/eventSummaries";
import { observableInAlertReadFactory } from "@mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
import { ObservableInstance } from "@/services/api/observable";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { metadataTagReadFactory } from "@mocks/metadata";

const props = {
  eventUuid: "uuid",
};

function factory() {
  return mount(EventObservableSummary, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
          },
        }),
        router,
      ],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("EventObservableSummary", () => {
  const resultA: observableSummary = {
    faqueueHits: 10000,
    faqueueLink: "testlink",
    ...observableInAlertReadFactory({ uuid: "ObservableA", value: "HighHits" }),
  };
  const resultB: observableSummary = {
    faqueueHits: 100,
    faqueueLink: "testlink",
    ...observableInAlertReadFactory({
      uuid: "ObservableB",
      forDetection: true,
      value: "MediumHits",
      tags: [metadataTagReadFactory({ value: "TestTag" })],
    }),
  };
  const resultC: observableSummary = {
    faqueueHits: 1,
    faqueueLink: "testlink",
    ...observableInAlertReadFactory({
      uuid: "ObservableC",
      value: "LowHits",
      observableRelationships: [
        {
          relatedObservable: observableInAlertReadFactory({
            value: "RelatedObservable",
          }),
          observableUuid: "observableUuid",
          uuid: "uuid",
          type: genericObjectReadFactory({ value: "TestRelationship" }),
        },
      ],
    }),
  };
  const observableSummaryResults: observableSummary[] = [
    resultA,
    resultB,
    resultC,
  ];

  it("renders correctly when request to fetch data fails", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .rejects(new Error("404 Request failed"));
    factory();
    cy.get("[data-cy=error-banner]").should("be.visible");
    cy.contains(
      "Could not fetch observable summary data: 404 Request failed",
    ).should("be.visible");
    cy.findByRole("table").should("be.visible");
    cy.contains("No observables found");
  });
  it("renders correctly when request to update observable status fails", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .returns(observableSummaryResults);
    cy.stub(ObservableInstance, "update").rejects(
      new Error("404 Request failed"),
    );
    factory();

    // Switch checked statuses
    cy.findAllByRole("checkbox").each(($el) => cy.wrap($el).click());
    // Save status
    cy.contains("Save Detection Status").click();
    cy.get("[data-cy=error-banner]").should("be.visible");
    cy.contains("Could not update observables: 404 Request failed").should(
      "be.visible",
    );
  });
  it("renders correctly when request successfully returns empty", () => {
    cy.stub(Event, "readObservableSummary").withArgs("uuid").returns([]);
    factory();
    cy.get("[data-cy=error-banner]").should("not.exist");
    cy.findByRole("table").should("be.visible");
    cy.contains("No observables found");
  });
  it("renders correctly when request successfully returns results", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .returns(observableSummaryResults);

    const observableSummaryCols = [
      "For Detection",
      "FAQueue Hits",
      "Type",
      "Value",
      "Relationships",
      "Tags",
    ];
    factory();
    cy.get("[data-cy=error-banner]").should("not.exist");
    cy.findByRole("table").should("be.visible");

    // Check table content
    cy.get("tr").should("have.length", 5);
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("contain.text", observableSummaryCols[index]);
      });
    cy.get("tr")
      .eq(2)
      .children()
      .should("not.have.class", "low-hits")
      .each(($li, index) => {
        if (index === 0) {
          cy.wrap($li)
            .findAllByRole("checkbox")
            .invoke("attr", "aria-checked")
            .should("equal", "false");
        } else if (index === 1) {
          cy.wrap($li).contains(resultA.faqueueHits);
          cy.wrap($li)
            .find("a")
            .invoke("attr", "href")
            .should("equal", resultA.faqueueLink);
        } else if (index === 2) {
          cy.wrap($li).contains(resultA.type.value);
        } else if (index === 3) {
          cy.wrap($li).contains(resultA.value);
        } else if (index === 4) {
          cy.wrap($li).children().should("have.length", 0);
        } else if (index === 5) {
          cy.wrap($li).children().should("have.length", 0);
        }
      });
    cy.get("tr")
      .eq(3)
      .children()
      .should("not.have.class", "low-hits")
      .each(($li, index) => {
        if (index === 0) {
          cy.wrap($li)
            .findAllByRole("checkbox")
            .invoke("attr", "aria-checked")
            .should("equal", "true");
        } else if (index === 1) {
          cy.wrap($li).contains(resultB.faqueueHits);
          cy.wrap($li)
            .find("a")
            .invoke("attr", "href")
            .should("equal", resultB.faqueueLink);
        } else if (index === 2) {
          cy.wrap($li).contains(resultB.type.value);
        } else if (index === 3) {
          cy.wrap($li).contains(resultB.value);
        } else if (index === 4) {
          cy.wrap($li).children().should("have.length", 0);
        } else if (index === 5) {
          cy.wrap($li).contains("TestTag");
        }
      });
    cy.get("tr")
      .eq(4)
      .should("have.class", "low-hits")
      .children()
      .each(($li, index) => {
        if (index === 0) {
          cy.wrap($li)
            .findAllByRole("checkbox")
            .invoke("attr", "aria-checked")
            .should("equal", "false");
        } else if (index === 1) {
          cy.wrap($li).contains(resultC.faqueueHits);
          cy.wrap($li)
            .find("a")
            .invoke("attr", "href")
            .should("equal", resultC.faqueueLink);
        } else if (index === 2) {
          cy.wrap($li).contains(resultC.type.value);
        } else if (index === 3) {
          cy.wrap($li).contains(resultC.value);
        } else if (index === 4) {
          cy.wrap($li).contains("TestRelationship: RelatedObservable");
        } else if (index === 5) {
          cy.wrap($li).children().should("have.length", 0);
        }
      });
  });
  it("correctly selects low hits and resets", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .returns(observableSummaryResults);

    factory();

    // Click low hits
    cy.contains("Select low hits").click();

    // Check that only low hit observable and originally selected are now checked
    cy.get("tr")
      .eq(2)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "false");
    cy.get("tr")
      .eq(3)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "true");
    cy.get("tr")
      .eq(4)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "true");

    // Click the reset
    cy.contains("Reset").click();

    // Check that now only the originally selected is checked again
    cy.get("tr")
      .eq(2)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "false");
    cy.get("tr")
      .eq(3)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "true");
    cy.get("tr")
      .eq(4)
      .children()
      .eq(0)
      .findAllByRole("checkbox")
      .invoke("attr", "aria-checked")
      .should("equal", "false");
  });
  it("correctly toggles max hits", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .returns(observableSummaryResults);

    factory();
    // Click max hits toggle
    cy.contains("Hide Max Hits").click();
    // Check that there is one less row
    cy.get("tr").should("have.length", 4);
    // And that the high hits row is the one missing
    cy.contains("HighHits").should("not.exist");

    // Click max hits toggle again
    cy.contains("Show Max Hits").click();
    // Check that there is the right number of rows again
    cy.get("tr").should("have.length", 5);
    // And that the button text switched back
    cy.contains("Hide Max Hits");
  });
  it("correctly updates detection status and reloads", () => {
    cy.stub(Event, "readObservableSummary")
      .withArgs("uuid")
      .as("readObservableSummary")
      .returns(observableSummaryResults);

    const updateStub = cy.stub(ObservableInstance, "update");
    updateStub
      .withArgs("ObservableA", {
        forDetection: true,
        historyUsername: "analyst",
      })
      .as("updateObservableA")
      .resolves();

    updateStub
      .withArgs("ObservableB", {
        forDetection: false,
        historyUsername: "analyst",
      })
      .as("updateObservableB")
      .resolves();

    updateStub
      .withArgs("ObservableC", {
        forDetection: true,
        historyUsername: "analyst",
      })
      .as("updateObservableC")
      .resolves();

    factory();

    // Switch checked statuses
    cy.findAllByRole("checkbox").each(($el) => cy.wrap($el).click());

    // Save status
    cy.contains("Save Detection Status").click();

    // Verify that calls were all made
    cy.get("@updateObservableA").should("have.been.calledOnce");
    cy.get("@updateObservableB").should("have.been.calledOnce");
    cy.get("@updateObservableC").should("have.been.calledOnce");
    cy.get("@readObservableSummary").should("have.been.calledTwice");

    // NOTE: The stub is still returning the initial observables before update, so not checking if the checkboxes changed
    // Verifying that the second call was made is good enough
  });
});
