/**
 * @vitest-environment node
 */

import { describe, it, expect } from "vitest";
import snakecaseKeys from "snakecase-keys";
import { ObservableInstance } from "@/services/api/observable";
import myNock from "@unit/services/api/nock";
import { observableCreate } from "@/models/observable";
import { createCustomPinia } from "@tests/unitHelpers";
import { observableCreateFactory } from "@mocks/observable";

createCustomPinia();

describe("OBservable API calls", () => {
  const successMessage = "Request successful";
  const failureMessage = "Request failed";
  const mockObjectCreate: observableCreate[] = [observableCreateFactory()];

  it("will make only a post request when create is called", async () => {
    myNock
      .post("/observable/", JSON.stringify(snakecaseKeys(mockObjectCreate)))
      .reply(200, successMessage);

    const res = await ObservableInstance.create(mockObjectCreate);
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /observable/{uuid} when read is called", async () => {
    myNock.get("/observable/1").reply(200, successMessage);

    const res = await ObservableInstance.read("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a get request to /observable/{uuid} when readHistory is called", async () => {
    myNock.get("/observable/1/history").reply(200, successMessage);

    const res = await ObservableInstance.readHistory("1");
    expect(res).toEqual(successMessage);
  });

  it("will make a patch request to /observable/{uuid} when update is called", async () => {
    myNock
      .patch(
        "/observable/1",
        JSON.stringify({ username: "Alice", value: "New Name" }),
      )
      .reply(200, successMessage);

    const res = await ObservableInstance.update("1", {
      username: "Alice",
      value: "New Name",
    });
    expect(res).toEqual(successMessage);
  });

  it("will throw an error if a request fails", async () => {
    myNock.get("/observable/1").reply(404, failureMessage);

    try {
      await ObservableInstance.read("1");
    } catch (e) {
      const error = e as Error;
      expect(error.message).toStrictEqual(
        "Request failed with status code 404",
      );
    }
  });
});
