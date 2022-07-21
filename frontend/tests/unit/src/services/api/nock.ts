/* Sets up the nock instance to mock out any requests being made */

import nock from "nock";

const defaultReplyHeaders = {
  "access-control-allow-origin": "*",
  "access-control-allow-credentials": "true",
};

const myNock = nock("http://localhost:3000/api").defaultReplyHeaders(
  defaultReplyHeaders,
);

export default myNock;
