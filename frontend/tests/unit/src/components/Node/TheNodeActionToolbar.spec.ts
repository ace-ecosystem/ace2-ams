import { createTestingPinia, TestingOptions } from "@pinia/testing";
import { flushPromises, mount, VueWrapper } from "@vue/test-utils";

import AssignModal from "@/components/Modals/AssignModal.vue";
import Button from "primevue/button";
import CommentModal from "@/components/Modals/CommentModal.vue";
import DispositionModal from "@/components/Modals/DispositionModal.vue";
import myNock from "@unit/services/api/nock";
import RemediationModal from "@/components/Modals/RemediateModal.vue";
import TagModal from "@/components/Modals/TagModal.vue";
import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import Toolbar from "primevue/toolbar";
import TheNodeActionToolbarVue from "@/components/Node/TheNodeActionToolbar.vue";
import { createRouterMock, injectRouterMock } from "vue-router-mock";
import { useAlertStore } from "@/stores/alert";
import { useModalStore } from "@/stores/modal";
import { useAlertTableStore } from "@/stores/alertTable";
import { useSelectedAlertStore } from "@/stores/selectedAlert";

interface factoryOptions {
  piniaOptions?: TestingOptions;
  props?: {
    reloadObject: "table" | "node" | "unknown";
    assign?: boolean;
    comment?: boolean;
    tag?: boolean;
    takeOwnership?: boolean;
  };
  nodeType?: string;
}

function factory(
  options: factoryOptions = {
    piniaOptions: undefined,
    props: { reloadObject: "table" },
    nodeType: "alerts",
  },
) {
  const router = createRouterMock();
  injectRouterMock(router);

  const wrapper: VueWrapper<any> = mount(TheNodeActionToolbarVue, {
    global: {
      plugins: [createTestingPinia(options.piniaOptions)],
      provide: {
        nodeType: options.nodeType,
      },
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
    props: options.props,
  });

  const alertStore = useAlertStore();
  const modalStore = useModalStore();
  const alertTableStore = useAlertTableStore();
  const selectedAlertStore = useSelectedAlertStore();

  return {
    wrapper,
    alertTableStore,
    alertStore,
    modalStore,
    selectedAlertStore,
  };
}

describe("TheAlertActionToolbar.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });

  it("contains toolbar", () => {
    const { wrapper } = factory();

    const toolbar = wrapper.findComponent(Toolbar);
    expect(toolbar.exists()).toBe(true);
  });

  it("contains expected components if all enabled", () => {
    const { wrapper } = factory();

    expect(wrapper.findComponent(AssignModal).exists()).toBe(true);
    expect(wrapper.findComponent(CommentModal).exists()).toBe(true);
    expect(wrapper.findComponent(TagModal).exists()).toBe(true);

    const buttonsWrapper: VueWrapper<any>[] = wrapper.findAllComponents(Button);
    expect(buttonsWrapper.length).toBe(4);
    expect(buttonsWrapper[0].vm.label).toBe("Comment");
    expect(buttonsWrapper[1].vm.label).toContain("Take Ownership");
    expect(buttonsWrapper[2].vm.label).toBe("Assign");
    expect(buttonsWrapper[3].vm.label).toBe("Tag");
  });

  it("contains expected components if none enabled", () => {
    const { wrapper } = factory({
      piniaOptions: undefined,
      props: {
        reloadObject: "table",
        assign: false,
        comment: false,
        tag: false,
        takeOwnership: false,
      },
      nodeType: "alerts",
    });
    const buttonsWrapper: VueWrapper<any>[] = wrapper.findAllComponents(Button);
    expect(buttonsWrapper.length).toBe(0);
  });

  it("opens a given modal when the open function is called", () => {
    const { wrapper } = factory({
      piniaOptions: { stubActions: false },
      props: { reloadObject: "table" },
      nodeType: "alerts",
    });

    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("updates ownership of selected node to current user and requests nodeTable reload when Take Ownership clicked", async () => {
    const { wrapper } = factory();
    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedStore.selected = ["uuid1", "uuid2"];
    await wrapper.vm.takeOwnership();
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.nodeStore.update).toHaveBeenNthCalledWith(1, [
      { owner: "testingUser", uuid: "uuid1" },
      { owner: "testingUser", uuid: "uuid2" },
    ]);
    expect(wrapper.vm.tableStore.requestReload).toBeTruthy();
  });

  it("sets the error and does not request reload if takeOwnership fails", async () => {
    myNock.options("/alert/").reply(200).patch("/alert/").reply(403);

    const { wrapper } = factory({
      piniaOptions: { stubActions: false },
      props: { reloadObject: "table" },
      nodeType: "alerts",
    });

    wrapper.vm.authStore.user = { username: "testingUser" };
    wrapper.vm.selectedStore.selected = ["uuid1", "uuid2"];

    await wrapper.vm.takeOwnership();
    expect(wrapper.vm.error).toEqual("Request failed with status code 403");
    // this will still be truthy bc it's in the same component as requestReload()
    expect(wrapper.vm.tableStore.requestReload).toBeFalsy();
  });

  it("sets requestReload for tableStore when the reloadObject is 'table'", async () => {
    const { wrapper, alertStore, alertTableStore } = factory({
      piniaOptions: { stubActions: true },
      props: { reloadObject: "table" },
      nodeType: "alerts",
    });

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeTruthy();
    expect(alertStore.requestReload).toBeFalsy();
  });

  it("sets requestReload for tableStore when the reloadObject is 'node'", async () => {
    const { wrapper, alertStore, alertTableStore } = factory({
      piniaOptions: { stubActions: true },
      props: { reloadObject: "node" },
      nodeType: "alerts",
    });

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeFalsy();
    expect(alertStore.requestReload).toBeTruthy();
  });

  it("wont set requestReload for tableStore when the requestObject is unknown", async () => {
    const { wrapper, alertStore, alertTableStore } = factory({
      piniaOptions: { stubActions: true },
      props: { reloadObject: "unknown" },
      nodeType: "alerts",
    });

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeFalsy();
    expect(alertStore.requestReload).toBeFalsy();
  });

  it("will clear the 'error' property when handleError is called", () => {
    const { wrapper } = factory();

    wrapper.vm.error = "Call failed";

    expect(wrapper.vm.error).toEqual("Call failed");
    wrapper.vm.handleError();
    expect(wrapper.vm.error).toBeNull();
  });
});
