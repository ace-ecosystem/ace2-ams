import EventURLSummary from "@/components/Events/EventURLSummary.vue";
import { shallowMount, VueWrapper, flushPromises } from "@vue/test-utils";
import { TestingOptions } from "@pinia/testing";
import { createCustomPinia } from "@unit/helpers";
import { expect } from "vitest";
import { genericObjectReadFactory } from "../../../../mocks/genericObject";
import { NodeTree } from "@/services/api/nodeTree";
import { observableReadFactory } from "../../../../mocks/observable.ts";

const mockObservableTypeURL = genericObjectReadFactory({ value: "url" });
const mockObservableTypeIPV4 = genericObjectReadFactory({ value: "ipv4" });
const allObservables = [
  observableReadFactory({
    value: "http://notEvil.com",
    type: mockObservableTypeURL,
  }),
  observableReadFactory({ value: "1.2.3.4", type: mockObservableTypeIPV4 }),
  observableReadFactory({
    value: "http://evil.com",
    type: mockObservableTypeURL,
  }),
];
const filteredAndSortedObservables = [
  observableReadFactory({
    value: "http://evil.com",
    type: mockObservableTypeURL,
  }),
  observableReadFactory({
    value: "http://notEvil.com",
    type: mockObservableTypeURL,
  }),
];

async function factory(options: TestingOptions = {}) {
  const readNodesOfNodeTreeSpy = vi
    .spyOn(NodeTree, "readNodesOfNodeTree")
    .mockResolvedValueOnce(allObservables);

  const wrapper: VueWrapper<any> = await shallowMount(EventURLSummary, {
    global: {
      plugins: [createCustomPinia(options)],
    },
    props: {
      eventAlertUuids: [
        "81d92d05-3b60-4ecf-931d-4525fc1113f3",
        "b8a03b05-020d-4da7-b543-bb08137f862d",
        "839e756b-39b7-407f-8e4a-513051ff4f53",
      ],
    },
  });

  await flushPromises();

  expect(readNodesOfNodeTreeSpy.mock.calls[0]).toEqual([
    [
      "81d92d05-3b60-4ecf-931d-4525fc1113f3",
      "b8a03b05-020d-4da7-b543-bb08137f862d",
      "839e756b-39b7-407f-8e4a-513051ff4f53",
    ],
    "observable",
  ]);

  return { wrapper };
}

describe("EventURLSummary", () => {
  it("renders", async () => {
    const { wrapper } = await factory();
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.vm.selectedURL).toBeNull();
    expect(wrapper.vm.sortedUrlObservables).toEqual(
      filteredAndSortedObservables,
    );
  });
  it("correctly returns all observables for an event on getAllObservables", async () => {
    const readNodesOfNodeTreeSpy = vi
      .spyOn(NodeTree, "readNodesOfNodeTree")
      .mockResolvedValueOnce(allObservables);
    const { wrapper } = await factory();

    wrapper.vm.getAllObservables();
    await flushPromises();
    expect(readNodesOfNodeTreeSpy.mock.calls[0]).toEqual([
      [
        "81d92d05-3b60-4ecf-931d-4525fc1113f3",
        "b8a03b05-020d-4da7-b543-bb08137f862d",
        "839e756b-39b7-407f-8e4a-513051ff4f53",
      ],
      "observable",
    ]);
  });
  it("correctly filters and sorts a list of observables on getURLObservables", async () => {
    const { wrapper } = await factory();
    const result = wrapper.vm.getURLObservables(allObservables);
    expect(result).toEqual(filteredAndSortedObservables);
  });
});
