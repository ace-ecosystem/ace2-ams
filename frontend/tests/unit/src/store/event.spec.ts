import myNock from "@unit/services/api/nock";
import { useEventStore } from "@/stores/event";
import { eventReadFactory } from "@mocks/events";
import { createCustomPinia } from "@unit/helpers";

createCustomPinia();

const store = useEventStore();

const mockEvent = eventReadFactory({ uuid: "uuid1" });

describe("event Actions", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will fetch event data given an event ID", async () => {
    const mockRequest = myNock.get("/event/uuid1").reply(200, mockEvent);
    await store.read("uuid1");

    expect(mockRequest.isDone()).toEqual(true);

    // The open is not parsed at all when received, so any dates will be in string format
    expect(store.open).toEqual(JSON.parse(JSON.stringify(mockEvent)));
  });

  it("will throw an error if read fails", async () => {
    const mockRequest = myNock.get("/event/uuid1").reply(403);
    await expect(store.read("uuid1")).rejects.toThrowError();

    expect(mockRequest.isDone()).toEqual(true);
  });

  it("will make a request to update an event given the UUID and update data upon the updateEvent action", async () => {
    const mockRequest = myNock.patch("/event/").reply(200);
    await store.update([{ uuid: "uuid1", name: "test" }]);

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.open).toBeNull();
  });

  it("will throw an error if update fails", async () => {
    const mockRequest = myNock.patch("/event/").reply(403);
    await expect(
      store.update([{ uuid: "uuid1", name: "test" }]),
    ).rejects.toThrowError();

    expect(mockRequest.isDone()).toEqual(true);
    // None of these should be changed
    expect(store.open).toBeNull();
  });
});
