import { mount } from "@cypress/vue";

import PrimeVue from "primevue/config";

import ObservableLeaf from "@/components/Observables/ObservableLeaf.vue";
import router from "@/router/index";
import { observableActionUrl, observableTreeRead } from "@/models/observable";
import { observableTreeReadFactory } from "@mocks/observable";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { userReadFactory } from "@mocks/user";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { testConfiguration } from "@/etc/configuration/test";
import { ObservableInstance } from "@/services/api/observable";
import ToastService from "primevue/toastservice";
import Tooltip from "primevue/tooltip";
import TagModalVue from "@/components/Modals/TagModal.vue";
import { analysisMetadataReadFactory } from "@mocks/analysisMetadata";
import {
  metadataDetectionPointReadFactory,
  metadataDisplayTypeReadFactory,
  metadataDisplayValueReadFactory,
  metadataTagReadFactory,
  metadataTimeReadFactory,
} from "@mocks/metadata";

interface ObservableLeafProps {
  observable: observableTreeRead;
  showCopyToClipboard?: boolean;
  showActionsMenu?: boolean;
  showTags?: boolean;
}

const defaultProps: ObservableLeafProps = {
  observable: observableTreeReadFactory(),
};

function factory(
  args: {
    props: ObservableLeafProps;
    config: Record<string, unknown>;
  } = {
    props: defaultProps,
    config: testConfiguration,
  },
) {
  return mount(ObservableLeaf, {
    global: {
      directives: { tooltip: Tooltip },
      plugins: [
        PrimeVue,
        ToastService,
        createCustomCypressPinia({
          initialState: {
            authStore: {
              user: userReadFactory(),
            },
          },
        }),
        router,
      ],
      provide: {
        config: args.config,
        objectType: "alerts",
      },
    },
    propsData: args.props,
  });
}

const observableWithDisplayType = observableTreeReadFactory({
  value: "Observable with display type",
  analysisMetadata: analysisMetadataReadFactory({
    displayType: metadataDisplayTypeReadFactory({ value: "displayType" }),
  }),
});

const observableWithDisplayValue = observableTreeReadFactory({
  value: "Observable with display value",
  analysisMetadata: analysisMetadataReadFactory({
    displayValue: metadataDisplayValueReadFactory({ value: "displayValue" }),
  }),
});

const observableWithTags = observableTreeReadFactory({
  value: "Observable w/ Tags",
  children: [],
  tags: [metadataTagReadFactory({ value: "testTag" })],
});

const observableWithTime = observableTreeReadFactory({
  value: "Observable w/ Time",
  children: [],
  analysisMetadata: analysisMetadataReadFactory({
    time: metadataTimeReadFactory({
      value: "2022-02-24T00:00:00.000000+00:00",
    }),
  }),
});

const observableWithDispositionHistory = observableTreeReadFactory({
  value: "Observable w/ DispositionHistory",
  children: [],
  dispositionHistory: [
    { count: 1, disposition: "testDisposition", percent: 100 },
  ],
});

const observableWithDetectionPoints = observableTreeReadFactory({
  value: "Observable w/ Detection Points",
  analysisMetadata: analysisMetadataReadFactory({
    detectionPoints: [
      metadataDetectionPointReadFactory({
        value: "test detection point1",
      }),
      metadataDetectionPointReadFactory({
        value: "test detection point2",
      }),
    ],
  }),
});

const observableWithForDetectionEnabled = observableTreeReadFactory({
  value: "Observable w/ For Detection Enabled",
  forDetection: true,
});

const ipv4Observable = observableTreeReadFactory({
  value: "1.2.3.4",
  type: genericObjectReadFactory({ value: "ipv4" }),
});
describe("ObservableLeaf", () => {
  it("renders correctly with all optional props set to false", () => {
    factory({
      props: {
        observable: observableWithTags,
        showCopyToClipboard: false,
        showActionsMenu: false,
        showTags: false,
      },
      config: testConfiguration,
    });
    cy.contains("testObservableType: Observable w/ Tags")
      .should("be.visible")
      .should("have.css", { color: "black" });
    cy.findByRole("button").should("not.exist");
    cy.get("[data-cy=detection-point-symbol]").should("not.exist");
  });
  it("renders correctly with default props", () => {
    factory({
      props: { observable: observableWithTags },
      config: testConfiguration,
    });
    cy.contains("testObservableType: Observable w/ Tags")
      .should("be.visible")
      .should("have.css", { color: "black" });
    cy.findAllByRole("button").should("have.length", 2);
    cy.get("span").contains("testTag");
  });

  it("renders correctly when observable has a display type", () => {
    factory({
      props: { observable: observableWithDisplayType },
      config: testConfiguration,
    });
    cy.contains(
      "displayType (testObservableType): Observable with display type",
    )
      .should("be.visible")
      .should("have.css", { color: "black" });
    cy.findAllByRole("button").should("have.length", 2);
  });

  it("renders correctly when observable has a display value", () => {
    factory({
      props: { observable: observableWithDisplayValue },
      config: testConfiguration,
    });
    cy.contains("testObservableType: displayValue")
      .should("be.visible")
      .should("have.css", { color: "black" });
    cy.findAllByRole("button").should("have.length", 2);
  });

  it("loads common and observable type-specific actions from config, if available", () => {
    factory({
      props: { observable: ipv4Observable },
      config: testConfiguration,
    });

    const expectedMenuItems = [
      "Test Action",
      "Enable Detection",
      "Subheader",
      "IPV4 Command",
    ];

    cy.get("[data-cy='show-actions-menu-button']").click();
    cy.findAllByRole("menuitem")
      .should("have.length", 4)
      .each((menuItem, index) => {
        cy.wrap(menuItem).should("have.text", expectedMenuItems[index]);
      });
  });
  it("observable actions menu toggle button will not show if no actions are available", () => {
    factory({
      props: { observable: observableWithTags },
      config: {
        observables: { commonObservableActions: [], observableMetadata: [] },
      },
    });
    cy.get("[data-cy='show-actions-menu-button']").should("not.exist");
  });
  it("loads style from config, if available", () => {
    factory({
      props: { observable: ipv4Observable },
      config: testConfiguration,
    });
    cy.contains("ipv4: 1.2.3.4")
      .should("be.visible")
      .should("have.css", { color: "blue" });
  });
  it("attempts to open modal when 'modal'-type observable action clicked", () => {
    factory({
      props: { observable: observableWithForDetectionEnabled },
      config: testConfiguration,
    });
    cy.get("[data-cy='show-actions-menu-button']").click();
    cy.contains("Update Expiration").click();
    cy.get("@stub-11").should("have.been.calledOnce");
    cy.findByRole("menu").should("not.exist"); // Menu should have been closed
  });
  it("attempts to run command when 'command'-type observable action clicked", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        forDetection: true,
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .resolves();

    factory({
      props: { observable: observableWithTags },
      config: testConfiguration,
    });
    cy.get("[data-cy='show-actions-menu-button']").click();
    cy.contains("Enable Detection").click();

    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.findByRole("menu").should("not.exist"); // Menu should have been closed
  });
  it("displays error message if 'command'-type observable action clicked, but command fails", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        forDetection: true,
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .rejects(new Error("404 request failed"));

    factory({
      props: { observable: observableWithTags },
      config: testConfiguration,
    });
    cy.get("[data-cy='show-actions-menu-button']").click();
    cy.contains("Enable Detection").click();

    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.get("[data-cy='observable-action-error']")
      .contains("'Enable Detection' Failed")
      .should("be.visible");
    cy.get("[data-cy='observable-action-error']")
      .contains("404 request failed")
      .should("be.visible");
    cy.findByRole("menu").should("not.exist"); // Menu should have been closed
  });
  it("displays a fire emoji for every detection point belonging to the observable", () => {
    factory({
      props: { observable: observableWithDetectionPoints },
      config: testConfiguration,
    });
    cy.get("span").should(
      "contain.text",
      "testObservableType: Observable w/ Detection Points",
    );
    cy.get("[data-cy=detection-point-symbol]").should("have.length", 2);
  });
  it("displays timestamp associated with observable, if available", () => {
    factory({
      props: { observable: observableWithTime },
      config: testConfiguration,
    });
    cy.get("span").should(
      "contain.text",
      "testObservableType: Observable w/ Time @ 2/24/2022, 12:00:00 AM UTC",
    );
  });
  it("displays disposition history group for observable, if available", () => {
    factory({
      props: { observable: observableWithDispositionHistory },
      config: testConfiguration,
    });
    cy.get("[data-cy=disposition-tag]")
      .should("be.visible")
      .should("contain.text", "testDisposition")
      .should("contain.text", "100%")
      .should("contain.text", "(1)");
  });
  it("sets the alert filters to the an observable's type and value when clicked", () => {
    factory({
      props: { observable: observableWithTags },
      config: testConfiguration,
    });
    cy.contains("Observable w/ Tags").click();
    cy.get("@stub-5").should("have.been.calledWith", {
      objectType: "alerts",
      filters: {
        observable: {
          included: [
            {
              category: observableWithTags.type,
              value: observableWithTags.value,
            },
          ],
          notIncluded: [],
        },
      },
    });
  });

  it("sets the alert filters to the an observable's type and value when clicked if there is a display type", () => {
    factory({
      props: { observable: observableWithDisplayType },
      config: testConfiguration,
    });
    cy.contains("Observable with display type").click();
    cy.get("@stub-5").should("have.been.calledWith", {
      objectType: "alerts",
      filters: {
        observable: {
          included: [
            {
              category: observableWithDisplayType.type,
              value: observableWithDisplayType.value,
            },
          ],
          notIncluded: [],
        },
      },
    });
  });

  it("sets the alert filters to the an observable's type and value when clicked if there is a display value", () => {
    factory({
      props: { observable: observableWithDisplayValue },
      config: testConfiguration,
    });
    cy.contains("displayValue").click();
    cy.get("@stub-5").should("have.been.calledWith", {
      objectType: "alerts",
      filters: {
        observable: {
          included: [
            {
              category: observableWithDisplayValue.type,
              value: observableWithDisplayValue.value,
            },
          ],
          notIncluded: [],
        },
      },
    });
  });

  it("attempts to requestReload on the alert store when child component emits 'requestReload", () => {
    let alertStore: any;
    factory({
      props: { observable: observableWithTags },
      config: testConfiguration,
    }).then((wrapper) => {
      alertStore = wrapper.vm.alertStore;
      cy.wrap(alertStore.requestReload).should("be.false");
    });
    cy.get('[data-cy="show-actions-menu-button"]').click();
    cy.contains("Test Action")
      .click()
      .then(() => {
        Cypress.vueWrapper.findComponent(TagModalVue).vm.$emit("requestReload");
        cy.wrap(alertStore.requestReload).should("be.true");
      });
  });
});

// Because this test changes the testing URL, it needs to be isolated
describe("ObservableLeaf URL test", () => {
  it("attempts to reroute to given URL when 'url'-type observable action clicked", () => {
    const urlTypeObservableAction: observableActionUrl = {
      type: "url",
      label: "Go to URL",
      description: "Test url",
      icon: "pi pi-link",
      url: "www.google.com",
    };

    factory({
      props: { observable: observableWithTags },
      config: {
        observables: {
          commonObservableActions: [urlTypeObservableAction],
          observableMetadata: [],
        },
      },
    });

    cy.get("[data-cy='show-actions-menu-button']").click();
    cy.contains("Go to URL").click();
    cy.location("pathname").should("contain", "www.google.com");
  });
});
