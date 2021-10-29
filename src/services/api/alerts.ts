import { GenericEndpoint } from "./base";

class alerts extends GenericEndpoint {
  getAll() {
    return Promise.reject(Error("Not implemented."));
  }
}

export default new alerts("/alert/");
