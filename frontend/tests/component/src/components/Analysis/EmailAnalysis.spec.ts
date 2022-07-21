import { mount } from "@cypress/vue";
import { createPinia } from "pinia";

import PrimeVue from "primevue/config";

import EmailAnalysisSummaryTable from "@/components/Analysis/EmailAnalysisSummaryTable.vue";
import EmailAnalysisHeadersBody from "@/components/Analysis/EmailAnalysisHeadersBody.vue";
import EmailAnalysis from "@/components/Analysis/EmailAnalysis.vue";
import router from "@/router/index";

const props = {
  eventUuid: "uuid",
};

describe("EmailAnalysis", () => {
  it("renders", () => {
    mount(EmailAnalysis, {
      global: {
        plugins: [PrimeVue, createPinia(), router],
      },
      propsData: props,
    }).then((wrapper) => {
      expect(wrapper.getComponent(EmailAnalysisSummaryTable)).to.exist;
      expect(wrapper.getComponent(EmailAnalysisHeadersBody)).to.exist;
    });
  });
});
