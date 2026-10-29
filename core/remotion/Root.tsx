import React from 'react';
import { Composition } from 'remotion';
import { LongForm } from './compositions/LongForm';
import { EpisodeProps, DEFAULT_THEME } from './types';

const demo: EpisodeProps = {
  fps: 30,
  theme: DEFAULT_THEME,
  scenes: [
    { id: 'demo', duration_s: 4, component: 'TitleCard', props: { title: 'デモ', sub: 'scenes.json を渡してください' } },
  ],
};

export const Root: React.FC = () => (
  <Composition
    id="LongForm"
    component={LongForm}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={120}
    defaultProps={demo}
    calculateMetadata={({ props }) => {
      const fps = props.fps || 30;
      const total = props.scenes.reduce((s, x) => s + x.duration_s, 0);
      return { fps, durationInFrames: Math.max(1, Math.round(total * fps)) };
    }}
  />
);
