import { createTestingPinia } from "@pinia/testing";
import { useAuthStore } from "@/stores/auth";
import { userRead } from "@/models/user";

createTestingPinia();

const store = useAuthStore();

const mockUser: userRead = {
  defaultAlertQueue: { description: null, uuid: "1", value: "default" },
  displayName: "Test Analyst",
  email: "analyst@test.com",
  enabled: true,
  roles: [],
  timezone: "UTC",
  username: "test analyst",
  uuid: "1",
};

describe("auth Getters", () => {
  beforeEach(() => {
    store.$reset();
  });

  it("will return isAuthenticated state when not logged in", () => {
    expect(store.isAuthenticated).toStrictEqual(false);
  });

  it("will return isAuthenticated state when logged in", () => {
    store.user = mockUser;

    expect(store.isAuthenticated).toStrictEqual(true);
  });
});
