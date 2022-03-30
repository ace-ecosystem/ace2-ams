import { createPinia } from "pinia";
import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";

import { alertSummary } from "@/models/alert";
import { alertSummaryFactory } from "@mocks/alert";
import { commentReadFactory } from "@mocks/comment";
import { genericObjectReadFactory } from "@mocks/genericObject";
import router from "@/router/index";

interface AlertTableCellProps {
  data: alertSummary;
  field: keyof alertSummary;
}

const mockAlert: alertSummary = alertSummaryFactory({
  name: "Test",
  comments: [commentReadFactory({ value: "Test comment" })],
  tags: [genericObjectReadFactory({ value: "testTag" })],
});

const defaultProps: AlertTableCellProps = {
  data: mockAlert,
  field: "name",
};

function factory(
  args = {
    props: defaultProps,
  },
) {
  return mount(AlertTableCell, {
    global: {
      plugins: [createPinia(), PrimeVue, router],
      provide: { nodeType: "alerts" },
    },
    propsData: args.props,
  });
}

describe("AlertTableCell", () => {
  it("renders", () => {
    factory();
  });
  it("correctly renders an alert name cell with any tags and comments", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "name",
    };
    factory({ props: props });
    // Alert name & link
    cy.contains("Test")
      .invoke("attr", "href")
      .should("contain", "/alert/testAlertUuid");
    // Tags
    cy.contains("testTag");
    // Comments
    cy.contains("(Test Analyst) Test comment");
  });
  it("correctly renders an alert time-type cell", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "eventTime",
    };
    factory({ props: props });
    cy.contains("3/24/2022, 12:00:00 AM");
  });
  it("correctly renders an alert comments cell", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "comments",
    };
    factory({ props: props });
    cy.contains("12/31/2019, 7:00:00 PM (Test Analyst) Test comment");
  });
  it("correctly renders a generic alert cell (queue)", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "queue",
    };
    factory({ props: props });
    cy.contains("testAlertQueue");
  });
});
