import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import DispositionModal from "@/components/Modals/DispositionModal.vue";
import { alertDispositionRead } from "@/models/alertDisposition";
import { createCustomCypressPinia } from "@tests/cypressHelpers";
import { genericObjectReadFactory } from "@mocks/genericObject";
import SaveToEventModalVue from "@/components/Modals/SaveToEventModal.vue";
import { Alert } from "@/services/api/alert";
import { NodeComment } from "@/services/api/nodeComment";
import { userReadFactory } from "@mocks/user";

function factory(
  args: { dipsositions: alertDispositionRead[]; selected: string[] } = {
    dipsositions: [],
    selected: [],
  },
) {
  return mount(DispositionModal, {
    global: {
      plugins: [
        PrimeVue,
        createCustomCypressPinia({
          stubActions: false,
          initialState: {
            authStore: { user: userReadFactory() },
            alertDispositionStore: {
              items: args.dipsositions,
            },
            selectedAlertStore: {
              selected: args.selected,
            },
          },
        }),
      ],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: {
      name: "DispositionModal",
    },
  }).then((wrapper) => {
    wrapper.vm.modalStore.open("DispositionModal");
    cy.get("[data-cy=DispositionModal]").should("be.visible");
    cy.findAllByText("Set Disposition").should("be.visible");
    cy.findAllByPlaceholderText("Add a comment...").should("be.visible");
    cy.contains("Save").should("be.visible").should("be.disabled");
  });
}

describe("DispositionModal", () => {
  const falsePositive = {
    ...genericObjectReadFactory({ value: "False Positive" }),
    rank: 0,
  };
  const badDisposition = {
    ...genericObjectReadFactory({ value: "Bad" }),
    rank: 2,
  };

  it("renders correctly when no dispositions are available", () => {
    factory();
    cy.findAllByText("No available options").should("be.visible");
  });
  it("renders correctly there are dispositions available", () => {
    factory({ dipsositions: [falsePositive, badDisposition], selected: [] });
    cy.findAllByRole("option").should("have.length", 2);
    cy.findAllByRole("option").eq(0).should("have.text", "False Positive");
    cy.findAllByRole("option").eq(1).should("have.text", "Bad");
  });
  it("has 'save' button enabled when alerts are selected and a disposition is selected", () => {
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("False Positive").click();
    cy.contains("Save").should("be.visible").should("not.be.disabled");
  });
  it("has 'save' button disabled when alerts are not selected and a disposition is selected", () => {
    factory({ dipsositions: [falsePositive, badDisposition], selected: [] });
    cy.contains("False Positive").click();
    cy.contains("Save").should("be.visible").should("be.disabled");
  });
  it("has 'save' button disabled when alerts are selected and a disposition is not selected", () => {
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Save").should("be.visible").should("be.disabled");
  });
  it("shows 'Save to Event' button when high-ranking disposition is selected", () => {
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.contains("Save").should("be.visible").should("not.be.disabled");
    cy.contains("Save to Event").should("be.visible");
  });
  it("attempts to open 'Save to Event' modal when 'Save to Event' button clicked", () => {
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.contains("Save to Event").click();
    cy.get('[data-cy="save-to-event-modal"]').should("be.visible");
  });
  it("attempts to set disposition when save button clicked and no comment is given", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", disposition: "Bad" }])
      .as("setDisposition")
      .resolves();
    cy.stub(NodeComment, "create").as("createComment");
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.contains("Save").click();
    cy.get("@setDisposition").should("have.been.calledOnce");
    cy.get("@createComment").should("not.have.been.called");
    cy.get("[data-cy=DispositionModal]").should("not.exist");
  });
  it("attempts to set disposition and create comment when save button clicked and comment is given", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", disposition: "Bad" }])
      .as("setDisposition")
      .resolves();
    cy.stub(NodeComment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "Test comment",
        },
      ])
      .as("createComment")
      .resolves();
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.findAllByPlaceholderText("Add a comment...")
      .click()
      .type("Test comment");
    cy.contains("Save").click();
    cy.get("@setDisposition").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.get("[data-cy=DispositionModal]").should("not.exist");
  });
  it("displays error if attempt to set disposition fails", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", disposition: "Bad" }])
      .as("setDisposition")
      .rejects(new Error("404 request failed"));
    cy.stub(NodeComment, "create").as("createComment");

    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.findAllByPlaceholderText("Add a comment...")
      .click()
      .type("Test comment");
    cy.contains("Save").click();
    cy.get("@setDisposition").should("have.been.calledOnce");
    cy.get("@createComment").should("not.have.been.called");
    cy.contains("404 request failed").should("be.visible");
  });
  it("displays error if attempt to create comment fails with non-409 error code", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", disposition: "Bad" }])
      .as("setDisposition")
      .resolves();
    cy.stub(NodeComment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "Test comment",
        },
      ])
      .as("createComment")
      .rejects(new Error("404 request failed"));
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.findAllByPlaceholderText("Add a comment...")
      .click()
      .type("Test comment");
    cy.contains("Save").click();
    cy.get("@setDisposition").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.contains("404 request failed").should("be.visible");
  });
  it("does not display error if attempt to create comment fails with 409 error code", () => {
    cy.stub(Alert, "update")
      .withArgs([{ uuid: "uuid", disposition: "Bad" }])
      .as("setDisposition")
      .resolves();
    cy.stub(NodeComment, "create")
      .withArgs([
        {
          username: "analyst",
          nodeUuid: "uuid",
          value: "Test comment",
        },
      ])
      .as("createComment")
      .rejects(new Error("409 request failed"));
    factory({
      dipsositions: [falsePositive, badDisposition],
      selected: ["uuid"],
    });
    cy.contains("Bad").click();
    cy.findAllByPlaceholderText("Add a comment...")
      .click()
      .type("Test comment");
    cy.contains("Save").click();
    cy.get("@setDisposition").should("have.been.calledOnce");
    cy.get("@createComment").should("have.been.calledOnce");
    cy.get("[data-cy=DispositionModal]").should("not.exist");
  });
});
