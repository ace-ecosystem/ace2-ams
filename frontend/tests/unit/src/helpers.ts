import { createTestingPinia, TestingOptions } from "@pinia/testing";

export const createCustomPinia = (options?: TestingOptions) => {
  const defaultOptions: TestingOptions = { createSpy: vi.fn };
  if (options) {
    return createTestingPinia({ ...options, ...defaultOptions });
  }

  return createTestingPinia(defaultOptions);
};

export const createCustomCypressPinia = (
  options?: TestingOptions,
  count = 0,
) => {
  let defaultOptions: TestingOptions = {
    createSpy: () => cy.stub().as(`stub-${(count += 1)}`),
  };

  if (options && Object.keys(options).length) {
    if (!options.stubActions) {
      defaultOptions = {
        createSpy: (fn) => {
          if (fn) {
            return cy.spy(fn).as(`spy-${(count += 1)}`);
          } else {
            return cy.spy().as(`spy-${(count += 1)}`);
          }
        },
      };
    }
    return createTestingPinia({ ...options, ...defaultOptions });
  }

  return createTestingPinia(defaultOptions);
};
