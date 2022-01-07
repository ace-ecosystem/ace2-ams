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
    props: {
      page: "Manage Alerts",
    },
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
    expect(buttonsWrapper.length).toBe(6);
    expect(buttonsWrapper[0].vm.label).toBe("Disposition");
    expect(buttonsWrapper[1].vm.label).toBe("Comment");
    expect(buttonsWrapper[2].vm.label).toBe("Take Ownership");
    expect(buttonsWrapper[3].vm.label).toBe("Assign");
    expect(buttonsWrapper[4].vm.label).toBe("Tag");
    expect(buttonsWrapper[5].vm.label).toBe("Remediate");
  });

  it("opens a modal when the open function is called", () => {
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("opens sets requestReload for the current page's correct store", async () => {
    wrapper.vm.alertTableStore.$reset();
    wrapper.vm.alertStore.$reset();
    wrapper.vm.requestReload();
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
    expect(wrapper.vm.alertStore.requestReload).toBeFalsy();

    wrapper.vm.alertTableStore.$reset();
    wrapper.vm.alertStore.$reset();
    await wrapper.setProps({ page: "View Alert" });
    wrapper.vm.requestReload();
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
    expect(wrapper.vm.alertStore.requestReload).toBeTruthy();

    wrapper.vm.alertTableStore.$reset();
    wrapper.vm.alertStore.$reset();
    await wrapper.setProps({ page: "Unknown" });
    wrapper.vm.requestReload();
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
    expect(wrapper.vm.alertStore.requestReload).toBeFalsy();
  });

  it("updates ownership of alert to current user and requests alertTable reload when Take Ownership clicked", async () => {
    await wrapper.setProps({ page: "Manage Alerts" });
    myNock
      .options("/alert/")
      .reply(200)
      .patch("/alert/", [
        { uuid: "uuid1", owner: "testingUser" },
        { uuid: "uuid2", owner: "testingUser" },
      ])
      .reply(204);
    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedAlertStore.selected = ["uuid1", "uuid2"];
    await wrapper.vm.takeOwnership();
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.alertTableStore.requestReload).toBeTruthy();
  });

  it("sets the error and does not request reload if takeOwnership fails", async () => {
    wrapper.vm.alertTableStore.$reset();
    wrapper.vm.alertStore.$reset();
    await wrapper.setProps({ page: "Manage Alerts" });
    myNock.options("/alert/").reply(200).patch("/alert/").reply(403);
    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedAlertStore.selected = ["uuid1", "uuid2"];
    await wrapper.vm.takeOwnership();
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.alertTableStore.requestReload).toBeFalsy();
  });
});
