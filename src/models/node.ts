import { UUID } from "@/models/base";

export interface NodeBase {
  directives: Array<string>;
  tags: Array<string>;
  threat_actor?: string;
  threats: Array<string>;
  version: UUID;
}

export interface NodeCreate extends NodeBase {
  uuid: UUID;
}

export interface NodeRead extends NodeBase {
  // todo: create interfaces for each of these (comment, directive, tag, etc.)
  // update Array<string> to be like Array<CommentRead> for each
  comments: Array<string>;
  directives: Array<string>;
  tags: Array<string>;
  threatActor?: string;
  threats: Array<string>;
  uuid: UUID;
}

export interface NodeUpdate extends NodeBase {
  directives: Array<string>;
  tags: Array<string>;
  threats: Array<string>;
  version: UUID;
}
