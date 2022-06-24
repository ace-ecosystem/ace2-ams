import { mount } from "@cypress/vue";

import PrimeVue from "primevue/config";

import FilterChipContainer from "@/components/Filters/FilterChipContainer.vue";
import router from "@/router/index";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertFilterParams } from "@/models/alert";
import { userReadFactory } from "@mocks/user";

function factory(filters: alertFilterParams) {
  return mount(FilterChipContainer, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: { filterStore: { alerts: filters } },
        }),
        router,
      ],
      provide: {
        objectType: "alerts",
      },
    },
  });
}

describe("FilterChipContainer", () => {
  it("renders when no filters are currently set", () => {
    factory({});
    cy.get("[data-cy=filter-chip]").should("not.exist");
  });
  it("renders when there are filters set", () => {
    factory({
      name: { included: ["test name"], notIncluded: [] },
      owner: { included: [userReadFactory()], notIncluded: [] },
    });
    cy.get("[data-cy=filter-chip]").should("have.length", 2);
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
    cy.contains("Owner:").should("be.visible");
    cy.contains("Test Analyst").should("be.visible");
  });
  it("re-renders when a filter is added", () => {
    factory({}).then((wrapper) => {
      wrapper.vm.filterStore.setFilter({
        objectType: "alerts",
        filterName: "name",
        filterValue: "test name",
        isIncluded: true,
      });
      cy.get("[data-cy=filter-chip]").should("have.length", 1);
      cy.contains("Name:").should("be.visible");
      cy.contains("test name").should("be.visible");
    });
  });
  it("re-renders when a filter is added", () => {
    factory({
      name: { included: ["test name"], notIncluded: [] },
      owner: { included: [userReadFactory()], notIncluded: [] },
    }).then((wrapper) => {
      wrapper.vm.filterStore.clearAll({ nodeType: "alerts" });
      cy.get("[data-cy=filter-chip]").should("not.exist");
    });
  });
});
