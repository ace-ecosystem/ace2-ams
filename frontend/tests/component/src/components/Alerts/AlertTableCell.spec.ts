// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createCustomCypressPinia } from "@unit/helpers";
import PrimeVue from "primevue/config";

import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";

import router from "@/router/index";
import { alertSummary } from "@/models/alert";
import { alertSummaryFactory } from "@mocks/alert";
import { commentReadFactory } from "@mocks/comment";
import { genericObjectReadFactory } from "@mocks/genericObject";

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
    piniaOptions: {},
    props: defaultProps,
  },
) {
  return mount(AlertTableCell, {
    global: {
      plugins: [createCustomCypressPinia(args.piniaOptions), PrimeVue, router],
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
    factory({ piniaOptions: {}, props: props });
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
    factory({ piniaOptions: {}, props: props });
    cy.contains("3/24/2022, 4:00:00 AM");
  });
  it("correctly renders an alert comments cell", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "comments",
    };
    factory({ piniaOptions: {}, props: props });
    cy.contains("12/31/2019, 7:00:00 PM (Test Analyst) Test comment");
  });
  it("correctly renders a generic alert cell (queue)", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "queue",
    };
    factory({ piniaOptions: {}, props: props });
    cy.contains("testAlertQueue");
  });
});
