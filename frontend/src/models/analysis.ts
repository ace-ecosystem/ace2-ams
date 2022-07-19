import { UUID } from "./base";
import {
  analysisModuleTypeAlertTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { analysisSummaryDetailRead } from "./analysisSummaryDetail";
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
  summaryDetails: analysisSummaryDetailRead[];
  uuid: UUID;
}

export interface analysisTreeRead {
  // analysisModuleType will be null in the case of the rootAnalysis object
  analysisModuleType: analysisModuleTypeAlertTreeRead | null;
  children: observableTreeRead[];
  errorMessage: string | null;
  criticalPath?: boolean;
  leafId: string;
  objectType: string;
  stackTrace: string | null;
  summary: string | null;
  summaryDetails: analysisSummaryDetailRead[];
  uuid: UUID;
}

export interface rootAnalysisTreeRead extends analysisTreeRead {
  details: Record<string, unknown> | null;
}
