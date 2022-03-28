import { createTestingPinia, TestingOptions } from "@pinia/testing";

export const createCustomCypressPinia = (options?: TestingOptions) => {
  const defaultOptions: TestingOptions = { createSpy: cy.spy };
  if (options) {
    return createTestingPinia({ ...options, ...defaultOptions });
  }

  return createTestingPinia(defaultOptions);
};
