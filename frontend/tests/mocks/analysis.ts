import { analysisRead, analysisTreeRead } from "../../src/models/analysis";
import { analysisModuleTypeRead } from "../../src/models/analysisModuleType";

export const analysisModuleTypeReadFactory = ({
  description = null,
  extendedVersion = null,
  manual = false,
  observableTypes = [],
  requiredDirectives = [],
  requiredTags = [],
  value = "File Analysis",
  version = "1.0.0",
  uuid = "e77f200e-93c9-4db8-b8b9-a0daddae1f0d",
}: Partial<analysisModuleTypeRead> = {}): analysisModuleTypeRead => ({
  description: description,
  extendedVersion: extendedVersion,
  manual: manual,
  observableTypes: observableTypes,
  requiredDirectives: requiredDirectives,
  requiredTags: requiredTags,
  value: value,
  version: version,
  uuid: uuid,
});

export const analysisReadFactory = ({
  version = "f0590bba-c854-4a2c-b414-71c2bc580c4b",
  analysisModuleType = analysisModuleTypeReadFactory(),
  details = { test: "test description" },
  errorMessage = null,
  stackTrace = null,
  summary = null,
  nodeType = "analysis",
  uuid = "uuid2",
}: Partial<analysisRead> = {}): analysisRead => ({
  version: version,
  analysisModuleType: analysisModuleType,
  details: details,
  errorMessage: errorMessage,
  stackTrace: stackTrace,
  summary: summary,
  nodeType: nodeType,
  uuid: uuid,
});

export const analysisTreeReadFactory = ({
  analysisModuleType = undefined,
  children = [],
  parentTreeUuid = "",
  treeUuid = "",
  nodeType = "",
  uuid = "",
  version = "",
}: Partial<analysisTreeRead> = {}): analysisTreeRead => ({
  analysisModuleType: analysisModuleType,
  children: children,
  parentTreeUuid: parentTreeUuid,
  treeUuid: treeUuid,
  nodeType: nodeType,
  uuid: uuid,
  version: version,
});
