import { genericObjectRead, UUID } from "./base";

import { metadataTagRead } from "./metadataTag";
import { metadataDirectiveRead } from "./metadataDirective";
import { observableTypeRead } from "./observableType";

export interface analysisModuleTypeRead extends genericObjectRead {
  cacheSeconds: number;
  extendedVersion: Record<string, unknown> | null;
  manual: boolean;
  observableTypes: observableTypeRead[];
  requiredDirectives: metadataDirectiveRead[];
  requiredTags: metadataTagRead[];
  version: string;
}

export interface analysisModuleTypeNodeTreeRead {
  uuid: UUID;
  value: string;
}
