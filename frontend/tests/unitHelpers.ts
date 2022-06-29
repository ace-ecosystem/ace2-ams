import { vi } from "vitest";
import { createTestingPinia, TestingOptions } from "@pinia/testing";

export const createCustomPinia = (options?: TestingOptions) => {
  const defaultOptions: TestingOptions = {
    createSpy: vi.fn,
    stubActions: false,
  };
  if (options) {
    return createTestingPinia({ ...options, ...defaultOptions });
  }

  return createTestingPinia(defaultOptions);
};
