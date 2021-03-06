import {
  observableInAlertRead,
  observableCreate,
  observableRead,
  observableTreeRead,
} from "@/models/observable";
import { analysisMetadataReadFactory } from "./analysisMetadata";
import { genericObjectReadFactory } from "./genericObject";

export const observableCreateFactory = ({
  forDetection = false,
  observableRelationships = [],
  tags = [],
  type = "testType",
  uuid = "observableUuid1",
  value = "TestObservable",
  version = "observableVersion1",
  whitelisted = false,
  parentAnalysisUuid = "parentAnalysisUuid1",
}: Partial<observableCreate> = {}): observableCreate => ({
  objectType: "observable",
  observableRelationships: observableRelationships,
  tags: tags,
  type: type,
  uuid: uuid,
  value: value,
  version: version,
  whitelisted: whitelisted,
  parentAnalysisUuid: parentAnalysisUuid,
});

export const observableReadFactory = ({
  context = null,
  expiresOn = null,
  forDetection = false,
  observableRelationships = [],
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  uuid = "observableUuid1",
  value = "TestObservable",
  version = "observableVersion1",
  whitelisted = false,
}: Partial<observableRead> = {}): observableRead => ({
  context: context,
  expiresOn: expiresOn,
  forDetection: forDetection,
  objectType: "observable",
  observableRelationships: observableRelationships,
  tags: tags,
  type: type,
  uuid: uuid,
  value: value,
  version: version,
  whitelisted: whitelisted,
});

export const observableInAlertReadFactory = ({
  analysisMetadata = analysisMetadataReadFactory(),
  context = null,
  dispositionHistory = [],
  expiresOn = null,
  forDetection = false,
  matchingEvents = [],
  observableRelationships = [],
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  uuid = "observableUuid1",
  value = "TestObservable",
  version = "observableVersion1",
  whitelisted = false,
}: Partial<observableInAlertRead> = {}): observableInAlertRead => ({
  analysisMetadata: analysisMetadata,
  context: context,
  dispositionHistory: dispositionHistory,
  expiresOn: expiresOn,
  forDetection: forDetection,
  matchingEvents: matchingEvents,
  objectType: "observable",
  observableRelationships: observableRelationships,
  tags: tags,
  type: type,
  uuid: uuid,
  value: value,
  version: version,
  whitelisted: whitelisted,
});

export const observableTreeReadFactory = ({
  analysisMetadata = analysisMetadataReadFactory(),
  children = [],
  context = null,
  dispositionHistory = [],
  expiresOn = null,
  criticalPath = undefined,
  forDetection = false,
  jumpToLeaf = null,
  leafId = "testTreeUuid",
  matchingEvents = [],
  observableRelationships = [],
  tags = [],
  type = genericObjectReadFactory({ value: "testObservableType" }),
  uuid = "observableUuid1",
  value = "TestObservable",
  version = "observableVersion1",
  whitelisted = false,
}: Partial<observableTreeRead> = {}): observableTreeRead => ({
  analysisMetadata: analysisMetadata,
  children: children,
  context: context,
  dispositionHistory: dispositionHistory,
  expiresOn: expiresOn,
  criticalPath: criticalPath,
  forDetection: forDetection,
  jumpToLeaf: jumpToLeaf,
  leafId: leafId,
  matchingEvents: matchingEvents,
  objectType: "observable",
  observableRelationships: observableRelationships,
  tags: tags,
  type: type,
  uuid: uuid,
  value: value,
  version: version,
  whitelisted: whitelisted,
});
