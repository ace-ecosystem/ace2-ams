import { createPinia } from "pinia";
import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTableCell from "@/components/Alerts/AlertTableCell.vue";

import { alertSummary } from "@/models/alert";
import { alertSummaryFactory } from "@mocks/alert";
import { commentReadFactory } from "@mocks/comment";
import { testConfiguration } from "@/etc/configuration/test";

import router from "@/router/index";
import { metadataTagReadFactory } from "@mocks/metadata";

interface AlertTableCellProps {
  data: alertSummary;
  field: keyof alertSummary;
}

const mockAlert: alertSummary = alertSummaryFactory({
  name: "Test",
  comments: [commentReadFactory({ value: "Test comment" })],
  tags: [metadataTagReadFactory({ value: "testTag" })],
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
      provide: { objectType: "alerts", config: testConfiguration },
    },
    propsData: args.props,
  });
}

describe("AlertTableCell", () => {
  it("renders", () => {
    factory();
  });
  it("correctly renders an alert name cell with icon, if available in config", () => {
    const props: AlertTableCellProps = {
      data: alertSummaryFactory({
        name: "Test",
        type: "testType",
      }),
      field: "name",
    };
    factory({ props: props });
    // Icon
    cy.get("[data-cy='alert-icon']").should("be.visible");
    // Alert name & link
    cy.contains("Test")
      .invoke("attr", "href")
      .should("contain", "/alert/testAlertUuid");
  });
  it("correctly renders an alert name cell with any tags and comments, but will not display icon if not available", () => {
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
    // Should not be an icon
    cy.get("[data-cy='alert-icon']").should("not.exist");
  });
  it("correctly renders an alert time-type cell", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "eventTime",
    };
    factory({ props: props });
    cy.contains("2/24/2022, 12:00:00 AM UTC");
  });
  it("correctly renders an alert comments cell", () => {
    const props: AlertTableCellProps = {
      data: mockAlert,
      field: "comments",
    };
    factory({ props: props });
    cy.contains("1/1/2020, 12:00:00 AM UTC (Test Analyst) Test comment");
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
