import { GenericEndpoint } from "./base";

class observableInstance extends GenericEndpoint {
  getAll() {
    return Promise.reject(Error("Not implemented."));
  }
}

export default new observableInstance("/observable/instance/");
