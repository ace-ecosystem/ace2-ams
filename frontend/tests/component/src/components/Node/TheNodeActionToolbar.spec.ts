import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import TheNodeActionToolbar from "@/components/Node/TheNodeActionToolbar.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertTreeReadFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";
import CommentModalVue from "@/components/Modals/CommentModal.vue";

interface TheNodeActionToolbarProps {
  reloadObject: "node" | "table";
  assign?: boolean;
  comment?: boolean;
  tag?: boolean;
  removeTag?: boolean;
  takeOwnership?: boolean;
}

const defaultProps: TheNodeActionToolbarProps = {
  reloadObject: "node",
};

function factory(
  args: {
    props: TheNodeActionToolbarProps;
    initialState: Record<string, unknown>;
  } = { props: defaultProps, initialState: {} },
) {
  return mount(TheNodeActionToolbar, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: args.initialState,
        }),
      ],
      provide: { nodeType: "alerts" },
    },
    propsData: args.props,
  });
}

describe("TheNodeActionToolbar", () => {
  it("renders correctly with default props", () => {
    factory();
    cy.contains("Comment").should("be.visible").click();
    cy.get("@stub-14").should("have.been.calledWith", "CommentModal");
    cy.contains("Take Ownership").should("be.visible").should("be.disabled");
    cy.contains("Assign").should("be.visible").click();
    cy.get("@stub-14").should("have.been.calledWith", "AssignModal");
    cy.contains("Tag").should("be.visible").click();
    cy.get("@stub-14").should("have.been.calledWith", "TagModal");
    cy.contains("Remove Tag").should("be.visible").click();
    cy.get("@stub-14").should("have.been.calledWith", "RemoveTagModal");
  });
  it("correctly attempts to assign owner if 'Take Ownership' button clicked", () => {
    factory({
      props: defaultProps,
      initialState: {
        selectedAlertStore: { selected: ["uuid"] },
        authStore: { user: userReadFactory() },
      },
    });
    cy.contains("Take Ownership")
      .should("be.visible")
      .should("not.be.disabled")
      .click();
    cy.get("@stub-3").should("have.been.calledWith", [
      {
        uuid: "uuid",
        owner: "analyst",
      },
    ]);
  });
  it("displays correct alternate text if reloadObject is node, and the open node's owner is the current user", () => {
    factory({
      props: { reloadObject: "node" },
      initialState: {
        authStore: { user: userReadFactory() },
        alertStore: {
          open: alertTreeReadFactory({ owner: userReadFactory() }),
        },
      },
    });
    cy.contains("Assigned to you!").should("be.visible");
  });
  it("attempts to reload the node if the given 'reloadObject' is 'node'", () => {
    factory({
      props: { reloadObject: "node" },
      initialState: {},
    }).then((wrapper) => {
      wrapper.findComponent(CommentModalVue).vm.$emit("requestReload");
      cy.wrap(wrapper.vm.nodeStore.requestReload).should("be.true");
      cy.wrap(wrapper.vm.tableStore.requestReload).should("be.false");
    });
  });
  it("attempts to reload the node table if the given 'reloadObject' is 'table'", () => {
    factory({
      props: { reloadObject: "table" },
      initialState: {},
    }).then((wrapper) => {
      wrapper.findComponent(CommentModalVue).vm.$emit("requestReload");
      cy.wrap(wrapper.vm.nodeStore.requestReload).should("be.false");
      cy.wrap(wrapper.vm.tableStore.requestReload).should("be.true");
    });
  });
  it("renders correctly with all optional buttons disabled", () => {
    factory({
      props: {
        reloadObject: "node",
        assign: false,
        tag: false,
        removeTag: false,
        comment: false,
        takeOwnership: false,
      },
      initialState: {},
    });
    cy.get("#ActionToolbar")
      .should("be.visible")
      .children()
      .should("not.be.visible");
  });
});
