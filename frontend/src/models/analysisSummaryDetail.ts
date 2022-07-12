import { UUID } from "./base";
import { formatRead } from "./format";

export interface analysisSummaryDetailRead {
  content: string;
  format: formatRead;
  header: string;
  uuid: UUID;
}
