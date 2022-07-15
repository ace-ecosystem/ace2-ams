/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { EventType } from "@/services/api/eventType";
import myNock from "@unit/services/api/nock";
import { eventTypeCreate } from "@/models/eventType";
import { createCustomPinia } from "@tests/unitHelpers";
import { genericObjectCreateFactory } from "@mocks/genericObject";

createCustomPinia();

describe("EventType API calls", () => {
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: eventTypeCreate = {
    ...genericObjectCreateFactory(),
    queues: [],
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/event/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await EventType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/event/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await EventType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/event/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await EventType.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/event/type/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await EventType.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /event/type/{uuid} when read is called", async () => {
    myNock.get("/event/type/1").reply(200, successMessage);

    const res = await EventType.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /event/type/ when readAll is called", async () => {
    myNock.get("/event/type/?offset=0").reply(200, readAllSuccesssObject);

    const res = await EventType.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /event/type/ with given params when readPage is called", async () => {
    myNock.get("/event/type/?offset=0&limit=10").reply(200, successMessage);

    const res = await EventType.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /event/type/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/event/type/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await EventType.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/event/type/1").reply(404, failureMessage);

    try {
      await EventType.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
