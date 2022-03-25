/**
 * @jest-environment node
 */

import { NodeTree } from "@/services/api/nodeTree";
import myNock from "./nock";

describe("nodeTree API calls", () => {
  const mockObjectReadArray: Record<string, unknown>[] = [
    {
      uuid: "1",
      value: "Test",
    },
    {
      uuid: "1",
      value: "Test",
    },
  ];

  it("will make a post request to the correct endpoint when readNodesOfNodeTree is called", async () => {
    myNock
      .post("/node/tree/observable", JSON.stringify(["1", "2"]))
      .reply(200, mockObjectReadArray);

    const res = await NodeTree.readNodesOfNodeTree(["1", "2"], "observable");
    expect(res).to.eql(mockObjectReadArray);
  });
});
