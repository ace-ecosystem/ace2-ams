import { UUID } from "./base";
import {
  analysisModuleTypeAlertTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { observableRead, observableTreeRead } from "./observable";

export interface analysisRead {
  analysisModuleType: analysisModuleTypeRead;
  cachedUntil: string | null;
  childObservables: observableRead[];
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  objectType: string;
  runTime: string;
  stackTrace: string | null;
  summary: string | null;
  uuid: UUID;
}

export interface analysisTreeRead {
  // analysisModuleType will be null in the case of the rootAnalysis object
  analysisModuleType: analysisModuleTypeAlertTreeRead | null;
  children: observableTreeRead[];
  errorMessage: string | null;
  firstAppearance?: boolean;
  objectType: string;
  stackTrace: string | null;
  summary: string | null;
  uuid: UUID;
}

export interface rootAnalysisTreeRead extends analysisTreeRead {
  details: Record<string, unknown> | null;
}
