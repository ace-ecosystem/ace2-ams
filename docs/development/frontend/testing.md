## Running Tests

Please see the [Running Tests](../index.md#frontend) section for further details on running tests.

### Unit Tests

#### What to test

Unit tests should be written for any TS/JS code:

- Pinia stores
- Services, such as API services
- Helper/validator functions

#### Testing Pinia Stores

ToDO

#### Testing Services

ToDo

#### Testing Helpers

ToDo

### Component Tests

#### What & How to Test

##### Basic Guidelines

_Do:_

- Create a respective test file for each Single-File Component
    - ```MyComponent.vue``` &rarr; ```MyComponent.spec.ts```
- Write test cases for each possible application state
    - *Blank state* - when the component is freshly loaded
    - *Interactive state* - when elements of the component are interacted with, and the component's behavior in response
    - *Error state* - when things go wrong (invalid input, API errors, etc.)
- Use a factory function to create a freshly mounted instance of the component under test in each test
- Write test cases for all (valid) prop-type combinations
- Write test cases for varying (valid) initial store states, if the component accesses any Pinia stores
- Think like a user when writing tests -- try to select elements by their visible text first
- Use the following precedence when choosing how to select an element (note: some PrimeVue elements may make this difficult, so this is just a guideline):
    - ```cy.contains("Desired Element Text")```
    - ```cy.get('[data-cy=desired-element-prop]')```
    - ```cy.get('[name=desired-element-name]')```
    - ```cy.get('#desired-element-id')```
    - ```cy.get('.desired-element-class) // Avoid as much as possible ```
    - ```cy.get('button') // Avoid at all costs```

_Do Not:_

- Test the internals of a component, e.g., any functions within the `<setup>` tags
- Test child component functionality/presentation where it can be avoided
- Test a component mounted with invalid props (this should not happen IRL)
- Write deterministic tests
    - Tests that rely on current date or time
    - Tests that rely on API availability
    - Tests that rely on any "random" value

##### Mocking

Because components pull in data from nearly every part of the application (Pinia stores, API services, configuration, helpers, 'external' data from backend, etc.), a lot of mocking and stubbing is required to make sure components are tested in isolation.

Below are some quick explanations of how to mock or stub some of those pieces, as well as examples in existing tests.

Cypress component test are built off of vue-test-utils in order to mount components. Examples and more detailed explanations of the below can be found [here](https://github.com/cypress-io/cypress/tree/develop/npm/vue).

###### Component Mounting Options
Because the Cypress Component Test Runner is built off of vue-test-utils, any of the mounting options available through vue-test-utils will also be available to use in component tests.

The most common in this project are the following:

- global/directives
    - Some components in Vue use 'directives,' which HTML attributes that tell the component to do something (focus, blur, appear on hover, etc.)
    - Because directives are registered at the base App-level, we have to define them in this section of component mounting
    - The most common directive currently in use is the 'ToolTip' -- watch out for strange errors from components that use this directive!
    - Example: 

            mount(MyComponent, {
                  global: {
                    directives: { tooltip: Tooltip }
                  },
                });
            

- global/plugins
    - This is where we can register our various plugins such as PrimeVue, our router, and Pinia
    - See [Mocking Pinia](#mocking-pinia) below for more details on setting up mock Pinia data
    - Examples:

              // Component does not use Pinia
              mount(MyComponent, {
                global: {
                  plugins: [
                    PrimeVue,
                    router,
                  ],
                },
              });

              // Component uses Pinia, but doesn't require any special configuration
              mount(MyComponent, {
                global: {
                  plugins: [
                    PrimeVue,
                    createPinia(),
                    router,
                  ],
                },
              });

              // Component uses Pinia, and will require special configuration
              mount(MyComponent, {
                global: {
                  plugins: [
                    PrimeVue,
                    createCustomCypressPinia(testingOptions),
                    router,
                  ],
                },
              });

- global/provide
    - This is where any data that is injected in the component under test can be mocked out
    - *Note:* If the test is injecting some form of configuration, make sure to import the data from `testConfiguration`
    - Example: 
                
            mount(MyComponent, {
                  global: {
                    provide: {
                      exampleProvide: "stubData",
                      exampleConfig: testConfiguration.exampleConfig,
                    },
                  },
                });
            
- propsData
    - This is where any data provided as props to the component under test can be mocked out
    - This is the mounting option most likely to change from test to test
    - Creating an interface for a given component's props can make it easier to confidently put together various props
    - Example:
          - AlertTableCell.spec.ts

                  interface myComponentProps {
                    name: string
                  }

                  const defaultProps: myComponentProps = {
                      name: "TestName"
                  }

                  mount(MyComponent, {
                    propsData: defaultProps
                  });

- slots
    - This is where custom slot templates can be given to components with any number of slots
    - Example: 
                  
            mount(MyComponent, {
              slots: {
                  header: '<h1>HEADER</h1>',
                  footer: '<div>FOOTER</div>',
                },
            }); 

###### Mocking Test Data

Mocking data, either in the form of props, injected data, or data returned from API calls is crucial.

Wherever possible use the mock object factories provided in the `mocks/**` directory. This will make sure that whatever mock data that is used aligns with its respective data model.

For data that will not be commonly re-used and does not have associated factory functions, feel free to create one-off mocks in the given test file. See `SandboxAnalysis.spec.ts` for an example. 

###### Mocking Pinia

_When to use CreatePinia()_

- A component uses Pinia but actions/getters/state do not need to be mocked (i.e. don't rely on outside data)
    - Example: a component uses the ModalStore to open/close modals , in which you want to test that clicking a Modal's button will open the modal.

_When to use CreateCustomCypressPinia()_

- A component using pinia needs to have an initial state.
    - Example: TheAlertDetails pulls details from the open alert in the alertStore
- A component using pinia needs to have pinia actions/getters stubbed out
    - Because of limitations between how `TestingPinia` and Cypress stubs and spies work, pinia actions/getters cannot be stubbed directly by name
    - If `stubActions` is set to `true` (default) in `createCustomCypressPinia`, Cypress **stubs** will be used, which do NOT call functions being stubbed
    - If `stubActions` is set to `false` in `createCustomCypressPinia`, Cypress **spies** will be used, which DO call functions being spied on
    - If you want to verify the callCount/arguments with which a pinia function was called, you can do so as below: 

            mount(MyComponent, { global: {
                plugins: [createCustomCypressPinia(), PrimeVue, router],
              }
            }); 

            cy.get("@stub-1").should("have.been.calledWith", expectedArgs);

        Stubs will be accessed like `stub-#`, the number being the order in which the method was called. **Definitely not ideal**, but again this is how it works based on a limitation with `testingPinia`.

###### Mocking API Calls

- Mock API calls by stubbing out the API service call rather than using nock or trying to respond dynamically to the request.
- Example:

        // Example of failed API request
        cy.stub(Event, "read")
          .as("fetchEvent")  // Alias to access this request later
          .rejects(new Error("Request failed with status code 404"));

        // Example of successful API request
        cy.stub(Event, "read")
          .withArgs("uuid") // Specify expected arguments here
          .as("fetchEvent")
          .resolves(eventStub);

- More detailed examples in following tests:
    - AnalyzeAlertForm.spec.ts    
    - EventAlertsTable.spec.ts    

##### Testing Strategies

Some things you might want to test might not be very intuitive using Cypress.

###### Testing Links

If a component dynamically generates a link, you might want to test that said link was correctly generated and attached to the element.

You can easily do this by doing the following, rather than clicking on the element and checking the resulting window location.

        cy.contains("Click Me to Go To New Page!")
          .invoke("attr", "href")
          .should("contain", "/my/page"); // check for the dynamically generated link here

###### Testing Time-Dependent Data

Component tests are set-up to automatically run in the Eastern/New_York timezone, no matter where the tests are actually being ran from. Make sure to consider that as some datetimes are reformatted to be in the browser's timezone.

In some cases, the current time will be auto-filled into forms. In order to check that these values are set correctly, `cy.clock` can be used to mock the current time, so that this value will be the same whenever tests are ran.

Example:

    // Using UTC for the test time will make it easier to convert where necessary
    const testTime = new Date(Date.UTC(2022, 2, 29, 12, 0, 0, 0)).getTime();
    
    describe("My Test Suite", () => {
      it("My Test", () => {
        cy.clock(testTime);
        // Rest of test...
      });
    });


###### Testing for Child Components

For the most part, you won't need to test for child components, however, in some cases you may want to access child components in order to verify that they were rendered. 

Example: `EmailAnalysis.vue`, is really just a container for its child components.

Example of how to check for child components:

    import ChildComponent from "@/components/ChildComponent.vue";
    import ParentComponent from "@/components/ParentComponent.vue";
    mount(ParentComponent).then((wrapper) => {
      expect(wrapper.getComponent(ChildComponent)).to.exist;
    });

###### Testing for Event (reaction and emitted)

TBU (once I get better examples :))

### End-to-End Tests

ToDo
