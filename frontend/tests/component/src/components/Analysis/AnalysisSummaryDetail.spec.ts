import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import AnalysisSummaryDetail from "@/components/Analysis/AnalysisSummaryDetail.vue";
import { analysisSummaryDetailRead } from "@/models/analysisSummaryDetail";
import { testConfiguration } from "@/etc/configuration/test";
import { alertTreeReadFactory } from "@mocks/alert";
import { rootAnalysisTreeReadFactory } from "@mocks/analysis";
import { stringLiteral } from "@babel/types";
import { genericObjectReadFactory } from "@mocks/genericObject";


interface analysisSummaryDetailProps {
  analysis?: analysisSummaryDetailRead;
}

function factory(props: analysisSummaryDetailProps = {}) {
  return mount(AnalysisSummaryDetail, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: { config: testConfiguration },
    },
    propsData: props,
  });
}


// alertTreeReadFactory({
//     rootAnalysis: rootAnalysisTreeReadFactory({
//       details: { test: "content" },
//     }),
//     type: genericObjectReadFactory({ value: "test type - a" }),
//   })

  describe("AnalysisDetailsBase", () => {
    it("displays summary detail in plaintext if summary format is not pre", () => {
        const summary={
            content: "test",
            format: genericObjectReadFactory(),
            header: "testHeader",
            uuid: "1111",
        };
        factory({summary:summary})
        cy.get('span').should('have.text','test')
    })
    it("displays summary detail in pre if summary format is not plaintext", () => {
        const summary={
            content: "test",
            format: genericObjectReadFactory({value:"pre"}),
            header: "testHeader",
            uuid: "1111",
        };
        factory({summary:summary})
        cy.get('pre').should('have.text','test')
    })
  });