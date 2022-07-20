import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";
import { alertTreeReadFactory } from "@mocks/alert";
import { rootAnalysisTreeReadFactory } from "@mocks/analysis";
import AlertTreeVue from "@/components/Alerts/AlertTree.vue";
import { analysisMetadataReadFactory } from "@mocks/analysisMetadata";

import AlertTreeContainer from "@/components/Alerts/AlertTreeContainer.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import router from "@/router/index";
import { observableTreeRead } from "@/models/observable";
import { observableTreeReadFactory } from "@mocks/observable";
import {
  analysisModuleTypeAlertTreeReadFactory,
  analysisTreeReadFactory,
} from "@mocks/analysis";
import { testConfiguration } from "@/etc/configuration/test";
import ToastService from "primevue/toastservice";
import { metadataTagReadFactory } from "@mocks/metadata";
import Tooltip from "primevue/tooltip";

const childObservable = observableTreeReadFactory({
  value: "Child Observable",
});
const childAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
    value: "Child Analysis",
  }),
  children: [childObservable],
});
const parentObservable = observableTreeReadFactory({
  value: "Parent Observable",
  children: [childAnalysis],
  tags: [metadataTagReadFactory({ value: "testTag" })],
});

const criticalChildObservable = observableTreeReadFactory({
  value: "Child Observable",
  analysisMetadata: analysisMetadataReadFactory({
    criticalPoints: [{ value: "critical" }],
  }),
  criticalPath: true,
});
const criticalChildAnalysis = analysisTreeReadFactory({
  analysisModuleType: analysisModuleTypeAlertTreeReadFactory({
    value: "Child Analysis",
  }),
  children: [criticalChildObservable],
  criticalPath: true,
});
const criticalParentObservable = observableTreeReadFactory({
  value: "Parent Observable",
  children: [criticalChildAnalysis],
  tags: [metadataTagReadFactory({ value: "testTag" })],
  criticalPath: true,
});

function factory(args: { initialAlertChildren: observableTreeRead[] }) {
  const initialAlert = alertTreeReadFactory({
    rootAnalysis: rootAnalysisTreeReadFactory({
      children: args.initialAlertChildren,
    }),
  });
  return mount(AlertTreeContainer, {
    global: {
      directives: { tooltip: Tooltip },
      plugins: [
        createCustomCypressPinia({
          initialState: {
            alertStore: {
              open: initialAlert,
            },
          },
        }),
        PrimeVue,
        router,
        ToastService,
      ],
      provide: { objectType: "alerts", config: testConfiguration },
    },
  });
}

describe("AlertTree", () => {
  it("renders toolbar as expected", () => {
    factory({
      initialAlertChildren: [],
    });
    cy.get('[type="checkbox"]').should("be.checked");
    cy.get('[type="checkbox"]').parent().should("be.visible");
    cy.contains("Critical Analysis").should("be.visible");
    cy.get(".pi-question-circle").should("be.visible");
    cy.contains("Expand All").should("be.visible");
    cy.contains("Collapse All").should("be.visible");
  });
  it("renders when there are no children to show", () => {
    factory({
      initialAlertChildren: [],
    });
    cy.contains("No alert data to display.").should("be.visible");
  });
  it("renders when there are children to show", () => {
    factory({
      initialAlertChildren: [parentObservable],
    }).then((wrapper) => {
      expect(wrapper.findComponent(AlertTreeVue)).to.exist;
    });
  });
  it("switches between critical and all analysis view as expected", () => {
    factory({
      initialAlertChildren: [parentObservable],
    });
    // Critical view -- default
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Analysis").should("not.exist");
    cy.contains("Child Observable").should("not.exist");
    // Switch to all view
    cy.get('[type="checkbox"]').parent().parent().click();
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Analysis").should("be.visible");
    cy.contains("Child Observable").should("be.visible");
    // Switch back to critical view
    cy.get('[type="checkbox"]').parent().parent().click();
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Observable").should("not.exist");
    cy.contains("Child Analysis").should("not.exist");
  });
  it("collapses and expands as expected", () => {
    factory({
      initialAlertChildren: [criticalParentObservable],
    });
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Analysis").should("be.visible");
    cy.contains("Child Observable").should("be.visible");

    cy.contains("Collapse All").click();
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Analysis").should("not.be.visible");
    cy.contains("Child Observable").should("not.be.visible");

    cy.contains("Expand All").click();
    cy.contains("Parent Observable").should("be.visible");
    cy.contains("Child Analysis").should("be.visible");
    cy.contains("Child Observable").should("be.visible");
  });
});
