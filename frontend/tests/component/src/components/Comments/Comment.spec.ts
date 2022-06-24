import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { commentRead } from "@/models/comment";

import { commentReadFactory } from "@mocks/comment";

import Comment from "@/components/Node/Comment.vue";

interface commentProps {
  comment: commentRead;
  includeTime?: boolean;
  includeLineBreak?: boolean;
}

const defaultProps = {
  comment: commentReadFactory(),
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
        comment: commentReadFactory({
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
      props: { comment: commentReadFactory(), includeLineBreak: false },
    });
    cy.contains("(Test Analyst) A test comment").should("be.visible");
    cy.get("br").should("not.exist");
  });
});
