import { mount } from "@cypress/vue";

import PrimeVue from "primevue/config";

import FilterChip from "@/components/Filters/FilterChip.vue";
import router from "@/router/index";
import { userReadFactory } from "@mocks/user";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertFilterValues } from "@/models/alert";
import { eventFilterValues } from "@/models/event";

function factory(props: {
  filterName: string;
  filterValue: alertFilterValues[] | eventFilterValues[];
}) {
  return mount(FilterChip, {
    global: {
      stubs: { NodePropertyInput: true },
      plugins: [PrimeVue, createCustomCypressPinia(), router],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: props,
  });
}

// Nothing will show because there is no queue set to decide the available columns
describe("FilterChip", () => {
  it("will not render if filterNameObject cannot be found", () => {
    factory({ filterName: "test", filterValue: ["test"] });
    cy.get('[data-cy="filter-chip"]').should("not.exist");
  });
  it("correctly renders if  filterNameObject does not provide any special formatting (ex. name filter)", () => {
    factory({ filterName: "name", filterValue: ["test name"] });
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
  });
  it("correctly renders if  filterNameObject provides a stringRepr method (ex. date)", () => {
    factory({
      filterName: "eventTimeAfter",
      filterValue: [new Date(2022, 4, 21, 12, 12, 12)],
    });
    cy.contains("Event Time After (UTC):").should("be.visible");
    cy.contains("2022-05-21T16:12:12").should("be.visible");
  });
  it("correctly renders if  filterNameObject provides an optionProperty (ex. owner)", () => {
    factory({ filterName: "owner", filterValue: [userReadFactory()] });
    cy.contains("Owner:").should("be.visible");
    cy.contains("Test Analyst").should("be.visible");
  });
  it("unsets filter if filter value is clicked", () => {
    factory({ filterName: "name", filterValue: ["test name"] });
    cy.contains("test name").click();
    cy.get("@stub-5").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
    });
  });
  it("unsets filter if clear filter (X button) is clicked", () => {
    factory({ filterName: "name", filterValue: ["test name"] });
    cy.get('[data-cy="filter-chip-remove-button"]').click();
    cy.get("@stub-5").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
    });
  });
  it("attempts to update filter when new value is entered in edit filter panel", () => {
    factory({ filterName: "name", filterValue: ["test name"] });
    cy.get('[data-cy="filter-chip-edit-button"]').click();
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test name",
    });
  });
});
