import { analysisMetadataRead } from "@/models/analysisMetadata";

export const analysisMetadataReadFactory = ({
  detectionPoints = [],
  directives = [],
  displayType = null,
  displayValue = null,
  tags = [],
  time = null,
}: Partial<analysisMetadataRead> = {}): analysisMetadataRead => ({
  detectionPoints: detectionPoints,
  directives: directives,
  displayType: displayType,
  displayValue: displayValue,
  tags: tags,
  time: time,
});
