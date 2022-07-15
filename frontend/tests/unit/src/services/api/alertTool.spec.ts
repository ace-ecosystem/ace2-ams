/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { AlertTool } from "@/services/api/alertTool";
import myNock from "@unit/services/api/nock";
import { alertToolCreate } from "@/models/alertTool";
import { createCustomPinia } from "@tests/unitHelpers";
import { genericObjectCreateFactory } from "@mocks/genericObject";

createCustomPinia();

describe("Tool API calls", () => {
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: alertToolCreate = genericObjectCreateFactory();

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/alert/tool/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await AlertTool.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/alert/tool/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await AlertTool.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/alert/tool/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await AlertTool.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/alert/tool/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await AlertTool.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /alert/tool/{uuid} when read is called", async () => {
    myNock.get("/alert/tool/1").reply(200, successMessage);

    const res = await AlertTool.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /alert/tool/ when readAll is called", async () => {
    myNock.get("/alert/tool/?offset=0").reply(200, readAllSuccesssObject);

    const res = await AlertTool.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /alert/tool/ with given params when readPage is called", async () => {
    myNock.get("/alert/tool/?offset=0&limit=10").reply(200, successMessage);

    const res = await AlertTool.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /alert/tool/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/alert/tool/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await AlertTool.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/alert/tool/1").reply(404, failureMessage);

    try {
      await AlertTool.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
