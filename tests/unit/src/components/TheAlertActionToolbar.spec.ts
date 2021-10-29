import TheAlertActionToolbar from "@/components/Alerts/TheAlertActionToolbar.vue";
import { mount, VueWrapper } from "@vue/test-utils";
import AssignModal from "@/components/Modals/AssignModal.vue";
import CommentModal from "@/components/Modals/CommentModal.vue";
import TagModal from "@/components/Modals/TagModal.vue";
import RemediationModal from "@/components/Modals/RemediateModal.vue";
import DeleteModal from "@/components/Modals/DeleteModal.vue";
import DispositionModal from "@/components/Modals/DispositionModal.vue";
import Toolbar from "primevue/toolbar";
import Button from "primevue/button";

describe("TheAlertActionToolbar.vue", () => {
  const wrapper = mount(TheAlertActionToolbar, {
    global: {
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

  it("contains expected components", () => {
    expect(wrapper.findComponent(AssignModal).exists()).toBe(true);
    expect(wrapper.findComponent(CommentModal).exists()).toBe(true);
    expect(wrapper.findComponent(TagModal).exists()).toBe(true);
    expect(wrapper.findComponent(RemediationModal).exists()).toBe(true);
    expect(wrapper.findComponent(DeleteModal).exists()).toBe(true);
    expect(wrapper.findComponent(DispositionModal).exists()).toBe(true);
  });

  it("contains buttons to open each component", () => {
    const buttonsWrapper: VueWrapper<any>[] = wrapper.findAllComponents(Button);
    expect(buttonsWrapper.length).toBe(8);
    expect(buttonsWrapper[0].vm.label).toBe("Disposition");
    expect(buttonsWrapper[1].vm.label).toBe("Comment");
    expect(buttonsWrapper[2].vm.label).toBe("Take Ownership");
    expect(buttonsWrapper[3].vm.label).toBe("Assign");
    expect(buttonsWrapper[4].vm.label).toBe("Tag");
    expect(buttonsWrapper[5].vm.label).toBe("Remediate");
    expect(buttonsWrapper[6].vm.label).toBe("Delete");
    expect(buttonsWrapper[7].vm.label).toBe("Link");
  });
});
