/**
 * @jest-environment node
 */

import snakecaseKeys from "snakecase-keys";
import { BaseApi, GenericEndpoint } from "@/services/api/base";
import myNock from "@unit/services/api/nock";

describe("BaseAPI calls", () => {
  const api = new BaseApi();

  it("will make a post and get request after a successful create when getAfterCreate is true and there is a 'content-location' header", async () => {
    myNock
      .post("/create")
      .reply(200, "Create successful", {
        "content-location": "http://test_app.com:1234/newItem",
      })
      .get("/newItem")
      .reply(200, "Read successful");
    const res = await api.createRequest("/create");
    expect(res).toEqual("Read successful");
  });

  it("will make only a post request when getAfterCreate is true and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.createRequest("/create");
    expect(res).toEqual("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful", {
      "content-location": "http://test_app.com:1234/newItem",
    });
    const res = await api.createRequest("/create", {}, false);
    expect(res).toEqual("Create successful");
  });

  it("will make only a post request when getAfterCreate is false and there is NOT a 'content-location' header", async () => {
    myNock.post("/create").reply(200, "Create successful");
    const res = await api.createRequest("/create", {}, false);
    expect(res).toEqual("Create successful");
  });

  it("make a get request when readRequest called", async () => {
    myNock.get("/read").reply(200, "Read successful");
    const res = await api.readRequest("/read");
    expect(res).toEqual("Read successful");
  });

  it("make a patch request when updateRequest called", async () => {
    myNock.patch("/update").reply(200, "Update successful");
    const res = await api.updateRequest("/update");
    expect(res).toEqual("Update successful");
  });

  it("will format outgoing data into snake_case keys", async () => {
    myNock
      .post("/create", { first_key: "A", second_key: 2 })
      .reply(200, "Update successful");
    const res = await api.createRequest("/create", {
      firstKey: "A",
      secondKey: 2,
    });
    expect(res).toEqual("Update successful");
  });

  it("will format incoming data into camelCase keys", async () => {
    myNock.post("/create").reply(200, { first_key: "A", second_key: 2 });
    const res = await api.createRequest("/create");
    expect(res).toEqual({
      firstKey: "A",
      secondKey: 2,
    });
  });

  it("will format incoming objects in a list format into camelCase keys", async () => {
    myNock.post("/create").reply(200, [
      { first_key: "A", second_key: 2 },
      { third_key: "B", fourth_key: 3 },
    ]);
    const res = await api.createRequest("/create");
    expect(res).toEqual([
      {
        firstKey: "A",
        secondKey: 2,
      },
      {
        thirdKey: "B",
        fourthKey: 3,
      },
    ]);
  });

  it("will throw an error if a request completes, but without a successful response code", async () => {
    myNock.patch("/update").reply(404, "Not found :(");
    await expect(api.updateRequest("/update")).rejects.toEqual(
      new Error("Request failed with status code 404"),
    );
  });
});

describe("generic API calls", () => {
  const genericObject = new GenericEndpoint("/object/");
  const successMessage = "Request successful";
  const secondSuccessMessage = "Request 2 successful";
  const failureMessage = "Request failed";
  const mockObject = {
    uuid: "1",
    name: "Test",
  };

  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is NOT a content-location header", async () => {
    myNock
      .post("/object/", JSON.stringify(snakecaseKeys(mockObject)))
      .reply(200, successMessage);

    const res = await genericObject.create(mockObject, false);
    expect(res).toEqual(successMessage);
  });
  it("will make only a post request when create is called and return create results if getAfterCreate is false and there is a content-location header", async () => {
    myNock
      .post("/object/", JSON.stringify(snakecaseKeys(mockObject)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      });

    const res = await genericObject.create(mockObject, false);
    expect(res).toEqual(successMessage);
  });
  it("will make only a post request when create is called and return create results if getAfterCreate is true and there is NOT a content-location header", async () => {
    myNock
      .post("/object/", JSON.stringify(snakecaseKeys(mockObject)))
      .reply(200, successMessage);

    const res = await genericObject.create(mockObject);
    expect(res).toEqual(successMessage);
  });
  it("will make a post and get request when create is called and return GET results if getAfterCreate is true and there is a content-location header", async () => {
    myNock
      .post("/object/", JSON.stringify(snakecaseKeys(mockObject)))
      .reply(200, successMessage, {
        "content-location": "http://test_app.com:1234/newItem",
      })
      .get("/newItem")
      .reply(200, secondSuccessMessage);

    const res = await genericObject.create(mockObject);
    expect(res).toEqual(secondSuccessMessage);
  });
  it("will make a get request to /object/{uuid} when getSingle is called", async () => {
    myNock.get("/object/1").reply(200, successMessage);

    const res = await genericObject.getSingle("1");
    expect(res).toEqual(successMessage);
  });
  it("will make a get request to /object/ when getAll is called", async () => {
    myNock.get("/object/").reply(200, JSON.stringify([mockObject, mockObject]));

    const res = await genericObject.getAll();
    expect(res).toEqual([mockObject, mockObject]);
  });
  it("will make a patch request to /object/{uuid} when updateSingle is called", async () => {
    myNock
      .patch("/object/1", JSON.stringify({ name: "New Name" }))
      .reply(200, successMessage);

    const res = await genericObject.updateSingle({ name: "New Name" }, "1");
    expect(res).toEqual(successMessage);
  });
  it("will throw an error if a request fails", async () => {
    myNock.get("/object/1").reply(404, failureMessage);

    await expect(genericObject.getSingle("1")).rejects.toEqual(
      new Error("Request failed with status code 404"),
    );
  });
});
