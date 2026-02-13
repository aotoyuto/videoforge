/**
 * VideoForge Remotion Types
 * Maps to the Python VideoSpec schema for seamless interop.
 */

import { z } from "zod";

// --- Enums ---

export const SceneType = z.enum(["color", "image", "video", "ai_generate"]);
export const Position = z.enum([
  "center",
  "top_center",
  "bottom_center",
  "top_left",
  "top_right",
  "bottom_left",
  "bottom_right",
]);
export const Animation = z.enum([
  "none",
  "fade_in",
  "fade_out",
  "slide_up",
  "slide_down",
  "typewriter",
]);
export const TransitionType = z.enum([
  "none",
  "fade",
  "crossfade",
  "wipe_left",
  "wipe_right",
  "dissolve",
]);

// --- Sub-schemas ---

export const TextOverlaySchema = z.object({
  content: z.string(),
  position: Position.default("bottom_center"),
  font: z.string().default("Yu Gothic"),
  font_size: z.number().default(48),
  color: z.string().default("#FFFFFF"),
  bg_color: z.string().nullable().optional(),
  border_color: z.string().nullable().optional(),
  border_width: z.number().default(0),
  animation: Animation.default("none"),
  start: z.number().nullable().optional(),
  end: z.number().nullable().optional(),
});

export const SceneSchema = z.object({
  id: z.string().optional(),
  type: SceneType.default("color"),
  duration: z.number().default(5),
  source: z.string().nullable().optional(),
  source_prompt: z.string().nullable().optional(),
  color: z.string().default("#000000"),
  fit: z.enum(["cover", "contain", "stretch"]).default("cover"),
  text_overlays: z.array(TextOverlaySchema).default([]),
  transition_in: TransitionType.default("none"),
  transition_out: TransitionType.default("none"),
  transition_duration: z.number().default(0.5),
});

export const BGMSchema = z.object({
  source: z.string().nullable().optional(),
  source_prompt: z.string().nullable().optional(),
  volume: z.number().default(0.3),
  fade_in: z.number().default(0),
  fade_out: z.number().default(0),
});

export const AudioSchema = z.object({
  bgm: BGMSchema.nullable().optional(),
});

export const VideoMetaSchema = z.object({
  title: z.string().default("Untitled"),
  resolution: z.tuple([z.number(), z.number()]).default([1920, 1080]),
  fps: z.number().default(30),
  background_color: z.string().default("#000000"),
});

export const ExportSchema = z.object({
  format: z.string().default("mp4"),
  codec: z.string().default("h264"),
  platform: z.string().default("youtube"),
  quality: z.string().default("high"),
});

// --- Root VideoSpec ---

export const VideoSpecSchema = z.object({
  version: z.string().default("1.0"),
  video: VideoMetaSchema.default({}),
  scenes: z.array(SceneSchema).default([]),
  audio: AudioSchema.default({}),
  export: ExportSchema.default({}),
});

export type TextOverlay = z.infer<typeof TextOverlaySchema>;
export type Scene = z.infer<typeof SceneSchema>;
export type VideoSpec = z.infer<typeof VideoSpecSchema>;
