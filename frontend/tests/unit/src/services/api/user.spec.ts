/**
 * @jest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { User } from "@/services/api/user";
import myNock from "@unit/services/api/nock";
import { userCreate, userRead } from "@/models/user";

describe("user API calls", () => {
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: userCreate = {
    description: "This is a user",
    value: "Test",
  };
  const mockObjectRead: userRead = {
    uuid: "1",
    description: "This is a user",
    value: "Test",
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/user/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await User.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/user/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      });

    const res = await User.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/user/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await User.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/user/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await User.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /user/{uuid} when getSingle is called", async () => {
    myNock.get("/user/1").reply(200, successMessage);

    const res = await User.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /user/ when readAll is called", async () => {
    myNock
      .get("/user/?offset=0")
      .reply(200, JSON.stringify({ items: [mockObjectRead, mockObjectRead] }));

    const res = await User.readAll();
    expect(res).toEqual([mockObjectRead, mockObjectRead]);
  });

  it("will make a patch request to /user/{uuid} when updateSingle is called", async () => {
    myNock
      .patch("/user/1", JSON.stringify({ value: "New Name" }))
      .reply(200, successMessage);

    const res = await User.update("1", { value: "New Name" });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/user/1").reply(404, failureMessage);

    try {
      await User.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
