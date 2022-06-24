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
  filterValue: {
    included: alertFilterValues[] | eventFilterValues[];
    notIncluded: alertFilterValues[] | eventFilterValues[];
  };
}) {
  return mount(FilterChip, {
    global: {
      stubs: { ObjectPropertyInput: true },
      plugins: [PrimeVue, createCustomCypressPinia(), router],
      provide: {
        objectType: "alerts",
      },
    },
    propsData: props,
  });
}

// Nothing will show because there is no queue set to decide the available columns
describe("FilterChip", () => {
  it("will not render if filterNameObject cannot be found", () => {
    factory({
      filterName: "test",
      filterValue: { included: ["test"], notIncluded: [] },
    });
    cy.get('[data-cy="filter-chip"]').should("not.exist");
  });
  it("correctly renders if  filterNameObject does not provide any special formatting (ex. name filter)", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
    cy.get('[data-cy="filter-chip-edit-button"]').should("have.length", 1);
    cy.get('[data-cy="filter-chip-add-button"]').should("have.length", 1);
  });
  it("correctly renders if there are multiple values set for a filter", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name", "test name 2"], notIncluded: [] },
    });
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
    cy.contains("|").should("be.visible");
    cy.contains("test name 2").should("be.visible");
    cy.get('[data-cy="filter-chip-edit-button"]').should("have.length", 2);
    cy.get('[data-cy="filter-chip-add-button"]').should("have.length", 1);
  });
  it("correctly renders if there are included and notIncluded filters added", () => {
    factory({
      filterName: "name",
      filterValue: {
        included: ["test name", "test name 2"],
        notIncluded: ["test name 3", "test name 4"],
      },
    });
    cy.contains("Name:").should("be.visible");
    cy.contains("test name").should("be.visible");
    cy.contains("|").should("be.visible");
    cy.contains("test name 2").should("be.visible");
    cy.contains("! test name 3").should("be.visible");
    cy.contains("! test name 4").should("be.visible");
    cy.get('[data-cy="filter-chip-edit-button"]').should("have.length", 4);
    cy.get('[data-cy="filter-chip-add-button"]').should("have.length", 1);
  });
  it("correctly renders if  filterNameObject provides a stringRepr method (ex. date)", () => {
    factory({
      filterName: "eventTimeAfter",
      filterValue: {
        included: [new Date(2022, 4, 21, 12, 12, 12)],
        notIncluded: [],
      },
    });
    cy.contains("Event Time After (UTC):").should("be.visible");
    cy.contains("2022-05-21T16:12:12").should("be.visible");
  });
  it("correctly renders if  filterNameObject provides an optionProperty (ex. owner)", () => {
    factory({
      filterName: "owner",
      filterValue: { included: [userReadFactory()], notIncluded: [] },
    });
    cy.contains("Owner:").should("be.visible");
    cy.contains("Test Analyst").should("be.visible");
  });
  it("unsets filter if filter value is clicked", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.contains("test name").click();
    cy.get("@stub-6").should("have.been.calledWith", {
      objectType: "alerts",
      filterName: "name",
      filterValue: "test name",
      isIncluded: true,
    });
  });
  it("unsets filter if 'NOT' filter value is clicked", () => {
    factory({
      filterName: "name",
      filterValue: { included: [], notIncluded: ["test name"] },
    });
    cy.contains("test name").click();
    cy.get("@stub-6").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test name",
      isIncluded: false,
    });
  });
  it("unsets filter if filter name is clicked is clicked", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.contains("Name").click();
    cy.get("@stub-5").should("have.been.calledWith", {
      objectType: "alerts",
      filterName: "name",
    });
  });
  it("attempts to update filter when new value is entered in edit filter panel", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.get('[data-cy="filter-chip-edit-button"]').first().click();
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.get("@stub-6").should("have.been.calledWith", {
      objectType: "alerts",
      filterName: "name",
      filterValue: "test name",
      isIncluded: true,
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      objectType: "alerts",
      filterName: "name",
      filterValue: "test name", // should be the 'new value' which hasn't changed since loading the old value
      isIncluded: true,
    });
  });
  it("attempts to update filter when 'NOT' switch is clicked in edit filter panel", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.get('[data-cy="filter-chip-edit-button"]').first().click();
    cy.get('[data-cy="filter-not-included-switch"]').parent().parent().click();
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.get("@stub-6").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test name",
      isIncluded: true,
    });
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: "test name", // should be the 'new value' which hasn't changed since loading the old value
      isIncluded: false,
    });
  });
  it("correctly adds new included filter via add filter button", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.get('[data-cy="filter-chip-add-button"]').click();
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.get("@stub-6").should("not.have.been.called");
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: undefined, // This will be undefined because ObjectPropertyInput is stubbed
      isIncluded: true,
    });
  });
  it("correctly adds new notIncluded filter via add filter button", () => {
    factory({
      filterName: "name",
      filterValue: { included: ["test name"], notIncluded: [] },
    });
    cy.get('[data-cy="filter-chip-add-button"]').click();
    cy.get('[data-cy="filter-not-included-switch"]').parent().parent().click();
    cy.get('[data-cy="filter-chip-submit-button"]').click();
    cy.get("@stub-6").should("not.have.been.called");
    cy.get("@stub-4").should("have.been.calledWith", {
      nodeType: "alerts",
      filterName: "name",
      filterValue: undefined, // This will be undefined because ObjectPropertyInput is stubbed
      isIncluded: false,
    });
  });
});
