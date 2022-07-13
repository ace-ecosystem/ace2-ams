/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { AlertToolInstance } from "@/services/api/alertToolInstance";
import myNock from "@unit/services/api/nock";
import { alertToolInstanceCreate } from "@/models/alertToolInstance";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

describe("ToolInstance API calls", () => {
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: alertToolInstanceCreate[] = [
    {
      submissionUuid: "uuid1",
      description: "This is a tool instance",
      username: "Alice",
      value: "Test",
    },
  ];

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/alert/tool/instance/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await AlertToolInstance.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post(
        "/alert/tool/instance/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await AlertToolInstance.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/alert/tool/instance/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await AlertToolInstance.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post(
        "/alert/tool/instance/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await AlertToolInstance.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /alert/tool/instance/{uuid} when read is called", async () => {
    myNock.get("/alert/tool/instance/1").reply(200, successMessage);

    const res = await AlertToolInstance.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /alert/tool/instance/ when readAll is called", async () => {
    myNock
      .get("/alert/tool/instance/?offset=0")
      .reply(200, readAllSuccesssObject);

    const res = await AlertToolInstance.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /alert/tool/instance/ with given params when readPage is called", async () => {
    myNock
      .get("/alert/tool/instance/?offset=0&limit=10")
      .reply(200, successMessage);

    const res = await AlertToolInstance.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /alert/tool/instance/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/alert/tool/instance/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await AlertToolInstance.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/alert/tool/instance/1").reply(404, failureMessage);

    try {
      await AlertToolInstance.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
