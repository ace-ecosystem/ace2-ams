import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import TagModal from "@/components/Modals/TagModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { nodeTagRead } from "@/models/nodeTag";
import { alertReadFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";
import { NodeTag } from "@/services/api/nodeTag";
import { Alert } from "@/services/api/alert";
import { observableTreeRead } from "@/models/observable";
import { ObservableInstance } from "@/services/api/observable";
import { observableTreeReadFactory } from "@mocks/observable";

const existingTag = genericObjectReadFactory({ value: "existingTag" });
const testTag = genericObjectReadFactory({ value: "testTag" });

function factory(
  args: {
    selected: string[];
    existingTags: nodeTagRead[];
    nodeType: "alerts" | "events" | "observable";
    reloadObject: "node" | "table";
    observable: undefined | observableTreeRead;
  } = {
    selected: [],
    existingTags: [],
    nodeType: "alerts",
    reloadObject: "node",
    observable: undefined,
  },
) {
  return mount(TagModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            alertStore: {
              open: alertReadFactory({
                uuid: "uuid",
                tags: args.existingTags,
              }),
            },
            alertTableStore: {
              visibleQueriedItems: [
                alertReadFactory({ uuid: "uuidA" }),
                alertReadFactory({ uuid: "uuidB" }),
              ],
              totalItems: 0,
              sortField: "eventTime",
              sortOrder: "desc",
              pageSize: 10,
              requestReload: false,
              stateFiltersLoaded: false,
              routeFiltersLoaded: false,
            },
            authStore: { user: userReadFactory() },
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
      name: "TagModal",
      reloadObject: args.reloadObject,
      nodeType: args.nodeType,
      observable: args.observable,
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("TagModal");
    cy.get("[data-cy=TagModal]").should("be.visible");
    cy.contains("Add Tags").should("be.visible");
    cy.get('[data-cy="chips-container"]').should("be.visible");
    cy.contains("Select from existing tags").should("be.visible");
    cy.contains("Nevermind").should("be.visible");
    cy.findByText("Add").should("be.visible");
  });
}

describe("TagModal", () => {
  it("renders", () => {
    factory();
  });
  it("displays correct empty message when there are no existing tags to select", () => {
    factory();
    cy.contains("Select from existing tags").click();
    cy.contains("No available options").should("be.visible");
  });
  it("adds existing tag to new tags list when clicked", () => {
    factory({
      selected: [],
      existingTags: [testTag],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.findByText("testTag").should("be.visible");
  });
  it("enables 'Add' button when there is a node selected and 1 or more tags added", () => {
    factory({
      selected: ["uuid"],
      existingTags: [],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").parent().should("not.be.disabled");
  });
  it("disables 'Add' button when there is not a node selected and 1 or more tags added", () => {
    factory();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").parent().should("be.disabled");
  });
  it("disables 'Add' button when there is a node selected and no tags added", () => {
    factory({
      selected: ["uuid"],
      existingTags: [],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.findByText("Add").parent().should("be.disabled");
  });
  it("attempts to create new tags and update selected nodes with new and existing tags and 'Add' clicked", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "newTag",
      })
      .as("createTag")
      .resolves();

    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .resolves([testTag, existingTag]);

    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          tags: ["testTag", "existingTag", "newTag"],
        },
      ])
      .as("updateAlert")
      .resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@createTag").should("have.been.calledOnce");
    cy.get("@readAllTags").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.get("[data-cy=TagModal]").should("not.exist");
  });
  it("attempts to update multiple alerts if multiple are selected in 'table' mode, tags are added to form, and 'Add' clicked", () => {
    const updateStub = cy.stub(Alert, "update");
    updateStub
      .withArgs([
        {
          uuid: "uuidA",
          tags: ["testTag", "existingTag"],
        },
        {
          uuid: "uuidB",
          tags: ["testTag", "existingTag"],
        },
      ])
      .as("updateAlerts")
      .resolves();

    factory({
      selected: ["uuidA", "uuidB"],
      existingTags: [testTag, existingTag],
      nodeType: "alerts",
      reloadObject: "table",
      observable: undefined,
    });
    // test that the tags are dedup'd with testTag
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("testTag")
      .type("{enter}");
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("existingTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@updateAlerts").should("have.been.calledOnce");
    cy.get("[data-cy=TagModal]").should("not.exist");
  });
  it("attempts to create new tags and update a given observable with new and existing tags and 'Add' clicked", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "newTag",
      })
      .as("createTag")
      .resolves();

    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .resolves([testTag, existingTag]);

    cy.stub(ObservableInstance, "update")
      .withArgs("observableUuid1", {
        tags: ["testTag", "existingTag", "newTag"],
        historyUsername: "analyst",
      })
      .as("updateObservable")
      .resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
      nodeType: "observable",
      reloadObject: "node",

      observable: observableTreeReadFactory({ tags: [testTag, existingTag] }),
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@createTag").should("have.been.calledOnce");
    cy.get("@readAllTags").should("have.been.calledOnce");
    cy.get("@updateObservable").should("have.been.calledOnce");
    cy.get("[data-cy=TagModal]").should("not.exist");
  });
  it("shows error if existing tags cannot be fetched", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "newTag",
      })
      .as("createTag")
      .resolves();

    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .rejects(new Error("404 request failed !"));

    cy.stub(Alert, "update").as("updateAlert").resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@createTag").should("have.been.calledOnce");
    cy.get("@readAllTags").should("have.been.calledOnce");
    cy.get("@updateAlert").should("not.have.been.called");
    cy.contains("404 request failed !").should("be.visible");
  });
  it("shows error if request to create a new tag fails", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "newTag",
      })
      .as("createTag")
      .rejects(new Error("404 request failed !"));

    cy.stub(NodeTag, "readAll").as("readAllTags").resolves();

    cy.stub(Alert, "update").as("updateAlert").resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@createTag").should("have.been.calledOnce");
    cy.get("@readAllTags").should("not.have.been");
    cy.get("@updateAlert").should("not.have.been");
    cy.contains("404 request failed !").should("be.visible");
  });
  it("shows error if request to update node tags fails", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "newTag",
      })
      .as("createTag")
      .resolves();

    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .resolves([testTag, existingTag]);

    cy.stub(Alert, "update")
      .withArgs([
        {
          uuid: "uuid",
          tags: ["testTag", "existingTag", "newTag"],
        },
      ])
      .as("updateAlert")
      .rejects(new Error("404 request failed !"));

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
      nodeType: "alerts",
      reloadObject: "node",

      observable: undefined,
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.get('[data-cy="chips-container"]')
      .click()
      .type("newTag")
      .type("{enter}");
    cy.findByText("Add").click();

    cy.get("@createTag").should("have.been.calledOnce");
    cy.get("@readAllTags").should("have.been.calledOnce");
    cy.get("@updateAlert").should("have.been.calledOnce");
    cy.contains("404 request failed !").should("be.visible");
  });
});
