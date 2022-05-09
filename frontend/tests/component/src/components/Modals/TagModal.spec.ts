import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import TagModal from "@/components/Modals/TagModal.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";
import { nodeTagRead } from "@/models/nodeTag";
import { alertReadFactory } from "@mocks/alert";
import { NodeTag } from "@/services/api/nodeTag";
import { Alert } from "@/services/api/alert";

const existingTag = genericObjectReadFactory({ value: "existingTag" });
const testTag = genericObjectReadFactory({ value: "testTag" });
const newTag = genericObjectReadFactory({ value: "newTag" });

function factory(
  args: { selected: string[]; existingTags: nodeTagRead[] } = {
    selected: [],
    existingTags: [],
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
            selectedAlertStore: {
              selected: args.selected,
            },
            nodeTagStore: {
              items: args.existingTags,
            },
          },
        }),
      ],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: {
      name: "TagModal",
      reloadObject: "node",
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
    });
    cy.contains("Select from existing tags").click();
    cy.contains("testTag").click();
    cy.findByText("testTag").should("be.visible");
  });
  it("enables 'Add' button when there is a node selected and 1 or more tags added", () => {
    factory({
      selected: ["uuid"],
      existingTags: [],
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
  it("shows error if existing tags cannot be fetched", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "testTag",
      })
      .as("createTag")
      .resolves();

    cy.stub(NodeTag, "readAll")
      .as("readAllTags")
      .rejects(new Error("404 request failed"));

    cy.stub(Alert, "update").as("updateAlert").resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
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
    cy.contains("404 request failed").should("be.visible");
  });
  it("shows error if request to create a new tag fails", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "testTag",
      })
      .as("createTag")
      .rejects(new Error("404 request failed"));

    cy.stub(NodeTag, "readAll").as("readAllTags").resolves();

    cy.stub(Alert, "update").as("updateAlert").resolves();

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
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
    cy.contains("404 request failed").should("be.visible");
  });
  it("shows error if request to update node tags fails", () => {
    cy.stub(NodeTag, "create")
      .withArgs({
        value: "testTag",
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
      .rejects(new Error("404 request failed"));

    factory({
      selected: ["uuid"],
      existingTags: [testTag, existingTag],
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
    cy.contains("404 request failed").should("be.visible");
  });
});
