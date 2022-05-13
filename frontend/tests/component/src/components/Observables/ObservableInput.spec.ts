import { mount } from "@cypress/vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";

import ObservableInput from "@/components/Observables/ObservableInput.vue";

function factory(args = {}) {
  return mount(ObservableInput, {
    global: {
      plugins: [PrimeVue, createPinia()],
    },
  });
}

describe("ObservableInput", () => {
  it("renders correctly with no given style or header props", () => {
    factory();
  });
});
