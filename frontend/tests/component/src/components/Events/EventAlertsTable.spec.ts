// Example Cypress Vue component test that we might use one day

import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import router from "@/router";

import { createCustomCypressPinia } from "@tests/cypressHelpers";
import EventAlertsTable from "@/components/Events/EventAlertsTable.vue";
import { Alert } from "@/services/api/alert";
import { alertReadFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";
import { testConfiguration } from "@/etc/configuration/test";

const mockAlertA = alertReadFactory({ uuid: "uuid1", name: "Test Alert A" });
const mockAlertB = alertReadFactory({ uuid: "uuid2", name: "Test Alert B" });
const mockAlertC = alertReadFactory({ uuid: "uuid3", name: "Test Alert C" });

function factory(args: { selected: string[] } = { selected: [] }) {
  return mount(EventAlertsTable, {
    global: {
      plugins: [
        router,
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
            selectedAlertStore: {
              selected: args.selected,
            },
          },
        }),
      ],
      provide: { objectType: "events", config: testConfiguration },
    },
    propsData: {
      eventUuid: "uuid1",
    },
  });
}

describe("EventAlertsTable", () => {
  it("renders correctly when call to fetch alerts fails", () => {
    cy.stub(Alert, "readAllPages")
      .as("fetchUserSummary")
      .rejects(new Error("Request failed with status code 404"));
    factory();
    cy.contains(
      "No alerts for this event were found. Request failed with status code 404",
    ).should("be.visible");
  });
  it("renders correctly when call to fetch alerts is successful but empty", () => {
    cy.stub(Alert, "readAllPages")
      .withArgs("uuid")
      .as("fetchUserSummary")
      .resolves([]);
    factory();
    cy.contains("No alerts for this event were found.").should("be.visible");
  });
  it("renders correctly when call to fetch alerts is successful and has results", () => {
    cy.stub(Alert, "readAllPages").returns([
      mockAlertA,
      mockAlertB,
      mockAlertC,
    ]);
    const columnValues = [
      { value: "", header: "" }, // Checkbox column
      { value: "2/24/2022, 12:00:00 AM UTC", header: "Event Time (UTC)" },
      { value: "Test Alert A", header: "Name" },
      { value: "None", header: "Owner" },
      { value: "OPEN", header: "Disposition" },
    ];
    factory();
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", columnValues[index].header);
      });
    cy.get("tr")
      .eq(1)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", columnValues[index].value);
      });
  });
  it("will attempt to remove selecteed alerts and reload the table when 'Remove Alerts' clicked", () => {
    let readAllCalled = false;
    function mockReadAll() {
      const res = readAllCalled
        ? [mockAlertB, mockAlertC]
        : [mockAlertA, mockAlertB, mockAlertC];
      readAllCalled = true;
      return res;
    }

    cy.stub(Alert, "readAllPages").as("readAllStub").callsFake(mockReadAll);
    cy.stub(Alert, "update")
      .withArgs([
        { uuid: "uuid1", eventUuid: null, historyUsername: "analyst" },
      ])
      .as("updateStub")
      .returns("Success");

    factory({ selected: ["uuid1"] });

    // Click to remove the first alert
    cy.get("tr").eq(1).children().eq(0).findByRole("checkbox").click();
    cy.contains("Remove Alerts").click();
    cy.get("@readAllStub").should("have.been.calledTwice");
    cy.get("@updateStub").should("have.been.called");

    // Should have reloaded and is now not showing alert a
    cy.contains("Test Alert A").should("not.exist");
  });
  it("will show an error message if a request to remove alerts fails", () => {
    let readAllCalled = false;
    function mockReadAll() {
      const res = readAllCalled
        ? [mockAlertB, mockAlertC]
        : [mockAlertA, mockAlertB, mockAlertC];
      readAllCalled = true;
      return res;
    }

    cy.stub(Alert, "readAllPages").as("readAllStub").callsFake(mockReadAll);
    cy.stub(Alert, "update")
      .withArgs([
        { uuid: "uuid1", eventUuid: null, historyUsername: "analyst" },
      ])
      .as("updateStub")
      .rejects(new Error("404 Request failed"));

    factory({ selected: ["uuid1"] });

    // Click to remove the first alert
    cy.get("tr").eq(1).children().eq(0).findByRole("checkbox").click();
    cy.contains("Remove Alerts").click();
    cy.get("@readAllStub").should("have.been.calledOnce");
    cy.get("@updateStub").should("have.been.calledOnce");

    // Should have reloaded and is now not showing alert a
    cy.contains("Could not remove alerts: 404 Request failed").should(
      "be.visible",
    );
  });
});
