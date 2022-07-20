import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import AlertTree from "@/components/Alerts/AlertTree.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import router from "@/router/index";
import { observableTreeRead } from "@/models/observable";
import { analysisTreeRead } from "@/models/analysis";
import { observableTreeReadFactory } from "@mocks/observable";
import {
  analysisModuleTypeAlertTreeReadFactory,
  analysisTreeReadFactory,
  rootAnalysisTreeReadFactory,
} from "@mocks/analysis";
import { testConfiguration } from "@/etc/configuration/test";
import ToastService from "primevue/toastservice";
import { metadataTagReadFactory } from "@mocks/metadata";
import { genericObjectReadFactory } from "@mocks/genericObject";
import AnalysisSummaryDetailVue from "@/components/Analysis/AnalysisSummaryDetail.vue";

const childObservable = observableTreeReadFactory({
  value: "Child Observable",
});
const childAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
    value: "Child Analysis",
  }),
});
const childAnalysis2 = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
    value: "Child Analysis 2",
  }),
  criticalPath: false,
  children: [childObservable],
});
const parentObservable2 = observableTreeReadFactory({
  value: "Parent Observable 2",
  children: [childAnalysis2],
  tags: [metadataTagReadFactory({ value: "testTag" })],
  criticalPath: true,
});
const parentObservable = observableTreeReadFactory({
  value: "Parent Observable",
  children: [childAnalysis],
  tags: [metadataTagReadFactory({ value: "testTag" })],
  criticalPath: false,
});
const parentAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
    value: "Parent Analysis",
  }),
  children: [childObservable],
});
interface AlertTreeProps {
  items: (analysisTreeRead | observableTreeRead)[];
  alertId: string;
  criticalOnly: boolean;
}

const defaultProps: AlertTreeProps = {
  items: [],
  alertId: "test",
  criticalOnly: false,
};

function factory(
  args = {
    props: defaultProps,
  },
) {
  return mount(AlertTree, {
    global: {
      plugins: [createCustomCypressPinia(), PrimeVue, router, ToastService],
      provide: { objectType: "alerts", config: testConfiguration },
    },
    propsData: args.props,
  });
}

describe("AlertTree", () => {
  it("renders when there are no given items", () => {
    factory();
  });
  it("only renders criticalPath items when criticalOnly is true", () => {
    const props: AlertTreeProps = {
      items: [parentObservable2],
      alertId: "test",
      criticalOnly: true,
    };
    factory({ props: props });
    cy.contains("Parent Observable 2").should("be.visible");
    cy.contains("Child Analysis 2").should("be.visible");
    cy.contains("Child Observable").should("not.exist");
  });
  it("collapses as expected on collapseAll", () => {
    factory({
      props: {
        items: [parentObservable2],
        alertId: "test",
        criticalOnly: false,
      },
    }).then((wrapper) => {
      wrapper.vm.collapseAll();
      cy.contains("Parent Observable 2").should("be.visible");
      cy.contains("Child Analysis 2").should("not.be.visible");
      cy.contains("Child Observable").should("not.be.visible");
      cy.get(".p-tree-toggler-icon").eq(0).click();
      cy.contains("Parent Observable 2").should("be.visible");
      cy.contains("Child Analysis 2").should("be.visible");
      cy.contains("Child Observable").should("not.be.visible");
      cy.get(".p-tree-toggler-icon").eq(1).click();
      cy.contains("Parent Observable 2").should("be.visible");
      cy.contains("Child Analysis 2").should("be.visible");
      cy.contains("Child Observable").should("be.visible");
    });
  });
  it("expands as expected on expandAll", () => {
    factory({
      props: {
        items: [parentObservable2],
        alertId: "test",
        criticalOnly: false,
      },
    });
    cy.get(".p-tree-toggler-icon").eq(1).click();
    cy.get(".p-tree-toggler-icon").eq(0).click();
    cy.get("body").then(() => {
      const wrapperVm = Cypress.vueWrapper.vm as any;
      wrapperVm.expandAll();
    });
    cy.contains("Parent Observable 2").should("be.visible");
    cy.contains("Child Analysis 2").should("be.visible");
    cy.contains("Child Observable").should("be.visible");
  });
  it("correctly renders list items that include children", () => {
    factory({
      props: {
        items: [parentObservable, parentAnalysis],
        alertId: "test",
        criticalOnly: false,
      },
    });
    // 4 Visible to start
    cy.get("li").should("have.length", 4);

    // Check icons and values
    cy.get("li").eq(0).get(".pi-chevron-down");
    cy.get("li")
      .eq(0)
      .should("contain.text", "Parent Observable")
      .get(".pi-chevron-down");

    cy.get("li").eq(1).get(".pi-minus");
    cy.get("li")
      .eq(1)
      .should("contain.text", "Child Analysis")
      .get(".pi-minus");

    cy.get("li").eq(2).get(".pi-chevron-down");
    cy.get("li")
      .eq(2)
      .should("contain.text", "Parent Analysis")
      .get(".pi-chevron-down");

    cy.get("li").eq(3).get(".pi-minus");
    cy.get("li")
      .eq(3)
      .should("contain.text", "testObservableType")
      .get(".pi-minus");
  });
  it("toggles showing child objects (analysis or observables) when toggle clicked", () => {
    factory({
      props: {
        items: [parentObservable, parentAnalysis],
        alertId: "test",
        criticalOnly: false,
      },
    });
    // Click first toggle
    cy.get(".pi-chevron-down").eq(0).click();
    cy.contains("Child Analysis").should("not.be.visible");
    // Check newest
    cy.get("li")
      .eq(2)
      .should("contain.text", "Parent Analysis")
      .get(".pi-minus");

    // Click toggle again
    cy.get(".pi-chevron-right").eq(0).click();
    // Should be 3 again
    cy.get("li").should("have.length", 4);
    cy.contains("Child Analysis").should("exist");
  });
  it("renders analysis list items with a link to that analysis's specifc page", () => {
    factory({
      props: {
        items: [parentObservable, parentAnalysis],
        alertId: "test",
        criticalOnly: false,
      },
    });
    cy.contains("Parent Analysis")
      .invoke("attr", "href")
      .should("contain", "/alert/test/testUuid");
  });
  it("displays all Analysis Summary Details", () => {
    const summary = {
      content: "test1",
      format: genericObjectReadFactory(),
      header: "testHeader1",
      uuid: "1111",
    };
    const summary2 = {
      content: "test2",
      format: genericObjectReadFactory(),
      header: "testHeader2",
      uuid: "2222",
    };
    const parentAnalysisWithSummary = analysisTreeReadFactory({
      analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
        value: "Parent Analysis",
      }),
      children: [childObservable],
      summaryDetails: [summary, summary2],
    });
    factory({
      props: {
        items: [parentObservable, parentAnalysisWithSummary],
        alertId: "test",
      },
    });
    cy.contains("Summary Details").should("be.visible");
    // cy.get('#pv_id_2_header > .pi').click();
    cy.contains("testHeader1").should("be.visible");
    cy.contains("testHeader2").should("be.visible");
  });
});
