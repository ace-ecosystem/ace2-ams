import {
  analysisRead,
  analysisTreeRead,
  rootAnalysisTreeRead,
} from "@/models/analysis";
import {
  analysisModuleTypeAlertTreeRead,
  analysisModuleTypeRead,
} from "@/models/analysisModuleType";
import { genericObjectReadFactory } from "./genericObject";

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
  analysisModuleType = analysisModuleTypeReadFactory(),
  cachedUntil = null,
  details = { test: "test description" },
  errorMessage = null,
  runTime = "2020-01-01T00:00:00.000000+00:00",
  stackTrace = null,
  status = genericObjectReadFactory({ value: "complete" }),
  summary = null,
  summaryDetails = [],
  objectType = "analysis",
  uuid = "uuid2",
}: Partial<analysisRead> = {}): analysisRead => ({
  analysisModuleType: analysisModuleType,
  cachedUntil: cachedUntil,
  childObservables: [],
  details: details,
  errorMessage: errorMessage,
  runTime: runTime,
  stackTrace: stackTrace,
  status: status,
  summary: summary,
  summaryDetails: summaryDetails,
  objectType: objectType,
  uuid: uuid,
});

export const analysisModuleTypeAlertTreeReadFactory = ({
  value = "TestAnalysis",
  uuid = "testUuid",
}: Partial<analysisModuleTypeAlertTreeRead> = {}): analysisModuleTypeAlertTreeRead => ({
  value: value,
  uuid: uuid,
});

export const analysisTreeReadFactory = ({
  analysisModuleType = analysisModuleTypeAlertTreeReadFactory(),
  children = [],
  errorMessage = null,
  leafId = "testTreeUuid",
  stackTrace = null,
  status = genericObjectReadFactory({ value: "complete" }),
  summary = null,
  summaryDetails = [],
  uuid = "testUuid",
}: Partial<analysisTreeRead> = {}): analysisTreeRead => ({
  analysisModuleType: analysisModuleType,
  children: children,
  errorMessage: errorMessage,
  leafId: leafId,
  objectType: "analysis",
  stackTrace: stackTrace,
  status: status,
  summary: summary,
  summaryDetails: summaryDetails,
  uuid: uuid,
});

export const rootAnalysisTreeReadFactory = ({
  children = [],
  details = null,
  leafId = "testTreeUuid",
  status = genericObjectReadFactory({ value: "complete" }),
  summaryDetails = [],
  uuid = "testUuid",
}: Partial<rootAnalysisTreeRead> = {}): rootAnalysisTreeRead => ({
  analysisModuleType: null,
  children: children,
  details: details,
  errorMessage: null,
  leafId: leafId,
  objectType: "analysis",
  stackTrace: null,
  status: status,
  summary: null,
  summaryDetails: summaryDetails,
  uuid: uuid,
});
