/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { MetadataDirective } from "@/services/api/metadataDirective";
import myNock from "@unit/services/api/nock";
import { metadataDirectiveCreate } from "@/models/metadataDirective";
import { createCustomPinia } from "@tests/unitHelpers";
import { genericObjectCreateFactory } from "@mocks/genericObject";

createCustomPinia();

describe("MetadataDirective API calls", () => {
  const successMessage = "Request successful";
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: metadataDirectiveCreate =
    genericObjectCreateFactory();

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/metadata/directive/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await MetadataDirective.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post(
        "/metadata/directive/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await MetadataDirective.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/metadata/directive/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await MetadataDirective.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post(
        "/metadata/directive/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await MetadataDirective.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /metadata/directive/{uuid} when read is called", async () => {
    myNock.get("/metadata/directive/1").reply(200, successMessage);

    const res = await MetadataDirective.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /metadata/directive/ when readAll is called", async () => {
    myNock
      .get("/metadata/directive/?offset=0")
      .reply(200, readAllSuccesssObject);

    const res = await MetadataDirective.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /metadata/directive/ with given params when readPage is called", async () => {
    myNock
      .get("/metadata/directive/?offset=0&limit=10")
      .reply(200, successMessage);

    const res = await MetadataDirective.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /metadata/directive/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/metadata/directive/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await MetadataDirective.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/metadata/directive/1").reply(404, failureMessage);

    try {
      await MetadataDirective.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
