import { createTestingPinia } from "@pinia/testing";
import { mount, VueWrapper } from "@vue/test-utils";
import AssignModal from "@/components/Modals/AssignModal.vue";
import Button from "primevue/button";
import CommentModal from "@/components/Modals/CommentModal.vue";
import DispositionModal from "@/components/Modals/DispositionModal.vue";
import myNock from "@unit/services/api/nock";
import RemediationModal from "@/components/Modals/RemediateModal.vue";
import TagModal from "@/components/Modals/TagModal.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import Toolbar from "primevue/toolbar";

describe("TheAlertActionToolbar.vue", () => {
  const wrapper: VueWrapper<any> = mount(TheAlertActionToolbar, {
    global: {
      plugins: [createTestingPinia({ stubActions: false })],
      stubs: {
        AssignModal: true,
        CommentModal: true,
        TagModal: true,
        RemediationModal: true,
        DeleteModal: true,
        DispositionModal: true,
        Button: Button,
      },
    },
  });

  it("renders", () => {
    expect(wrapper.exists()).toBe(true);
  });

  it("contains toolbar", () => {
    const toolbar = wrapper.findComponent(Toolbar);
    expect(toolbar.exists()).toBe(true);
  });

  it("will clear the 'error' property when handleError is called", async () => {
    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });

  it("contains expected components", () => {
    expect(wrapper.findComponent(AssignModal).exists()).toBe(true);
    expect(wrapper.findComponent(CommentModal).exists()).toBe(true);
    expect(wrapper.findComponent(TagModal).exists()).toBe(true);
    expect(wrapper.findComponent(RemediationModal).exists()).toBe(true);
    expect(wrapper.findComponent(DispositionModal).exists()).toBe(true);
  });

  it("contains buttons to open each component", () => {
    const buttonsWrapper: VueWrapper<any>[] = wrapper.findAllComponents(Button);
    expect(buttonsWrapper.length).toBe(7);
    expect(buttonsWrapper[0].vm.label).toBe("Disposition");
    expect(buttonsWrapper[1].vm.label).toBe("Comment");
    expect(buttonsWrapper[2].vm.label).toBe("Take Ownership");
    expect(buttonsWrapper[3].vm.label).toBe("Assign");
    expect(buttonsWrapper[4].vm.label).toBe("Tag");
    expect(buttonsWrapper[5].vm.label).toBe("Remediate");
    expect(buttonsWrapper[6].vm.label).toBe("Link");
  });

  it("opens a modal when the open function is called", () => {
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("updates ownership of alert to current user and requests alertTable reload when clicked", async () => {
    myNock
      .options("/alert/uuid1")
      .reply(200)
      .patch("/alert/uuid1", { owner: "testingUser" })
      .reply(204);
    myNock
      .options("/alert/uuid2")
      .reply(200)
      .patch("/alert/uuid2", { owner: "testingUser" })
      .reply(204);
    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedAlertStore.selected = ["uuid1", "uuid2"];
    await wrapper.vm.takeOwnership();
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
  });
});
