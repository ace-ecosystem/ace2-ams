/**
 * @jest-environment node
 */

import { eventFilterParams } from "@/models/event";
import { Event } from "@/services/api/event";
import myNock from "@unit/services/api/nock";
import {
  eventCreateFactory,
  eventUpdateFactory,
} from "../../../../mocks/events";

describe("Event calls", () => {
  const api = Event;

  it("will make a post to the /event endpoint with eventCreate data when 'create' is called", async () => {
    myNock.post("/event/").reply(200, "Create successful", {
      "content-location": "/newItem",
    });
    const res = await api.create(eventCreateFactory());
    expect(res).toEqual("Create successful");
  });

  it("will make a get request to fetch new event when 'create' is called with getAfterEvent set to true", async () => {
    myNock
      .post("/event/")
      .reply(200, "Create successful", {
        "content-location": "/newItem",
      })
      .get("/newItem")
      .reply(200, "Read successful");
    const res = await api.create(eventCreateFactory(), true);
    expect(res).toEqual("Read successful");
  });

  it("will make a get request to the /event/{uuid} endpoint when 'read' is called with a given UUID", async () => {
    myNock.get("/event/uuid").reply(200, "Read successful");
    const res = await api.read("uuid");
    expect(res).toEqual("Read successful");
  });

  it("will make a get request to the /event/ endpoint when 'readPage' is called with no params, if none given", async () => {
    myNock.get("/event/").reply(200, "Read successful");
    const res = await api.readPage();
    expect(res).toEqual("Read successful");
  });

  it("will make a get request to the /event/ endpoint when 'readPage' is called with properly formatted params", async () => {
    const eventParams: eventFilterParams = {
      limit: 10,
      offset: 10,
      name: "Test Name",
    };
    myNock
      .get("/event/?limit=10&offset=10&name=Test+Name")
      .reply(200, "Read successful");
    const res = await api.readPage(eventParams);
    expect(res).toEqual("Read successful");
  });

  it("will make a patch request to the /event/ endpoint when 'update' is called with an array of update data", async () => {
    myNock.patch("/event/").reply(200, "Update successful");
    const res = await api.update([eventUpdateFactory()]);
    expect(res).toEqual("Update successful");
  });
});
