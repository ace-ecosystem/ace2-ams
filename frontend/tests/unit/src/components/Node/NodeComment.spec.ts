import NodeComment from "../../../../../src/components/Node/NodeComment.vue";
import { mount } from "@vue/test-utils";
import { createTestingPinia } from "@pinia/testing";
import { commentReadFactory } from "../../../../mocks/comment";

const mockComment = commentReadFactory();

function factory(includeTime = true, includeLineBreak = true) {
  const wrapper = mount(NodeComment, {
    props: {
      comment: mockComment,
      includeTime: includeTime,
      includeLineBreak: includeLineBreak,
    },
    global: {
      plugins: [createTestingPinia()],
    },
  });

  return { wrapper };
}

describe("NodeComment.vue", () => {
  it("renders", () => {
    const { wrapper } = factory();
    expect(wrapper.exists()).toBe(true);
  });
  it("receives props as expected", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.props).toEqual({
      comment: mockComment,
      includeTime: true,
      includeLineBreak: true,
    });
  });
  it("correctly returns formatComment when includeTime is set to true", () => {
    const { wrapper } = factory();
    expect(wrapper.vm.formatComment(mockComment)).toEqual(
      "1/1/2020, 12:00:00 AM (Test Analyst) A test comment",
    );
  });
  it("correctly returns formatComment when includeTime is set to false", () => {
    const { wrapper } = factory(false);
    expect(wrapper.vm.formatComment(mockComment)).toEqual(
      "(Test Analyst) A test comment",
    );
  });
});
