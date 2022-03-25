/**
 * @vitest-environment node
 */

import snakecaseKeys from "snakecase-keys";
import { NodeComment } from "@/services/api/nodeComment";
import myNock from "@unit/services/api/nock";
import { nodeCommentCreate, nodeCommentRead } from "@/models/nodeComment";
import { createCustomPinia } from "@unit/helpers";

createCustomPinia();

describe("NodeComment API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: nodeCommentCreate[] = [
    {
      nodeUuid: "uuid1",
      description: "This is a comment",
      value: "Test",
    },
  ];
  //   const mockObjectRead: nodeCommentRead = {
  //     nodeUuid: "uuid1",
  //     user: {username: "Alice"},
  //     uuid: "1",
  //     value: "Test",
  //   };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await NodeComment.create(mockObjectCreate, false);
    expect(res).to.eql(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await NodeComment.create(mockObjectCreate, false);
    expect(res).to.eql(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await NodeComment.create(mockObjectCreate);
    expect(res).to.eql(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await NodeComment.create(mockObjectCreate, true);
    expect(res).to.eql(secondSuccessMessage);
  });

  it("will make a get request to /node/comment/{uuid} when getSingle is called", async () => {
    myNock.get("/node/comment/1").reply(200, successMessage);

    const res = await NodeComment.read("1");
    expect(res).to.eql(successMessage);
  });

  it("will make a patch request to /node/comment/{uuid} when updateSingle is called", async () => {
    myNock
      .patch(
        "/node/comment/1",
        JSON.stringify({ uuid: "1", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await NodeComment.update("1", { uuid: "1", value: "New Name" });
    expect(res).to.eql(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/node/comment/1").reply(404, failureMessage);

    try {
      await NodeComment.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).to.equal("Request failed with status code 404");
    }
  });
});
