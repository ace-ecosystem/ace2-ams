import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import Tooltip from "primevue/tooltip";

import { testConfiguration } from "@/etc/configuration/test/index";

import DateRangePicker from "@/components/UserInterface/DateRangePicker.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertFilterParams } from "@/models/alert";

function factory(args: { filters: alertFilterParams } = { filters: {} }) {
  return mount(DateRangePicker, {
    global: {
      directives: { tooltip: Tooltip },
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: { filterStore: { alerts: args.filters, events: {} } },
        }),
      ],
      provide: {
        nodeType: "alerts",
        rangeFilters: testConfiguration.alerts.alertRangeFilters,
      },
    },
  });
}

const testTime = new Date(Date.UTC(2022, 2, 29, 12, 0, 0, 0)).getTime();

describe("DateRangePicker", () => {
  it("renders as expected when no current filter is set", () => {
    factory();
    cy.findAllByPlaceholderText("The beginning of time").should("be.visible");
    cy.findAllByPlaceholderText("Now").should("be.visible");
  });
  it("renders as expected when there are date filters set", () => {
    factory({
      filters: {
        eventTimeAfter: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
        eventTimeBefore: new Date(Date.UTC(2022, 4, 30, 12, 0, 0, 0)),
        insertTimeAfter: new Date(Date.UTC(2022, 2, 25, 12, 0, 0, 0)),
        insertTimeBefore: new Date(Date.UTC(2022, 2, 30, 12, 0, 0, 0)),
      },
    });
    // Make sure the "Event Time" filters are the ones that are showing
    cy.findByDisplayValue("05/25/2022 08:00").should("be.visible");
    cy.findByDisplayValue("05/30/2022 08:00").should("be.visible");
  });
  it("correctly sets the 'start' date filter when a date is entered enter the start input", () => {
    factory();
    cy.findAllByPlaceholderText("The beginning of time")
      .click()
      .type("05/25/2022 08:00")
      .type("{enter}");
    cy.get("@spy-2").should("be.calledOnceWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
    });
  });
  it("correctly clears the 'start' date filter the clear button is clicked", () => {
    factory({
      filters: {
        eventTimeAfter: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
        eventTimeBefore: new Date(Date.UTC(2022, 4, 30, 12, 0, 0, 0)),
        insertTimeAfter: new Date(Date.UTC(2022, 2, 25, 12, 0, 0, 0)),
        insertTimeBefore: new Date(Date.UTC(2022, 2, 30, 12, 0, 0, 0)),
      },
    });
    cy.get('[data-cy="date-range-picker-start-clear"]').click();
    cy.get("@spy-3").should("be.calledOnceWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
    });
    cy.findAllByPlaceholderText("The beginning of time").should("be.visible");
  });
  it("correctly sets the 'end' date filter when a date is entered enter the end input", () => {
    factory();
    cy.findAllByPlaceholderText("Now")
      .click()
      .type("05/25/2022 08:00")
      .type("{enter}");
    cy.get("@spy-2").should("be.calledOnceWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
    });
  });
  it("correctly clears the 'end' date filter the clear button is clicked", () => {
    factory({
      filters: {
        eventTimeAfter: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
        eventTimeBefore: new Date(Date.UTC(2022, 4, 30, 12, 0, 0, 0)),
        insertTimeAfter: new Date(Date.UTC(2022, 2, 25, 12, 0, 0, 0)),
        insertTimeBefore: new Date(Date.UTC(2022, 2, 30, 12, 0, 0, 0)),
      },
    });
    cy.get('[data-cy="date-range-picker-end-clear"]').click();
    cy.get("@spy-3").should("be.calledOnceWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
    });
    cy.findAllByPlaceholderText("Now").should("be.visible");
  });
  it("correctly sets the date filters when the 'Today' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Today").click();
    cy.findByDisplayValue("03/29/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/29/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 2, 29, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 29, 23, 59, 59)),
    });
    cy.contains("Today").should("not.exist");
  });
  it("correctly sets the date filters when the 'Yesterday' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Yesterday").click();
    cy.findByDisplayValue("03/28/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/28/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 2, 28, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 28, 23, 59, 59)),
    });
    cy.contains("Yesterday").should("not.exist");
  });
  it("correctly sets the date filters when the 'Last 7 Days' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Last 7 Days").click();
    cy.findByDisplayValue("03/22/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/29/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 2, 22, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 29, 23, 59, 59)),
    });
    cy.contains("Last 7 Days").should("not.exist");
  });
  it("correctly sets the date filters when the 'Last 30 Days' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Last 30 Days").click();
    cy.findByDisplayValue("02/27/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/29/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 1, 30, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 29, 23, 59, 59)),
    });
    cy.contains("Last 30 Days").should("not.exist");
  });
  it("correctly sets the date filters when the 'Last 60 Days' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Last 60 Days").click();
    cy.findByDisplayValue("01/28/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/29/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 0, 30, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 29, 23, 59, 59)),
    });
    cy.contains("Last 60 Days").should("not.exist");
  });
  it("correctly sets the date filters when the 'This Month' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("This Month").click();
    cy.findByDisplayValue("03/01/2022 00:00").should("be.visible");
    cy.findByDisplayValue("03/29/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 2, 0, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 2, 29, 23, 59, 59)),
    });
    cy.contains("This Month").should("not.exist");
  });
  it("correctly sets the date filters when the 'Last Month' button is clicked", () => {
    cy.clock(testTime);
    factory();
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Last Month").click();
    cy.findByDisplayValue("02/01/2022 00:00").should("be.visible");
    cy.findByDisplayValue("02/28/2022 23:59").should("be.visible");
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
      filterValue: new Date(Date.UTC(2022, 1, 0, 0, 0, 0)),
    });
    cy.get("@spy-2").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
      filterValue: new Date(Date.UTC(2022, 1, 28, 23, 59, 59)),
    });
    cy.contains("Last Month").should("not.exist");
  });
  it("clears currently set date filters when date filter type is changed", () => {
    factory({
      filters: {
        eventTimeAfter: new Date(Date.UTC(2022, 4, 25, 12, 0, 0, 0)),
        eventTimeBefore: new Date(Date.UTC(2022, 4, 30, 12, 0, 0, 0)),
        insertTimeAfter: new Date(Date.UTC(2022, 2, 25, 12, 0, 0, 0)),
        insertTimeBefore: new Date(Date.UTC(2022, 2, 30, 12, 0, 0, 0)),
      },
    });
    cy.get('[data-cy="date-range-picker-options-button"]').click();
    cy.contains("Event Time").click();
    cy.contains("Insert Time").click();
    cy.contains("Insert Time").should("not.exist");

    cy.get("@spy-3").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeAfter",
    });
    cy.get("@spy-3").should("be.calledWith", {
      nodeType: "alerts",
      filterName: "eventTimeBefore",
    });

    // Now the set filters for "Insert Time" should be showing
    cy.findByDisplayValue("03/25/2022 08:00").should("be.visible");
    cy.findByDisplayValue("03/30/2022 08:00").should("be.visible");
  });
});
