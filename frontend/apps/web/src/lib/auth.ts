import {
  loginApiV1AuthLoginPost,
  refreshTokenApiV1AuthRefreshPost,
} from "@/client";
import type { LoginSchema } from "@/client";

export async function login(payload: LoginSchema) {
  const response = await loginApiV1AuthLoginPost({
    body: payload,
  });
}
