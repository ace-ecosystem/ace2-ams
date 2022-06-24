import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { alertCommentRead } from "@/models/alertComment";

import { alertCommentReadFactory } from "@mocks/comment";

import Comment from "@/components/Comments/Comment.vue";

interface commentProps {
  comment: alertCommentRead;
  includeTime?: boolean;
  includeLineBreak?: boolean;
}

const defaultProps = {
  comment: alertCommentReadFactory(),
};

function factory(args: { props: commentProps } = { props: defaultProps }) {
  mount(Comment, {
    global: {
      plugins: [PrimeVue, createPinia()],
    },
    propsData: args.props,
  });
}

describe("Comment", () => {
  it("renders as expected with default props", () => {
    factory();
    cy.contains("(Test Analyst) A test comment").should("be.visible");
    cy.get("br").should("exist");
  });
  it("renders as expected with includeTime set to true", () => {
    factory({
      props: {
        comment: alertCommentReadFactory({
          insertTime: "2022-03-25T12:00:00.000000+00:00",
        }),
        includeTime: true,
      },
    });
    cy.contains(
      "3/25/2022, 12:00:00 PM UTC (Test Analyst) A test comment",
    ).should("be.visible");
  });
  it("renders as expected with includeLineBreak set to false", () => {
    factory({
      props: { comment: alertCommentReadFactory(), includeLineBreak: false },
    });
    cy.contains("(Test Analyst) A test comment").should("be.visible");
    cy.get("br").should("not.exist");
  });
});
