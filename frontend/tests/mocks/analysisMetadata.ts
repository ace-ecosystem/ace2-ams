import { analysisMetadataRead } from "@/models/analysisMetadata";

export const analysisMetadataReadFactory = ({
  criticalPoints = [],
  detectionPoints = [],
  directives = [],
  displayType = null,
  displayValue = null,
  sort = null,
  tags = [],
  time = null,
}: Partial<analysisMetadataRead> = {}): analysisMetadataRead => ({
  criticalPoints: criticalPoints,
  detectionPoints: detectionPoints,
  directives: directives,
  displayType: displayType,
  displayValue: displayValue,
  sort: sort,
  tags: tags,
  time: time,
});
