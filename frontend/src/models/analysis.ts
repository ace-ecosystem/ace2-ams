import { UUID } from "./base";
import { nodeCreate, nodeRead, nodeUpdate } from "./node";
import { analysisModuleTypeRead } from "./analysisModuleType";

export interface analysisCreate extends nodeCreate {
  alertUuid: UUID;
  analysisModuleType?: UUID;
  details?: Record<string, unknown>;
  errorMessage?: string;
  parentUuid?: UUID;
  stackTrace?: string;
  summary?: string;
}

export interface analysisRead extends nodeRead {
  alertUuid: UUID;
  analysisModuleType: analysisModuleTypeRead;
  details: Record<string, unknown> | null;
  errorMessage: string | null;
  parentUuid: UUID | null;
  stackTrace: string | null;
  summary: string | null;
}

export interface analysisUpdate extends nodeUpdate {
  analysisModuleType?: UUID;
  details?: Record<string, unknown> | null;
  errorMessage?: string | null;
  stackTrace?: string | null;
  summary?: string | null;
}
