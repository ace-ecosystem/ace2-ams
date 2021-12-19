import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeTreeCreate, nodeUpdate } from "./node";
import {
  analysisModuleTypeNodeTreeRead,
  analysisModuleTypeRead,
} from "./analysisModuleType";
import { observableTreeRead } from "./observable";

export interface analysisCreate extends nodeCreate {
  alertUuid: UUID;
  analysisModuleType?: UUID;
  details?: Record<string, unknown>;
  errorMessage?: string;
  nodeTree: nodeTreeCreate;
  stackTrace?: string;
  summary?: string;
  [key: string]: unknown;
}

export interface analysisRead extends nodeRead {
  alertUuid?: UUID;
  analysisModuleType: analysisModuleTypeRead;
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  stackTrace: string | null;
  summary: string | null;
}

export interface analysisTreeRead {
  analysisModuleType: analysisModuleTypeNodeTreeRead;
  children: observableTreeRead[];
  firstAppearance?: boolean;
  nodeType: string;
  parentTreeUuid: UUID | null;
  treeUuid: UUID;
  uuid: UUID;
}

export interface analysisUpdate extends nodeUpdate {
  analysisModuleType?: UUID;
  details?: Record<string, unknown> | null;
  errorMessage?: string | null;
  stackTrace?: string | null;
  summary?: string | null;
  [key: string]: unknown;
}
