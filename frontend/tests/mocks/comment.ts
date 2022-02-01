import { nodeCommentRead } from "@/models/nodeComment";
import { userReadFactory } from "./user";

export const commentReadFactory = ({
  insertTime = new Date("2020-01-01"),
  nodeUuid = "nodeUuid1",
  user = userReadFactory(),
  uuid = "commentUuid1",
  value = "A test comment",
}: Partial<nodeCommentRead> = {}): nodeCommentRead => ({
  insertTime: insertTime,
  nodeUuid: nodeUuid,
  user: user,
  uuid: uuid,
  value: value,
});
