/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { Comment } from "@/services/api/comment";
import myNock from "@unit/services/api/nock";
import { commentCreate } from "@/models/comment";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

describe("Comment API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: commentCreate[] = [
    {
      nodeUuid: "uuid1",
      description: "This is a comment",
      username: "Alice",
      value: "Test",
    },
  ];
  //   const mockObjectRead: commentRead = {
  //     nodeUuid: "uuid1",
  //     user: {username: "Alice"},
  //     uuid: "1",
  //     value: "Test",
  //   };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await Comment.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await Comment.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await Comment.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/node/comment/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await Comment.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /node/comment/{uuid} when getSingle is called", async () => {
    myNock.get("/node/comment/1").reply(200, successMessage);

    const res = await Comment.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /node/comment/{uuid} when updateSingle is called", async () => {
    myNock
      .patch(
        "/node/comment/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await Comment.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/node/comment/1").reply(404, failureMessage);

    try {
      await Comment.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
