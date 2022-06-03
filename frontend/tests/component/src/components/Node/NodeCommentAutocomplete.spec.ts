import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";
import { createCustomCypressPinia } from "@tests/cypressHelpers";

import NodeCommentAutocomplete from "@/components/Node/NodeCommentAutocomplete.vue";

function factory(recentComments: string[] = []) {
  return mount(NodeCommentAutocomplete, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            recentCommentsStore: {
              recentComments: recentComments,
            },
          },
        }),
      ],
    },
  });
}

describe("NodeCommentAutocomplete", () => {
  it("renders correctly if there are no options available", () => {
    factory();
    cy.contains("No recent comments available").should("be.visible");
    cy.get("input").should("be.disabled");
  });
  it("renders correctly if there are options available", () => {
    factory(["test"]);
    cy.contains("Choose a recent comment").should("be.visible");
    cy.get("input").should("have.value", "");
    cy.get("input").should("not.be.disabled");
  });
  it("renders options correctly", () => {
    const comments = ["example", "test", "another one"];
    factory(comments);
    cy.contains("Choose a recent comment").should("be.visible");
    cy.get(".p-button").click();
    comments.forEach((comment) => {
      cy.contains(comment).should("be.visible");
    });
  });
  it("autocompletes as expected", () => {
    const comments = ["example", "test", "another one"];
    factory(comments);
    cy.get("input").click().type("t");
    cy.contains("test").should("be.visible");
    cy.contains("example").should("not.exist");
    cy.contains("another one").should("not.exist");
  });
  it("emits expected event suggestion is clicked", () => {
    const comments = ["example", "test", "another one"];
    factory(comments).then((wrapper) => {
      cy.contains("Choose a recent comment").should("be.visible");
      cy.get(".p-button").click();
      cy.contains("example").click();
      cy.get("input").should("have.value", "");
      expect("commentClicked" in wrapper.emitted());
      expect(wrapper.emitted()["commentClicked"] === "example");
    });
  });
  it("attempts to remove suggestions from recentComments when delete button clicked", () => {
    const comments = ["example", "test", "another one"];
    factory(comments);
    cy.contains("Choose a recent comment").should("be.visible");
    cy.get(".p-button").click();
    cy.contains("example").siblings().click();
    cy.get("@spy-2").should("have.been.calledOnceWith", "example");
    cy.get("input").should("have.value", "");
    cy.get(".p-button").click();
    cy.contains("example").should("not.exist");
  });
});
