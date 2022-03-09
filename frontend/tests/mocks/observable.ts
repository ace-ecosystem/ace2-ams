import { observableRead } from "@/models/observable";
import { genericObjectReadFactory } from "./genericObject";

export const observableReadFactory = ({
  time = new Date("2020-01-01"),
  uuid = "observableUuid1",
  value = "TestObservable",
  comments = [],
  context = null,
  directives = [],
  forDetection = false,
  redirectionUuid = null,
  tags = [],
  threatActors = [],
  threats = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  version = "observableVersion1",
}: Partial<observableRead> = {}): observableRead => ({
  time: time,
  uuid: uuid,
  value: value,
  comments: comments,
  context: context,
  directives: directives,
  forDetection: forDetection,
  redirectionUuid: redirectionUuid,
  tags: tags,
  threatActors: threatActors,
  threats: threats,
  type: type,
  nodeType: "observable",
  version: version,
});
