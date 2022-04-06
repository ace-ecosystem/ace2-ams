// Example Cypress Vue component test that we might use one day
// NOTE: This test is not fully functional at this point.

import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import EmailAnalysisHeadersBody from "@/components/Analysis/EmailAnalysisHeadersBody.vue";
import router from "@/router/index";
import { Event } from "@/services/api/event";
import { emailHeadersBody } from "@/models/eventSummaries";

const props = {
  eventUuid: "uuid",
};

function factory() {
  return mount(EmailAnalysisHeadersBody, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
    propsData: props,
  });
}

const emailHeadersBodyStub: emailHeadersBody = {
  alertUuid: "alertUuid",
  bodyHtml:
    "<span>Hello,\nThis is an <strong>important</strong> email.\nThank you!</span>",
  bodyText: "Hello,This is an important email. Thank you!",
  headers: "Totally\nLegit\nHeaders",
};
const emailHeadersBodyStubOnlyHtml: emailHeadersBody = {
  alertUuid: "alertUuid",
  bodyHtml:
    "<span>Hello,\nThis is an <strong>important</strong> email.\nThank you!</span>",
  bodyText: "",
  headers: "Totally\nLegit\nHeaders",
};
const emailHeadersBodyStubOnlyText: emailHeadersBody = {
  alertUuid: "alertUuid",
  bodyHtml: "",
  bodyText: "Hello,This is an important email. Thank you!",
  headers: "Totally\nLegit\nHeaders",
};

describe("EmailAnalysisHeadersBody", () => {
  it("renders correctly when emailHeadersBody cannot be fetched", () => {
    cy.stub(Event, "readEmailHeadersAndBody")
      .as("fetchHeadersAndBody")
      .rejects(new Error("Request failed with status code 404"));
    factory();
    cy.contains(
      "Couldn't load email details: Request failed with status code 404",
    ).should("be.visible");
  });
  it("renders title and headers correctly", () => {
    cy.stub(Event, "readEmailHeadersAndBody")
      .withArgs("uuid")
      .as("fetchHeadersAndBody")
      .resolves(emailHeadersBodyStub);
    factory();
    cy.contains("Email Details (Alert)").should("be.visible");
    cy.findByText("(Alert)")
      .invoke("attr", "href")
      .should("contain", `/alert/${emailHeadersBodyStub.alertUuid}`);
    cy.contains("Headers")
      .parent()
      .parent()
      .children()
      .find("pre")
      .should("contain.text", emailHeadersBodyStub.headers);
  });
  it("renders correctly when emailHeadersBody can be fetched and both text and html are given", () => {
    cy.stub(Event, "readEmailHeadersAndBody")
      .withArgs("uuid")
      .as("fetchHeadersAndBody")
      .resolves(emailHeadersBodyStub);
    factory();
    cy.contains("Body").should("be.visible");
    cy.contains("Body Text")
      .siblings()
      .should("contain.text", emailHeadersBodyStub.bodyText);
    cy.get("#divider").should("exist");
    cy.contains("Body HTML")
      .siblings()
      .should("contain.text", emailHeadersBodyStub.bodyHtml);
  });
  it("renders correctly when emailHeadersBody can be fetched and only text is given", () => {
    cy.stub(Event, "readEmailHeadersAndBody")
      .withArgs("uuid")
      .as("fetchHeadersAndBody")
      .resolves(emailHeadersBodyStubOnlyText);
    factory();
    cy.contains("Body").should("be.visible");
    cy.contains("Body Text")
      .siblings()
      .should("contain.text", emailHeadersBodyStub.bodyText);
    cy.get("#divider").should("not.exist");
    cy.contains("Body HTML").should("not.exist");
  });
  it("renders correctly when emailHeadersBody can be fetched and only html is given", () => {
    cy.stub(Event, "readEmailHeadersAndBody")
      .withArgs("uuid")
      .as("fetchHeadersAndBody")
      .resolves(emailHeadersBodyStubOnlyHtml);
    factory();
    cy.contains("Body").should("be.visible");
    cy.contains("Body Text").should("not.exist");
    cy.get("#divider").should("not.exist");
    cy.contains("Body HTML")
      .siblings()
      .should("contain.text", emailHeadersBodyStub.bodyHtml);
  });
});
