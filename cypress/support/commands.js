// cy.window()
//   .its("authStore")
//   .then((authStore) => {
//     console.log("user", authStore.user);
//   });

Cypress.Commands.add("login", () => {
  cy.request({
    method: "POST",
    url: "/api/auth",
    form: true,
    body: {
      username: "analyst",
      password: "analyst",
    },
  });
});

Cypress.Commands.add("logout", () => {
  cy.get('[href="/login"] > .p-button').click();
});

Cypress.Commands.add("addFormObservable", () => {
  cy.get("#add-observable").click();
});
