import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import { Event } from "@/services/api/event";

import EmailAnalysisSummaryTable from "@/components/Analysis/EmailAnalysisSummaryTable.vue";
import router from "@/router/index";
import { emailSummary } from "@/models/eventSummaries";

const props = {
  eventUuid: "uuid",
};

function factory() {
  return mount(EmailAnalysisSummaryTable, {
    global: {
      plugins: [PrimeVue, createPinia(), router],
    },
    propsData: props,
  });
}

describe("EmailAnalysisSummaryTable", () => {
  it("renders correctly when call to fetch email summary fails", () => {
    cy.stub(Event, "readEmailSummary")
      .as("fetchEmailSummary")
      .rejects(new Error("Request failed with status code 404"));
    factory();
    cy.contains(
      "Could not find any emails. Request failed with status code 404",
    ).should("be.visible");
  });
  it("renders correctly when call to fetch email summary is successful but nothing is returned", () => {
    const emailSummaries: emailSummary[] = [];

    cy.stub(Event, "readEmailSummary")
      .withArgs("uuid")
      .as("fetchEmailSummary")
      .resolves(emailSummaries);
    factory();
    cy.contains("Could not find any emails.").should("be.visible");
  });
  it("renders correctly when call to fetch email summary is successful and returns results", () => {
    const emailSummaries: emailSummary[] = [
      {
        alertUuid: "alertUuid",
        attachments: [],
        ccAddresses: ["otherguy@company.com"],
        fromAddress: "123abc@evil.com",
        messageId: "<123abc@evil.com>",
        replyToAddress: null,
        subject: "Hello",
        time: "2022-02-29T12:00:00.000000+00:00",
        toAddress: "to@company.com",
      },
    ];

    const emailSummaryTableCols = [
      "URL",
      "Time (UTC)",
      "From",
      "To",
      "Subject",
      "Attachments",
      "CC",
      "Reply-To",
      "Message-ID",
    ];
    const emailSummaryTableValues = [
      "Alert",
      "3/1/2022, 12:00:00 PM UTC",
      "123abc@evil.com",
      "to@company.com",
      "Hello",
      "None",
      "otherguy@company.com",
      "None",
      "<123abc@evil.com>",
    ];

    cy.stub(Event, "readEmailSummary")
      .withArgs("uuid")
      .as("fetchEmailSummary")
      .resolves(emailSummaries);
    factory();

    // Check columns and values
    cy.get("tr")
      .eq(0)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", emailSummaryTableCols[index]);
      });
    cy.get("tr")
      .eq(1)
      .children()
      .each(($li, index) => {
        cy.wrap($li).should("have.text", emailSummaryTableValues[index]);

        // Check link back to given email's alert
        if (index === 0) {
          cy.wrap($li)
            .find("a")
            .invoke("attr", "href")
            .should("contain", `/alert/${emailSummaries[0].alertUuid}`);
        }
      });
  });
});
