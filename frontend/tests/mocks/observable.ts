import { observableRead, observableTreeRead } from "@/models/observable";
import { genericObjectReadFactory } from "./genericObject";

export const observableReadFactory = ({
  time = new Date("2020-01-01"),
  uuid = "observableUuid1",
  value = "TestObservable",
  comments = [],
  context = null,
  directives = [],
  forDetection = false,
  expiresOn = null,
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
  expiresOn: expiresOn,
  redirectionUuid: redirectionUuid,
  tags: tags,
  threatActors: threatActors,
  threats: threats,
  type: type,
  nodeType: "observable",
  version: version,
});

export const observableTreeReadFactory = ({
  children = [],
  parentTreeUuid = "",
  treeUuid = "",
  time = new Date("2020-01-01"),
  uuid = "observableUuid1",
  value = "TestObservable",
  comments = [],
  context = null,
  directives = [],
  forDetection = false,
  expiresOn = null,
  redirectionUuid = null,
  tags = [],
  threatActors = [],
  threats = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  version = "observableVersion1",
}: Partial<observableTreeRead> = {}): observableTreeRead => ({
  children: children,
  parentTreeUuid: parentTreeUuid,
  treeUuid: treeUuid,
  uuid: uuid,
  version: version,
  time: time,
  value: value,
  comments: comments,
  context: context,
  directives: directives,
  forDetection: forDetection,
  expiresOn: expiresOn,
  redirectionUuid: redirectionUuid,
  tags: tags,
  threatActors: threatActors,
  threats: threats,
  type: type,
  nodeType: "observable",
});
