import { UUID } from "./base";
import {
  analysisModuleTypeNodeTreeRead,
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
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  children: observableTreeRead[];
  errorMessage: string | null;
  firstAppearance?: boolean;
  objectType: string;
  stackTrace: string | null;
  summary: string | null;
  uuid: UUID;
}
