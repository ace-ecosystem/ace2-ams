import { createCustomCypressPinia } from "@tests/cypressHelpers";

import PrimeVue from "primevue/config";
import { testConfiguration } from "@/etc/configuration/test/index";
import Tooltip from "primevue/tooltip";

import TheFilterToolbar from "@/components/Filters/TheFilterToolbar.vue";
import router from "@/router/index";
import { mount } from "@cypress/vue";
import { alertFilterParams } from "@/models/alert";
import { eventFilterParams } from "@/models/event";
import FilterChipContainerVue from "@/components/Filters/FilterChipContainer.vue";
import DateRangePickerVue from "@/components/UserInterface/DateRangePicker.vue";
import { genericObjectReadFactory } from "@mocks/genericObject";

function factory(
  filters: { alerts: alertFilterParams; events: eventFilterParams } = {
    alerts: {},
    events: {},
  },
) {
  return mount(TheFilterToolbar, {
    global: {
      directives: { tooltip: Tooltip },
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: {
            currentUserSettingsStore: {
              queues: {
                alerts: { value: "external" },
                events: { value: "external" },
              },
            },
            filterStore: filters,
            alertDispositionStore: {
              items: [genericObjectReadFactory()],
            },
          },
        }),
        router,
      ],
      provide: {
        nodeType: "alerts",
        rangeFilters: testConfiguration.alerts.alertRangeFilters,
        availableFilters: testConfiguration.alerts.alertFilters,
      },
    },
  });
}
// Nothing will show because there is no queue set to decide the available columns
describe("TheFilterToolbar", () => {
  it("renders as expected when no filters are applied", () => {
    factory().then((wrapper) => {
      cy.contains("Quick Add").should("be.visible");
      cy.wrap(wrapper.findComponent(FilterChipContainerVue)).should("exist");
      cy.wrap(wrapper.findComponent(DateRangePickerVue)).should("exist");
    });
  });
  it("renders as expected when there are filters applied", () => {
    factory({
      alerts: {
        name: "test name",
        eventTimeAfter: new Date(2022, 4, 22, 12, 0, 0),
        eventTimeBefore: new Date(2022, 4, 23, 12, 0, 0),
      },
      events: {},
    });
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
    cy.contains("2022-05-22T16:00:00.000Z").should("be.visible"); // filter chip
    cy.contains("2022-05-23T16:00:00.000Z").should("be.visible"); // filter chip
    cy.findByDisplayValue("05/22/2022 12:00").should("be.visible"); // date range picker
    cy.findByDisplayValue("05/23/2022 12:00").should("be.visible"); // date range picker
  });
  it("opens quick add panel when quick add filter button clicked", () => {
    factory();
    cy.contains("Quick Add").click();
    cy.get('[data-cy="quick-add-filter-panel"]').should("be.visible");
    cy.get('[data-cy="filter-input"]').should("be.visible");
    cy.get('[data-cy="quick-add-filter-submit-button"]').should("be.visible");
  });
  it("attempts to add a filter when submit button clicked in quick add panel ", () => {
    factory();
    cy.contains("Quick Add").click();
    cy.get('[data-cy="quick-add-filter-panel"]').should("be.visible");
    cy.get('[data-cy="quick-add-filter-submit-button"]').click();
    cy.get("@stub-2").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filterName: "disposition",
      filterValue: genericObjectReadFactory(),
    }); // set filter
    cy.get('[data-cy="quick-add-filter-panel"]').should("not.exist");
  });
  it("opens the edit modal when 'Edit' button clicked in filter menu dropdown", () => {
    factory();
    cy.get('[data-cy="edit-filter-button"]').siblings().click();
    cy.contains("Edit").click();
    cy.get("@stub-6").should("have.been.calledOnceWith", "EditFilterModal"); // Open modal
  });
  it("resets filters when 'Reset' button clicked in filter menu dropdown", () => {
    factory();
    cy.get('[data-cy="edit-filter-button"]').siblings().click();
    cy.contains("Reset").click();
    cy.get("@stub-4").should("have.been.calledOnceWith", {
      nodeType: "alerts",
    }); // clear all
    cy.get("@stub-1").should("have.been.calledOnceWith", {
      nodeType: "alerts",
      filters: {
        queue: {
          value: "external",
        },
      },
    }); // set filters to defaults
  });
  it("clears filters when 'Clear All' button clicked in filter menu dropdown", () => {
    factory();
    cy.get('[data-cy="edit-filter-button"]').siblings().click();
    cy.contains("Clear All").click();
    cy.get("@stub-4").should("have.been.calledOnceWith", {
      nodeType: "alerts",
    }); // clear all
  });
});
