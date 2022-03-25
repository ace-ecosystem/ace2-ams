import { eventFilterParams } from "@/models/event";
import { Event } from "@/services/api/event";
import myNock from "@unit/services/api/nock";
import { eventCreateFactory, eventUpdateFactory } from "@mocks/events";

describe("Event calls", () => {
  const api = Event;

  it("will make a post to the /event endpoint with eventCreate data when 'create' is called", async () => {
    myNock.post("/event/").reply(200, "Create successful", {
      "content-location": "/newItem",
    });
    const res = await api.create(eventCreateFactory());
    expect(res).to.eql("Create successful");
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
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid} endpoint when 'read' is called with a given UUID", async () => {
    myNock.get("/event/uuid").reply(200, "Read successful");
    const res = await api.read("uuid");
    expect(res).to.eql("Read successful");
  });
  it("will make a get request to the /event/{uuid}/history endpoint when 'readHistory' is called with a given UUID", async () => {
    myNock.get("/event/uuid/history").reply(200, "Read successful");
    const res = await api.readHistory("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/observable endpoint when 'readObservableSummary' is called with a given UUID", async () => {
    myNock.get("/event/uuid/summary/observable").reply(200, "Read successful");
    const res = await api.readObservableSummary("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/user endpoint when 'readUserSummary' is called with a given UUID", async () => {
    myNock.get("/event/uuid/summary/user").reply(200, "Read successful");
    const res = await api.readUserSummary("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/url_domain endpoint when 'readUrlDomainSummary' is called with a given UUID", async () => {
    myNock.get("/event/uuid/summary/url_domain").reply(200, "Read successful");
    const res = await api.readUrlDomainSummary("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/email endpoint when 'readEmailSummary' is called with a given UUID", async () => {
    myNock.get("/event/uuid/summary/email").reply(200, "Read successful");
    const res = await api.readEmailSummary("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/email_headers_body endpoint when 'readEmailHeadersAndBody' is called with a given UUID", async () => {
    myNock
      .get("/event/uuid/summary/email_headers_body")
      .reply(200, "Read successful");
    const res = await api.readEmailHeadersAndBody("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/{uuid}/summary/detection_point endpoint when 'readDetectionSummary' is called with a given UUID", async () => {
    myNock
      .get("/event/uuid/summary/detection_point")
      .reply(200, "Read successful");
    const res = await api.readDetectionSummary("uuid");
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/ endpoint when 'readPage' is called with no params, if none given", async () => {
    myNock.get("/event/").reply(200, "Read successful");
    const res = await api.readPage();
    expect(res).to.eql("Read successful");
  });

  it("will make a get request to the /event/?offset={offset} endpoint as many times as needed to get all pages when 'readAllPages' is called with no params, if none given", async () => {
    myNock
      .get("/event/?offset=0")
      .reply(200, { limit: 1, total: 1, items: ["eventA"] });
    const res = await api.readAllPages();
    expect(res).to.eql(["eventA"]);
  });

  it("will make a get request to the /event/?offset={offset} endpoint as many times as needed to get all pages when 'readAllPages' is called with formatted params, if given", async () => {
    const eventParams: eventFilterParams = {
      limit: 10,
      name: "Test Name",
    };
    myNock
      .get("/event/?offset=0&limit=10&name=Test+Name")
      .reply(200, { limit: 10, total: 1, items: ["eventA"] });
    const res = await api.readAllPages(eventParams);
    expect(res).to.eql(["eventA"]);
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
    expect(res).to.eql("Read successful");
  });

  it("will make a patch request to the /event/ endpoint when 'update' is called with an array of update data", async () => {
    myNock.patch("/event/").reply(200, "Update successful");
    const res = await api.update([eventUpdateFactory()]);
    expect(res).to.eql("Update successful");
  });
});
