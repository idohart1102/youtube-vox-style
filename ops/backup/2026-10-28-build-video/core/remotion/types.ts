export type Theme = {
  palette: { bg: string; fg: string; accent: string; [k: string]: string };
  font: string;
  grain?: number;
  vignette?: number;
  subtitles?: boolean;
};

export type Scene = {
  id: string;
  duration_s: number;
  component: string;
  asset?: string;
  props?: Record<string, any>;
  narration?: string;
};

export type EpisodeProps = {
  fps: number;
  scenes: Scene[];
  theme: Theme;
  audio?: string; // đường dẫn trong public, vd 'ep/audio/narration.mp3'
  grainAsset?: string; // vd 'assets/backgrounds/paper.png'
};

export const DEFAULT_THEME: Theme = {
  palette: { bg: '#1b1712', fg: '#f2e6cf', accent: '#e0a030' },
  font: 'Noto Serif JP',
  grain: 0.35,
  vignette: 0.4,
  subtitles: true,
};

// Asset trong scenes.json là đường dẫn tương đối với assets/ (render.mjs gắn assets/ vào public/assets)
export const assetPath = (a: string) => `assets/${a}`;
