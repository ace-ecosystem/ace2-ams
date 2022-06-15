import { genericObjectRead, UUID } from "./base";

import { metadataTagRead } from "./metadataTag";
import { nodeDirectiveRead } from "./nodeDirective";
import { observableTypeRead } from "./observableType";

export interface analysisModuleTypeRead extends genericObjectRead {
  cacheSeconds: number;
  extendedVersion: Record<string, unknown> | null;
  manual: boolean;
  observableTypes: observableTypeRead[];
  requiredDirectives: nodeDirectiveRead[];
  requiredTags: metadataTagRead[];
  version: string;
}

export interface analysisModuleTypeNodeTreeRead {
  uuid: UUID;
  value: string;
}
