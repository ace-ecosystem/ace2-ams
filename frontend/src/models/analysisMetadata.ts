import { metadataCriticalPointRead } from "./metadataCriticalPoint";
import { metadataDetectionPointRead } from "./metadataDetectionPoint";
import { metadataDirectiveRead } from "./metadataDirective";
import { metadataDisplayTypeRead } from "./metadataDisplayType";
import { metadataDisplayValueRead } from "./metadataDisplayValue";
import { metadataSortRead } from "./metadataSort";
import { metadataTagRead } from "./metadataTag";
import { metadataTimeRead } from "./metadataTime";

export interface analysisMetadataCreate {
  type:
    | "critical_point"
    | "detection_point"
    | "directive"
    | "display_type"
    | "display_value"
    | "sort"
    | "tag"
    | "time";
  value: string;
}

export interface analysisMetadataRead {
  criticalPoints: metadataCriticalPointRead[];
  detectionPoints: metadataDetectionPointRead[];
  directives: metadataDirectiveRead[];
  displayType: metadataDisplayTypeRead | null;
  displayValue: metadataDisplayValueRead | null;
  sort: metadataSortRead | null;
  tags: metadataTagRead[];
  time: metadataTimeRead | null;
}
