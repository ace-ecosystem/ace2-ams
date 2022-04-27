import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import NodeQueueSelector from "@/components/Node/NodeQueueSelector.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";

function factory(
  args: { props: { nodeQueue: "alerts" | "events" }; initialState: any } = {
    props: { nodeQueue: "alerts" },
    initialState: {},
  },
) {
  return mount(NodeQueueSelector, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: args.initialState,
        }),
      ],
    },
    propsData: args.props,
  });
}

describe("NodeQueueSelector", () => {
  const externalQueue = genericObjectReadFactory({ value: "external" });
  const internalQueue = genericObjectReadFactory({ value: "internal" });

  it("renders correctly when there is no current queue set or any available", () => {
    factory();
    cy.contains("Queue").should("be.visible");
    cy.get("#queue-dropdown").click();
    cy.contains("No available options").should("be.visible");
  });
  it("renders correctly when there a queue currently set", () => {
    factory({
      props: { nodeQueue: "alerts" },
      initialState: {
        currentUserSettingsStore: {
          queues: { alerts: externalQueue, events: internalQueue },
        },
        queueStore: { items: [externalQueue, internalQueue] },
      },
    });
    cy.get("#queue-dropdown").should("have.text", "external");
    cy.get("#queue-dropdown").click();
    cy.contains("external").should("be.visible");
    cy.contains("internal").should("be.visible");
  });
  it("will update alert filter for given queue when a different is selected", () => {
    factory({
      props: { nodeQueue: "alerts" },
      initialState: {
        currentUserSettingsStore: {
          queues: { alerts: externalQueue, events: internalQueue },
        },
        queueStore: { items: [externalQueue, internalQueue] },
      },
    });
    cy.contains("external").should("be.visible");
    cy.get("#queue-dropdown").click();
    cy.contains("internal").click();
    cy.get("@spy-4").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filterName: "queue",
      filterValue: internalQueue,
    });
    cy.get("#queue-dropdown").should("have.text", "internal");
  });
  it("will update event filter for given queue when a different is selected", () => {
    factory({
      props: { nodeQueue: "events" },
      initialState: {
        currentUserSettingsStore: {
          queues: { alerts: externalQueue, events: internalQueue },
        },
        queueStore: { items: [externalQueue, internalQueue] },
      },
    });
    cy.contains("internal").should("be.visible");
    cy.get("#queue-dropdown").click();
    cy.contains("external").click();
    cy.get("@spy-4").should("have.been.calledOnceWith", {
      nodeType: "events",
      filterName: "queue",
      filterValue: externalQueue,
    });
    cy.get("#queue-dropdown").should("have.text", "external");
  });
});
