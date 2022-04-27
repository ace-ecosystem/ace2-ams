import { analysisRead, analysisTreeRead } from "@/models/analysis";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "@/models/analysisModuleType";

export const analysisModuleTypeReadFactory = ({
  cacheSeconds = 90,
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
  cacheSeconds: cacheSeconds,
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
  cachedUntil = new Date(),
  details = { test: "test description" },
  errorMessage = null,
  stackTrace = null,
  summary = null,
  nodeType = "analysis",
  uuid = "uuid2",
}: Partial<analysisRead> = {}): analysisRead => ({
  version: version,
  analysisModuleType: analysisModuleType,
  cachedUntil: cachedUntil,
  childObservables: [],
  details: details,
  errorMessage: errorMessage,
  stackTrace: stackTrace,
  summary: summary,
  nodeType: nodeType,
  uuid: uuid,
});

export const analysisModuleTypeNodeTreeReadFactory = ({
  value = "TestAnalysis",
  uuid = "testUuid",
}: Partial<analysisModuleTypeNodeTreeRead> = {}): analysisModuleTypeNodeTreeRead => ({
  value: value,
  uuid: uuid,
});

export const analysisTreeReadFactory = ({
  analysisModuleType = analysisModuleTypeNodeTreeReadFactory(),
  children = [],
  parentTreeUuid = "",
  treeUuid = "",
  firstAppearance = undefined,
  uuid = "testUuid",
  version = "",
}: Partial<analysisTreeRead> = {}): analysisTreeRead => ({
  analysisModuleType: analysisModuleType,
  children: children,
  parentTreeUuid: parentTreeUuid,
  treeUuid: treeUuid,
  firstAppearance: firstAppearance,
  nodeType: "analysis",
  uuid: uuid,
  version: version,
});
