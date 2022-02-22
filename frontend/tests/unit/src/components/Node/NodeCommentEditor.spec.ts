import { commentReadFactory } from "./../../../../mocks/comment";
import { useNodeThreatTypeStore } from "@/stores/nodeThreatType";
import NodeCommentEditor from "../../../../../src/components/Node/NodeCommentEditor.vue";
import { mount } from "@vue/test-utils";
import { createCustomPinia } from "@unit/helpers";
import Tooltip from "primevue/tooltip";
import PrimeVue from "primevue/config";

import { useNodeThreatStore } from "@/stores/nodeThreat";

function factory() {
  const wrapper = mount(NodeCommentEditor, {
    props: {
      modelValue: [commentReadFactory()],
    },
    global: {
      plugins: [createCustomPinia(), PrimeVue],
    },
  });

  return { wrapper };
}

describe("NodeCommentEditor.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("sets data correctly on openEditCommentPanel", () => {
    const { wrapper } = factory();
    wrapper.vm.openEditCommentPanel(commentReadFactory());
    expect(wrapper.vm.editingCommentValue).toEqual("A test comment");
    expect(wrapper.vm.editingCommentUuid).toEqual("commentUuid1");
    expect(wrapper.vm.editCommentPanelOpen).toBeTruthy();
  });
  it("sets data correctly on closeEditCommentPanel", () => {
    const { wrapper } = factory();

    wrapper.vm.editingCommentValue = "Test";
    wrapper.vm.editingCommentUuid = "Uuid";
    wrapper.vm.editCommentPanelOpen = true;

    wrapper.vm.closeEditCommentPanel();
    expect(wrapper.vm.editingCommentValue).toEqual(null);
    expect(wrapper.vm.editingCommentUuid).toEqual(null);
    expect(wrapper.vm.editCommentPanelOpen).toBeFalsy();
  });
  it("correctly updates model, emits update:modelValue, and closes editing panel on saveModelComment", () => {
    const { wrapper } = factory();

    wrapper.vm.comments = [
      commentReadFactory({ value: "Comment A", uuid: "1" }),
      commentReadFactory({ value: "Comment B", uuid: "2" }),
    ];

    wrapper.vm.editingCommentValue = "Updated";
    wrapper.vm.editingCommentUuid = "2";
    wrapper.vm.editCommentPanelOpen = true;

    wrapper.vm.saveModelComment();
    expect(wrapper.vm.comments[1]).toEqual(
      commentReadFactory({ value: "Updated", uuid: "2" }),
    );
    expect(wrapper.emitted("update:modelValue")).toBeTruthy();
    expect(wrapper.vm.editingCommentValue).toEqual(null);
    expect(wrapper.vm.editingCommentUuid).toEqual(null);
    expect(wrapper.vm.editCommentPanelOpen).toBeFalsy();
  });
});
