import {
  observableInAlertRead,
  observableRead,
  observableTreeRead,
} from "@/models/observable";
import { analysisMetadataReadFactory } from "./analysisMetadata";
import { genericObjectReadFactory } from "./genericObject";

export const observableReadFactory = ({
  uuid = "observableUuid1",
  value = "TestObservable",
  context = null,
  forDetection = false,
  expiresOn = null,
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  version = "observableVersion1",
  observableRelationships = [],
}: Partial<observableRead> = {}): observableRead => ({
  uuid: uuid,
  value: value,
  context: context,
  forDetection: forDetection,
  expiresOn: expiresOn,
  tags: tags,
  type: type,
  objectType: "observable",
  version: version,
  observableRelationships: observableRelationships,
});

export const observableInAlertReadFactory = ({
  uuid = "observableUuid1",
  value = "TestObservable",
  analysisMetadata = analysisMetadataReadFactory(),
  context = null,
  dispositionHistory = [],
  forDetection = false,
  expiresOn = null,
  matchingEvents = [],
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  version = "observableVersion1",
  observableRelationships = [],
}: Partial<observableInAlertRead> = {}): observableInAlertRead => ({
  uuid: uuid,
  value: value,
  analysisMetadata: analysisMetadata,
  context: context,
  dispositionHistory: dispositionHistory,
  forDetection: forDetection,
  expiresOn: expiresOn,
  matchingEvents: matchingEvents,
  tags: tags,
  type: type,
  objectType: "observable",
  version: version,
  observableRelationships: observableRelationships,
});

export const observableTreeReadFactory = ({
  children = [],
  uuid = "observableUuid1",
  value = "TestObservable",
  analysisMetadata = analysisMetadataReadFactory(),
  context = null,
  dispositionHistory = [],
  firstAppearance = undefined,
  forDetection = false,
  expiresOn = null,
  matchingEvents = [],
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  version = "observableVersion1",
  observableRelationships = [],
}: Partial<observableTreeRead> = {}): observableTreeRead => ({
  children: children,
  uuid: uuid,
  version: version,
  value: value,
  analysisMetadata: analysisMetadata,
  context: context,
  dispositionHistory: dispositionHistory,
  firstAppearance: firstAppearance,
  forDetection: forDetection,
  expiresOn: expiresOn,
  matchingEvents: matchingEvents,
  tags: tags,
  type: type,
  objectType: "observable",
  observableRelationships: observableRelationships,
});
