/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { ObservableType } from "@/services/api/observableType";
import myNock from "@unit/services/api/nock";
import { observableTypeCreate } from "@/models/observableType";
import { createCustomPinia } from "@tests/unitHelpers";
import { genericObjectCreateFactory } from "@mocks/genericObject";

createCustomPinia();

describe("Observable type API calls", () => {
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: observableTypeCreate = genericObjectCreateFactory();

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/observable/type/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await ObservableType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post(
        "/observable/type/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await ObservableType.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/observable/type/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await ObservableType.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post(
        "/observable/type/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await ObservableType.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /observable/type/{uuid} when read is called", async () => {
    myNock.get("/observable/type/1").reply(200, successMessage);

    const res = await ObservableType.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /observable/type/ when readAll is called", async () => {
    myNock.get("/observable/type/?offset=0").reply(200, readAllSuccesssObject);

    const res = await ObservableType.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /observable/type/ with given params when readPage is called", async () => {
    myNock
      .get("/observable/type/?offset=0&limit=10")
      .reply(200, successMessage);

    const res = await ObservableType.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /observable/type/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/observable/type/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await ObservableType.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/observable/type/1").reply(404, failureMessage);

    try {
      await ObservableType.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
