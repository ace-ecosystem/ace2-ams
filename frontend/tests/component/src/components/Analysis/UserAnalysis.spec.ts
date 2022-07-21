import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import UserAnalysis from "@/components/Analysis/UserAnalysis.vue";
import router from "@/router/index";
import { Event } from "@/services/api/event";
import { userSummary } from "@/models/eventSummaries";

const props = {
  eventUuid: "uuid",
};

function factory() {
  return mount(UserAnalysis, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
    propsData: props,
  });
}

describe("UserAnalysis", () => {
  it("renders correctly when call to fetch user analysis fails", () => {
    cy.stub(Event, "readUserSummary")
      .as("fetchUserSummary")
      .rejects(new Error("Request failed with status code 404"));
    factory();
    cy.contains(
      "No users could be found. Request failed with status code 404",
    ).should("be.visible");
  });
  it("renders correctly when call to fetch user analysis is successful but empty", () => {
    cy.stub(Event, "readUserSummary")
      .withArgs("uuid")
      .as("fetchUserSummary")
      .resolves([]);
    factory();
    cy.contains("No users could be found.").should("be.visible");
  });
  it("renders correctly when call to fetch user analysis is successful and has results", () => {
    const userSummaries: userSummary[] = [
      {
        company: "Widgets & Co.",
        department: "Information Security",
        division: "IT",
        email: "joe@widgets.com",
        managerEmail: "bob@widgets.com",
        title: "Widget Security Engineer",
        userId: "W123456",
      },
    ];

    const userSummaryCols = [
      "User ID",
      "Email",
      "Company",
      "Division",
      "Department",
      "Title",
      "Manager Email",
    ];
    const userSummaryVals = [
      userSummaries[0].userId,
      userSummaries[0].email,
      userSummaries[0].company,
      userSummaries[0].division,
      userSummaries[0].department,
      userSummaries[0].title,
      userSummaries[0].managerEmail,
    ];

    cy.stub(Event, "readUserSummary")
      .withArgs("uuid")
      .as("fetchUserSummary")
      .resolves(userSummaries);
    factory();

    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", userSummaryCols[index]);
      });
    cy.get("tr")
      .eq(1)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", userSummaryVals[index]);
      });
  });
});
