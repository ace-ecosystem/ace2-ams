import { mount } from "@cypress/vue";
import PrimeVue from "primevue/config";

import TheObjectActionToolbar from "@/components/Objects/TheObjectActionToolbar.vue";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { alertTreeReadFactory } from "@mocks/alert";
import { userReadFactory } from "@mocks/user";
import CommentModalVue from "@/components/Modals/CommentModal.vue";

interface TheObjectActionToolbarProps {
  reloadObject: "object" | "table";
  assign?: boolean;
  comment?: boolean;
  tag?: boolean;
  removeTag?: boolean;
  takeOwnership?: boolean;
}

const defaultProps: TheObjectActionToolbarProps = {
  reloadObject: "object",
};

function factory(
  args: {
    props: TheObjectActionToolbarProps;
    initialState: Record<string, unknown>;
  } = { props: defaultProps, initialState: {} },
) {
  return mount(TheObjectActionToolbar, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          initialState: args.initialState,
        }),
      ],
      provide: { objectType: "alerts" },
    },
    propsData: args.props,
  });
}

describe("TheObjectActionToolbar", () => {
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
        historyUsername: "analyst",
      },
    ]);
  });
  it("displays correct alternate text if reloadObject is object, and the open object's owner is the current user", () => {
    factory({
      props: { reloadObject: "object" },
      initialState: {
        authStore: { user: userReadFactory() },
        alertStore: {
          open: alertTreeReadFactory({ owner: userReadFactory() }),
        },
      },
    });
    cy.contains("Assigned to you!").should("be.visible");
  });
  it("attempts to reload the object if the given 'reloadObject' is 'object'", () => {
    factory({
      props: { reloadObject: "object" },
      initialState: {},
    }).then((wrapper) => {
      wrapper.findComponent(CommentModalVue).vm.$emit("requestReload");
      cy.wrap(wrapper.vm.objectStore.requestReload).should("be.true");
      cy.wrap(wrapper.vm.tableStore.requestReload).should("be.false");
    });
  });
  it("attempts to reload the object table if the given 'reloadObject' is 'table'", () => {
    factory({
      props: { reloadObject: "table" },
      initialState: {},
    }).then((wrapper) => {
      wrapper.findComponent(CommentModalVue).vm.$emit("requestReload");
      cy.wrap(wrapper.vm.objectStore.requestReload).should("be.false");
      cy.wrap(wrapper.vm.tableStore.requestReload).should("be.true");
    });
  });
  it("renders correctly with all optional buttons disabled", () => {
    factory({
      props: {
        reloadObject: "object",
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
