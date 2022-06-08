import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import AnalysisDetailsBase from "@/components/Analysis/AnalysisDetailsBase.vue";
import { analysisRead } from "@/models/analysis";
import { testConfiguration } from "@/etc/configuration/test";
import { analysisReadFactory } from "@mocks/analysis";

const analysisDetails = {
  id: "1",
  name: "Test Analysis",
  description: "Test Analysis Description",
  createdAt: "2020-01-01T00:00:00.000Z",
  updatedAt: "2020-01-01T00:00:00.000Z",
  status: "pending",
  type: "analysis",
  owner: { id: "1", name: "Test User" },
  project: { id: "1", name: "Test Project" },
};

// Pretty printed string
const expectedAnalysisDetailsString =
  '{\n    "id": "1",\n    "name": "Test Analysis",\n    "description": "Test Analysis Description",\n    "createdAt": "2020-01-01T00:00:00.000Z",\n    "updatedAt": "2020-01-01T00:00:00.000Z",\n    "status": "pending",\n    "type": "analysis",\n    "owner": {\n        "id": "1",\n        "name": "Test User"\n    },\n    "project": {\n        "id": "1",\n        "name": "Test Project"\n    }\n}';

interface analysisDetailsBaseProps {
  analysis?: analysisRead;
}

function factory(props: analysisDetailsBaseProps = {}) {
  return mount(AnalysisDetailsBase, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}

describe("AnalysisDetailsBase", () => {
  it("renders expected message when not given analysis prop", () => {
    factory();
    cy.contains("Analysis is unavailable.").should("be.visible");
    cy.contains("No analysis details available.").should("not.exist");
  });
  it("renders expected message when given analysis prop that does not contain details", () => {
    factory({ analysis: analysisReadFactory({ details: null }) });
    cy.contains("Analysis is unavailable.").should("not.exist");
    cy.contains("No analysis details available.").should("be.visible");
  });
  it("renders pretty-printed analysis details when given analysis prop containing details", () => {
    factory({ analysis: analysisReadFactory({ details: analysisDetails }) });
    cy.contains("Analysis is unavailable.").should("not.exist");
    cy.contains("No analysis details available.").should("not.exist");
    cy.get("pre").should("contain.text", expectedAnalysisDetailsString);
  });
});
