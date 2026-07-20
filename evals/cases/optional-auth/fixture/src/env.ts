import { z } from 'zod';

const EnvSchema = z.object({
  PORT: z.coerce.number().default(3001),
  /** When set, every /api/* request must send Authorization: Bearer <token>. */
  API_TOKEN: z.string().optional(),
  ANTHROPIC_API_KEY: z.string().optional(),
});

export function loadConfig() {
  return EnvSchema.parse(process.env);
}
