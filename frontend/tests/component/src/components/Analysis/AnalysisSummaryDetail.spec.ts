import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import AnalysisSummaryDetail from "@/components/Analysis/AnalysisSummaryDetail.vue";
import { analysisSummaryDetailRead } from "@/models/analysisSummaryDetail";
import { testConfiguration } from "@/etc/configuration/test";
import { alertTreeReadFactory } from "@mocks/alert";
import { rootAnalysisTreeReadFactory } from "@mocks/analysis";


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

alertTreeReadFactory({
    rootAnalysis: rootAnalysisTreeReadFactory({
      details: { test: "content" },
    }),
    type: genericObjectReadFactory({ value: "test type - a" }),
  })
