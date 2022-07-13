/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { AlertDisposition } from "@/services/api/alertDisposition";
import myNock from "@unit/services/api/nock";
import { alertDispositionCreate } from "@/models/alertDisposition";
import { createCustomPinia } from "@tests/unitHelpers";

createCustomPinia();

describe("Disposition API calls", () => {
  const readAllSuccesssObject = { items: [], response: "Request successful" };
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: alertDispositionCreate[] = [
    {
      submissionUuid: "uuid1",
      description: "This is a disposition",
      username: "Alice",
      value: "Test",
    },
  ];

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/alert/disposition/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await AlertDisposition.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post(
        "/alert/disposition/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await AlertDisposition.create(mockObjectCreate, false);
    expect(res).toEqual(successMessage);
  });

  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post(
        "/alert/disposition/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage);

    const res = await AlertDisposition.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post(
        "/alert/disposition/",
        JSON.stringify(snakecaseKeys(mockObjectCreate)),
      )
      .reply(200, successMessage, {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await AlertDisposition.create(mockObjectCreate, true);
    expect(res).toEqual(secondSuccessMessage);
  });

  it("will make a get request to /alert/disposition/{uuid} when read is called", async () => {
    myNock.get("/alert/disposition/1").reply(200, successMessage);

    const res = await AlertDisposition.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /alert/disposition/ when readAll is called", async () => {
    myNock
      .get("/alert/disposition/?offset=0")
      .reply(200, readAllSuccesssObject);

    const res = await AlertDisposition.readAll();
    expect(res).toEqual(readAllSuccesssObject.items);
  });

  it("will make a get request to /alert/disposition/ with given params when readPage is called", async () => {
    myNock
      .get("/alert/disposition/?offset=0&limit=10")
      .reply(200, successMessage);

    const res = await AlertDisposition.readPage({ offset: 0, limit: 10 });
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /alert/disposition/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/alert/disposition/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await AlertDisposition.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/alert/disposition/1").reply(404, failureMessage);

    try {
      await AlertDisposition.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
