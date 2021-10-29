import Vuex from "vuex";
import makeGenericModule from "../../../../src/store/generic";
import myNock from "../services/api/nock";
import axios from "axios";

class stubService {
  async getAll() {
    const response = await axios
      .get("http://test_app.com:1234/item/")
      .catch((error) => {
        throw error;
      });
    return response.data;
  }
}

const genericStore = makeGenericModule(new stubService());
const actions = genericStore.actions;
const mutations = genericStore.mutations;
const getters = genericStore.getters;

const mockItem = {
  uuid: "id1",
};

describe("generic Getters", () => {
  it("will return empty list when no items exist/have been pulled", () => {
    const state = { items: [] };
    const store = new Vuex.Store({ state, getters });

    expect(store.getters["allItems"]).toStrictEqual([]);
  });
  it("will return list of retrieved items", () => {
    const items = [mockItem];
    const state = { items: items };
    const store = new Vuex.Store({ state, getters });

    expect(store.getters["allItems"]).toStrictEqual(items);
  });
});

describe("generic Mutations", () => {
  it("will set a received list of items to the items list", () => {
    const state = { items: [] };
    const store = new Vuex.Store({ state, getters, mutations });

    store.commit("addItems", [mockItem, mockItem]);
    expect(state.items.length).toBe(2);
  });
});

describe("generic Actions", () => {
  it("will call the given service's getAll method upon the getAll action", async () => {
    const state = { items: [] };
    const store = new Vuex.Store({ state, getters, mutations, actions });
    const mockRequest = myNock.get("/item/").reply(200, [mockItem, mockItem]);

    await store.dispatch("getAll");

    expect(mockRequest.isDone()).toEqual(true);
    expect(state.items[0]).toEqual(mockItem);
    expect(state.items.length).toEqual(2);
  });

  it("will throw an error if the call to getAll items fails", async () => {
    const state = { items: [] };
    const store = new Vuex.Store({ state, getters, mutations, actions });
    myNock.get("/item/").reply(403, "Bad request :(");

    await expect(store.dispatch("getAll")).rejects.toEqual(
      new Error("Request failed with status code 403"),
    );
  });
});
