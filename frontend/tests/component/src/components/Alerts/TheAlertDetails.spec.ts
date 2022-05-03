import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";

import TheAlertDetails from "@/components/Alerts/TheAlertDetails.vue";
import router from "@/router/index";
import { alertReadFactory } from "@mocks/alert";
import { alertRead } from "@/models/alert";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { NodeTree } from "@/services/api/nodeTree";
import { observableReadFactory } from "@mocks/observable";

function factory(initialAlertStoreState: {
  open: null | alertRead;
  requestReload: boolean;
}) {
  return mount(TheAlertDetails, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: { alertStore: initialAlertStoreState },
        }),
        router,
      ],
    },
  });
}

describe("TheAlertDetails", () => {
  it("renders correctly when there is not an open alert", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree").as("getObservables").resolves([]);
    factory({
      open: null,
      requestReload: false,
    });
    cy.get("@getObservables").should("not.have.been.called");
    cy.contains("Test Alert").should("not.exist");
  });
  it("renders correctly when there is an open alert that has no observables with detection points", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(["testAlertUuid"], "observable")
      .as("getObservables")
      .resolves([]);
    factory({
      open: alertReadFactory({
        tags: [genericObjectReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.get("@getObservables").should("have.been.calledOnce");

    cy.contains("Test Alert").should("be.visible");
    cy.get("button .pi-link").should("be.visible");
    cy.get("tr").should("have.length", 11);
    cy.contains("Insert Time")
      .siblings()
      .should("have.text", "3/24/2022, 12:00:00 AM");
    cy.contains("Event Time")
      .siblings()
      .should("have.text", "3/24/2022, 12:00:00 AM");
    cy.contains("Tool").siblings().should("have.text", "testAlertTool");
    cy.contains("Tool Instance")
      .siblings()
      .should("have.text", "testAlertToolInstance");
    cy.contains("Type").siblings().should("have.text", "testAlertType");
    cy.contains("Disposition").siblings().should("have.text", "OPEN");
    cy.get("td:contains(Event)").eq(1).siblings().should("have.text", "None");
    cy.contains("Queue").siblings().should("have.text", "testAlertQueue");
    cy.contains("Owner").siblings().should("have.text", "None");
    cy.contains("Comments").siblings().should("have.text", "None");
    cy.contains("No detections found").should("be.visible");
  });
  it("renders correctly when there is an open alert that does have observables with detection points", () => {
    const detectionPointA = {
      insertTime: new Date(),
      nodeUuid: "nodeUuidB",
      uuid: "uuidB",
      value: "detectionA",
    };
    const detectionPointB = {
      insertTime: new Date(),
      nodeUuid: "nodeUuidB",
      uuid: "uuidB",
      value: "detectionB",
    };
    const detectionPointC = {
      insertTime: new Date(),
      nodeUuid: "nodeUuidC",
      uuid: "uuidC",
      value: "detectionC",
    };

    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(["testAlertUuid"], "observable")
      .as("getObservables")
      .resolves([
        observableReadFactory({
          detectionPoints: [detectionPointC],
        }),
        observableReadFactory({
          detectionPoints: [detectionPointB, detectionPointA],
        }),
      ]);
    factory({
      open: alertReadFactory({
        tags: [genericObjectReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.get("@getObservables").should("have.been.calledOnce");

    cy.findAllByText("Detection").should("have.length", 3);
    cy.findAllByText("Detection")
      .eq(0)
      .siblings()
      .should("have.text", "detectionC");
    cy.findAllByText("Detection");
    cy.findAllByText("Detection")
      .eq(1)
      .siblings()
      .should("have.text", "detectionB");
    cy.findAllByText("Detection")
      .eq(2)
      .siblings()
      .should("have.text", "detectionA");
  });
  it("displays error if request to fetch observables fails", () => {
    cy.stub(NodeTree, "readNodesOfNodeTree")
      .withArgs(["testAlertUuid"], "observable")
      .as("getObservables")
      .rejects(new Error("404 request failed"));
    factory({
      open: alertReadFactory({
        tags: [genericObjectReadFactory({ value: "TestTag" })],
      }),
      requestReload: false,
    });

    cy.get("@getObservables").should("have.been.calledOnce");

    cy.get("[data-cy=error-message]")
      .should("be.visible")
      .should("have.text", "404 request failed");
    cy.contains("No detections found").should("be.visible");
  });
});
