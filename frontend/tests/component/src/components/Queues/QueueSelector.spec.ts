import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import QueueSelector from "@/components/Queues/QueueSelector.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";

function factory(
  args: { props: { objectQueue: "alerts" | "events" }; initialState: any } = {
    props: { objectQueue: "alerts" },
    initialState: {},
  },
) {
  return mount(QueueSelector, {
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

describe("QueueSelector", () => {
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
      props: { objectQueue: "alerts" },
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
      props: { objectQueue: "alerts" },
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
      objectType: "alerts",
      filterName: "queue",
      filterValue: internalQueue,
    });
    cy.get("#queue-dropdown").should("have.text", "internal");
  });
  it("will update event filter for given queue when a different is selected", () => {
    factory({
      props: { objectQueue: "events" },
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
      objectType: "events",
      filterName: "queue",
      filterValue: externalQueue,
    });
    cy.get("#queue-dropdown").should("have.text", "external");
  });
});
