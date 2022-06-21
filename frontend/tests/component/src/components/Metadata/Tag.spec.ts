import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import MetadataTag from "@/components/Metadata/MetadataTag.vue";
import router from "@/router/index";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { metadataTagReadFactory } from "@mocks/metadata";

const testTag = metadataTagReadFactory({ value: "testTag" });

function factory(
  nodeType: "alerts" | "events" = "alerts",
  overrideNodeType?: "alerts" | "events",
) {
  return mount(MetadataTag, {
    global: {
      plugins: [PrimeVue, createCustomCypressPinia(), router],
      provide: { nodeType: nodeType },
    },
    propsData: {
      tag: testTag,
      overrideNodeType: overrideNodeType,
    },
  });
}

describe("MetadataTag", () => {
  it("renders as expected", () => {
    factory();
    cy.contains("testTag").should("be.visible");
  });
  it("adds a filter for provided node type as expected on click (alert)", () => {
    factory();
    cy.contains("testTag").click();
    cy.get("@stub-1").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filters: {
        tags: [["testTag"]],
      },
    });
  });
  it("adds a filter for provided node type as expected on click (event)", () => {
    factory("events");
    cy.contains("testTag").click();
    cy.get("@stub-1").should("have.been.calledOnceWith", {
      nodeType: "events",
      filters: {
        tags: [["testTag"]],
      },
    });
  });
  it("if set, 'overrideNodeType' is used for filtering as expected on click", () => {
    factory("events", "alerts");
    cy.contains("testTag").click();
    cy.get("@stub-1").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filters: {
        tags: [["testTag"]],
      },
    });
  });
});
