import { TestingOptions } from "@pinia/testing";
import { mount, VueWrapper } from "@vue/test-utils";

import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import Toolbar from "primevue/toolbar";
import { useAlertTableStore } from "@/stores/alertTable";
import { useAlertStore } from "@/stores/alert";
import { createCustomPinia } from "@unit/helpers";

function factory(options?: TestingOptions, reloadObject = "table") {
  const wrapper: VueWrapper<any> = mount(TheAlertActionToolbar, {
    props: {
      reloadObject: reloadObject,
    },
    global: {
      plugins: [createCustomPinia(options)],
      provide: { nodeType: "alerts" },
      stubs: {
        AssignModal: true,
        CommentModal: true,
        TagModal: true,
        RemediationModal: true,
        DeleteModal: true,
        DispositionModal: true,
      },
    },
  });

  return { wrapper };
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

  it("opens a modal when the open function is called", () => {
    const { wrapper } = factory({ stubActions: false });
    expect(wrapper.vm.modalStore.openModals).toStrictEqual([]);
    wrapper.vm.open("modal1");
    expect(wrapper.vm.modalStore.openModals).toStrictEqual(["modal1"]);
  });

  it("will call on the child NodeActionToolbar to requestReload on requestReload", () => {
    const { wrapper } = factory();

    const alertTableStore = useAlertTableStore();
    const alertStore = useAlertStore();

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeTruthy();
    expect(alertStore.requestReload).toBeFalsy();
  });
  it("will call on the child NodeActionToolbar to requestReload on requestReload", () => {
    const { wrapper } = factory(undefined, "node");

    const alertTableStore = useAlertTableStore();
    const alertStore = useAlertStore();

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeFalsy();
    expect(alertStore.requestReload).toBeTruthy();
  });
  it("will call on the child NodeActionToolbar to requestReload on requestReload", () => {
    const { wrapper } = factory(undefined, "unkown");

    const alertTableStore = useAlertTableStore();
    const alertStore = useAlertStore();

    wrapper.vm.requestReload();
    expect(alertTableStore.requestReload).toBeFalsy();
    expect(alertStore.requestReload).toBeFalsy();
  });
});
