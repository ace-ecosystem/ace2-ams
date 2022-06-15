import { UUID } from "./base";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { observableRead, observableTreeRead } from "./observable";

export interface analysisRead {
  analysisModuleType: analysisModuleTypeRead;
  cachedUntil: Date;
  childObservables: observableRead[];
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  nodeType: string;
  runTime: Date;
  stackTrace: string | null;
  summary: string | null;
  uuid: UUID;
}

export interface analysisTreeRead {
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  children: observableTreeRead[];
  errorMessage: string | null;
  firstAppearance?: boolean;
  nodeType: string;
  stackTrace: string | null;
  summary: string | null;
  uuid: UUID;
}
