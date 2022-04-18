import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import BaseModal from "@/components/Modals/BaseModal.vue";
import { VueWrapper } from "@vue/test-utils";
import { ComponentPublicInstance } from "vue";

function factory(props = {}) {
  mount(BaseModal, {
    global: {
      plugins: [PrimeVue, createPinia()],
      provide: {
        nodeType: "alerts",
      },
    },
    propsData: {
      name: "BaseModal",
      ...props,
    },
  });
  cy.wrap(
    Cypress.vueWrapper as VueWrapper<ComponentPublicInstance<typeof BaseModal>>,
  ).then((wrapper) => {
    wrapper.vm.store.open("BaseModal");
    cy.get("[data-cy=BaseModal]").should("be.visible");
  });
}

describe("BaseModal", () => {
  it("renders correctly with no given style or header props", () => {
    factory();
    cy.get("[data-cy=BaseModal]")
      .should("be.visible")
      .children()
      .should("have.length", 3);

    cy.get("[data-cy=BaseModal]")
      .children()
      .eq(1)
      .children()
      .should("have.length", 0);
  });
  it("emits expected event on closing", () => {
    factory();
    cy.get("[data-cy=BaseModal]").children().eq(0).click();
    cy.get("[data-cy=BaseModal]").should("not.exist");
    cy.wrap(Cypress.vueWrapper).then((wrapper) => {
      expect("dialogClose" in wrapper.emitted());
    });
  });
  it("renders correctly when given header prop", () => {
    factory({ header: "My Modal" });

    cy.contains("My Modal").should("be.visible");

    cy.get("[data-cy=BaseModal]").children().eq(0).children().eq(1).click();
    cy.get("[data-cy=BaseModal]").should("not.exist");
  });
});
