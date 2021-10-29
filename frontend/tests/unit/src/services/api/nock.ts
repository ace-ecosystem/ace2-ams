/* Sets up the nock instance to mock out any requests being made */

import nock from "nock";

const defaultReplyHeaders = {
  "access-control-allow-origin": "*",
  "access-control-allow-credentials": "true",
};

const myNock = nock("http://test_app.com:1234").defaultReplyHeaders(
  defaultReplyHeaders,
);

export default myNock;
