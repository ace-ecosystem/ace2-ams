import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import RemoveTagModal from "@/components/Modals/RemoveTagModal.vue";
import BaseModal from "@/components/Modals/BaseModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { nodeTagRead } from "@/models/nodeTag";
import { alertReadFactory } from "@mocks/alert";
import { NodeTag } from "@/services/api/nodeTag";
import { Alert } from "@/services/api/alert";
import { observableTreeRead } from "@/models/observable";
import { ObservableInstance } from "@/services/api/observable";
import { observableTreeReadFactory } from "@mocks/observable";

const existingTag = genericObjectReadFactory({ value: "existingTag" });
const testTag = genericObjectReadFactory({ value: "testTag" });
const otherTag = genericObjectReadFactory({ value: "otherTag" });

function factory(
  args: {
    selected: string[];
    openAlertTags: nodeTagRead[];
    existingTags: nodeTagRead[];
    nodeType: "alerts" | "events" | "observable";
    reloadObject: "node" | "table";
    observable: undefined | observableTreeRead;
  } = {
    selected: [],
    openAlertTags: [],
    existingTags: [],
    nodeType: "alerts",
    reloadObject: "node",
    observable: undefined,
  },
) {
  return mount(RemoveTagModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            alertStore: {
              open: alertReadFactory({
                uuid: "uuid",
                tags: args.openAlertTags,
              }),
            },
            alertTableStore: {
              visibleQueriedItems: [
                alertReadFactory({ uuid: "uuidA", tags: [testTag, otherTag] }),
                alertReadFactory({
                  uuid: "uuidB",
                  tags: [existingTag, testTag],
                }),
                alertReadFactory({ uuid: "uuidC", tags: [] }),
              ],
              totalItems: 0,
              sortField: "eventTime",
              sortOrder: "desc",
              pageSize: 10,
              requestReload: false,
              stateFiltersLoaded: false,
              routeFiltersLoaded: false,
            },
            selectedAlertStore: {
              selected: args.selected,
            },
            nodeTagStore: {
              items: args.existingTags,
            },
          },
        }),
      ],
    },
    propsData: {
      name: "RemoveTagModal",
      reloadObject: args.reloadObject,
      nodeType: args.nodeType,
      observable: args.observable,
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("RemoveTagModal");
    cy.get("[data-cy=RemoveTagModal]").should("be.visible");
    cy.contains("Remove Tag(s)").should("be.visible");
    cy.get('[data-cy="chips-container"]').should("be.visible");
    cy.contains("Select from existing tags").should("be.visible");
    cy.contains("Nevermind").should("be.visible");
    cy.findByText("Remove").should("be.visible");
    Cypress.vueWrapper.findComponent(BaseModal).vm.$emit("show");
  });
}

describe("RemoveTagModal", () => {
  it("renders", () => {
    factory();
  });
  it("will use given observable's current tags as existing tag options if the given nodeType is 'observable'", () => {
    factory({
      selected: [],
      existingTags: [existingTag, testTag, otherTag],
      openAlertTags: [],
      nodeType: "observable",
      reloadObject: "node",
      observable: observableTreeReadFactory({
        tags: [existingTag, testTag],
      }),
    });

    cy.contains("Select from existing tags").click();
    cy.contains("existingTag").should("be.visible");
    cy.contains("testTag").should("be.visible");
    cy.contains("otherTag").should("not.exist");
  });
  it("will use selected node's current tags as existing tag options if the given nodeType is not 'observable' and reloadObject is 'node'", () => {
    factory({
      selected: ["uuid"],
      openAlertTags: [testTag, otherTag],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });

    cy.contains("Select from existing tags").click();
    cy.contains("existingTag").should("not.exist");
    cy.contains("testTag").should("be.visible");
    cy.contains("otherTag").should("be.visible");
  });
  it("enables 'Add' button when given nodeType is 'observable' and 1 or more tags added", () => {
    factory({
      selected: [],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "observable",
      reloadObject: "node",
      observable: observableTreeReadFactory({
        tags: [existingTag, testTag],
      }),
    });
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.get("[data-cy='remove-button']").should("not.be.disabled");
  });
  it("enables 'Add' button when given nodeType is not 'observable', selectedStore has 1 or more nodes selected, and 1 or more tags added", () => {
    factory({
      selected: ["uuid"],
      openAlertTags: [testTag, otherTag],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.get("[data-cy='remove-button']").should("not.be.disabled");
  });
  it("disables 'Add' button when given nodeType is 'observable' and no tags are added to form", () => {
    factory({
      selected: [],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "observable",
      reloadObject: "node",
      observable: observableTreeReadFactory({
        tags: [existingTag, testTag],
      }),
    });
    cy.get("[data-cy='remove-button']").should("be.disabled");
  });
  it("disables 'Add' button when given nodeType is not 'observable', selectedStore has 1 or more nodes selected, and no tags added", () => {
    factory({
      selected: ["uuid"],
      openAlertTags: [],
      existingTags: [],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });
    cy.get("[data-cy='remove-button']").should("be.disabled");
  });
  it("disables 'Add' button when given nodeType is not 'observable', selectedStore has no nodes selected, and 1 or more tags added", () => {
    factory({
      selected: [],
      openAlertTags: [],
      existingTags: [],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.get("[data-cy='remove-button']").should("be.disabled");
  });
  it("will fetch and use all available tags in nodeTagStore as as existing tag options if the given nodeType is not 'observable' and reloadObject is not 'node'", () => {
    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .resolves([existingTag, testTag, otherTag]);

    factory({
      selected: ["uuidA", "uuidB"],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "table",
      observable: undefined,
    });

    cy.get("@readAllTags").should("have.been.calledOnce");

    cy.contains("Select from existing tags").click();
    cy.contains("existingTag").should("be.visible");
    cy.contains("testTag").should("be.visible");
    cy.contains("otherTag").should("be.visible");
  });
  it("will make the expected call to update an observable's tags w/o tags in form when 'Remove' is clicked and the given nodeType is 'observable'", async () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        tags: ["testTag"],
      })
      .as("updateObservable")
      .resolves();

    factory({
      selected: [],
      existingTags: [existingTag, testTag, otherTag],
      openAlertTags: [],
      nodeType: "observable",
      reloadObject: "node",
      observable: observableTreeReadFactory({
        tags: [existingTag, testTag],
      }),
    });

    cy.contains("Select from existing tags").click();
    cy.contains("existingTag").click();
    cy.get("[data-cy='remove-button']").click();
    cy.get("@updateObservable").should("have.been.calledOnce");
  });
  it("will make the expected call to update a single node's tags w/o tags in form when 'Remove' is clicked and the given nodeType is not 'observable' and reloadObject is 'node'", () => {
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          tags: ["otherTag"],
        },
      ])
      .as("updateAlert")
      .resolves();

    factory({
      selected: ["uuid"],
      openAlertTags: [testTag, otherTag],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });

    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get("[data-cy='remove-button']").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
  });
  it("will make the expected call to update multiple node's tags w/o tags in form when 'Remove' is clicked and the given nodeType is not 'observable' and reloadObject is not 'node'", () => {
    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .resolves([existingTag, testTag, otherTag]);

    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuidA",
          tags: ["otherTag"],
        },
        {
          uuid: "uuidB",
          tags: ["existingTag"],
        },
        {
          uuid: "uuidC",
          tags: [],
        },
      ])
      .as("updateAlerts")
      .resolves();

    factory({
      selected: ["uuidA", "uuidB", "uuidC"],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "table",
      observable: undefined,
    });

    cy.get("@readAllTags").should("have.been.calledOnce");

    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get("[data-cy='remove-button']").click();
    cy.get("@updateAlerts").should("have.been.calledOnce");
  });
  it("will show an error if attempt to fetch all node tags fails", () => {
    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .rejects(new Error("404 request failed !"));

    factory({
      selected: ["uuidA", "uuidB", "uuidC"],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "table",
      observable: undefined,
    });

    cy.get("@readAllTags").should("have.been.calledOnce");
    cy.contains("404 request failed !").should("be.visible");
  });
  it("will show an error if attempt to update an observable's tags fails", () => {
    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        tags: ["testTag"],
      })
      .as("updateObservable")
      .rejects(new Error("404 request failed !"));

    factory({
      selected: [],
      openAlertTags: [],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "observable",
      reloadObject: "node",
      observable: observableTreeReadFactory({
        tags: [existingTag, testTag],
      }),
    });

    cy.contains("Select from existing tags").click();
    cy.contains("existingTag").click();
    cy.get("[data-cy='remove-button']").click();
    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.contains("404 request failed !").should("be.visible");
  });
  it("will show an error if attempt to update one or more node's tags fails", () => {
    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          tags: ["otherTag"],
        },
      ])
      .as("updateAlert")
      .rejects(new Error("404 request failed !"));

    factory({
      selected: ["uuid"],
      openAlertTags: [testTag, otherTag],
      existingTags: [existingTag, testTag, otherTag],
      nodeType: "alerts",
      reloadObject: "node",
      observable: undefined,
    });

    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get("[data-cy='remove-button']").click();
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.contains("404 request failed !").should("be.visible");
  });
});
