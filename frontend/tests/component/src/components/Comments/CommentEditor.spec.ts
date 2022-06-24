import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import PrimeVue from "primevue/config";

import { alertCommentReadFactory } from "@mocks/comment";

import CommentEditor from "@/components/Comments/CommentEditor.vue";
import { alertCommentRead } from "@/models/alertComment";

let comments = [
  alertCommentReadFactory({ insertTime: "2022-04-25T12:00:00.000000+00:00" }),
  alertCommentReadFactory({
    value: "Other comment",
    insertTime: "2022-04-25T01:00:00.000000+00:00",
  }),
];

function factory(props: alertCommentRead[] = comments) {
  mount(CommentEditor, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            recentCommentsStore: {
              recentComments: ["example"],
            },
          },
        }),
      ],
    },
    propsData: { modelValue: props },
  });
}

describe("CommentEditor", () => {
  // these props get updated in some tests, need to reset value here
  beforeEach(() => {
    comments = [
      alertCommentReadFactory({
        insertTime: "2022-04-25T12:00:00.000000+00:00",
      }),
      alertCommentReadFactory({
        value: "Other comment",
        insertTime: "2022-04-25T01:00:00.000000+00:00",
      }),
    ];
  });

  it("renders correctly when no comments are given", () => {
    factory([]);
    cy.contains("No comments found.").should("be.visible");
  });
  it("renders correctly when given comments", () => {
    factory();
    cy.findAllByRole("listitem").should("have.length", 2);
    cy.get('[data-cy="edit-comment-button"]').should("have.length", 2);
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible");
    cy.contains(
      "4/25/2022, 1:00:00 AM UTC (Test Analyst) Other comment",
    ).should("be.visible");
  });
  it("does not change comment value if edit panel opened and closed", () => {
    factory();
    cy.get('[data-cy="edit-comment-button"]').first().click();
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible"); // list item should be visible still
    cy.get('[data-cy="edit-comment-panel"]').should("be.visible");
    cy.findAllByDisplayValue("A test comment").click().type("Updated"); // input should have current value filled in
    cy.get('[data-cy="close-edit-comment-panel"]').click(); // close without saving
    cy.get('[data-cy="edit-comment-panel"]').should("not.exist");
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible");
  });
  it("does update comment value if edit panel opened, comment edited, and saved", () => {
    factory([
      alertCommentReadFactory({
        insertTime: "2022-04-25T12:00:00.000000+00:00",
      }),
    ]);
    cy.get('[data-cy="edit-comment-button"]').first().click();
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible"); // list item should be visible still
    cy.get('[data-cy="edit-comment-panel"]').should("be.visible");
    cy.findAllByDisplayValue("A test comment")
      .clear()
      .type("New comment value");
    cy.get('[data-cy="save-comment-button"]').click();
    cy.get('[data-cy="edit-comment-panel"]').should("not.exist");
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) New comment value",
    ).should("be.visible");
  });
  it("does not allow updating comment value with an empty string", () => {
    factory();
    cy.get('[data-cy="edit-comment-button"]').first().click();
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible"); // list item should be visible still
    cy.get('[data-cy="edit-comment-panel"]').should("be.visible");
    cy.findAllByDisplayValue("A test comment").clear();
    cy.get('[data-cy="save-comment-button"]').click();
    cy.get('[data-cy="edit-comment-panel"]').should("be.visible");
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible");
  });
  it("correctly updates comment data when selecting from recent comments", () => {
    factory([
      alertCommentReadFactory({
        insertTime: "2022-04-25T12:00:00.000000+00:00",
      }),
    ]);
    cy.get('[data-cy="edit-comment-button"]').first().click();
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible");
    cy.get('[data-cy="edit-comment-panel"]').should("be.visible");
    cy.get(".p-autocomplete > .p-button").click();
    cy.contains("example").click();
    cy.findAllByDisplayValue("example").type(" extra text");
    cy.get('[data-cy="save-comment-button"]').click();
    cy.get('[data-cy="edit-comment-panel"]').should("not.exist");
    cy.contains(
      "4/25/2022, 12:00:00 PM UTC (Test Analyst) example extra text",
    ).should("be.visible");
  });
});
